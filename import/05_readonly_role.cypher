// 05_readonly_role.cypher — read-only користувач для text-to-Cypher. ТІЛЬКИ Enterprise/Aura (RBAC); у Community ролей немає —
// там захист = READ_ACCESS-сесія драйвера + cypher_guard. Виконувати в базі `system` від імені адміністратора.
CREATE ROLE t2c_reader IF NOT EXISTS;
GRANT ACCESS ON DATABASE neo4j TO t2c_reader;
GRANT MATCH {*} ON GRAPH neo4j TO t2c_reader;
CREATE USER t2c_user IF NOT EXISTS SET PASSWORD 'change-me-please' CHANGE NOT REQUIRED;
GRANT ROLE t2c_reader TO t2c_user;
// Перевірка: з цього користувача `CREATE (:X)` має завершитися помилкою Permission/Forbidden.
