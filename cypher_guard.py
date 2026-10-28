import re

SCHEMA = {
    "labels": {
        "Intersection": ["uid", "code", "name_uk", "name_en", "has_lights", "surface_type", "wear_level", "latitude", "longitude", "source", "synthetic"],
        "RoadSegment": ["uid", "code", "name_uk", "name_en", "road_name", "lanes_count", "length_m", "speed_limit", "surface_type", "wear_level", "source", "synthetic"],
        "SensorDevice": ["uid", "code", "name_uk", "name_en", "install_date", "latitude", "longitude", "source", "synthetic"],
        "TrafficLight": ["uid", "code", "name_uk", "name_en", "current_phase", "cycle_duration", "mode", "source", "synthetic"],
        "Vehicle": ["uid", "code", "name_uk", "name_en", "direction", "speed", "latitude", "longitude", "timestamp", "source", "synthetic"],
        "Driver": ["uid", "code", "name_uk", "name_en", "license_category", "route_preference", "travel_history", "source", "synthetic"],
        "TrafficAccident": ["uid", "code", "name_uk", "name_en", "incident_type", "status", "blocked_lanes", "start_time", "duration_min", "source", "synthetic"],
        "TrafficCongestion": ["uid", "code", "name_uk", "name_en", "severity_level", "avg_speed", "duration_min", "start_time", "source", "synthetic"],
        "Route": ["uid", "code", "name_uk", "name_en", "est_travel_time_min", "load_rating", "total_length_km", "source", "synthetic"],
        "DataProcess": ["uid", "code", "name_uk", "name_en", "source", "synthetic"],
    },
    "extra_labels": ["TrafficEvent", "RoadInfrastructureElement", "VideoCamera", "RadarSensor", "InductiveLoop",
                     "PassengerCar", "Truck", "EmergencyCar", "PublicTransport", "DataCollection", "DataAnalysis", "Planning", "Control"],
    "rels": {
        "DETECTS": ("SensorDevice", "Vehicle"), "REGISTERS": ("SensorDevice", "TrafficEvent"), "MOUNTED_ON": ("SensorDevice", "RoadInfrastructureElement"),
        "OCCURS_ON": ("TrafficEvent", "RoadInfrastructureElement"), "MOVES_ALONG": ("Vehicle", "RoadInfrastructureElement"), "CROSSES": ("Vehicle", "Intersection"),
        "DRIVES": ("Driver", "Vehicle"), "INVOLVED_IN": ("Vehicle", "TrafficAccident"), "CAUSES": ("TrafficAccident", "TrafficCongestion"),
        "AFFECTS_ROUTE": ("TrafficCongestion", "Route"), "PASSES_THROUGH": ("Route", "RoadInfrastructureElement"), "RECOMMENDS_TO": ("DataProcess", "Driver"),
        "PRODUCES_ROUTE": ("DataProcess", "Route"), "RECOMMENDED_TO": ("Route", "Driver"), "CONNECTS_TO": ("RoadSegment", "Intersection"),
        "REGULATES": ("TrafficLight", "Intersection"), "ADJUSTS": ("DataProcess", "TrafficLight"), "NOTIFIES": ("DataProcess", "Vehicle"),
        "RESPONDS_TO": ("Vehicle", "TrafficAccident"), "CLASSIFIES": ("DataProcess", "TrafficEvent"), "SUPPLIES_DATA_TO": ("DataProcess", "DataProcess"),
        "IS_BASIS_FOR": ("DataProcess", "DataProcess"),
    },
    "rel_props": ["source", "confidence", "validFrom"],
}
ALL_LABELS = set(SCHEMA["labels"]) | set(SCHEMA["extra_labels"])
ALL_PROPS = {p for ps in SCHEMA["labels"].values() for p in ps} | set(SCHEMA["rel_props"])
FORBIDDEN = re.compile(r"\b(CREATE|MERGE|DELETE|DETACH|SET|REMOVE|DROP|LOAD|FOREACH|CALL|ALTER|GRANT|DENY|REVOKE|START|STOP|TERMINATE|USE)\b|apoc\.|dbms\.", re.I)


def clean(q):
    q = (q or "").strip()
    q = re.sub(r"^```\w*\s*", "", q)
    q = re.sub(r"\s*```$", "", q)
    return q.strip().rstrip(";").strip()


def _strip_strings(q):
    return re.sub(r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"", "''", q)


def forbidden(q):
    """Повертає перший знайдений заборонений токен або None."""
    m = FORBIDDEN.search(_strip_strings(q))
    return m.group(0) if m else None


def schema_check(q):
    """Повертає список невідомих елементів (порожній список = схема дотримана)."""
    s = _strip_strings(q)
    bad = []
    for m in re.finditer(r"\(\s*[A-Za-z_]\w*\s*((?::\s*[A-Za-z_]\w*\s*)+)|\(\s*((?::\s*[A-Za-z_]\w*\s*)+)", s):
        for lab in re.findall(r":\s*([A-Za-z_]\w*)", m.group(1) or m.group(2)):
            if lab not in ALL_LABELS:
                bad.append(f"мітка:{lab}")
    for m in re.finditer(r"\[\s*[A-Za-z_]?\w*\s*:\s*([A-Za-z_0-9|:\s]+)", s):
        for t in re.split(r"[|:\s]+", m.group(1).strip()):
            if t and t not in SCHEMA["rels"]:
                bad.append(f"тип:{t}")
    for m in re.finditer(r"(?<=[\w\)])\.([A-Za-z_]\w*)", s):
        if m.group(1) not in ALL_PROPS:
            bad.append(f"властивість:{m.group(1)}")
    for m in re.finditer(r"[{,]\s*([A-Za-z_]\w*)\s*:", s):
        if m.group(1) not in ALL_PROPS:
            bad.append(f"властивість:{m.group(1)}")
    return sorted(set(bad))


def add_limit(q, n=100):
    if re.search(r"\bLIMIT\s+\d+\s*$", q, re.I) or re.search(r"\bLIMIT\b", q, re.I):
        return q
    return q + f"\nLIMIT {n}"


def schema_prompt():
    lines = ["Мітки вузлів і властивості:"]
    for l, ps in SCHEMA["labels"].items():
        lines.append(f"  (:{l}) {{{', '.join(ps)}}}")
    lines.append("Додаткові мітки (підкласи/надкласи): " + ", ".join(SCHEMA["extra_labels"]))
    lines.append("  TrafficEvent = TrafficAccident|TrafficCongestion; RoadInfrastructureElement = Intersection|RoadSegment;")
    lines.append("  VideoCamera/RadarSensor/InductiveLoop ⊂ SensorDevice; PassengerCar/Truck/EmergencyCar/PublicTransport ⊂ Vehicle;")
    lines.append("  DataCollection/DataAnalysis/Planning/Control ⊂ DataProcess.")
    lines.append("Зв'язки (напрям суворий):")
    for t, (a, b) in SCHEMA["rels"].items():
        lines.append(f"  (:{a})-[:{t}]->(:{b})")
    lines.append("Властивості зв'язків: source, confidence (0..1), validFrom (date).")
    return "\n".join(lines)
