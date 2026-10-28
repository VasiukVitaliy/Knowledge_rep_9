// 01_nodes.cypher — імпорт вузлів через LOAD CSV + MERGE за uid (ідемпотентно).
// Файли data/nodes_*.csv мають бути в import-каталозі Neo4j (Docker: -v $PWD/data:/var/lib/neo4j/import).
// Мітки-надкласи (TrafficEvent, RoadInfrastructureElement) і підкласи (VideoCamera, ...) додаються SET/FOREACH.

// Intersection
LOAD CSV WITH HEADERS FROM 'file:///nodes_intersections.csv' AS row
MERGE (n:Intersection {uid: row.uid})
SET n += {code: row.code, name_uk: row.name_uk, name_en: row.name_en, source: row.source, synthetic: toBoolean(row.synthetic), has_lights: toBoolean(row.has_lights), surface_type: row.surface_type, wear_level: row.wear_level, latitude: toFloat(row.latitude), longitude: toFloat(row.longitude)}
SET n:RoadInfrastructureElement;

// RoadSegment
LOAD CSV WITH HEADERS FROM 'file:///nodes_segments.csv' AS row
MERGE (n:RoadSegment {uid: row.uid})
SET n += {code: row.code, name_uk: row.name_uk, name_en: row.name_en, source: row.source, synthetic: toBoolean(row.synthetic), road_name: row.road_name, lanes_count: toInteger(row.lanes_count), length_m: toInteger(row.length_m), speed_limit: toInteger(row.speed_limit), surface_type: row.surface_type, wear_level: row.wear_level}
SET n:RoadInfrastructureElement;

// SensorDevice
LOAD CSV WITH HEADERS FROM 'file:///nodes_sensors.csv' AS row
MERGE (n:SensorDevice {uid: row.uid})
SET n += {code: row.code, name_uk: row.name_uk, name_en: row.name_en, source: row.source, synthetic: toBoolean(row.synthetic), install_date: CASE WHEN coalesce(row.install_date,'') = '' THEN null ELSE date(row.install_date) END, latitude: toFloat(row.latitude), longitude: toFloat(row.longitude)}
FOREACH (_ IN CASE WHEN row.subtype = 'VideoCamera' THEN [1] ELSE [] END | SET n:VideoCamera)
FOREACH (_ IN CASE WHEN row.subtype = 'RadarSensor' THEN [1] ELSE [] END | SET n:RadarSensor)
FOREACH (_ IN CASE WHEN row.subtype = 'InductiveLoop' THEN [1] ELSE [] END | SET n:InductiveLoop);

// TrafficLight
LOAD CSV WITH HEADERS FROM 'file:///nodes_lights.csv' AS row
MERGE (n:TrafficLight {uid: row.uid})
SET n += {code: row.code, name_uk: row.name_uk, name_en: row.name_en, source: row.source, synthetic: toBoolean(row.synthetic), current_phase: row.current_phase, cycle_duration: toInteger(row.cycle_duration), mode: row.mode};

// Vehicle
LOAD CSV WITH HEADERS FROM 'file:///nodes_vehicles.csv' AS row
MERGE (n:Vehicle {uid: row.uid})
SET n += {code: row.code, name_uk: row.name_uk, name_en: row.name_en, source: row.source, synthetic: toBoolean(row.synthetic), direction: row.direction, speed: toFloat(row.speed), latitude: toFloat(row.latitude), longitude: toFloat(row.longitude), timestamp: CASE WHEN coalesce(row.timestamp,'') = '' THEN null ELSE datetime(row.timestamp) END}
FOREACH (_ IN CASE WHEN row.subtype = 'PassengerCar' THEN [1] ELSE [] END | SET n:PassengerCar)
FOREACH (_ IN CASE WHEN row.subtype = 'Truck' THEN [1] ELSE [] END | SET n:Truck)
FOREACH (_ IN CASE WHEN row.subtype = 'EmergencyCar' THEN [1] ELSE [] END | SET n:EmergencyCar)
FOREACH (_ IN CASE WHEN row.subtype = 'PublicTransport' THEN [1] ELSE [] END | SET n:PublicTransport);

// Driver
LOAD CSV WITH HEADERS FROM 'file:///nodes_drivers.csv' AS row
MERGE (n:Driver {uid: row.uid})
SET n += {code: row.code, name_uk: row.name_uk, name_en: row.name_en, source: row.source, synthetic: toBoolean(row.synthetic), license_category: row.license_category, route_preference: row.route_preference, travel_history: row.travel_history};

// TrafficAccident
LOAD CSV WITH HEADERS FROM 'file:///nodes_accidents.csv' AS row
MERGE (n:TrafficAccident {uid: row.uid})
SET n += {code: row.code, name_uk: row.name_uk, name_en: row.name_en, source: row.source, synthetic: toBoolean(row.synthetic), incident_type: row.incident_type, status: row.status, blocked_lanes: toInteger(row.blocked_lanes), start_time: CASE WHEN coalesce(row.start_time,'') = '' THEN null ELSE datetime(row.start_time) END, duration_min: toInteger(row.duration_min)}
SET n:TrafficEvent;

// TrafficCongestion
LOAD CSV WITH HEADERS FROM 'file:///nodes_congestions.csv' AS row
MERGE (n:TrafficCongestion {uid: row.uid})
SET n += {code: row.code, name_uk: row.name_uk, name_en: row.name_en, source: row.source, synthetic: toBoolean(row.synthetic), severity_level: toInteger(row.severity_level), avg_speed: toFloat(row.avg_speed), duration_min: toInteger(row.duration_min), start_time: CASE WHEN coalesce(row.start_time,'') = '' THEN null ELSE datetime(row.start_time) END}
SET n:TrafficEvent;

// Route
LOAD CSV WITH HEADERS FROM 'file:///nodes_routes.csv' AS row
MERGE (n:Route {uid: row.uid})
SET n += {code: row.code, name_uk: row.name_uk, name_en: row.name_en, source: row.source, synthetic: toBoolean(row.synthetic), est_travel_time_min: toInteger(row.est_travel_time_min), load_rating: row.load_rating, total_length_km: toFloat(row.total_length_km)};

// DataProcess
LOAD CSV WITH HEADERS FROM 'file:///nodes_processes.csv' AS row
MERGE (n:DataProcess {uid: row.uid})
SET n += {code: row.code, name_uk: row.name_uk, name_en: row.name_en, source: row.source, synthetic: toBoolean(row.synthetic)}
FOREACH (_ IN CASE WHEN row.subtype = 'DataCollection' THEN [1] ELSE [] END | SET n:DataCollection)
FOREACH (_ IN CASE WHEN row.subtype = 'DataAnalysis' THEN [1] ELSE [] END | SET n:DataAnalysis)
FOREACH (_ IN CASE WHEN row.subtype = 'Planning' THEN [1] ELSE [] END | SET n:Planning)
FOREACH (_ IN CASE WHEN row.subtype = 'Control' THEN [1] ELSE [] END | SET n:Control);

