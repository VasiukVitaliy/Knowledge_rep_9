from cypher_guard import *
assert forbidden("MATCH (n) DETACH DELETE n") == "DETACH"
assert forbidden("MATCH (n {status:'SET'}) RETURN n") is None
assert forbidden("CALL db.labels()") == "CALL"
assert forbidden("MATCH (a:TrafficAccident) RETURN a.uid") is None
assert schema_check("MATCH (a:TrafficAccident {status:'active'})-[:OCCURS_ON]->(p:RoadInfrastructureElement) RETURN a.uid, p.uid") == []
assert schema_check("MATCH (a:Accident)-[:HAPPENS_ON]->(p) RETURN a.foo") == ["властивість:foo", "мітка:Accident", "тип:HAPPENS_ON"]
assert schema_check("MATCH p=(a:Intersection {uid:'X'})-[:CONNECTS_TO*2..6]-(b:Intersection) RETURN min(length(p)/2)") == []
assert schema_check("MATCH (c:TrafficCongestion) WHERE c.severity_level > 0.5 RETURN avg(c.avg_speed)") == []
assert schema_check("MATCH (a)-[:CAUSES|AFFECTS_ROUTE|RECOMMENDED_TO*1..4]->(x) RETURN x.uid") == []
assert schema_check("MATCH (a)-[r:CAUSES]->(x) RETURN r.confidence, r.weight") == ["властивість:weight"]
assert add_limit("MATCH (n) RETURN n").endswith("LIMIT 100")
assert add_limit("MATCH (n) RETURN n LIMIT 5") == "MATCH (n) RETURN n LIMIT 5"
assert clean("```cypher\nMATCH (n) RETURN n;\n```") == "MATCH (n) RETURN n"
print("test_guard: OK")
