# Результати GDS (автогенерація run_gds.py)

GDS версія: `2.13.14`

## Запуск

| nodePropertiesWritten | ranIterations | didConverge |
|---|---|---|
| 227 | 20 | False |

| communityCount | modularity | nodePropertiesWritten |
|---|---|---|
| 10 | 0.5637330860810513 | 227 |

## PageRank: топ-10

| uid | kind | pagerank | community |
|---|---|---|---|
| INT_LV_12 | Intersection | 3.179 | 203 |
| INT_LV_21 | Intersection | 2.6681 | 203 |
| INT_LV_07 | Intersection | 1.8167 | 100 |
| INT_LV_25 | Intersection | 1.6273 | 30 |
| SEC_ST_03 | RoadSegment | 1.576 | 100 |
| SEC_ST_07 | RoadSegment | 1.3804 | 54 |
| INT_LV_28 | Intersection | 1.2576 | 59 |
| SEC_ST_11 | RoadSegment | 1.2495 | 203 |
| INT_LV_38 | Intersection | 1.1624 | 191 |
| INT_LV_34 | Intersection | 1.1619 | 53 |

## Louvain: спільноти

| community | size | sample | склад |
|---|---|---|---|
| 39 | 39 | ['INT_LV_32', 'INT_LV_33', 'INT_LV_40', 'SEC_ST_12', 'SEC_ST_24', 'SEC_ST_25', 'SEC_ST_29', 'SEC_ST_38'] | {'Vehicle': 9, 'Driver': 6, 'RoadSegment': 5, 'SensorDevice': 5, 'Intersection': 3} |
| 59 | 31 | ['INT_LV_22', 'INT_LV_27', 'INT_LV_28', 'INT_LV_31', 'INT_LV_41', 'SEC_ST_14', 'SEC_ST_15', 'SEC_ST_20'] | {'RoadSegment': 6, 'Intersection': 5, 'SensorDevice': 4, 'TrafficLight': 4, 'Vehicle': 3} |
| 191 | 31 | ['INT_LV_26', 'INT_LV_37', 'INT_LV_38', 'SEC_ST_18', 'SEC_ST_19', 'SEC_ST_30', 'SEC_ST_36', 'CAM_109'] | {'Vehicle': 5, 'RoadSegment': 4, 'DataProcess': 4, 'Intersection': 3, 'SensorDevice': 3} |
| 53 | 24 | ['INT_LV_23', 'INT_LV_34', 'INT_LV_35', 'INT_LV_36', 'SEC_ST_26', 'SEC_ST_27', 'SEC_ST_32', 'SEC_ST_35'] | {'RoadSegment': 5, 'Intersection': 4, 'TrafficLight': 3, 'DataProcess': 3, 'Driver': 2} |
| 30 | 23 | ['INT_LV_24', 'INT_LV_25', 'SEC_ST_16', 'SEC_ST_17', 'CAM_106', 'CAM_110', 'CAM_113', 'LOOP_120'] | {'DataProcess': 5, 'SensorDevice': 4, 'Vehicle': 3, 'Driver': 3, 'Intersection': 2} |
| 203 | 19 | ['INT_LV_12', 'INT_LV_21', 'SEC_ST_11', 'SEC_ST_13', 'RAD_017', 'TL_21_A', 'BUS_A05', 'AMB_02'] | {'DataProcess': 4, 'Vehicle': 3, 'Intersection': 2, 'RoadSegment': 2, 'Driver': 2} |
| 100 | 17 | ['INT_LV_07', 'SEC_ST_03', 'LOOP_105', 'CAM_043', 'TL_07_A', 'AA5821KP', 'FIRE_01', 'BC3055IT'] | {'DataProcess': 4, 'Vehicle': 3, 'SensorDevice': 2, 'Driver': 2, 'Intersection': 1} |
| 113 | 16 | ['INT_LV_29', 'INT_LV_30', 'INT_LV_39', 'SEC_ST_21', 'SEC_ST_22', 'SEC_ST_37', 'TL_29_A', 'BC4148IT'] | {'Intersection': 3, 'RoadSegment': 3, 'Vehicle': 2, 'Driver': 2, 'DataProcess': 2} |
| 114 | 14 | ['SEC_ST_28', 'SEC_ST_31', 'RAD_111', 'RAD_115', 'CAM_122', 'BC4074HP', 'BC4111IT', 'BC4259KA'] | {'Vehicle': 4, 'SensorDevice': 3, 'Driver': 3, 'RoadSegment': 2, 'TrafficAccident': 1} |
| 54 | 13 | ['SEC_ST_07', 'CAM_042', 'TL_12_A', 'AMB_01', 'BC1234AA', 'DRV_9041', 'INC_317', 'CONG_881'] | {'DataProcess': 4, 'Vehicle': 2, 'RoadSegment': 1, 'SensorDevice': 1, 'TrafficLight': 1} |

## Перевірка збереження властивостей

| nodes | with_pagerank | with_community |
|---|---|---|
| 227 | 227 | 227 |
