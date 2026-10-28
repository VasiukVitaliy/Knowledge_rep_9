// CQ3: Скільки датчиків кожного типу встановлено?
// Конструкція: агрегація count + розбір міток
MATCH (s:SensorDevice)
WITH s, [l IN labels(s) WHERE l <> 'SensorDevice'][0] AS sensor_type
RETURN sensor_type, count(*) AS cnt
ORDER BY cnt DESC, sensor_type;
