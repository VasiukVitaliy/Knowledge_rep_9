import os
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "")
DB = os.getenv("NEO4J_DATABASE", "neo4j")


def driver():
    d = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    d.verify_connectivity()
    return d


def statements(path):
    lines = [l for l in Path(path).read_text(encoding="utf-8").splitlines() if not l.strip().startswith("//")]
    return [s.strip() for s in "\n".join(lines).split(";") if s.strip()]


def run(session, query, **params):
    return [r.data() for r in session.run(query, **params)]


def counts(session):
    n = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
    r = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
    return n, r


def md_table(rows):
    if not rows:
        return "_порожній результат_\n"
    cols = list(rows[0].keys())
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        out.append("| " + " | ".join(str(r[c]).replace("|", "\\|") for c in cols) + " |")
    return "\n".join(out) + "\n"
