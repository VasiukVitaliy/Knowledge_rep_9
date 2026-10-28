# ЛР 9. Графова база знань у Neo4j (Domain Knowledge Hub, гілка `lab09`)

Предметна область: моніторинг дорожнього руху (Львів). Вхід: онтологія й індивіди з ЛР 7/8 (`data/traffic_monitoring.jsonld`).

## Версії
Python 3.11+, Neo4j 5.26 (Community достатньо; для GDS — Docker/Desktop із плагіном Graph Data Science 2.x), драйвер `neo4j>=5.20`.
`pip install -r requirements.txt`; скопіюйте `.env.example` у `.env` і впишіть пароль Neo4j та ключ LLM (`.env` не потрапляє в git).
Детермінізм: синтетичний генератор `seed=42`; Louvain `randomSeed=42`; LLM — `temperature=0`, seed `n/a`.

## Запуск Neo4j (Docker)
```bash
docker run -d --name neo4j-lab9 -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password123 -e NEO4J_PLUGINS='["graph-data-science"]' \
  -v "$PWD/data:/var/lib/neo4j/import" neo4j:5.26
```
(Aura Free: GDS немає; `LOAD CSV` з `file:///` недоступний — використайте URL CSV або Docker.)

## Запуск з нуля
| Крок | Команда | Результат |
|---|---|---|
| 0. Дані | `python make_graph_data.py` | `data/nodes_*.csv`, `data/rels.csv` (227 вузлів, 486 зв'язків; 47/98 реальних) |
| 0. Еталон | `python reference.py` | `docs/reference_results.json` (очікування без Neo4j) |
| 2. Імпорт | `python run_import.py` | `docs/import_log.md` (кількості, ідемпотентність, порушення обмеження) |
| 3. Запити | `python run_queries.py` | `docs/cypher_results_auto.md` |
| 4. GDS | `python run_gds.py` | `docs/gds_results_auto.md`; `pagerank`, `community` у графі |
| 4. PROFILE | `python run_profile.py` | `docs/profile_auto.md` (до/після індексу) |
| 5. SPARQL vs Cypher | `python run_compare.py` (за потреби запустіть Fuseki ЛР 8) | `docs/compare_auto.md` |
| 5. Text-to-Cypher | `python t2c_pipeline.py v1`, `v2`, `python make_t2c_report.py` | `docs/t2c_*_detail.json`, `docs/t2c_eval_auto.md`, `llm_log/` |
| Тести | `python test_guard.py` | перевірка захисних функцій (без Neo4j) |

Ручний запуск у Neo4j Browser: файли `import/00…03` по черзі (cypher-shell: `cypher-shell -f import/00_schema.cypher`).

## Структура
`data/` CSV · `import/` Cypher-скрипти · `queries/` q01–q11, v1–v3 (ручна перевірка), `cmp/` (порівняння зі SPARQL) · `sparql/` запити ЛР 8 · `tests/t2c.jsonl` · `docs/` (graph_schema.png/.dot, cq_mapping.md, cypher_results.md, gds_report.md, sparql_vs_cypher.md, llm_protocol.md) · `llm_log/` · `claims/claims.csv`.

## Чесні застереження
- Реальних даних лише 47 вузлів / 98 зв'язків; решту (180 / 388) згенеровано (`synthetic=true`, `source=synthetic:seed42`).
- Cypher-скрипти та драйвери підготовлено без доступу до Neo4j: їх треба запустити й виправити можливі розбіжності; доки `run_*.py` не виконано, числа в `docs/*.md` — еталонні (`reference.py`).
- Read-only роль RBAC — лише Enterprise/Aura (`import/05_readonly_role.cypher`); у Community захист = READ-сесія + `cypher_guard.py`.
