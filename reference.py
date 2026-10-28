import csv, json, collections
from pathlib import Path
import networkx as nx

D = Path("data")
FILES = ["intersections", "segments", "sensors", "lights", "vehicles", "drivers", "accidents", "congestions", "routes", "processes"]
LABEL = dict(zip(FILES, ["Intersection", "RoadSegment", "SensorDevice", "TrafficLight", "Vehicle", "Driver", "TrafficAccident", "TrafficCongestion", "Route", "DataProcess"]))


def load():
    G = nx.MultiDiGraph()
    for fn in FILES:
        for r in csv.DictReader(open(D / f"nodes_{fn}.csv", encoding="utf-8")):
            labels = {LABEL[fn]}
            if r["subtype"]:
                labels.add(r["subtype"])
            if fn in ("intersections", "segments"):
                labels.add("RoadInfrastructureElement")
            if fn in ("accidents", "congestions"):
                labels.add("TrafficEvent")
            G.add_node(r["uid"], labels=labels, **r)
    for r in csv.DictReader(open(D / "rels.csv", encoding="utf-8")):
        G.add_edge(r["from_uid"], r["to_uid"], key=r["type"], type=r["type"], confidence=float(r["confidence"]), source=r["source"])
    return G


G = load()
N = G.nodes
lab = lambda u, l: l in N[u]["labels"]
out = lambda u, t=None: [(v, d["type"]) for _, v, d in G.out_edges(u, data=True) if t is None or d["type"] in t]


def kind(u, skip=("TrafficEvent", "RoadInfrastructureElement")):
    return sorted(l for l in N[u]["labels"] if l not in skip)[0]


def bfs_depth(start, types, maxd):
    depth, frontier = {start: 0}, [start]
    for d in range(1, maxd + 1):
        nxt = []
        for u in frontier:
            for v, _ in out(u, types):
                if v not in depth:
                    depth[v] = d
                    nxt.append(v)
        frontier = nxt
    return {k: v for k, v in depth.items() if k != start}


def undirected_int_graph():
    H = nx.Graph()
    for u, v, d in G.edges(data=True):
        if d["type"] == "CONNECTS_TO":
            H.add_edge(u, v)
    return H


