# PROFILE (автогенерація run_profile.py)

### P1 — ДО оптимізації (індексу немає)

```cypher
MATCH (s:RoadSegment) WHERE s.road_name = 'Horodotska St.' RETURN s.uid AS uid, s.length_m AS length_m
```

Рядків: 3; сумарно dbHits: **69**; медіана часу: **3 мс**

| Оператор | dbHits | rows |
|---|---|---|
| ProduceResults@neo4j | 0 | 3 |
| &nbsp;&nbsp;Projection@neo4j | 0 | 3 |
| &nbsp;&nbsp;&nbsp;&nbsp;CacheProperties@neo4j | 6 | 3 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Filter@neo4j | 31 | 3 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;NodeByLabelScan@neo4j | 32 | 31 |

### P1 — ПІСЛЯ оптимізації (індекс seg_road_name)

```cypher
MATCH (s:RoadSegment) WHERE s.road_name = 'Horodotska St.' RETURN s.uid AS uid, s.length_m AS length_m
```

Рядків: 3; сумарно dbHits: **10**; медіана часу: **2 мс**

| Оператор | dbHits | rows |
|---|---|---|
| ProduceResults@neo4j | 0 | 3 |
| &nbsp;&nbsp;Projection@neo4j | 0 | 3 |
| &nbsp;&nbsp;&nbsp;&nbsp;CacheProperties@neo4j | 6 | 3 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;NodeIndexSeek@neo4j | 4 | 3 |

**Підсумок P1:** dbHits 69 → 10; час 3 мс → 2 мс.

### P2 — аналіз впливу (q09)

```cypher
MATCH p = (a:TrafficAccident {uid: 'INC_317'})-[:CAUSES|AFFECTS_ROUTE|RECOMMENDED_TO*1..4]->(x)
RETURN x.uid AS affected, [l IN labels(x) WHERE l <> 'TrafficEvent'][0] AS kind, min(length(p)) AS depth
ORDER BY depth, affected
```

Рядків: 3; сумарно dbHits: **33**; медіана часу: **2 мс**

| Оператор | dbHits | rows |
|---|---|---|
| ProduceResults@neo4j | 0 | 3 |
| &nbsp;&nbsp;Sort@neo4j | 0 | 3 |
| &nbsp;&nbsp;&nbsp;&nbsp;EagerAggregation@neo4j | 6 | 3 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;VarLengthExpand(Pruning,BFS,All)@neo4j | 25 | 3 |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;NodeUniqueIndexSeek@neo4j | 2 | 1 |
