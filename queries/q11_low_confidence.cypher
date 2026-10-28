// CQ11 (походження): Скільки тверджень (зв'язків) мають confidence < 0.8 і з яких джерел?
// Конструкція: фільтр за властивістю зв'язку + агрегація
MATCH ()-[r]->()
WHERE r.confidence < 0.8
RETURN type(r) AS rel_type, r.source AS source, count(*) AS cnt, round(avg(r.confidence), 2) AS avg_conf
ORDER BY cnt DESC, rel_type;
