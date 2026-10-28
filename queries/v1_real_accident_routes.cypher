// Ручна перевірка 1 (= SPARQL q5 з ЛР 8)
MATCH (a:TrafficAccident {synthetic: false})-[:CAUSES]->(c:TrafficCongestion {synthetic: false})-[:AFFECTS_ROUTE]->(r:Route {synthetic: false})
RETURN a.uid AS accident, r.uid AS route ORDER BY accident;
