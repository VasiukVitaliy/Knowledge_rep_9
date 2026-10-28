// CQ8: Які водії керують авто, що беруть участь в активних ДТП?
// Конструкція: шлях довжини 3 + DISTINCT + collect
MATCH (d:Driver)-[:DRIVES]->(v:Vehicle)-[:INVOLVED_IN]->(a:TrafficAccident {status: 'active'})
RETURN d.uid AS driver, v.uid AS vehicle, collect(DISTINCT a.uid) AS accidents
ORDER BY driver;
