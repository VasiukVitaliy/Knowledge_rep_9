// Ручна перевірка 2: вплив INC_317 (лише реальні вузли)
MATCH p = (a:TrafficAccident {uid: 'INC_317'})-[:CAUSES|AFFECTS_ROUTE|RECOMMENDED_TO*1..4]->(x {synthetic: false})
RETURN x.uid AS affected, min(length(p)) AS depth ORDER BY depth, affected;
