MATCH p = (a:Intersection {synthetic: false})-[:CONNECTS_TO*2..6]-(b:Intersection {synthetic: false})
WHERE a <> b AND all(n IN nodes(p) WHERE n.synthetic = false)
RETURN DISTINCT a.uid AS a, b.uid AS b
