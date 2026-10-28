"""Результат 5 (кроки 1–2): 5 питань у SPARQL (Fuseki, ЛР 8) і Cypher (реальний підграф synthetic=false) — збіг результатів і час.
Якщо Fuseki недоступний, SPARQL-результати беруться зі збережених sparql/qN_res.csv (час тоді не вимірюється).
Запуск: python run_compare.py -> docs/compare_auto.md"""
import csv, io, statistics, subprocess, time
from pathlib import Path
from neo import driver

ENDPOINT = "http://localhost:3030/mn/sparql"
NS = "http://www.semanticweb.org/vital/ontologies/2026/9/traffic-monitoring#"
PAIRS = [(1, "c1"), (3, "c3"), (4, "c4"), (5, "c5"), (6, "c6")]


def norm_rows(rows):
    return sorted(tuple(("" if v is None else str(v).replace(NS, "")) for v in r) for r in rows)


def sparql(i):
    q = Path(f"sparql/q{i}.rq")
    t = []
    for _ in range(5):
        t0 = time.perf_counter()
        p = subprocess.run(["curl", "-s", "-G", ENDPOINT, "--data-urlencode", f"query@{q}", "-H", "Accept: text/csv"], capture_output=True, timeout=30)
        t.append(time.perf_counter() - t0)
    if p.returncode != 0 or not p.stdout.strip() or p.stdout.lstrip().startswith(b"<"):
        raise RuntimeError("Fuseki недоступний")
    return list(csv.reader(io.StringIO(p.stdout.decode("utf-8"))))[1:], statistics.median(t) * 1000


def sparql_cached(i):
    return list(csv.reader(open(f"sparql/q{i}_res.csv", encoding="utf-8")))[1:], None


out = ["# SPARQL vs Cypher: результати та час (автогенерація run_compare.py)\n", "| Питання | SPARQL рядків | Cypher рядків | Збіг | SPARQL, мс | Cypher, мс | Джерело SPARQL |", "|---|---|---|---|---|---|---|"]
details = []
with driver() as drv, drv.session() as s:
    for i, c in PAIRS:
        try:
            sr, st = sparql(i); src = "Fuseki (live)"
        except Exception:
            sr, st = sparql_cached(i); src = "збережений CSV ЛР 8"
        q = Path(f"queries/cmp/{c}.cypher").read_text(encoding="utf-8")
        ts = []
        for _ in range(5):
            t0 = time.perf_counter(); cr = [list(r.values()) for r in s.run(q)]; ts.append(time.perf_counter() - t0)
        a, b = norm_rows(sr), norm_rows(cr)
        out.append(f"| q{i} | {len(a)} | {len(b)} | {'так' if a == b else 'НІ'} | {'—' if st is None else f'{st:.1f}'} | {statistics.median(ts) * 1000:.1f} | {src} |")
        if a != b:
            details.append(f"### q{i}: розбіжність\nSPARQL: {a}\n\nCypher: {b}\n")
out += [""] + details
Path("docs/compare_auto.md").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
