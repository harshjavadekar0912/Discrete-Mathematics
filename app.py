"""
Tourist Guide Knowledge Graph Chatbot
Flask Backend Application
Discrete Mathematics Project
"""

import os
from flask import Flask, render_template, request, jsonify

from graph_db import kg_service
from cypher_queries import bot_engine


app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["JSON_AS_ASCII"] = False


# =============================================================================
# HTML PAGE ROUTES
# =============================================================================

@app.route("/")
def index():
    """Chatbot Home Interface."""
    return render_template(
        "index.html",
        page="chat",
        neo4j_connected=kg_service.is_neo4j_connected,
        total_nodes=len(kg_service.nodes),
        total_edges=len(kg_service.edges)
    )


@app.route("/graph")
def graph_page():
    """Interactive Knowledge Graph Visualizer."""
    return render_template(
        "graph.html",
        page="graph",
        neo4j_connected=kg_service.is_neo4j_connected,
        total_nodes=len(kg_service.nodes),
        total_edges=len(kg_service.edges)
    )


@app.route("/discrete-math")
def discrete_math_page():
    """Discrete Mathematics Algorithms & Concepts Studio."""
    return render_template(
        "discrete_math.html",
        page="math",
        neo4j_connected=kg_service.is_neo4j_connected,
        places=[p for p in kg_service.nodes if p.get("category") != "City"]
    )


@app.route("/places")
def places_directory_page():
    """Tourist Places Explorer & Cards."""
    return render_template(
        "explorer.html",
        page="places",
        neo4j_connected=kg_service.is_neo4j_connected,
        places=[p for p in kg_service.nodes if p.get("category") != "City"]
    )


# =============================================================================
# REST API ENDPOINTS
# =============================================================================

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Chatbot query endpoint."""
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    api_key = data.get("api_key", "").strip() or None

    if not message:
        return jsonify({"error": "Empty message prompt"}), 400

    response = bot_engine.process_query(message, user_api_key=api_key)
    return jsonify(response)


@app.route("/api/graph/data", methods=["GET"])
def api_graph_data():
    """Returns node and edge data for vis-network graph visualization."""
    city_filter = request.args.get("city", "").strip() or None
    graph_data = kg_service.get_graph_visualization_data(filter_city=city_filter)
    return jsonify(graph_data)


@app.route("/api/places/list", methods=["GET"])
def api_places_list():
    """Returns places list filtered by category, city, or price."""
    category = request.args.get("category", "").strip() or None
    city = request.args.get("city", "").strip() or None
    places = kg_service.get_all_places(category=category, city=city)
    return jsonify({"places": places, "count": len(places)})


@app.route("/api/algorithms/bfs", methods=["POST"])
def api_bfs():
    """Executes Breadth-First Search with full step trace."""
    data = request.get_json() or {}
    start_id = data.get("start_id", "mumbai_gateway")
    target_category = data.get("target_category") or None
    max_depth = int(data.get("max_depth", 3))

    res = kg_service.math_engine.run_bfs(start_id, target_category, max_depth)
    return jsonify(res)


@app.route("/api/algorithms/dfs", methods=["POST"])
def api_dfs():
    """Executes Depth-First Search with full LIFO stack trace and timestamps."""
    data = request.get_json() or {}
    start_id = data.get("start_id", "mumbai_gateway")
    max_depth = int(data.get("max_depth", 4))

    res = kg_service.math_engine.run_dfs(start_id, max_depth)
    return jsonify(res)


@app.route("/api/algorithms/dijkstra", methods=["POST"])
def api_dijkstra():
    """Executes Dijkstra's Shortest Path Algorithm with step-by-step edge relaxation table."""
    data = request.get_json() or {}
    start_id = data.get("start_id", "mumbai_metro_csmt")
    end_id = data.get("end_id", "mumbai_gateway")

    res = kg_service.math_engine.run_dijkstra(start_id, end_id)
    return jsonify(res)


@app.route("/api/sets/operate", methods=["POST"])
def api_set_operation():
    """Executes Set Theory operations (Union, Intersection, Difference, etc.)."""
    data = request.get_json() or {}
    set_a = data.get("set_a", {"category": "Museum", "label": "Museums"})
    set_b = data.get("set_b", {"category": "Monument", "label": "Monuments"})
    op = data.get("operation", "UNION")

    res = kg_service.math_engine.run_set_operation(set_a, set_b, op)
    return jsonify(res)


@app.route("/api/relations/properties", methods=["GET"])
def api_relation_properties():
    """Analyzes mathematical properties of binary relations."""
    rel = request.args.get("relation", "NEAR")
    city = request.args.get("city", "Mumbai")

    res = kg_service.math_engine.analyze_relation_properties(relation_type=rel, city=city)
    return jsonify(res)


@app.route("/api/matrix", methods=["GET"])
def api_adjacency_matrix():
    """Returns the adjacency matrix for places."""
    city = request.args.get("city", "Mumbai")
    limit = int(request.args.get("limit", 12))
    matrix_data = kg_service.math_engine.get_adjacency_matrix(filter_city=city, max_nodes=limit)
    return jsonify(matrix_data)


@app.route("/api/status", methods=["GET"])
def api_status():
    """Returns database connection status and metrics."""
    metrics = kg_service.math_engine.get_graph_metrics()
    return jsonify({
        "neo4j_connected": kg_service.is_neo4j_connected,
        "neo4j_uri": kg_service.uri,
        "neo4j_user": kg_service.user,
        "error": kg_service.connection_error,
        "active_engine": "Neo4j Database (Bolt: 7687)" if kg_service.is_neo4j_connected else "In-Memory Knowledge Graph Engine",
        "total_nodes": metrics["num_vertices"],
        "total_edges": metrics["num_edges"],
        "density": metrics["graph_density"]
    })


@app.route("/api/neo4j/connect", methods=["POST"])
def api_neo4j_connect():
    """Allows user to test and reconnect to Neo4j instance from UI."""
    data = request.get_json() or {}
    uri = data.get("uri", "bolt://localhost:7687")
    user = data.get("user", "neo4j")
    passw = data.get("password", "password")

    success, msg = kg_service.connect_neo4j(uri, user, passw)
    return jsonify({"success": success, "message": msg, "connected": kg_service.is_neo4j_connected})


@app.route("/api/neo4j/seed", methods=["POST"])
def api_neo4j_seed():
    """Seeds the active Neo4j database."""
    res = kg_service.seed_neo4j_database()
    return jsonify(res)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Tourist Guide Knowledge Graph Chatbot on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
