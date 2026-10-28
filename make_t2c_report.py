import json
from pathlib import Path

lines = ["# Text-to-Cypher: оцінка (автогенерація make_t2c_report.py)\n"]
for v in ("v1", "v2"):
    p = Path(f"docs/t2c_{v}_detail.json")
    if not p.exists():
        lines.append(f"## {v}: файлу немає — запустіть `python t2c_pipeline.py {v}`\n"); continue
    d = json.loads(p.read_text(encoding="utf-8")); n = len(d)
    lines += [f"## Підказка {v}\n", f"Синтаксично коректних: {sum(x['syntax'] for x in d)}/{n}; лише зі схеми: {sum(x['schema'] for x in d)}/{n}; "
              f"**правильних: {sum(x['correct'] for x in d)}/{n} ({100 * sum(x['correct'] for x in d) / n:.0f}%)**\n",
              "| Складність | правильних / усього |\n|---|---|"]
    for diff in ("easy", "medium", "hard"):
        s = [x for x in d if x["difficulty"] == diff]
        lines.append(f"| {diff} | {sum(x['correct'] for x in s)} / {len(s)} |")
    lines.append("\n### Помилки (для ручного аналізу)\n")
    for x in [x for x in d if not x["correct"]][:10]:
        lines.append(f"- **{x['id']}** ({x['difficulty']}): {x['question']}\n  - причина: `{x['reason']}`\n  - запит: `{x['query'].replace(chr(10), ' ')}`\n")
Path("docs/t2c_eval_auto.md").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
