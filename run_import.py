import datetime
from pathlib import Path
from neo4j.exceptions import ClientError
from neo import driver, statements, counts, run, md_table

log = [f"# Журнал імпорту ({datetime.datetime.now():%Y-%m-%d %H:%M})\n"]
with driver() as drv, drv.session() as s:
    for f in ["import/00_schema.cypher", "import/01_nodes.cypher", "import/02_rels.cypher"]:
        for st in statements(f):
            s.run(st).consume()
        print("виконано", f)
    s.run("CALL db.awaitIndexes()").consume()
    n1, r1 = counts(s)
    log.append(f"## Перший імпорт\nВузлів: **{n1}**, зв'язків: **{r1}**\n")

    for f in ["import/00_schema.cypher", "import/01_nodes.cypher", "import/02_rels.cypher"]:
        for st in statements(f):
            s.run(st).consume()
    n2, r2 = counts(s)
    ok = (n1, r1) == (n2, r2)
    log.append(f"## Повторний імпорт\nВузлів: **{n2}**, зв'язків: **{r2}** → ідемпотентність: **{'підтверджена' if ok else 'ПОРУШЕНА'}**\n")

    for st in statements("import/03_verify.cypher"):
        title = st.splitlines()[0][:70]
        log.append(f"### `{title}`\n" + md_table(run(s, st)))

    log.append("## Порушення обмеження\n```cypher\n" + statements("import/04_violation_demo.cypher")[0] + ";\n```\n")
    try:
        s.run(statements("import/04_violation_demo.cypher")[0]).consume()
        log.append("**УВАГА:** запит виконався — обмеження не працює!\n")
    except ClientError as e:
        log.append(f"Код: `{e.code}`\n\nПовідомлення: `{e.message}`\n")
    n3, r3 = counts(s)
    log.append(f"Після спроби порушення: вузлів {n3}, зв'язків {r3} (без змін: {(n3, r3) == (n1, r1)})\n")

Path("docs").mkdir(exist_ok=True)
Path("docs/import_log.md").write_text("\n".join(log), encoding="utf-8")
print("\n".join(log))
