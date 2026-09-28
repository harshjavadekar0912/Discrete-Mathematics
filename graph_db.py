"""
Unified Graph Database Layer
Connects to live Neo4j via Cypher, or seamlessly falls back to the
in-memory graph engine with Cypher interpretation.
"""

import os
import re
from typing import Dict, List, Any, Optional, Tuple
from neo4j import GraphDatabase, exceptions as neo4j_exceptions

import seed_data
from algorithms import DiscreteMathEngine


class KnowledgeGraphService:
    def __init__(self, uri: Optional[str] = None, user: Optional[str] = None, password: Optional[str] = None):
        self.uri = uri or os.environ.get("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.environ.get("NEO4J_USER", "neo4j")
        self.password = password or os.environ.get("NEO4J_PASSWORD", "password")

        self.driver = None
        self.is_neo4j_connected = False
        self.connection_error = None

        # Build In-Memory graph
        self.nodes = list(seed_data.PLACES) + list(seed_data.CITIES)
        self.edges = []
        self._init_in_memory_edges()

        # Instantiate Discrete Math Engine
        self.math_engine = DiscreteMathEngine(self.nodes, self.edges)

        # Attempt initial Neo4j connection
        self.connect_neo4j(self.uri, self.user, self.password)

    def _init_in_memory_edges(self):
        """Constructs edges list from seed_data for in-memory graph."""
        self.edges = []
        
        # LOCATED_IN
        for p in seed_data.PLACES:
            city_id = "city_mumbai" if p["city"] == "Mumbai" else "city_delhi"
            self.edges.append({
                "source": p["id"],
                "target": city_id,
                "type": "LOCATED_IN",
                "label": "LOCATED_IN"
            })

        # NEAR
        for src, dst, dist in seed_data.NEAR_RELATIONSHIPS:
            self.edges.append({
                "source": src,
                "target": dst,
                "type": "NEAR",
                "label": f"NEAR ({dist} km)",
                "distance_km": dist
            })

        # CONNECTED_TO
        for item in seed_data.CONNECTED_TO_RELATIONSHIPS:
            src, dst, dist, mode = item
            self.edges.append({
                "source": src,
                "target": dst,
                "type": "CONNECTED_TO",
                "label": f"CONNECTED_TO ({mode}, {dist} km)",
                "distance_km": dist,
                "mode": mode
            })

    def connect_neo4j(self, uri: str, user: str, passw: str) -> Tuple[bool, str]:
        """Tries to connect to a live Neo4j instance."""
        self.uri = uri
        self.user = user
        self.password = passw

        try:
            if self.driver:
                self.driver.close()

            # Timeout after 2 seconds to keep app responsive if Neo4j is not running
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
                connection_timeout=2.0
            )
            self.driver.verify_connectivity()
            self.is_neo4j_connected = True
            self.connection_error = None
            return True, f"Successfully connected to Neo4j at {self.uri}"
        except Exception as e:
            self.is_neo4j_connected = False
            self.connection_error = str(e)
            return False, f"Could not connect to Neo4j: {str(e)}"

    def seed_neo4j_database(self) -> Dict[str, Any]:
        """Runs the seed Cypher statements against the active Neo4j database."""
        if not self.is_neo4j_connected or not self.driver:
            return {"success": False, "message": "Neo4j is not connected. Seed script saved locally in data/seed_graph.cypher."}

        try:
            cypher_content = seed_data.generate_cypher_seed_script()
            # Split into individual statements separated by semicolon
            statements = [s.strip() for s in cypher_content.split(";") if s.strip() and not s.strip().startswith("//")]

            with self.driver.session() as session:
                for stmt in statements:
                    if stmt:
                        session.run(stmt)

            return {
                "success": True,
                "message": f"Successfully executed {len(statements)} Cypher seed statements in Neo4j!",
                "statements_count": len(statements)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def execute_cypher(self, cypher_query: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Executes a Cypher query.
        If Neo4j is live, executes on database.
        Otherwise, interprets the query through the in-memory graph engine.
        """
        params = params or {}

        if self.is_neo4j_connected and self.driver:
            try:
                with self.driver.session() as session:
                    result = session.run(cypher_query, params)
                    records = [record.data() for record in result]
                    return {
                        "execution_engine": "Neo4j Database (Bolt Protocol)",
                        "cypher": cypher_query,
                        "records": records,
                        "count": len(records),
                        "success": True
                    }
            except Exception as e:
                # If error, fallback to in-memory evaluation
                pass

        # In-Memory Cypher Interpreter Fallback
        return self._interpret_in_memory_cypher(cypher_query, params)

    def _interpret_in_memory_cypher(self, query: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Interprets standard tourist Cypher queries against the loaded in-memory graph."""
        q_upper = query.upper()
        results = []

        # Find place by name matching helper
        def get_node_by_name(name_needle: str):
            name_clean = name_needle.strip().lower()
            for n in self.nodes:
                if n.get("name", "").lower() == name_clean:
                    return n
                if n.get("alt_name", "").lower() == name_clean:
                    return n
            # Substring match
            for n in self.nodes:
                if name_clean in n.get("name", "").lower():
                    return n
            return None

        # 1. Nearby Restaurants / Hotels / Places to a given landmark:
        # e.g.: MATCH (p {name: 'Gateway of India'})-[r:NEAR]-(target:Restaurant)
        match_near = re.search(r"\{name:\s*['\"]([^'\"]+)['\"]\}[^\]]*\[r:NEAR\]-*\(([^:\)]*):?([A-Za-z]+)?\)", query, re.IGNORECASE)
        if not match_near:
            match_near = re.search(r"\{name:\s*['\"]([^'\"]+)['\"]\}[^\]]*-[^\]]*NEAR[^\]]*-*\(([^:\)]*):?([A-Za-z]+)?\)", query, re.IGNORECASE)

        if match_near:
            landmark_name = match_near.group(1)
            target_category = match_near.group(3) if match_near.group(3) else None
            landmark_node = get_node_by_name(landmark_name)

            if landmark_node:
                lid = landmark_node["id"]
                # Find all edges with type NEAR connected to lid
                for edge in self.edges:
                    if edge.get("type") == "NEAR":
                        nbr_id = None
                        if edge["source"] == lid:
                            nbr_id = edge["target"]
                        elif edge["target"] == lid:
                            nbr_id = edge["source"]

                        if nbr_id:
                            nbr_node = next((n for n in self.nodes if n["id"] == nbr_id), None)
                            if nbr_node:
                                if not target_category or nbr_node.get("category", "").lower() == target_category.lower():
                                    rec = {
                                        "name": nbr_node["name"],
                                        "category": nbr_node.get("category"),
                                        "distance_km": edge.get("distance_km", 1.0),
                                        "rating": nbr_node.get("rating", 4.0),
                                        "area": nbr_node.get("area", ""),
                                        "city": nbr_node.get("city", "")
                                    }
                                    if "price_inr" in nbr_node:
                                        rec["price_inr"] = nbr_node["price_inr"]
                                    if "cuisine" in nbr_node:
                                        rec["cuisine"] = nbr_node["cuisine"]
                                    if "stars" in nbr_node:
                                        rec["stars"] = nbr_node["stars"]
                                    results.append(rec)

                # Sorting and limits
                if "ORDER BY H.PRICE_INR ASC" in q_upper or "ORDER BY RES.PRICE_INR ASC" in q_upper or "ORDER BY PRICE" in q_upper:
                    results.sort(key=lambda x: x.get("price_inr", 999999))
                else:
                    results.sort(key=lambda x: x.get("distance_km", 999))

                if "LIMIT 1" in q_upper:
                    results = results[:1]
                elif "LIMIT" in q_upper:
                    m_lim = re.search(r"LIMIT\s+(\d+)", q_upper)
                    if m_lim:
                        results = results[:int(m_lim.group(1))]

                return {
                    "execution_engine": "In-Memory Knowledge Graph Engine (Graph Traversal)",
                    "cypher": query,
                    "records": results,
                    "count": len(results),
                    "success": True
                }

        # 2. Category in City:
        # e.g.: MATCH (p:Museum)-[:LOCATED_IN]->(c:City {name: 'Mumbai'})
        match_cat_city = re.search(r"\(([^:\)]*):?([A-Za-z]+)?\)-.*LOCATED_IN.*c:City\s*\{\s*name:\s*['\"]([^'\"]+)['\"]\s*\}", query, re.IGNORECASE)
        if match_cat_city:
            cat_name = match_cat_city.group(2)
            city_name = match_cat_city.group(3)

            for n in self.nodes:
                if n.get("category") == "City":
                    continue
                if n.get("city", "").lower() == city_name.lower():
                    if not cat_name or cat_name == "Place" or n.get("category", "").lower() == cat_name.lower():
                        results.append({
                            "name": n["name"],
                            "category": n.get("category"),
                            "city": n.get("city"),
                            "area": n.get("area"),
                            "rating": n.get("rating"),
                            "description": n.get("description"),
                            "entry_fee": n.get("entry_fee", 0),
                            "price_tier": n.get("price_tier", "Moderate")
                        })

            return {
                "execution_engine": "In-Memory Knowledge Graph Engine (Index Lookup)",
                "cypher": query,
                "records": results,
                "count": len(results),
                "success": True
            }

        # 3. Set Operations (Union / OR queries):
        # e.g.: MATCH (p) WHERE p:Museum OR p:Monument
        if "MUSEUM" in q_upper and "MONUMENT" in q_upper and ("OR" in q_upper or "UNION" in q_upper):
            for n in self.nodes:
                if n.get("category") in ["Museum", "Monument"]:
                    results.append({
                        "name": n["name"],
                        "category": n.get("category"),
                        "city": n.get("city"),
                        "rating": n.get("rating"),
                        "area": n.get("area"),
                        "description": n.get("description")
                    })
            return {
                "execution_engine": "In-Memory Knowledge Graph Engine (Set Union)",
                "cypher": query,
                "records": results,
                "count": len(results),
                "success": True
            }

        # 4. Route from Station to Landmark (Shortest Path / CONNECTED_TO):
        # e.g.: MATCH (m {name: 'Gateway of India'})-[r:CONNECTED_TO|NEAR]-(s:MetroStation)
        if "METROSTATION" in q_upper or "STATION" in q_upper:
            # Check for landmark
            m_place = re.search(r"\{name:\s*['\"]([^'\"]+)['\"]\s*\}", query)
            if m_place:
                lm = get_node_by_name(m_place.group(1))
                if lm:
                    # Find nearest metro station using BFS or Dijkstra
                    stations = [n for n in self.nodes if n.get("category") == "MetroStation" and n.get("city") == lm.get("city")]
                    routes = []
                    for st in stations:
                        dijkstra_res = self.math_engine.run_dijkstra(st["id"], lm["id"])
                        if dijkstra_res.get("found"):
                            routes.append({
                                "station_name": st["name"],
                                "destination": lm["name"],
                                "distance_km": dijkstra_res["total_distance_km"],
                                "path": dijkstra_res["shortest_path"],
                                "line": st.get("line", "Metro Line")
                            })
                    routes.sort(key=lambda x: x["distance_km"])
                    results = routes[:1] if "LIMIT 1" in q_upper else routes
                    return {
                        "execution_engine": "In-Memory Knowledge Graph Engine (Dijkstra Shortest Path)",
                        "cypher": query,
                        "records": results,
                        "count": len(results),
                        "success": True
                    }

        # Fallback: general node scan
        for n in self.nodes:
            if n.get("category") != "City":
                results.append({"name": n["name"], "category": n.get("category"), "city": n.get("city")})

        return {
            "execution_engine": "In-Memory Knowledge Graph Engine (General Scan)",
            "cypher": query,
            "records": results[:10],
            "count": min(len(results), 10),
            "success": True
        }

    def get_all_places(self, category: Optional[str] = None, city: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns places filtered by category and/or city."""
        res = []
        for n in self.nodes:
            if n.get("category") == "City":
                continue
            if category and n.get("category") != category:
                continue
            if city and n.get("city") != city:
                continue
            res.append(n)
        return res

    def get_graph_visualization_data(self, filter_city: Optional[str] = None) -> Dict[str, Any]:
        """
        Formats graph nodes and edges for vis-network.js visualization.
        Color codes node types, adds icons and badges.
        """
        COLOR_MAP = {
            "City": {"background": "#0284c7", "border": "#0369a1", "text": "#ffffff"},
            "Monument": {"background": "#f59e0b", "border": "#d97706", "text": "#ffffff"},
            "Museum": {"background": "#8b5cf6", "border": "#7c3aed", "text": "#ffffff"},
            "Hotel": {"background": "#10b981", "border": "#059669", "text": "#ffffff"},
            "Restaurant": {"background": "#ef4444", "border": "#dc2626", "text": "#ffffff"},
            "MetroStation": {"background": "#06b6d4", "border": "#0891b2", "text": "#ffffff"},
        }

        ICON_MAP = {
            "City": "🏙️",
            "Monument": "🏛️",
            "Museum": "🏺",
            "Hotel": "🏨",
            "Restaurant": "🍽️",
            "MetroStation": "🚇"
        }

        vis_nodes = []
        node_id_set = set()

        for n in self.nodes:
            if filter_city and n.get("category") != "City" and n.get("city") != filter_city:
                continue
            if filter_city and n.get("category") == "City" and n.get("name") != filter_city:
                continue

            node_id_set.add(n["id"])
            cat = n.get("category", "Place")
            color_info = COLOR_MAP.get(cat, {"background": "#64748b", "border": "#475569", "text": "#ffffff"})
            icon = ICON_MAP.get(cat, "📍")

            label = f"{icon} {n['name']}"
            if cat == "Hotel" and "price_inr" in n:
                label += f"\n₹{n['price_inr']}"
            elif cat == "Restaurant" and "cuisine" in n:
                label += f"\n{n['cuisine'][:15]}"

            vis_nodes.append({
                "id": n["id"],
                "label": label,
                "title": f"<b>{n['name']}</b><br>Type: {cat}<br>Area: {n.get('area', '')}<br>Rating: ⭐ {n.get('rating', 'N/A')}<br>{n.get('description', '')}",
                "color": {
                    "background": color_info["background"],
                    "border": color_info["border"],
                    "highlight": {"background": "#f43f5e", "border": "#be123c"}
                },
                "shape": "box",
                "margin": 10,
                "font": {"color": "#ffffff", "face": "Outfit, Inter, sans-serif", "size": 13},
                "category": cat,
                "city": n.get("city", ""),
                "rating": n.get("rating", 4.0),
                "raw_data": n
            })

        vis_edges = []
        for e in self.edges:
            if e["source"] in node_id_set and e["target"] in node_id_set:
                rel_type = e.get("type", "RELATED_TO")
                edge_color = "#94a3b8"
                dashes = False
                width = 1.5

                if rel_type == "NEAR":
                    edge_color = "#fbbf24"
                    dashes = [5, 5]
                    width = 2.0
                elif rel_type == "CONNECTED_TO":
                    edge_color = "#38bdf8"
                    width = 2.5
                elif rel_type == "LOCATED_IN":
                    edge_color = "#64748b"
                    width = 1.0

                vis_edges.append({
                    "from": e["source"],
                    "to": e["target"],
                    "label": e.get("label", rel_type),
                    "arrows": "to" if rel_type == "LOCATED_IN" else "",
                    "color": {"color": edge_color, "highlight": "#f43f5e"},
                    "dashes": dashes,
                    "width": width,
                    "font": {"size": 10, "color": "#cbd5e1", "align": "middle", "strokeWidth": 0}
                })

        return {
            "nodes": vis_nodes,
            "edges": vis_edges,
            "total_nodes": len(vis_nodes),
            "total_edges": len(vis_edges),
            "filter_city": filter_city
        }


# Global singleton instance
kg_service = KnowledgeGraphService()
