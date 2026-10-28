MATCH (r:Route {synthetic: false})
OPTIONAL MATCH (r)-[:RECOMMENDED_TO]->(d:Driver {synthetic: false})
RETURN r.uid AS route, r.load_rating AS load_rating, d.uid AS driver
