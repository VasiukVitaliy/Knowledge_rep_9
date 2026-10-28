// CQ9 (аналіз впливу): На що (маршрути, водії) впливає ДТП INC_317 до глибини 4?
// Конструкція: аналіз впливу: змінна довжина з альтернативою типів, глибина ≥ 3
MATCH p = (a:TrafficAccident {uid: 'INC_317'})-[:CAUSES|AFFECTS_ROUTE|RECOMMENDED_TO*1..4]->(x)
RETURN x.uid AS affected, [l IN labels(x) WHERE l <> 'TrafficEvent'][0] AS kind, min(length(p)) AS depth
ORDER BY depth, affected;
