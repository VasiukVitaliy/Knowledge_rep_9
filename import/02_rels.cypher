// 02_rels.cypher — імпорт зв'язків з data/rels.csv; по одному оператору на тип (без APOC).
// Властивості походження: source, confidence, validFrom. MERGE за (from, type, to) -> повторний запуск не створює дублікатів.

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'DETECTS'
MATCH (a:SensorDevice {uid: row.from_uid}), (b:Vehicle {uid: row.to_uid})
MERGE (a)-[r:DETECTS]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'REGISTERS'
MATCH (a:SensorDevice {uid: row.from_uid}), (b:TrafficEvent {uid: row.to_uid})
MERGE (a)-[r:REGISTERS]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'MOUNTED_ON'
MATCH (a:SensorDevice {uid: row.from_uid}), (b:RoadInfrastructureElement {uid: row.to_uid})
MERGE (a)-[r:MOUNTED_ON]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'OCCURS_ON'
MATCH (a:TrafficEvent {uid: row.from_uid}), (b:RoadInfrastructureElement {uid: row.to_uid})
MERGE (a)-[r:OCCURS_ON]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'MOVES_ALONG'
MATCH (a:Vehicle {uid: row.from_uid}), (b:RoadInfrastructureElement {uid: row.to_uid})
MERGE (a)-[r:MOVES_ALONG]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'CROSSES'
MATCH (a:Vehicle {uid: row.from_uid}), (b:Intersection {uid: row.to_uid})
MERGE (a)-[r:CROSSES]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'DRIVES'
MATCH (a:Driver {uid: row.from_uid}), (b:Vehicle {uid: row.to_uid})
MERGE (a)-[r:DRIVES]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'INVOLVED_IN'
MATCH (a:Vehicle {uid: row.from_uid}), (b:TrafficAccident {uid: row.to_uid})
MERGE (a)-[r:INVOLVED_IN]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'CAUSES'
MATCH (a:TrafficAccident {uid: row.from_uid}), (b:TrafficCongestion {uid: row.to_uid})
MERGE (a)-[r:CAUSES]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'AFFECTS_ROUTE'
MATCH (a:TrafficCongestion {uid: row.from_uid}), (b:Route {uid: row.to_uid})
MERGE (a)-[r:AFFECTS_ROUTE]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'PASSES_THROUGH'
MATCH (a:Route {uid: row.from_uid}), (b:RoadInfrastructureElement {uid: row.to_uid})
MERGE (a)-[r:PASSES_THROUGH]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'RECOMMENDS_TO'
MATCH (a:DataProcess {uid: row.from_uid}), (b:Driver {uid: row.to_uid})
MERGE (a)-[r:RECOMMENDS_TO]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'PRODUCES_ROUTE'
MATCH (a:DataProcess {uid: row.from_uid}), (b:Route {uid: row.to_uid})
MERGE (a)-[r:PRODUCES_ROUTE]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'RECOMMENDED_TO'
MATCH (a:Route {uid: row.from_uid}), (b:Driver {uid: row.to_uid})
MERGE (a)-[r:RECOMMENDED_TO]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'CONNECTS_TO'
MATCH (a:RoadSegment {uid: row.from_uid}), (b:Intersection {uid: row.to_uid})
MERGE (a)-[r:CONNECTS_TO]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'REGULATES'
MATCH (a:TrafficLight {uid: row.from_uid}), (b:Intersection {uid: row.to_uid})
MERGE (a)-[r:REGULATES]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'ADJUSTS'
MATCH (a:DataProcess {uid: row.from_uid}), (b:TrafficLight {uid: row.to_uid})
MERGE (a)-[r:ADJUSTS]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'NOTIFIES'
MATCH (a:DataProcess {uid: row.from_uid}), (b:Vehicle {uid: row.to_uid})
MERGE (a)-[r:NOTIFIES]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'RESPONDS_TO'
MATCH (a:Vehicle {uid: row.from_uid}), (b:TrafficAccident {uid: row.to_uid})
MERGE (a)-[r:RESPONDS_TO]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'CLASSIFIES'
MATCH (a:DataProcess {uid: row.from_uid}), (b:TrafficEvent {uid: row.to_uid})
MERGE (a)-[r:CLASSIFIES]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'SUPPLIES_DATA_TO'
MATCH (a:DataProcess {uid: row.from_uid}), (b:DataProcess {uid: row.to_uid})
MERGE (a)-[r:SUPPLIES_DATA_TO]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

LOAD CSV WITH HEADERS FROM 'file:///rels.csv' AS row
WITH row WHERE row.type = 'IS_BASIS_FOR'
MATCH (a:DataProcess {uid: row.from_uid}), (b:DataProcess {uid: row.to_uid})
MERGE (a)-[r:IS_BASIS_FOR]->(b)
SET r.source = row.source, r.confidence = toFloat(row.confidence), r.validFrom = date(row.validFrom);

