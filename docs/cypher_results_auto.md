# Результати Cypher-запитів (автогенерація run_queries.py)

## q01_active_accidents

> CQ1: Які ДТП зараз активні і де вони відбуваються?
> Конструкція: фільтр за властивістю + шаблон шляху довжини 1

```cypher
MATCH (a:TrafficAccident {status: 'active'})-[:OCCURS_ON]->(p:RoadInfrastructureElement)
RETURN a.uid AS accident, a.incident_type AS type, p.uid AS place, a.synthetic AS synthetic
ORDER BY accident
```

Рядків: 6; час: 88.5 мс

| accident | type | place | synthetic |
|---|---|---|---|
| INC_317 | collision | SEC_ST_07 | False |
| INC_319 | collision | SEC_ST_11 | False |
| INC_323 | breakdown | SEC_ST_17 | True |
| INC_324 | collision | SEC_ST_39 | True |
| INC_328 | collision | SEC_ST_38 | True |
| INC_329 | breakdown | SEC_ST_25 | True |

## q02_severe_congestion_street

> CQ2: Чи є на вул. Городоцькій затор із серйозністю ≥ 8?
> Конструкція: EXISTS-підзапит / фільтр, повертає boolean

```cypher
RETURN EXISTS {
  MATCH (c:TrafficCongestion)-[:OCCURS_ON]->(s:RoadSegment {road_name: 'Horodotska St.'})
  WHERE c.severity_level >= 8
} AS has_severe_congestion
```

Рядків: 1; час: 107.3 мс

| has_severe_congestion |
|---|
| True |

## q03_sensors_by_type

> CQ3: Скільки датчиків кожного типу встановлено?
> Конструкція: агрегація count + розбір міток

```cypher
MATCH (s:SensorDevice)
WITH s, [l IN labels(s) WHERE l <> 'SensorDevice'][0] AS sensor_type
RETURN sensor_type, count(*) AS cnt
ORDER BY cnt DESC, sensor_type
```

Рядків: 3; час: 63.9 мс

| sensor_type | cnt |
|---|---|
| VideoCamera | 12 |
| InductiveLoop | 6 |
| RadarSensor | 6 |

## q04_routes_recipients

> CQ4: Які маршрути кому рекомендовано, і чи є маршрути без адресата?
> Конструкція: OPTIONAL MATCH + WITH + collect

```cypher
MATCH (r:Route)
OPTIONAL MATCH (r)-[:RECOMMENDED_TO]->(d:Driver)
WITH r, collect(d.uid) AS drivers
RETURN r.uid AS route, r.load_rating AS load_rating, drivers, size(drivers) AS recipients
ORDER BY recipients, route
```

Рядків: 15; час: 90.5 мс

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
| R_ALT_1 | low | ['DRV_9044', 'DRV_9042'] | 2 |

## q05_accident_routes

> CQ5: Які маршрути зачіпає ДТП через спричинений нею затор?
> Конструкція: шлях фіксованої довжини + WITH-агрегація

```cypher
MATCH (a:TrafficAccident)-[:CAUSES]->(c:TrafficCongestion)-[:AFFECTS_ROUTE]->(r:Route)
WITH a, collect(DISTINCT r.uid) AS routes
RETURN a.uid AS accident, routes, size(routes) AS routes_cnt
ORDER BY routes_cnt DESC, accident
```

Рядків: 12; час: 98.7 мс

