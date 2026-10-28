# Відображення CQ на шаблони Cypher-шляхів (Результат 1)

CQ1–CQ8 успадковано з ЛР 8 (SPARQL q1–q7) та ЛР 6–7; CQ9–CQ11 додано в ЛР 9 (аналіз впливу та походження).

| CQ | Питання | Шаблон шляху | Запит |
|---|---|---|---|
| CQ1 | Які ДТП зараз активні і де вони відбуваються? | `(:TrafficAccident {status:'active'})-[:OCCURS_ON]->(:RoadInfrastructureElement)` | q01 |
| CQ2 | Чи є на вул. Городоцькій затор із серйозністю ≥ 8? | `(:TrafficCongestion)-[:OCCURS_ON]->(:RoadSegment {road_name:'Horodotska St.'})` + `severity_level >= 8` | q02 |
| CQ3 | Скільки датчиків кожного типу встановлено? | `(:SensorDevice)` + розбір додаткових міток (VideoCamera/RadarSensor/InductiveLoop), `count` | q03 |
| CQ4 | Які маршрути кому рекомендовано, чи є маршрути без адресата? | `(:Route)` + `OPTIONAL MATCH (r)-[:RECOMMENDED_TO]->(:Driver)` | q04 |
| CQ5 | Які маршрути зачіпає ДТП через спричинений нею затор? | `(:TrafficAccident)-[:CAUSES]->(:TrafficCongestion)-[:AFFECTS_ROUTE]->(:Route)` | q05 |
| CQ6 | Які перехрестя досяжні з INT_LV_12 не більш ніж через 3 сегменти? | `(:Intersection)-[:CONNECTS_TO*2..6]-(:Intersection)` (перехрестя—сегмент—перехрестя…) | q06 |
| CQ7 | Який найкоротший шлях між двома перехрестями? | `shortestPath((:Intersection)-[:CONNECTS_TO*..20]-(:Intersection))` | q07 |
| CQ8 | Які водії керують авто, що беруть участь в активних ДТП? | `(:Driver)-[:DRIVES]->(:Vehicle)-[:INVOLVED_IN]->(:TrafficAccident {status:'active'})` | q08 |
| CQ9 | На що впливає ДТП INC_317 (глибина ≥ 3)? | `(:TrafficAccident)-[:CAUSES|AFFECTS_ROUTE|RECOMMENDED_TO*1..4]->(x)` | q09 |
| CQ10 | Що залежить від збору даних COLLECT_1 (глибина ≥ 3)? | `(:DataCollection)-[:SUPPLIES_DATA_TO|IS_BASIS_FOR|PRODUCES_ROUTE|RECOMMENDS_TO|RECOMMENDED_TO|ADJUSTS|NOTIFIES*1..5]->(x)` | q10 |
| CQ11 | Скільки тверджень має низьку достовірність і з яких джерел? | `()-[r]->() WHERE r.confidence < 0.8` — властивості походження | q11 |

## Властивості походження на зв'язках

| Властивість | Тип | Значення | Призначення |
|---|---|---|---|
| `source` | string | `ontology:lab7` (98 зв'язків із онтології) / `synthetic:seed42` (388 згенерованих) | відрізняти курований знання від згенерованих |
| `confidence` | float 0..1 | 1.0 для курованих; 0.70–0.99 для синтетичних `DETECTS`, `REGISTERS`, `CLASSIFIES` | імітація достовірності детекції/класифікації |
| `validFrom` | date | подія → дата `start_time`; монтаж датчика → `install_date`; інакше дата знімка 2026-10-04 | часова валідність твердження |

Вузли також мають `source` і `synthetic` (true/false).

## Порівняння зі схемою ЛР 7 (онтологія → LPG)

| Елемент онтології (ЛР 7) | У графі Neo4j | Коментар |
|---|---|---|
| Клас верхнього рівня (`Vehicle`, `Driver`, `Route`, `TrafficAccident`, …) | Мітка вузла (10 основних) | `owl:Class` → мітка |
| Підклас (`VideoCamera ⊂ SensorDevice`, `Truck ⊂ Vehicle`, `Planning ⊂ DataProcess`) | Додаткова мітка на тому ж вузлі | вузол має обидві мітки → запит за надкласом працює без `rdfs:subClassOf*` |
| Надклас-обʼєднання (`TrafficEvent`, `RoadInfrastructureElement`) | Додаткова мітка | потрібні для `REGISTERS`, `OCCURS_ON`, `PASSES_THROUGH` |
| `owl:DatatypeProperty` (`severity_level`, `road_name`, …) | Властивість вузла (типізована: int/float/bool/date/datetime) | `xsd:*` → типи Cypher |
| `owl:ObjectProperty` (`causes`, `affectsRoute`, …) | Тип зв'язку `CAUSES`, `AFFECTS_ROUTE` (22 типи) | напрям збережено; зв'язки можуть мати властивості |
| `owl:inverseOf` (`drives`/`isDrivenBy`) | Не матеріалізується | обхід у зворотному напрямку: `<-[:DRIVES]-` |
| `rdfs:label` / `rdfs:comment` (uk, en) | Властивості `name_uk`, `name_en` | мовні теги → окремі властивості; коментарі не імпортовано |
| Індивід (`:INC_317`) | Вузол з `uid = 'INC_317'` | `code` = «INC-317» (значення `incident_id`) |
| `owl:AllDisjointClasses`, `owl:Restriction` | Частково: унікальні обмеження (uid) | дизʼюнктність і кардинальності в LPG не виводяться; для них потрібен SHACL/додаткові перевірки |
| Реіфікація тверджень (RDF-star / іменовані графи) | Властивості на зв'язках (`source`, `confidence`, `validFrom`) | головна перевага LPG для походження |
