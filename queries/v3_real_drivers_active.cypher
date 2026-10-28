// Ручна перевірка 3: водії в активних ДТП (лише реальні)
MATCH (d:Driver {synthetic: false})-[:DRIVES]->(v:Vehicle {synthetic: false})-[:INVOLVED_IN]->(a:TrafficAccident {status: 'active', synthetic: false})
RETURN d.uid AS driver, v.uid AS vehicle, a.uid AS accident ORDER BY driver;
