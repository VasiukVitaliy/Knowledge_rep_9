MATCH (a:TrafficAccident {status: 'active', synthetic: false})-[:OCCURS_ON]->(p)
RETURN a.uid AS inc, a.incident_type AS type, p.uid AS where_
