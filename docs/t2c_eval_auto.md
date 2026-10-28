# Text-to-Cypher: оцінка (автогенерація make_t2c_report.py)

## Підказка v1

Синтаксично коректних: 15/15; лише зі схеми: 15/15; **правильних: 3/15 (20%)**

| Складність | правильних / усього |
|---|---|
| easy | 0 / 5 |
| medium | 3 / 6 |
| hard | 0 / 4 |

### Помилки (для ручного аналізу)

- **q01** (easy): Які ДТП зараз активні?
  - причина: `wrong result`
  - запит: `MATCH (ta:TrafficAccident) WHERE toLower(ta.status) = 'active' RETURN ta`

- **q02** (easy): Скільки смуг має сегмент SEC_ST_11?
  - причина: `wrong result`
  - запит: `MATCH (rs:RoadSegment {code: 'SEC_ST_11'}) RETURN rs.lanes_count AS lanes_count`

- **q03** (easy): Які світлофори працюють в адаптивному режимі?
  - причина: `wrong result`
  - запит: `MATCH (tl:TrafficLight) WHERE toLower(tl.mode) CONTAINS 'adapt' RETURN tl`

- **q04** (easy): Яке обмеження швидкості на сегменті SEC_ST_03?
  - причина: `wrong result`
  - запит: `MATCH (r:RoadSegment {code: 'SEC_ST_03'}) RETURN r.speed_limit`

- **q05** (easy): Які перехрестя мають світлофори?
  - причина: `wrong result`
  - запит: `MATCH (tl:TrafficLight)-[:REGULATES]->(i:Intersection) RETURN DISTINCT i`

- **q08** (medium): Які маршрути мають високе завантаження?
  - причина: `wrong result`
  - запит: `MATCH (r:Route) WHERE toLower(toString(r.load_rating)) IN ['high', 'високий'] OR r.load_rating >= 0.7 OR r.load_rating >= 4 RETURN r`

- **q09** (medium): Які водії мають категорію B?
  - причина: `wrong result`
  - запит: `MATCH (d:Driver) WHERE d.license_category CONTAINS 'B' RETURN d`

- **q10** (medium): Які маршрути рекомендовано водієві DRV_9041?
  - причина: `wrong result`
  - запит: `MATCH (r:Route)-[:RECOMMENDED_TO]->(d:Driver {code: 'DRV_9041'}) RETURN r`

- **q12** (hard): Які маршрути зачіпає ДТП INC_317 через спричинений нею затор?
  - причина: `wrong result`
  - запит: `MATCH (ta:TrafficAccident {code: 'INC_317'})-[:CAUSES]->(tc:TrafficCongestion)-[:AFFECTS_ROUTE]->(r:Route) RETURN r`

- **q13** (hard): Які ДТП обслуговує більше однієї екстреної машини?
  - причина: `wrong result`
  - запит: `MATCH (v:EmergencyCar)-[:RESPONDS_TO]->(a:TrafficAccident) WITH a, count(DISTINCT v) AS emergency_cars_count WHERE emergency_cars_count > 1 RETURN a, emergency_cars_count`

## Підказка v2

Синтаксично коректних: 15/15; лише зі схеми: 15/15; **правильних: 15/15 (100%)**

| Складність | правильних / усього |
|---|---|
| easy | 5 / 5 |
| medium | 6 / 6 |
| hard | 4 / 4 |

### Помилки (для ручного аналізу)
