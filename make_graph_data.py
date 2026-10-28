import csv
import json
import random
from pathlib import Path

NS = "http://www.semanticweb.org/vital/ontologies/2026/9/traffic-monitoring#"
OWL_NI = "http://www.w3.org/2002/07/owl#NamedIndividual"
SRC = Path("data/traffic_monitoring.jsonld")
OUT = Path("data")
SEED = 42
KB_DATE = "2026-10-04"          

PRIMARY = {
    "Intersection": "intersections", "RoadSegment": "segments", "SensorDevice": "sensors",
    "TrafficLight": "lights", "Vehicle": "vehicles", "Driver": "drivers",
    "TrafficAccident": "accidents", "TrafficCongestion": "congestions",
    "Route": "routes", "DataProcess": "processes",
}
SUBTYPE_TO_PRIMARY = {
    "VideoCamera": "SensorDevice", "RadarSensor": "SensorDevice", "InductiveLoop": "SensorDevice",
    "PassengerCar": "Vehicle", "Truck": "Vehicle", "EmergencyCar": "Vehicle", "PublicTransport": "Vehicle",
    "DataCollection": "DataProcess", "DataAnalysis": "DataProcess", "Planning": "DataProcess", "Control": "DataProcess",
}
REL = {
    "detects": "DETECTS", "registers": "REGISTERS", "isMountedOn": "MOUNTED_ON", "occursOn": "OCCURS_ON",
    "movesAlong": "MOVES_ALONG", "crosses": "CROSSES", "drives": "DRIVES", "involvedIn": "INVOLVED_IN",
    "causes": "CAUSES", "affectsRoute": "AFFECTS_ROUTE", "passesThrough": "PASSES_THROUGH",
    "recommendsTo": "RECOMMENDS_TO", "producesRoute": "PRODUCES_ROUTE", "isRecommendedTo": "RECOMMENDED_TO",
    "connectsTo": "CONNECTS_TO", "regulates": "REGULATES", "adjusts": "ADJUSTS", "notifies": "NOTIFIES",
    "respondsTo": "RESPONDS_TO", "classifies": "CLASSIFIES", "suppliesDataTo": "SUPPLIES_DATA_TO",
    "isBasisFor": "IS_BASIS_FOR",
}
PROPS = {
    "intersection_id": "code", "is_traffic_lights": "has_lights", "surface_type": "surface_type", "wear_level": "wear_level",
    "latitude": "latitude", "longitude": "longitude",
    "street_id": "code", "road_name": "road_name", "lanes_count": "lanes_count", "length": "length_m", "speed_limit": "speed_limit",
    "sensor_id": "code", "install_date": "install_date",
    "traffic_light_id": "code", "current_phase": "current_phase", "cycle_duration": "cycle_duration", "mode": "mode",
    "vehicle_id": "code", "direction": "direction", "speed": "speed", "timestamp": "timestamp",
    "driver_id": "code", "license_category": "license_category", "route_preference": "route_preference", "travel_history": "travel_history",
    "incident_id": "code", "incident_type": "incident_type", "status": "status", "blocked_lanes": "blocked_lanes",
    "start_time": "start_time", "duration": "duration_min",
    "congestion_id": "code", "severity_level": "severity_level", "avg_speed": "avg_speed",
    "route_id": "code", "est_travel_time": "est_travel_time_min", "load_rating": "load_rating", "total_length": "total_length_km",
}
COMMON = ["uid", "subtype", "code", "name_uk", "name_en"]
TAIL = ["source", "synthetic"]
COLS = {
    "Intersection": COMMON + ["has_lights", "surface_type", "wear_level", "latitude", "longitude"] + TAIL,
    "RoadSegment": COMMON + ["road_name", "lanes_count", "length_m", "speed_limit", "surface_type", "wear_level"] + TAIL,
    "SensorDevice": COMMON + ["install_date", "latitude", "longitude"] + TAIL,
    "TrafficLight": COMMON + ["current_phase", "cycle_duration", "mode"] + TAIL,
    "Vehicle": COMMON + ["direction", "speed", "latitude", "longitude", "timestamp"] + TAIL,
    "Driver": COMMON + ["license_category", "route_preference", "travel_history"] + TAIL,
    "TrafficAccident": COMMON + ["incident_type", "status", "blocked_lanes", "start_time", "duration_min"] + TAIL,
    "TrafficCongestion": COMMON + ["severity_level", "avg_speed", "duration_min", "start_time"] + TAIL,
    "Route": COMMON + ["est_travel_time_min", "load_rating", "total_length_km"] + TAIL,
    "DataProcess": COMMON + TAIL,
}
REL_COLS = ["from_uid", "to_uid", "type", "source", "confidence", "validFrom"]


