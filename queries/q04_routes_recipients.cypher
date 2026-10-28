// CQ4: Які маршрути кому рекомендовано, і чи є маршрути без адресата?
// Конструкція: OPTIONAL MATCH + WITH + collect
MATCH (r:Route)
OPTIONAL MATCH (r)-[:RECOMMENDED_TO]->(d:Driver)
WITH r, collect(d.uid) AS drivers
RETURN r.uid AS route, r.load_rating AS load_rating, drivers, size(drivers) AS recipients
ORDER BY recipients, route;
