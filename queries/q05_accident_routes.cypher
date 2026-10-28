// CQ5: Які маршрути зачіпає ДТП через спричинений нею затор?
// Конструкція: шлях фіксованої довжини + WITH-агрегація
MATCH (a:TrafficAccident)-[:CAUSES]->(c:TrafficCongestion)-[:AFFECTS_ROUTE]->(r:Route)
WITH a, collect(DISTINCT r.uid) AS routes
RETURN a.uid AS accident, routes, size(routes) AS routes_cnt
ORDER BY routes_cnt DESC, accident;
