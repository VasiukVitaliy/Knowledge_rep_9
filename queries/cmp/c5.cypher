MATCH (a:TrafficAccident {synthetic: false})-[:CAUSES]->(:TrafficCongestion {synthetic: false})-[:AFFECTS_ROUTE]->(r:Route {synthetic: false})
RETURN a.uid AS inc, r.uid AS route