def loc(u):
    return u.replace(NS, "")


def val(v):
    x = v["@value"]
    return str(x).lower() if isinstance(x, bool) else x


def load_real():
    nodes, rels = {}, []
    for n in json.loads(SRC.read_text(encoding="utf-8")):
        types = [loc(t) for t in n.get("@type", []) if t.startswith(NS)]
        if OWL_NI not in n.get("@type", []) or not types:
            continue
        sub = types[0]
        prim = SUBTYPE_TO_PRIMARY.get(sub, sub)
        uid = loc(n["@id"])
        row = {"uid": uid, "subtype": sub if sub != prim else "", "source": "ontology:lab7", "synthetic": "false"}
        for k, vs in n.items():
            if k.startswith("@"):
                continue
            key = loc(k)
            if key in PROPS:
                row[PROPS[key]] = val(vs[0])
            elif k.endswith("#label"):
                for v in vs:
                    row["name_" + v["@language"]] = v["@value"]
            elif key in REL:
                for v in vs:
                    rels.append({"from_uid": uid, "to_uid": loc(v["@id"]), "type": REL[key]})
        nodes[uid] = (prim, row)
    return nodes, rels


def prov_real(rel, nodes):
    """Походження реальних зв'язків. validFrom: подія -> start_time, монтаж -> install_date, інакше дата знімка."""
    f, t = nodes[rel["from_uid"]][1], nodes[rel["to_uid"]][1]
    vf = f.get("start_time") or (f.get("install_date") if rel["type"] == "MOUNTED_ON" else None) or t.get("start_time") or KB_DATE
    rel.update(source="ontology:lab7", confidence=1.0, validFrom=str(vf)[:10])


