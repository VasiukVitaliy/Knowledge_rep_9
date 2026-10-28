// CQ2: Чи є на вул. Городоцькій затор із серйозністю ≥ 8?
// Конструкція: EXISTS-підзапит / фільтр, повертає boolean
RETURN EXISTS {
  MATCH (c:TrafficCongestion)-[:OCCURS_ON]->(s:RoadSegment {road_name: 'Horodotska St.'})
  WHERE c.severity_level >= 8
} AS has_severe_congestion;
