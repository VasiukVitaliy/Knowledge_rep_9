import time
from pathlib import Path
from neo import driver, run, md_table

out = ["# Результати Cypher-запитів (автогенерація run_queries.py)\n"]
with driver() as drv, drv.session() as s:
    for f in sorted(Path("queries").glob("[qv]*.cypher")):
        text = f.read_text(encoding="utf-8")
        head = [l[3:] for l in text.splitlines() if l.startswith("// ")]
        q = "\n".join(l for l in text.splitlines() if not l.startswith("//")).strip().rstrip(";")
        t0 = time.perf_counter()
        rows = run(s, q)
        dt = time.perf_counter() - t0
        out += [f"## {f.stem}\n", "\n".join(f"> {h}" for h in head) + "\n", f"```cypher\n{q}\n```\n",
                f"Рядків: {len(rows)}; час: {dt * 1000:.1f} мс\n", md_table(rows)]
        print(f.stem, len(rows), f"{dt * 1000:.1f} ms")
Path("docs/cypher_results_auto.md").write_text("\n".join(out), encoding="utf-8")