def synth(nodes, rels):
    rnd = random.Random(SEED)
    streets = ["Horodotska St.", "Stryiska St.", "Chornovola Ave.", "Lychakivska St.", "Kulparkivska St.", "Zelena St.",
               "Pasichna St.", "Shevchenka Ave.", "Naukova St.", "Sykhivska St."]
    streets_uk = ["Городоцька", "Стрийська", "Чорновола", "Личаківська", "Кульпарківська", "Зелена", "Пасічна", "Шевченка", "Наукова", "Сихівська"]
    S = {"ints": [], "segs": [], "lights": [], "sens": [], "veh": [], "drv": [], "acc": [], "cong": [], "routes": []}

    def add(prim, uid, sub, **k):
        nodes[uid] = (prim, dict(uid=uid, subtype=sub, source="synthetic:seed42", synthetic="true", **k))
        return uid

    def rel(f, t, typ, conf=1.0, vf=KB_DATE):
        rels.append({"from_uid": f, "to_uid": t, "type": typ, "source": "synthetic:seed42", "confidence": round(conf, 2), "validFrom": vf})

    def lat():
        return round(49.80 + rnd.random() * 0.07, 4)

    def lon():
        return round(23.98 + rnd.random() * 0.09, 4)

    # перехрестя 22..41 (20) + світлофори на двох третинах
    for i in range(22, 42):
        lights = "true" if i % 3 else "false"
        u = add("Intersection", f"INT_LV_{i:02d}", "", code=f"INT-LV-{i:02d}", name_uk=f"Перехрестя INT-LV-{i:02d}",
                name_en=f"Intersection INT-LV-{i:02d}", has_lights=lights,
                surface_type=rnd.choice(["asphalt", "asphalt + cobblestone", "concrete"]),
                wear_level=rnd.choice(["low", "medium", "moderate"]), latitude=lat(), longitude=lon())
        S["ints"].append(u)
        if lights == "true":
            tl = add("TrafficLight", f"TL_{i:02d}_A", "", code=f"TL-{i:02d}-A", name_uk=f"Світлофор TL-{i:02d}-A",
                     name_en=f"Traffic light TL-{i:02d}-A", current_phase=rnd.choice(["red", "yellow", "green"]),
                     cycle_duration=rnd.choice([70, 80, 90, 100]), mode=rnd.choice(["adaptive", "fixed-time"]))
            S["lights"].append(tl)
            rel(tl, u, "REGULATES")
    allints = ["INT_LV_07", "INT_LV_12", "INT_LV_21"] + S["ints"]
    for k, i in enumerate(range(12, 40)):
        si = rnd.randrange(len(streets))
        u = add("RoadSegment", f"SEC_ST_{i:02d}", "", code=f"SEC-ST-{i:02d}",
                name_uk=f"Вулиця {streets_uk[si]} (SEC-ST-{i:02d})", name_en=f"{streets[si]} (SEC-ST-{i:02d})",
                road_name=streets[si], lanes_count=rnd.choice([2, 2, 3, 4]), length_m=rnd.randrange(300, 1600, 10),
                speed_limit=rnd.choice([40, 50, 50, 60]), surface_type=rnd.choice(["asphalt", "concrete", "asphalt + cobblestone"]),
                wear_level=rnd.choice(["low", "medium", "moderate"]))
        S["segs"].append(u)
        if k < 20:
            a, b = allints[k % len(allints)], allints[(k + 1) % len(allints)]
        else:
            a = rnd.choice(allints)
            b = rnd.choice([x for x in allints if x != a])
        rel(u, a, "CONNECTS_TO")
        rel(u, b, "CONNECTS_TO")
    allsegs = ["SEC_ST_03", "SEC_ST_07", "SEC_ST_11"] + S["segs"]
    subs = ["VideoCamera", "RadarSensor", "InductiveLoop", "VideoCamera"] * 5
    for n_, sub in zip(range(106, 126), subs):
        pre = {"VideoCamera": "CAM", "RadarSensor": "RAD", "InductiveLoop": "LOOP"}[sub]
        code = f"{pre}-{n_:03d}"
        u = add("SensorDevice", code.replace("-", "_"), sub, code=code, name_uk=f"Датчик {code}", name_en=f"Sensor {code}",
                install_date=f"202{rnd.choice([3, 4, 5])}-{rnd.randrange(1, 13):02d}-{rnd.randrange(1, 28):02d}",
                latitude=lat(), longitude=lon())
        S["sens"].append(u)
        rel(u, rnd.choice(allints + allsegs), "MOUNTED_ON", vf=nodes[u][1]["install_date"])
    types = [("PassengerCar", "Легковик", "Passenger car"), ("Truck", "Вантажівка", "Truck"),
             ("PublicTransport", "Автобус", "Bus"), ("PassengerCar", "Легковик", "Passenger car")]
    for j in range(20):
        sub, uk, en = types[j % 4]
        plate = f"BC{4000 + j * 37:04d}{rnd.choice(['KA', 'HP', 'IT', 'XO'])}"
        v = add("Vehicle", plate, sub, code=plate, name_uk=f"{uk} {plate}", name_en=f"{en} {plate}",
                direction=rnd.choice(["North", "South", "East", "West"]), speed=round(rnd.random() * 60, 1),
                latitude=lat(), longitude=lon(), timestamp=f"{KB_DATE}T18:15:00+00:00")
        S["veh"].append(v)
        d = add("Driver", f"DRV_{9046 + j}", "", code=f"DRV-{9046 + j}", name_uk=f"Водій DRV-{9046 + j}",
                name_en=f"Driver DRV-{9046 + j}", license_category={"PassengerCar": "B", "Truck": "C", "PublicTransport": "D"}[sub],
                route_preference=rnd.choice(["fastest time", "shortest distance", "avoid cobblestone", "avoid city centre"]),
                travel_history=f"{rnd.randrange(3, 40)} trips/week")
        S["drv"].append(d)
        rel(d, v, "DRIVES")
        rel(v, rnd.choice(allsegs), "MOVES_ALONG")
        if rnd.random() < 0.6:
            rel(v, rnd.choice(allints), "CROSSES")
        for s in rnd.sample(S["sens"], 2):
            rel(s, v, "DETECTS", conf=rnd.uniform(0.7, 0.99))
    for j in range(10):
        place = rnd.choice(allsegs)
        st = f"{KB_DATE}T{rnd.randrange(6, 20):02d}:{rnd.randrange(0, 60):02d}:00"
        a = add("TrafficAccident", f"INC_{320 + j}", "", code=f"INC-{320 + j}", name_uk=f"ДТП INC-{320 + j}",
                name_en=f"Accident INC-{320 + j}", incident_type=rnd.choice(["collision", "breakdown"]),
                status=rnd.choice(["active", "resolved"]), blocked_lanes=rnd.choice([1, 1, 2]), start_time=st,
                duration_min=rnd.randrange(15, 90, 5))
        c = add("TrafficCongestion", f"CONG_{884 + j}", "", code=f"CONG-{884 + j}", name_uk=f"Затор CONG-{884 + j}",
                name_en=f"Congestion CONG-{884 + j}", severity_level=rnd.randrange(2, 10), avg_speed=round(rnd.uniform(4, 30), 1),
                duration_min=rnd.randrange(10, 60, 5), start_time=st)
        S["acc"].append(a)
        S["cong"].append(c)
        rel(a, place, "OCCURS_ON", vf=st[:10])
        rel(c, place, "OCCURS_ON", vf=st[:10])
        rel(a, c, "CAUSES", vf=st[:10])
        for v in rnd.sample(S["veh"], rnd.choice([1, 2])):
            rel(v, a, "INVOLVED_IN", vf=st[:10])
        for s in rnd.sample(S["sens"], 2):
            rel(s, a, "REGISTERS", conf=rnd.uniform(0.75, 0.99), vf=st[:10])
    for j in range(3, 9):
        u = add("Vehicle", f"AMB_{j:02d}", "EmergencyCar", code=f"AMB-{j:02d}", name_uk=f"Швидка AMB-{j:02d}",
                name_en=f"Ambulance AMB-{j:02d}", direction=rnd.choice(["North", "South", "East", "West"]),
                speed=round(rnd.uniform(30, 70), 1), latitude=lat(), longitude=lon(), timestamp=f"{KB_DATE}T18:12:00+00:00")
        rel(u, rnd.choice(S["acc"]), "RESPONDS_TO")
        rel(u, rnd.choice(allsegs), "MOVES_ALONG")
    for j in range(6, 18):
        r = add("Route", f"R_OPT_{j}", "", code=f"R-OPT-{j}", name_uk=f"Маршрут R-OPT-{j}", name_en=f"Route R-OPT-{j}",
                est_travel_time_min=rnd.randrange(10, 45), load_rating=rnd.choice(["low", "moderate", "high"]),
                total_length_km=round(rnd.uniform(2, 9), 1))
        S["routes"].append(r)
        for x in rnd.sample(allsegs, rnd.choice([2, 3])) + rnd.sample(allints, 1):
            rel(r, x, "PASSES_THROUGH")
        rel(r, rnd.choice(S["drv"]), "RECOMMENDED_TO")
    for c in S["cong"]:
        for r in rnd.sample(S["routes"] + ["R_OPT_3", "R_OPT_5", "R_ALT_1"], 2):
            rel(c, r, "AFFECTS_ROUTE", vf=nodes[c][1]["start_time"][:10])
    for j in range(4, 9):
        col = add("DataProcess", f"COLLECT_{j}", "DataCollection", code=f"COLLECT-{j}", name_uk=f"Збір даних №{j}", name_en=f"Data collection #{j}")
        an = add("DataProcess", f"ANALYSIS_{j}", "DataAnalysis", code=f"ANALYSIS-{j}", name_uk=f"Аналіз даних №{j}", name_en=f"Data analysis #{j}")
        pl = add("DataProcess", f"PLANNING_{j}", "Planning", code=f"PLANNING-{j}", name_uk=f"Планування №{j}", name_en=f"Planning #{j}")
        ct = add("DataProcess", f"CONTROL_{j}", "Control", code=f"CONTROL-{j}", name_uk=f"Керування №{j}", name_en=f"Control #{j}")
        rel(col, an, "SUPPLIES_DATA_TO")
        rel(an, pl, "IS_BASIS_FOR")
        rel(an, ct, "IS_BASIS_FOR")
        k = j - 4
        for e in (S["acc"][2 * k % 10], S["cong"][2 * k % 10], S["acc"][(2 * k + 1) % 10], S["cong"][(2 * k + 1) % 10]):
            rel(an, e, "CLASSIFIES", conf=rnd.uniform(0.8, 0.99))
        rel(pl, rnd.choice(S["routes"]), "PRODUCES_ROUTE")
        rel(pl, rnd.choice(S["drv"]), "RECOMMENDS_TO")
        rel(ct, rnd.choice(S["lights"]), "ADJUSTS")


def main():
    nodes, rels = load_real()
    for r in rels:
        prov_real(r, nodes)
    n_real, r_real = len(nodes), len(rels)
    synth(nodes, rels)
    seen, clean = set(), []
    for r in rels:
        assert r["from_uid"] in nodes and r["to_uid"] in nodes, r
        key = (r["from_uid"], r["to_uid"], r["type"])
        if key not in seen:
            seen.add(key)
            clean.append(r)
    OUT.mkdir(exist_ok=True)
    by = {p: [] for p in PRIMARY}
    for _, (prim, row) in nodes.items():
        by[prim].append(row)
    for prim, fn in PRIMARY.items():
        with open(OUT / f"nodes_{fn}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=COLS[prim], extrasaction="raise", restval="")
            w.writeheader()
            w.writerows(by[prim])
    with open(OUT / "rels.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=REL_COLS)
        w.writeheader()
        w.writerows(clean)
    print(f"реальних: {n_real} вузлів / {r_real} зв'язків; усього: {len(nodes)} вузлів / {len(clean)} зв'язків; "
          f"типів зв'язків: {len({r['type'] for r in clean})}")


if __name__ == "__main__":
    main()
