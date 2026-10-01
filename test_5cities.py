import sys
sys.stdout.reconfigure(encoding='utf-8')
import seed_data, graph_db, cypher_queries, algorithms

print(f"Total Cities: {len(seed_data.CITIES)}")
print(f"Total Places: {len(seed_data.PLACES)}")
print(f"Graph Vertices: {len(graph_db.kg_service.nodes)}")
print(f"Graph Edges: {len(graph_db.kg_service.edges)}")

queries = [
    ("Mumbai", "Which restaurants are near Gateway of India?"),
    ("Delhi", "Find hotels near Red Fort."),
    ("Pune", "Find restaurants near Shaniwar Wada."),
    ("Chennai", "Show museums in Chennai."),
    ("Hyderabad", "Find hotels near Charminar."),
    ("Transit Dijkstra", "How can I reach Charminar from the nearest station?"),
    ("Set Union", "Show museums and monuments.")
]

for tag, q in queries:
    res = cypher_queries.bot_engine.process_query(q)
    print(f"[{tag}] '{q}' -> Records: {len(res['records'])}, Cypher: {bool(res['cypher_query'])}")

# Test Dijkstra between Hyderabad Metro and Charminar
dijkstra_res = graph_db.kg_service.math_engine.run_dijkstra("hyd_metro_charminar", "hyd_charminar")
print(f"Dijkstra Hyd Metro -> Charminar: Distance {dijkstra_res.get('total_distance_km')} km, Path: {dijkstra_res.get('shortest_path')}")

# Test Set Theory across all 5 cities
set_res = graph_db.kg_service.math_engine.run_set_operation({"category": "Monument"}, {"category": "Museum"}, "UNION")
print(f"Set Union (Monuments ∪ Museums): |Union| = {set_res['cardinality_Union']} places across 5 cities. PIE holds: {set_res['inclusion_exclusion_principle']['holds']}")
