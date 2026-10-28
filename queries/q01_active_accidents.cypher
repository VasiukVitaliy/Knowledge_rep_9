// CQ1: Які ДТП зараз активні і де вони відбуваються?
// Конструкція: фільтр за властивістю + шаблон шляху довжини 1
MATCH (a:TrafficAccident {status: 'active'})-[:OCCURS_ON]->(p:RoadInfrastructureElement)
RETURN a.uid AS accident, a.incident_type AS type, p.uid AS place, a.synthetic AS synthetic
ORDER BY accident;
