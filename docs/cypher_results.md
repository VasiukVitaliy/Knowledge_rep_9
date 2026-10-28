# Результати Cypher-запитів (Результат 3)

> **Статус результатів.** Нижче наведено **очікувані результати**, обчислені незалежно в `reference.py` (networkx) із тих самих CSV. Фактичний вивід Neo4j генерує `python run_queries.py` → `docs/cypher_results_auto.md`; після запуску звірте та позначте колонку «Збіг з Neo4j». Інтерпретації — чернетки (пов'язані з твердженнями claims.csv c10–c14, статус pending до звірки).

## q01_active_accidents

**CQ1: Які ДТП зараз активні і де вони відбуваються?**  
*Конструкція:* фільтр за властивістю + шаблон шляху довжини 1

```cypher
MATCH (a:TrafficAccident {status: 'active'})-[:OCCURS_ON]->(p:RoadInfrastructureElement)
RETURN a.uid AS accident, a.incident_type AS type, p.uid AS place, a.synthetic AS synthetic
ORDER BY accident;
```

**Очікуваний результат:**

| accident | type | place | synthetic |
|---|---|---|---|
| INC_317 | collision | SEC_ST_07 | false |
| INC_319 | collision | SEC_ST_11 | false |
| INC_323 | breakdown | SEC_ST_17 | true |
| INC_324 | collision | SEC_ST_39 | true |
| INC_328 | collision | SEC_ST_38 | true |
| INC_329 | breakdown | SEC_ST_25 | true |


**Інтерпретація:** Шість активних ДТП: 2 реальні (INC_317 на SEC_ST_07, INC_319 на SEC_ST_11 — збігається з SPARQL q1 з ЛР 8) і 4 синтетичні. Кожна ДТП прив'язана до сегмента дороги, тож диспетчер одразу бачить локацію.

**Збіг з Neo4j:** ☐ так ☐ ні (після `run_queries.py`)

---

## q02_severe_congestion_street

**CQ2: Чи є на вул. Городоцькій затор із серйозністю ≥ 8?**  
*Конструкція:* EXISTS-підзапит / фільтр, повертає boolean

```cypher
RETURN EXISTS {
  MATCH (c:TrafficCongestion)-[:OCCURS_ON]->(s:RoadSegment {road_name: 'Horodotska St.'})
  WHERE c.severity_level >= 8
} AS has_severe_congestion;
```

**Очікуваний результат:**

`has_severe_congestion = True` (затор CONG_881)

**Інтерпретація:** Так, на Городоцькій (SEC_ST_07) є затор CONG_881 із severity 8 — його спричинила ДТП INC_317. `EXISTS {}` повертає один boolean без побудови всіх рядків.

**Збіг з Neo4j:** ☐ так ☐ ні (після `run_queries.py`)

---

## q03_sensors_by_type

**CQ3: Скільки датчиків кожного типу встановлено?**  
*Конструкція:* агрегація count + розбір міток

```cypher
MATCH (s:SensorDevice)
WITH s, [l IN labels(s) WHERE l <> 'SensorDevice'][0] AS sensor_type
RETURN sensor_type, count(*) AS cnt
ORDER BY cnt DESC, sensor_type;
```

**Очікуваний результат:**

| sensor_type | cnt |
|---|---|
| VideoCamera | 12 |
| InductiveLoop | 6 |
| RadarSensor | 6 |


**Інтерпретація:** Парк датчиків: 12 відеокамер, по 6 радарів і індуктивних петель (разом 24 = 4 реальні + 20 синтетичних). Тип береться з додаткової мітки, а не з властивості.

**Збіг з Neo4j:** ☐ так ☐ ні (після `run_queries.py`)

---

## q04_routes_recipients

**CQ4: Які маршрути кому рекомендовано, і чи є маршрути без адресата?**  
*Конструкція:* OPTIONAL MATCH + WITH + collect

```cypher
MATCH (r:Route)
OPTIONAL MATCH (r)-[:RECOMMENDED_TO]->(d:Driver)
WITH r, collect(d.uid) AS drivers
RETURN r.uid AS route, r.load_rating AS load_rating, drivers, size(drivers) AS recipients
ORDER BY recipients, route;
```

**Очікуваний результат:**

| route | load_rating | drivers | recipients |
|---|---|---|---|
| R_OPT_5 | high | [] | 0 |
| R_OPT_10 | moderate | ['DRV_9058'] | 1 |
| R_OPT_11 | high | ['DRV_9059'] | 1 |
| R_OPT_12 | high | ['DRV_9064'] | 1 |
| R_OPT_13 | low | ['DRV_9058'] | 1 |
| R_OPT_14 | moderate | ['DRV_9059'] | 1 |
| R_OPT_15 | moderate | ['DRV_9050'] | 1 |
| R_OPT_16 | low | ['DRV_9062'] | 1 |
| R_OPT_17 | low | ['DRV_9061'] | 1 |
| R_OPT_3 | moderate | ['DRV_9041'] | 1 |
| R_OPT_6 | high | ['DRV_9063'] | 1 |
| R_OPT_7 | moderate | ['DRV_9053'] | 1 |
| R_OPT_8 | moderate | ['DRV_9060'] | 1 |
| R_OPT_9 | high | ['DRV_9054'] | 1 |
| R_ALT_1 | low | ['DRV_9042', 'DRV_9044'] | 2 |


**Інтерпретація:** 15 маршрутів; R_OPT_5 (high) не рекомендовано нікому — його видно лише завдяки OPTIONAL MATCH (як у SPARQL q4). R_ALT_1 рекомендовано двом водіям.

**Збіг з Neo4j:** ☐ так ☐ ні (після `run_queries.py`)

---

## q05_accident_routes

**CQ5: Які маршрути зачіпає ДТП через спричинений нею затор?**  
*Конструкція:* шлях фіксованої довжини + WITH-агрегація

```cypher
MATCH (a:TrafficAccident)-[:CAUSES]->(c:TrafficCongestion)-[:AFFECTS_ROUTE]->(r:Route)
WITH a, collect(DISTINCT r.uid) AS routes
RETURN a.uid AS accident, routes, size(routes) AS routes_cnt
ORDER BY routes_cnt DESC, accident;
```

**Очікуваний результат:**

| accident | routes | routes_cnt |
|---|---|---|
| INC_320 | ['R_OPT_10', 'R_OPT_3'] | 2 |
| INC_321 | ['R_OPT_11', 'R_OPT_15'] | 2 |
| INC_322 | ['R_OPT_12', 'R_OPT_17'] | 2 |
| INC_323 | ['R_OPT_16', 'R_OPT_7'] | 2 |
| INC_324 | ['R_OPT_11', 'R_OPT_5'] | 2 |
| INC_325 | ['R_OPT_16', 'R_OPT_5'] | 2 |
| INC_326 | ['R_OPT_14', 'R_OPT_5'] | 2 |
| INC_327 | ['R_OPT_11', 'R_OPT_12'] | 2 |
| INC_328 | ['R_OPT_16', 'R_OPT_17'] | 2 |
| INC_329 | ['R_ALT_1', 'R_OPT_3'] | 2 |
| INC_317 | ['R_OPT_3'] | 1 |
| INC_319 | ['R_OPT_5'] | 1 |


**Інтерпретація:** Кожна ДТП зачіпає 1–2 маршрути через спричинений затор. Реальні INC_317→R_OPT_3 та INC_319→R_OPT_5 збігаються з SPARQL q5.

**Збіг з Neo4j:** ☐ так ☐ ні (після `run_queries.py`)

---

## q06_reachable_intersections

**CQ6: Які перехрестя досяжні з INT_LV_12 не більш ніж через 3 сегменти доріг?**  
*Конструкція:* шлях змінної довжини *2..6 (перехрестя—сегмент—перехрестя ...)

```cypher
MATCH p = (a:Intersection {uid: 'INT_LV_12'})-[:CONNECTS_TO*2..6]-(b:Intersection)
WHERE a <> b
RETURN b.uid AS intersection, min(length(p) / 2) AS min_segments
ORDER BY min_segments, intersection;
```

**Очікуваний результат:**

| intersection | min_segments |
|---|---|
| INT_LV_07 | 1 |
| INT_LV_21 | 1 |
| INT_LV_39 | 1 |
| INT_LV_22 | 2 |
| INT_LV_38 | 2 |
| INT_LV_23 | 3 |
| INT_LV_37 | 3 |


**Інтерпретація:** Із INT_LV_12 за ≤ 3 сегменти досяжні 7 перехресть; мінімальна кількість сегментів = довжина шляху / 2, бо шлях чергує перехрестя й сегменти.

**Збіг з Neo4j:** ☐ так ☐ ні (після `run_queries.py`)

---

## q07_shortest_path

**CQ7: Який найкоротший маршрут між INT_LV_07 і INT_LV_30 (у сегментах і перехрестях)?**  
*Конструкція:* shortestPath

```cypher
MATCH (a:Intersection {uid: 'INT_LV_07'}), (b:Intersection {uid: 'INT_LV_30'})
MATCH p = shortestPath((a)-[:CONNECTS_TO*..20]-(b))
RETURN [n IN nodes(p) | n.uid] AS path, length(p) / 2 AS segments;
```

**Очікуваний результат:**

Довжина: **8 сегментів** (шлях з 17 вузлів). Один із можливих шляхів: `INT_LV_07 → SEC_ST_03 → INT_LV_21 → SEC_ST_14 → INT_LV_22 → SEC_ST_15 → INT_LV_23 → SEC_ST_16 → INT_LV_24 → SEC_ST_17 → INT_LV_25 → SEC_ST_34 → INT_LV_28 → SEC_ST_21 → INT_LV_29 → SEC_ST_22 → INT_LV_30`.

**Інтерпретація:** shortestPath знаходить мінімальну кількість сегментів між INT_LV_07 і INT_LV_30. Якщо існує кілька шляхів однакової довжини, Neo4j поверне довільний, тому звіряти слід довжину.

**Збіг з Neo4j:** ☐ так ☐ ні (після `run_queries.py`)

---

## q08_drivers_in_active_accidents

**CQ8: Які водії керують авто, що беруть участь в активних ДТП?**  
*Конструкція:* шлях довжини 3 + DISTINCT + collect

```cypher
MATCH (d:Driver)-[:DRIVES]->(v:Vehicle)-[:INVOLVED_IN]->(a:TrafficAccident {status: 'active'})
RETURN d.uid AS driver, v.uid AS vehicle, collect(DISTINCT a.uid) AS accidents
ORDER BY driver;
```

**Очікуваний результат:**

| driver | vehicle | accidents |
|---|---|---|
| DRV_9041 | BC1234AA | ['INC_317'] |
| DRV_9043 | BC7410HM | ['INC_319'] |
| DRV_9046 | BC4000IT | ['INC_329'] |
| DRV_9048 | BC4074HP | ['INC_329'] |
| DRV_9049 | BC4111IT | ['INC_328'] |
| DRV_9050 | BC4148IT | ['INC_324'] |
| DRV_9060 | BC4518KA | ['INC_328'] |
| DRV_9061 | BC4555IT | ['INC_323'] |
| DRV_9065 | BC4703HP | ['INC_323'] |


**Інтерпретація:** 9 водіїв мають авто в активних ДТП, серед них DRV_9041 (INC_317) і DRV_9043 (INC_319) — збігається з даними ЛР 7.

**Збіг з Neo4j:** ☐ так ☐ ні (після `run_queries.py`)

---

## q09_impact_accident

**CQ9 (аналіз впливу): На що (маршрути, водії) впливає ДТП INC_317 до глибини 4?**  
*Конструкція:* аналіз впливу: змінна довжина з альтернативою типів, глибина ≥ 3

```cypher
MATCH p = (a:TrafficAccident {uid: 'INC_317'})-[:CAUSES|AFFECTS_ROUTE|RECOMMENDED_TO*1..4]->(x)
RETURN x.uid AS affected, [l IN labels(x) WHERE l <> 'TrafficEvent'][0] AS kind, min(length(p)) AS depth
ORDER BY depth, affected;
```

**Очікуваний результат:**

| affected | kind | depth |
|---|---|---|
| CONG_881 | TrafficCongestion | 1 |
| R_OPT_3 | Route | 2 |
| DRV_9041 | Driver | 3 |


**Інтерпретація:** Аналіз впливу INC_317: глибина 1 — затор CONG_881; 2 — маршрут R_OPT_3; 3 — водій DRV_9041, якому цей маршрут рекомендовано. Тобто аварія через ланцюжок «ДТП → затор → маршрут → водій» впливає на конкретну людину.

**Збіг з Neo4j:** ☐ так ☐ ні (після `run_queries.py`)

---

## q10_impact_collection

**CQ10 (аналіз впливу): Які сутності залежать від збору даних COLLECT_1 (до глибини 5)?**  
*Конструкція:* аналіз впливу: ланцюг процесів → маршрути/світлофори/екстрені авто → водії

```cypher
MATCH p = (c:DataCollection {uid: 'COLLECT_1'})-[:SUPPLIES_DATA_TO|IS_BASIS_FOR|PRODUCES_ROUTE|RECOMMENDS_TO|RECOMMENDED_TO|ADJUSTS|NOTIFIES*1..5]->(x)
WITH x, min(length(p)) AS depth
RETURN depth, [l IN labels(x) WHERE NOT l IN ['DataProcess','RoadInfrastructureElement','TrafficEvent']][0] AS kind, collect(x.uid) AS entities
ORDER BY depth, kind;
```

**Очікуваний результат:**

| depth | kind | entities |
|---|---|---|
| 1 | DataAnalysis | ['ANALYSIS_1'] |
| 2 | Control | ['CONTROL_1'] |
| 2 | Planning | ['PLANNING_1'] |
| 3 | Driver | ['DRV_9041'] |
| 3 | EmergencyCar | ['AMB_01'] |
| 3 | Route | ['R_OPT_3'] |
| 3 | TrafficLight | ['TL_12_A'] |


**Інтерпретація:** Збій збору даних COLLECT_1 каскадно зачіпає: аналіз ANALYSIS_1 (1), керування CONTROL_1 і планування PLANNING_1 (2), світлофор TL_12_A, швидку AMB_01, маршрут R_OPT_3 (3) і водія DRV_9041 (3).

**Збіг з Neo4j:** ☐ так ☐ ні (після `run_queries.py`)

---

## q11_low_confidence

**CQ11 (походження): Скільки тверджень (зв'язків) мають confidence < 0.8 і з яких джерел?**  
*Конструкція:* фільтр за властивістю зв'язку + агрегація

```cypher
MATCH ()-[r]->()
WHERE r.confidence < 0.8
RETURN type(r) AS rel_type, r.source AS source, count(*) AS cnt, round(avg(r.confidence), 2) AS avg_conf
ORDER BY cnt DESC, rel_type;
```

**Очікуваний результат:**

| rel_type | source | cnt | avg_conf |
|---|---|---|---|
| DETECTS | synthetic:seed42 | 14 | 0.75 |
| REGISTERS | synthetic:seed42 | 5 | 0.76 |


**Інтерпретація:** Низьку достовірність (< 0.8) мають лише синтетичні `DETECTS` і `REGISTERS`; усі курованi зв'язки онтології мають confidence = 1.0.

**Збіг з Neo4j:** ☐ так ☐ ні (після `run_queries.py`)

---

## Ручна перевірка на малому підграфі (≥ 3 запити)

Підграф — 47 реальних вузлів ЛР 7 (`synthetic = false`). Очікування виведено **вручну з `data/traffic_monitoring.jsonld`**, без виконання коду; запити — `queries/v1…v3`.

| Запит | Ручне виведення з даних | Очікуваний результат | Збіг з Neo4j |
|---|---|---|---|
| v1 (CQ5) | `INC_317 causes CONG_881`, `CONG_881 affectsRoute R_OPT_3`; `INC_319 causes CONG_883`, `CONG_883 affectsRoute R_OPT_5`; `INC_318 causes CONG_882`, але CONG_882 не має `affectsRoute` | (INC_317, R_OPT_3), (INC_319, R_OPT_5) | ☐ |
| v2 (вплив INC_317) | `INC_317→CONG_881` (1); `CONG_881→R_OPT_3` (2); `R_OPT_3 isRecommendedTo DRV_9041` (3); у DRV_9041 вихідних зв'язків типів CAUSES/AFFECTS_ROUTE/RECOMMENDED_TO немає | CONG_881 (1), R_OPT_3 (2), DRV_9041 (3) | ☐ |
| v3 (CQ8) | активні ДТП: INC_317, INC_319 (INC_318 — resolved); `BC1234AA involvedIn INC_317`, `BC7410HM involvedIn INC_319`; `DRV_9041 drives BC1234AA`, `DRV_9043 drives BC7410HM` | (DRV_9041, BC1234AA, INC_317), (DRV_9043, BC7410HM, INC_319) | ☐ |

Еталонний `reference.py` дає ті самі три результати (v1, v2, v3), тобто ручне виведення і незалежний код збіглися.
