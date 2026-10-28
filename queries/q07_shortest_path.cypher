// CQ7: Який найкоротший маршрут між INT_LV_07 і INT_LV_30 (у сегментах і перехрестях)?
// Конструкція: shortestPath
MATCH (a:Intersection {uid: 'INT_LV_07'}), (b:Intersection {uid: 'INT_LV_30'})
MATCH p = shortestPath((a)-[:CONNECTS_TO*..20]-(b))
RETURN [n IN nodes(p) | n.uid] AS path, length(p) / 2 AS segments;