def run():
    R = {"nodes": G.number_of_nodes(), "relationships": G.number_of_edges()}
    R["labels"] = dict(collections.Counter(l for u in N for l in N[u]["labels"]))
    R["rel_types"] = dict(collections.Counter(d["type"] for *_, d in G.edges(data=True)))
    R["real_nodes"] = sum(1 for u in N if N[u]["synthetic"] == "false")
    R["real_rels"] = sum(1 for *_, d in G.edges(data=True) if d["source"].startswith("ontology"))
    assert all(len(N[u]["labels"]) >= 1 for u in N)
    R["q01"] = sorted((u, N[u]["incident_type"], v, N[u]["synthetic"]) for u in N if lab(u, "TrafficAccident") and N[u]["status"] == "active" for v, t in out(u, {"OCCURS_ON"}))
    sev = [c for c in N if lab(c, "TrafficCongestion") and int(N[c]["severity_level"]) >= 8 and any(lab(s, "RoadSegment") and N[s]["road_name"] == "Horodotska St." for s, _ in out(c, {"OCCURS_ON"}))]
    R["q02"] = {"value": bool(sev), "congestions": sorted(sev)}
    R["q03"] = sorted(collections.Counter(next(l for l in N[u]["labels"] if l != "SensorDevice") for u in N if lab(u, "SensorDevice")).items(), key=lambda x: (-x[1], x[0]))

    rows = []
    for r in N:
        if lab(r, "Route"):
            ds = sorted(d for d in {v for u, v, dd in G.out_edges(r, data=True) if dd["type"] == "RECOMMENDED_TO"})
            rows.append((r, N[r]["load_rating"], ds, len(ds)))
    R["q04"] = sorted(rows, key=lambda x: (x[3], x[0]))

    q5 = collections.defaultdict(set)
    for a in N:
        if lab(a, "TrafficAccident"):
            for c, _ in out(a, {"CAUSES"}):
                for r, _ in out(c, {"AFFECTS_ROUTE"}):
                    q5[a].add(r)
    R["q05"] = sorted(((a, sorted(r), len(r)) for a, r in q5.items()), key=lambda x: (-x[2], x[0]))

    H = undirected_int_graph()
    dist = nx.single_source_shortest_path_length(H, "INT_LV_12", cutoff=6)
    R["q06"] = sorted(((u, d // 2) for u, d in dist.items() if u != "INT_LV_12" and lab(u, "Intersection")), key=lambda x: (x[1], x[0]))
    p = nx.shortest_path(H, "INT_LV_07", "INT_LV_30")
    R["q07"] = {"path_example": p, "segments": (len(p) - 1) // 2, "note": "при кількох найкоротших шляхах Neo4j повертає один довільний; перевіряйте довжину"}

    rows = []
    for d in N:
        if lab(d, "Driver"):
            for v, t in out(d, {"DRIVES"}):
                acc = sorted(a for a, _ in out(v, {"INVOLVED_IN"}) if N[a]["status"] == "active")
                if acc:
                    rows.append((d, v, acc))
    R["q08"] = sorted(rows)

    dep = bfs_depth("INC_317", {"CAUSES", "AFFECTS_ROUTE", "RECOMMENDED_TO"}, 4)
    R["q09"] = sorted(((u, kind(u), d) for u, d in dep.items()), key=lambda x: (x[2], x[0]))
    dep = bfs_depth("COLLECT_1", {"SUPPLIES_DATA_TO", "IS_BASIS_FOR", "PRODUCES_ROUTE", "RECOMMENDS_TO", "RECOMMENDED_TO", "ADJUSTS", "NOTIFIES"}, 5)
    g = collections.defaultdict(list)
    for u, d in dep.items():
        k = [l for l in sorted(N[u]["labels"]) if l not in ("DataProcess", "RoadInfrastructureElement", "TrafficEvent")]
        g[(d, k[0])].append(u)
    R["q10"] = [(d, k, sorted(v)) for (d, k), v in sorted(g.items())]

    c = collections.defaultdict(list)
    for *_, d in G.edges(data=True):
        if d["confidence"] < 0.8:
            c[(d["type"], d["source"])].append(d["confidence"])
    R["q11"] = sorted(((t, s, len(v), round(sum(v) / len(v), 2)) for (t, s), v in c.items()), key=lambda x: (-x[2], x[0]))

    real = lambda u: N[u]["synthetic"] == "false"
    R["v1"] = sorted((a, r) for a in N if lab(a, "TrafficAccident") and real(a) for c, _ in out(a, {"CAUSES"}) if real(c) for r, _ in out(c, {"AFFECTS_ROUTE"}) if real(r))
    dep = {u: d for u, d in bfs_depth("INC_317", {"CAUSES", "AFFECTS_ROUTE", "RECOMMENDED_TO"}, 4).items() if real(u)}
    R["v2"] = sorted(dep.items(), key=lambda x: (x[1], x[0]))
    R["v3"] = sorted((d, v, a) for d in N if lab(d, "Driver") and real(d) for v, _ in out(d, {"DRIVES"}) if real(v) for a, _ in out(v, {"INVOLVED_IN"}) if real(a) and N[a]["status"] == "active")

    nodes = list(G.nodes); idx = {u: i for i, u in enumerate(nodes)}
    outdeg = {u: G.out_degree(u) for u in nodes}
    inc = collections.defaultdict(list)
    for u, v, _ in G.edges(data=True):
        inc[v].append(u)
    s = {u: 1.0 for u in nodes}
    for _ in range(20):
        s = {u: 0.15 + 0.85 * sum(s[w] / outdeg[w] for w in inc[u]) for u in nodes}
    top = sorted(s.items(), key=lambda x: -x[1])[:10]
    R["pagerank_top10"] = [(u, kind(u), round(v, 4)) for u, v in top]
  
    U = nx.Graph(); U.add_nodes_from(nodes); U.add_edges_from((u, v) for u, v, _ in G.edges(data=True))
    comms = sorted(nx.community.louvain_communities(U, seed=42), key=len, reverse=True)
    R["louvain"] = [{"size": len(c), "kinds": dict(collections.Counter(kind(u) for u in c).most_common(4)), "sample": sorted(c)[:6]} for c in comms]
    R["louvain_modularity"] = round(nx.community.modularity(U, comms), 4)
    return R


if __name__ == "__main__":
    R = run()
    Path("docs").mkdir(exist_ok=True)
    Path("docs/reference_results.json").write_text(json.dumps(R, ensure_ascii=False, indent=1, default=list), encoding="utf-8")
    print(R["nodes"], R["relationships"], "real:", R["real_nodes"], R["real_rels"])
    for k in ["q01", "q02", "q03", "q04", "q05", "q07", "q08", "q09", "q10", "q11", "v1", "v2", "v3", "pagerank_top10"]:
        print(k, R[k])
    print("q06", R["q06"][:8], len(R["q06"]))
    print("louvain", [(c["size"], c["kinds"]) for c in R["louvain"]], R["louvain_modularity"])
