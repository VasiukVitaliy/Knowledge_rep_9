MATCH (s:SensorDevice {synthetic: false})
WITH [l IN labels(s) WHERE l <> 'SensorDevice'][0] AS type
RETURN type, count(*) AS n
