// CQ6: Які перехрестя досяжні з INT_LV_12 не більш ніж через 3 сегменти доріг?
// Конструкція: шлях змінної довжини *2..6 (перехрестя—сегмент—перехрестя ...)
MATCH p = (a:Intersection {uid: 'INT_LV_12'})-[:CONNECTS_TO*2..6]-(b:Intersection)
WHERE a <> b
RETURN b.uid AS intersection, min(length(p) / 2) AS min_segments
ORDER BY min_segments, intersection;
