// CQ10 (аналіз впливу): Які сутності залежать від збору даних COLLECT_1 (до глибини 5)?
// Конструкція: аналіз впливу: ланцюг процесів → маршрути/світлофори/екстрені авто → водії
MATCH p = (c:DataCollection {uid: 'COLLECT_1'})-[:SUPPLIES_DATA_TO|IS_BASIS_FOR|PRODUCES_ROUTE|RECOMMENDS_TO|RECOMMENDED_TO|ADJUSTS|NOTIFIES*1..5]->(x)
WITH x, min(length(p)) AS depth
RETURN depth, [l IN labels(x) WHERE NOT l IN ['DataProcess','RoadInfrastructureElement','TrafficEvent']][0] AS kind, collect(x.uid) AS entities
ORDER BY depth, kind;
