// 00_schema.cypher — унікальні обмеження та індекси (Neo4j 5.x). Ідемпотентно: IF NOT EXISTS.

// --- Унікальні обмеження: uid = локальне ім'я IRI з онтології (INC_317, SEC_ST_07, ...) ---
CREATE CONSTRAINT intersection_uid IF NOT EXISTS FOR (n:Intersection) REQUIRE n.uid IS UNIQUE;
CREATE CONSTRAINT roadsegment_uid IF NOT EXISTS FOR (n:RoadSegment) REQUIRE n.uid IS UNIQUE;
CREATE CONSTRAINT sensordevice_uid IF NOT EXISTS FOR (n:SensorDevice) REQUIRE n.uid IS UNIQUE;
CREATE CONSTRAINT trafficlight_uid IF NOT EXISTS FOR (n:TrafficLight) REQUIRE n.uid IS UNIQUE;
CREATE CONSTRAINT vehicle_uid IF NOT EXISTS FOR (n:Vehicle) REQUIRE n.uid IS UNIQUE;
CREATE CONSTRAINT driver_uid IF NOT EXISTS FOR (n:Driver) REQUIRE n.uid IS UNIQUE;
CREATE CONSTRAINT trafficaccident_uid IF NOT EXISTS FOR (n:TrafficAccident) REQUIRE n.uid IS UNIQUE;
CREATE CONSTRAINT trafficcongestion_uid IF NOT EXISTS FOR (n:TrafficCongestion) REQUIRE n.uid IS UNIQUE;
CREATE CONSTRAINT route_uid IF NOT EXISTS FOR (n:Route) REQUIRE n.uid IS UNIQUE;
CREATE CONSTRAINT dataprocess_uid IF NOT EXISTS FOR (n:DataProcess) REQUIRE n.uid IS UNIQUE;
CREATE CONSTRAINT trafficevent_uid IF NOT EXISTS FOR (n:TrafficEvent) REQUIRE n.uid IS UNIQUE;
CREATE CONSTRAINT roadinfrastructureelement_uid IF NOT EXISTS FOR (n:RoadInfrastructureElement) REQUIRE n.uid IS UNIQUE;

// --- Індекси за властивостями, які використовують запити (RANGE-індекси) ---
CREATE INDEX seg_road_name IF NOT EXISTS FOR (n:RoadSegment) ON (n.road_name);
CREATE INDEX acc_status IF NOT EXISTS FOR (n:TrafficAccident) ON (n.status);
CREATE INDEX cong_severity IF NOT EXISTS FOR (n:TrafficCongestion) ON (n.severity_level);
CREATE INDEX veh_code IF NOT EXISTS FOR (n:Vehicle) ON (n.code);