| accident | routes | routes_cnt |
|---|---|---|
| INC_320 | ['R_OPT_10', 'R_OPT_3'] | 2 |
| INC_321 | ['R_OPT_15', 'R_OPT_11'] | 2 |
| INC_322 | ['R_OPT_12', 'R_OPT_17'] | 2 |
| INC_323 | ['R_OPT_16', 'R_OPT_7'] | 2 |
| INC_324 | ['R_OPT_11', 'R_OPT_5'] | 2 |
| INC_325 | ['R_OPT_16', 'R_OPT_5'] | 2 |
| INC_326 | ['R_OPT_14', 'R_OPT_5'] | 2 |
| INC_327 | ['R_OPT_12', 'R_OPT_11'] | 2 |
| INC_328 | ['R_OPT_17', 'R_OPT_16'] | 2 |
| INC_329 | ['R_OPT_3', 'R_ALT_1'] | 2 |
| INC_317 | ['R_OPT_3'] | 1 |
| INC_319 | ['R_OPT_5'] | 1 |

## q06_reachable_intersections

> CQ6: Які перехрестя досяжні з INT_LV_12 не більш ніж через 3 сегменти доріг?
> Конструкція: шлях змінної довжини *2..6 (перехрестя—сегмент—перехрестя ...)

```cypher
MATCH p = (a:Intersection {uid: 'INT_LV_12'})-[:CONNECTS_TO*2..6]-(b:Intersection)
WHERE a <> b
RETURN b.uid AS intersection, min(length(p) / 2) AS min_segments
ORDER BY min_segments, intersection
```

Рядків: 7; час: 165.5 мс

| intersection | min_segments |
|---|---|
| INT_LV_07 | 1 |
| INT_LV_21 | 1 |
| INT_LV_39 | 1 |
| INT_LV_22 | 2 |
| INT_LV_38 | 2 |
| INT_LV_23 | 3 |
| INT_LV_37 | 3 |

## q07_shortest_path

> CQ7: Який найкоротший маршрут між INT_LV_07 і INT_LV_30 (у сегментах і перехрестях)?
> Конструкція: shortestPath

```cypher
MATCH (a:Intersection {uid: 'INT_LV_07'}), (b:Intersection {uid: 'INT_LV_30'})
MATCH p = shortestPath((a)-[:CONNECTS_TO*..20]-(b))
RETURN [n IN nodes(p) | n.uid] AS path, length(p) / 2 AS segments
```

Рядків: 1; час: 108.3 мс

| path | segments |
|---|---|
| ['INT_LV_07', 'SEC_ST_03', 'INT_LV_21', 'SEC_ST_14', 'INT_LV_22', 'SEC_ST_15', 'INT_LV_23', 'SEC_ST_16', 'INT_LV_24', 'SEC_ST_17', 'INT_LV_25', 'SEC_ST_34', 'INT_LV_28', 'SEC_ST_21', 'INT_LV_29', 'SEC_ST_22', 'INT_LV_30'] | 8 |

## q08_drivers_in_active_accidents

> CQ8: Які водії керують авто, що беруть участь в активних ДТП?
> Конструкція: шлях довжини 3 + DISTINCT + collect

```cypher
MATCH (d:Driver)-[:DRIVES]->(v:Vehicle)-[:INVOLVED_IN]->(a:TrafficAccident {status: 'active'})
RETURN d.uid AS driver, v.uid AS vehicle, collect(DISTINCT a.uid) AS accidents
ORDER BY driver
```

Рядків: 9; час: 74.1 мс

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

## q09_impact_accident

> CQ9 (аналіз впливу): На що (маршрути, водії) впливає ДТП INC_317 до глибини 4?
> Конструкція: аналіз впливу: змінна довжина з альтернативою типів, глибина ≥ 3

```cypher
MATCH p = (a:TrafficAccident {uid: 'INC_317'})-[:CAUSES|AFFECTS_ROUTE|RECOMMENDED_TO*1..4]->(x)
RETURN x.uid AS affected, [l IN labels(x) WHERE l <> 'TrafficEvent'][0] AS kind, min(length(p)) AS depth
ORDER BY depth, affected
```

Рядків: 3; час: 95.8 мс

| affected | kind | depth |
|---|---|---|
| CONG_881 | TrafficCongestion | 1 |
| R_OPT_3 | Route | 2 |
| DRV_9041 | Driver | 3 |

