# Журнал імпорту (2026-10-24 13:23)

## Перший імпорт
Вузлів: **227**, зв'язків: **486**

## Повторний імпорт
Вузлів: **227**, зв'язків: **486** → ідемпотентність: **підтверджена**

### `MATCH (n) RETURN count(n) AS nodes`
| nodes |
|---|
| 227 |

### `MATCH ()-[r]->() RETURN count(r) AS relationships`
| relationships |
|---|
| 486 |

### `MATCH (n) UNWIND labels(n) AS label RETURN label, count(*) AS cnt ORDE`
| label | cnt |
|---|---|
| RoadInfrastructureElement | 54 |
| Vehicle | 34 |
| DataProcess | 32 |
| RoadSegment | 31 |
| TrafficEvent | 26 |
| Driver | 25 |
| SensorDevice | 24 |
| Intersection | 23 |
| TrafficLight | 17 |
| Route | 15 |
| PassengerCar | 13 |
| TrafficAccident | 13 |
| TrafficCongestion | 13 |
| VideoCamera | 12 |
| EmergencyCar | 9 |
| DataAnalysis | 8 |
| DataCollection | 8 |
| Planning | 8 |
| Control | 8 |
| InductiveLoop | 6 |
| RadarSensor | 6 |
| PublicTransport | 6 |
| Truck | 6 |

### `MATCH ()-[r]->() RETURN type(r) AS rel_type, count(*) AS cnt ORDER BY `
| rel_type | cnt |
|---|---|
| CONNECTS_TO | 61 |
| PASSES_THROUGH | 51 |
| DETECTS | 47 |
| MOVES_ALONG | 33 |
| REGISTERS | 27 |
| OCCURS_ON | 26 |
| CLASSIFIES | 26 |
| DRIVES | 25 |
| MOUNTED_ON | 24 |
| AFFECTS_ROUTE | 22 |
| INVOLVED_IN | 20 |
| CROSSES | 19 |
| REGULATES | 17 |
| IS_BASIS_FOR | 16 |
| RECOMMENDED_TO | 15 |
| CAUSES | 13 |
| RESPONDS_TO | 9 |
| RECOMMENDS_TO | 8 |
| PRODUCES_ROUTE | 8 |
| ADJUSTS | 8 |
| SUPPLIES_DATA_TO | 8 |
| NOTIFIES | 3 |

### `MATCH (n) WHERE n.synthetic = false RETURN count(n) AS real_nodes`
| real_nodes |
|---|
| 47 |

### `MATCH ()-[r]->() WHERE r.source STARTS WITH 'ontology' RETURN count(r)`
| real_relationships |
|---|
| 98 |

### `SHOW CONSTRAINTS YIELD name, type, labelsOrTypes, properties RETURN na`
| name | type | labelsOrTypes | properties |
|---|---|---|---|
| dataprocess_uid | UNIQUENESS | ['DataProcess'] | ['uid'] |
| driver_uid | UNIQUENESS | ['Driver'] | ['uid'] |
| intersection_uid | UNIQUENESS | ['Intersection'] | ['uid'] |
| roadinfrastructureelement_uid | UNIQUENESS | ['RoadInfrastructureElement'] | ['uid'] |
| roadsegment_uid | UNIQUENESS | ['RoadSegment'] | ['uid'] |
| route_uid | UNIQUENESS | ['Route'] | ['uid'] |
| sensordevice_uid | UNIQUENESS | ['SensorDevice'] | ['uid'] |
| trafficaccident_uid | UNIQUENESS | ['TrafficAccident'] | ['uid'] |
| trafficcongestion_uid | UNIQUENESS | ['TrafficCongestion'] | ['uid'] |
| trafficevent_uid | UNIQUENESS | ['TrafficEvent'] | ['uid'] |
| trafficlight_uid | UNIQUENESS | ['TrafficLight'] | ['uid'] |
| vehicle_uid | UNIQUENESS | ['Vehicle'] | ['uid'] |

### `SHOW INDEXES YIELD name, type, labelsOrTypes, properties, state RETURN`
| name | type | labelsOrTypes | properties | state |
|---|---|---|---|---|
| acc_status | RANGE | ['TrafficAccident'] | ['status'] | ONLINE |
| cong_severity | RANGE | ['TrafficCongestion'] | ['severity_level'] | ONLINE |
| dataprocess_uid | RANGE | ['DataProcess'] | ['uid'] | ONLINE |
| driver_uid | RANGE | ['Driver'] | ['uid'] | ONLINE |
| index_343aff4e | LOOKUP | None | None | ONLINE |
| index_f7700477 | LOOKUP | None | None | ONLINE |
| intersection_uid | RANGE | ['Intersection'] | ['uid'] | ONLINE |
| roadinfrastructureelement_uid | RANGE | ['RoadInfrastructureElement'] | ['uid'] | ONLINE |
| roadsegment_uid | RANGE | ['RoadSegment'] | ['uid'] | ONLINE |
| route_uid | RANGE | ['Route'] | ['uid'] | ONLINE |
| seg_road_name | RANGE | ['RoadSegment'] | ['road_name'] | ONLINE |
| sensordevice_uid | RANGE | ['SensorDevice'] | ['uid'] | ONLINE |
| trafficaccident_uid | RANGE | ['TrafficAccident'] | ['uid'] | ONLINE |
| trafficcongestion_uid | RANGE | ['TrafficCongestion'] | ['uid'] | ONLINE |
| trafficevent_uid | RANGE | ['TrafficEvent'] | ['uid'] | ONLINE |
| trafficlight_uid | RANGE | ['TrafficLight'] | ['uid'] | ONLINE |
| veh_code | RANGE | ['Vehicle'] | ['code'] | ONLINE |
| vehicle_uid | RANGE | ['Vehicle'] | ['uid'] | ONLINE |

## Порушення обмеження
```cypher
CREATE (:Intersection {uid: 'INT_LV_12', code: 'DUPLICATE-TEST'});
```

Код: `Neo.ClientError.Schema.ConstraintValidationFailed`

Повідомлення: `Node(0) already exists with label `Intersection` and property `uid` = 'INT_LV_12'`

Після спроби порушення: вузлів 227, зв'язків 486 (без змін: True)
