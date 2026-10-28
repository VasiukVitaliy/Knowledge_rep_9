from pathlib import Path
from neo import driver, run

P1 = "MATCH (s:RoadSegment) WHERE s.road_name = 'Horodotska St.' RETURN s.uid AS uid, s.length_m AS length_m"
P2 = Path("queries/q09_impact_accident.cypher").read_text(encoding="utf-8")
P2 = "\n".join(l for l in P2.splitlines() if not l.startswith("//")).strip().rstrip(";")


def flat(p, depth=0, acc=None):
    acc = [] if acc is None else acc
    acc.append((depth, p.get("operatorType", "?"), p.get("dbHits", 0) or 0, p.get("rows", 0) or 0))
    for c in p.get("children") or []:
        flat(c, depth + 1, acc)
    return acc


def profile(s, q, label):
    best = None
    for _ in range(5): 
        res = s.run("PROFILE " + q)
        rows = list(res)
        summ = res.consume()
        t = summ.result_available_after + summ.result_consumed_after
        best = best or []
        best.append(t)
    best.sort()
    ops = flat(summ.profile)
    total = sum(o[2] for o in ops)
    txt = [f"### {label}\n", f"```cypher\n{q}\n```\n", f"Рядків: {len(rows)}; сумарно dbHits: **{total}**; медіана часу: **{best[2]} мс**\n",
           "| Оператор | dbHits | rows |\n|---|---|---|"]
    txt += [f"| {'&nbsp;&nbsp;' * d}{op} | {h} | {r} |" for d, op, h, r in ops]
    return "\n".join(txt) + "\n", total, best[2]


out = ["# PROFILE (автогенерація run_profile.py)\n"]
with driver() as drv, drv.session() as s:
    s.run("DROP INDEX seg_road_name IF EXISTS").consume()
    s.run("CALL db.awaitIndexes()").consume()
    a, ta, ma = profile(s, P1, "P1 — ДО оптимізації (індексу немає)")
    s.run("CREATE INDEX seg_road_name IF NOT EXISTS FOR (n:RoadSegment) ON (n.road_name)").consume()
    s.run("CALL db.awaitIndexes()").consume()
    b, tb, mb = profile(s, P1, "P1 — ПІСЛЯ оптимізації (індекс seg_road_name)")
    c, tc, mc = profile(s, P2, "P2 — аналіз впливу (q09)")
    out += [a, b, f"**Підсумок P1:** dbHits {ta} → {tb}; час {ma} мс → {mb} мс.\n", c]
Path("docs/profile_auto.md").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))