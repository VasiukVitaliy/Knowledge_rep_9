from collections import defaultdict
from pathlib import Path
from neo import driver, run, md_table

out = ["# Результати GDS (автогенерація run_gds.py)\n"]
with driver() as drv, drv.session() as s:
    ver = run(s, "RETURN gds.version() AS gds_version")[0]["gds_version"]
    out.append(f"GDS версія: `{ver}`\n")
    for g in ("traffic", "trafficU"):
        s.run("CALL gds.graph.drop($g, false)", g=g).consume()
    s.run("CALL gds.graph.project('traffic', '*', '*')").consume() 
    s.run("CALL gds.graph.project('trafficU', '*', {ALL: {type: '*', orientation: 'UNDIRECTED'}})").consume()  # для Louvain

    pr = run(s, "CALL gds.pageRank.write('traffic', {writeProperty: 'pagerank', maxIterations: 20, dampingFactor: 0.85}) "
                "YIELD nodePropertiesWritten, ranIterations, didConverge RETURN nodePropertiesWritten, ranIterations, didConverge")
    lv = run(s, "CALL gds.louvain.write('trafficU', {writeProperty: 'community', concurrency: 1}) "
                "YIELD communityCount, modularity, nodePropertiesWritten RETURN communityCount, modularity, nodePropertiesWritten")
    out += ["## Запуск\n", md_table(pr), md_table(lv)]

    top = run(s, "MATCH (n) WHERE n.pagerank IS NOT NULL RETURN n.uid AS uid, [l IN labels(n) WHERE NOT l IN ['TrafficEvent','RoadInfrastructureElement']][0] AS kind, "
                 "round(n.pagerank, 4) AS pagerank, n.community AS community ORDER BY pagerank DESC LIMIT 10")
    out += ["## PageRank: топ-10\n", md_table(top)]
    comm = run(s, "MATCH (n) WHERE n.community IS NOT NULL WITH n.community AS community, collect(n) AS ms "
                  "RETURN community, size(ms) AS size, "
                  "[m IN ms | [l IN labels(m) WHERE NOT l IN ['TrafficEvent','RoadInfrastructureElement']][0]] AS kinds, "
                  "[m IN ms | m.uid][..8] AS sample ORDER BY size DESC")
    for c in comm:
        cnt = defaultdict(int)
        for k in c.pop("kinds"):
            cnt[k] += 1
        c["склад"] = dict(sorted(cnt.items(), key=lambda x: -x[1])[:5])
    out += ["## Louvain: спільноти\n", md_table(comm)]
    chk = run(s, "MATCH (n) RETURN count(n) AS nodes, count(n.pagerank) AS with_pagerank, count(n.community) AS with_community")
    out += ["## Перевірка збереження властивостей\n", md_table(chk)]
    for g in ("traffic", "trafficU"):
        s.run("CALL gds.graph.drop($g, false)", g=g).consume()
Path("docs/gds_results_auto.md").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
