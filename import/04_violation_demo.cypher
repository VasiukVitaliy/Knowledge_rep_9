// 04_violation_demo.cypher — навмисне порушення обмеження (очікується ConstraintValidationFailed).
// Запускається окремо (run_import.py --violation); у разі успіху цього запиту обмеження НЕ працює.
CREATE (:Intersection {uid: 'INT_LV_12', code: 'DUPLICATE-TEST'});
