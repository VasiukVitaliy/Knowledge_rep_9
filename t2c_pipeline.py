import datetime, hashlib, json, os, sys, time
from pathlib import Path

import openai
from dotenv import load_dotenv
from neo4j import GraphDatabase
from cypher_guard import clean, forbidden, schema_check, add_limit, schema_prompt

load_dotenv(override=True)
MODEL = os.getenv("T2C_MODEL", "gemini-3.8-flash")        # v1 і v2 — з ОДНІЄЮ моделлю
MAX_TOKENS, PAUSE_SEC, RETRIES, TIMEOUT = 4000, 15, 3, 10
TESTS = Path("tests/t2c.jsonl")
client = openai.OpenAI(api_key=os.getenv("OPEN_API_SECRET_KEY"),
                       base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

PROMPT_V1 = """Ти експерт з Neo4j Cypher. За питанням українською напиши один запит Cypher для графа дорожнього руху.
{schema}
Поверни лише текст запиту."""
PROMPT_V2 = PROMPT_V1 + """

Правила:
- Використовуй ЛИШЕ мітки, типи зв'язків і властивості зі схеми. Нічого не вигадуй.
- Дозволено тільки читання: MATCH, OPTIONAL MATCH, WITH, WHERE, RETURN, ORDER BY, LIMIT. Без CREATE/MERGE/SET/DELETE/CALL.
- Індивідів шукай за властивістю uid (наприклад {{uid: 'INC_317'}}) з підкресленнями, а не за code (в code дефіси).
- Булеві та числові значення пиши без лапок (has_lights: true, severity_level > 5); текст — в одинарних лапках: 'active', 'high', 'B'.
- Типи датчиків/транспорту/процесів визначаються додатковими мітками (VideoCamera, Truck, ...), а не властивістю.
- «скільки», «середній», «найвищий» — агрегація (count, avg, max); «більше одного» — WITH ... count(...) AS n WHERE n > 1.
- Не додавай зайвих стовпців: повертай лише те, про що питають.

Приклади (не з тестового набору):
Питання: Які сегменти доріг мають більше трьох смуг?
MATCH (s:RoadSegment) WHERE s.lanes_count > 3 RETURN s.uid
Питання: Які датчики встановлені на перехресті INT_LV_12?
MATCH (s:SensorDevice)-[:MOUNTED_ON]->(:Intersection {{uid: 'INT_LV_12'}}) RETURN s.uid
Питання: Яка середня довжина сегментів доріг?
MATCH (s:RoadSegment) RETURN avg(s.length_m)"""


def system(v):
    return (PROMPT_V1 if v == "v1" else PROMPT_V2).format(schema=schema_prompt())


def ask_llm(sys_prompt, question, version):
    raw, finish, error, daily = "", None, "", False
    for attempt in range(1, RETRIES + 1):
        try:
            r = client.chat.completions.create(model=MODEL, max_tokens=MAX_TOKENS, temperature=0,
                                               messages=[{"role": "system", "content": sys_prompt}, {"role": "user", "content": question}])
            raw, finish, error = r.choices[0].message.content or "", r.choices[0].finish_reason, ""
            break
        except Exception as e:
            error = f"{type(e).__name__}: {e}"
            print(f"  помилка API ({attempt}/{RETRIES}): {error[:150]}")
            if "PerDay" in error:
                daily = True
                break
            time.sleep(PAUSE_SEC * attempt)
    Path("llm_log").mkdir(exist_ok=True)
    log = {"date": datetime.datetime.now().isoformat(), "model": MODEL, "temperature": 0, "max_tokens": MAX_TOKENS, "seed": "n/a",
           "prompt_version": f"t2c-{version}", "question": question, "raw_output": raw, "finish_reason": finish, "api_error": error,
           "human_decision": "pending", "system_prompt_sha256": hashlib.sha256(sys_prompt.encode()).hexdigest()[:16]}
    path = Path("llm_log") / f"t2c-{version}_{int(time.time() * 1000)}.json"
    path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    return raw, finish, path, daily


def set_decision(path, text):
    j = json.loads(Path(path).read_text(encoding="utf-8"))
    j["human_decision"] = text
    Path(path).write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")


def norm(rows):
    def v(x):
        return round(x, 3) if isinstance(x, float) else (tuple(v(i) for i in x) if isinstance(x, list) else x)
    return sorted((tuple(v(x) for x in r.values()) for r in rows), key=repr)


def execute(drv, q, db):
    """Безпечне виконання: READ_ACCESS-сесія + таймаут."""
    with drv.session(database=db, default_access_mode="READ") as s:
        return norm([r.data() for r in s.run(q, timeout=TIMEOUT)])


def syntax_ok(drv, q, db):
    try:
        with drv.session(database=db, default_access_mode="READ") as s:
            s.run("EXPLAIN " + q).consume()
        return True
    except Exception:
        return False


def evaluate(version):
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    db = os.getenv("NEO4J_DATABASE", "neo4j")
    ro_user, ro_pass = os.getenv("T2C_USER"), os.getenv("T2C_PASSWORD")
    admin = GraphDatabase.driver(uri, auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "")))
    ro = GraphDatabase.driver(uri, auth=(ro_user, ro_pass)) if ro_user else admin
    rows = [json.loads(l) for l in TESTS.open(encoding="utf-8") if l.strip()]
    out_path = Path(f"docs/t2c_{version}_detail.json")
    done = {}
    if out_path.exists():
        done = {d["id"]: d for d in json.loads(out_path.read_text(encoding="utf-8")) if d.get("query")}
    detail, called, sys_prompt = [], 0, system(version)
    for r in rows:
        if r["id"] in done:
            detail.append(done[r["id"]]); print(r["id"], "(з кешу)"); continue
        if called:
            time.sleep(PAUSE_SEC)
        raw, finish, log_path, daily = ask_llm(sys_prompt, r["question"], version)
        called += 1
        q = clean(raw)
        bad_kw = forbidden(q) if q else None
        bad_schema = schema_check(q) if q else ["порожня відповідь"]
        q_safe = add_limit(q) if q and not bad_kw else q
        syn = bool(q) and not bad_kw and syntax_ok(ro, q_safe, db)
        sch = syn and not bad_schema
        correct, err = False, ""
        if sch:
            try:
                correct = execute(ro, q_safe, db) == execute(admin, r["gold_cypher"], db)
            except Exception as e:
                err = str(e)[:200]
        reason = ("api error" if not q else f"заборонено: {bad_kw}" if bad_kw else "syntax" if not syn else
                  f"schema: {bad_schema}" if not sch else "wrong result" if not correct else "")
        set_decision(log_path, "accepted: result matches gold" if correct else f"rejected: {reason}")
        detail.append({"id": r["id"], "difficulty": r["difficulty"], "question": r["question"], "syntax": syn, "schema": sch,
                       "correct": correct, "reason": reason, "query": q, "error": err})
        print(r["id"], "syntax" if syn else "-", "schema" if sch else "-", "OK" if correct else "X", reason)
        if daily:
            print("Денну квоту вичерпано; повторіть команду завтра (кеш збережено)."); break
    n = len(rows)
    print(f"\n{version}: syntax={sum(d['syntax'] for d in detail)}/{n} schema={sum(d['schema'] for d in detail)}/{n} correct={sum(d['correct'] for d in detail)}/{n}")
    out_path.write_text(json.dumps(detail, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    evaluate(sys.argv[1] if len(sys.argv) > 1 else "v1")