## q10_impact_collection

> CQ10 (аналіз впливу): Які сутності залежать від збору даних COLLECT_1 (до глибини 5)?
> Конструкція: аналіз впливу: ланцюг процесів → маршрути/світлофори/екстрені авто → водії

```cypher
MATCH p = (c:DataCollection {uid: 'COLLECT_1'})-[:SUPPLIES_DATA_TO|IS_BASIS_FOR|PRODUCES_ROUTE|RECOMMENDS_TO|RECOMMENDED_TO|ADJUSTS|NOTIFIES*1..5]->(x)
WITH x, min(length(p)) AS depth
RETURN depth, [l IN labels(x) WHERE NOT l IN ['DataProcess','RoadInfrastructureElement','TrafficEvent']][0] AS kind, collect(x.uid) AS entities
ORDER BY depth, kind
```

Рядків: 7; час: 82.5 мс

| depth | kind | entities |
|---|---|---|
| 1 | DataAnalysis | ['ANALYSIS_1'] |
| 2 | Control | ['CONTROL_1'] |
| 2 | Planning | ['PLANNING_1'] |
| 3 | Driver | ['DRV_9041'] |
| 3 | Route | ['R_OPT_3'] |
| 3 | TrafficLight | ['TL_12_A'] |
| 3 | Vehicle | ['AMB_01'] |

## q11_low_confidence

> CQ11 (походження): Скільки тверджень (зв'язків) мають confidence < 0.8 і з яких джерел?
> Конструкція: фільтр за властивістю зв'язку + агрегація

```cypher
MATCH ()-[r]->()
WHERE r.confidence < 0.8
RETURN type(r) AS rel_type, r.source AS source, count(*) AS cnt, round(avg(r.confidence), 2) AS avg_conf
ORDER BY cnt DESC, rel_type
```

Рядків: 2; час: 71.1 мс

| rel_type | source | cnt | avg_conf |
|---|---|---|---|
| DETECTS | synthetic:seed42 | 14 | 0.75 |
| REGISTERS | synthetic:seed42 | 5 | 0.76 |

## v1_real_accident_routes

> Ручна перевірка 1 (= SPARQL q5 з ЛР 8)

```cypher
MATCH (a:TrafficAccident {synthetic: false})-[:CAUSES]->(c:TrafficCongestion {synthetic: false})-[:AFFECTS_ROUTE]->(r:Route {synthetic: false})
RETURN a.uid AS accident, r.uid AS route ORDER BY accident
```

Рядків: 2; час: 69.6 мс

| accident | route |
|---|---|
| INC_317 | R_OPT_3 |
| INC_319 | R_OPT_5 |

## v2_real_impact_INC_317

> Ручна перевірка 2: вплив INC_317 (лише реальні вузли)

```cypher
MATCH p = (a:TrafficAccident {uid: 'INC_317'})-[:CAUSES|AFFECTS_ROUTE|RECOMMENDED_TO*1..4]->(x {synthetic: false})
RETURN x.uid AS affected, min(length(p)) AS depth ORDER BY depth, affected
```

Рядків: 3; час: 65.6 мс

| affected | depth |
|---|---|
| CONG_881 | 1 |
| R_OPT_3 | 2 |
| DRV_9041 | 3 |

## v3_real_drivers_active

> Ручна перевірка 3: водії в активних ДТП (лише реальні)

```cypher
MATCH (d:Driver {synthetic: false})-[:DRIVES]->(v:Vehicle {synthetic: false})-[:INVOLVED_IN]->(a:TrafficAccident {status: 'active', synthetic: false})
RETURN d.uid AS driver, v.uid AS vehicle, a.uid AS accident ORDER BY driver
```

Рядків: 2; час: 70.3 мс

| driver | vehicle | accident |
|---|---|---|
| DRV_9041 | BC1234AA | INC_317 |
| DRV_9043 | BC7410HM | INC_319 |
