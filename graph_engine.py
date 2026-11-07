"""
Graph Theory Engine - Discrete Mathematics Road Network Analyzer
Pure Python implementation of:
  - Dijkstra's Shortest Path Algorithm
  - Breadth-First Search (BFS) Traversal
  - Depth-First Search (DFS) Traversal
  - Adjacency List & Adjacency Matrix Generators
  - Graph Theory Metrics (Density, Degrees, Connectivity)
Uses real OpenStreetMap road-network nodes and edge distances.
"""

import os
import json
import heapq
import math
from collections import deque
from typing import Dict, List, Tuple, Any, Optional

NETWORKS_FILE = os.path.join(os.path.dirname(__file__), "osm_road_networks.json")

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two points in km."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 3)


class RoadNetworkGraph:
    """
    In-memory representation of an OpenStreetMap road network graph
    for Discrete Mathematics analysis.
    """
    def __init__(self, city_key: str, data: dict):
        self.city_key = city_key
        self.city_name = data.get("city_name", city_key.title())
        self.center = data.get("center", {"lat": 18.5204, "lng": 73.8567})
        self.nodes: Dict[str, dict] = {str(n["id"]): n for n in data.get("nodes", [])}
        self.edges: List[dict] = data.get("edges", [])
        
        # Build adjacency structures
        self.adj_list: Dict[str, List[dict]] = {nid: [] for nid in self.nodes}
        self.edge_map: Dict[Tuple[str, str], dict] = {}
        
        for e in self.edges:
            u, v = str(e["u"]), str(e["v"])
            w = float(e.get("weight_km", 0.1))
            road = e.get("road", "Main Road")
            coords = e.get("coords", [])
            
            if u in self.adj_list and v in self.adj_list:
                self.adj_list[u].append({
                    "neighbor_id": v,
                    "neighbor_label": self.nodes[v]["label"],
                    "weight_km": w,
                    "road": road,
                    "coords": coords
                })
                self.adj_list[v].append({
                    "neighbor_id": u,
                    "neighbor_label": self.nodes[u]["label"],
                    "weight_km": w,
                    "road": road,
                    "coords": list(reversed(coords))
                })
                self.edge_map[(u, v)] = e
                self.edge_map[(v, u)] = e

    def get_summary(self) -> dict:
        """Return graph metadata, nodes, edges, adjacency list, matrix, and metrics."""
        node_ids = sorted(list(self.nodes.keys()))
        n_count = len(node_ids)
        e_count = len(self.edges)
        
        # Adjacency Matrix
        # matrix[i][j] = distance or None
        matrix = []
        for i, u in enumerate(node_ids):
            row = []
            for j, v in enumerate(node_ids):
                if u == v:
                    row.append(0.0)
                else:
                    edge = self.edge_map.get((u, v))
                    row.append(edge["weight_km"] if edge else None)
            matrix.append(row)
            
        # Degree metrics
        degrees = {nid: len(self.adj_list[nid]) for nid in node_ids}
        avg_deg = sum(degrees.values()) / max(n_count, 1)
        max_deg = max(degrees.values()) if degrees else 0
        min_deg = min(degrees.values()) if degrees else 0
        
        # Graph Density = 2|E| / (|V|*(|V|-1))
        density = (2.0 * e_count) / (n_count * (n_count - 1)) if n_count > 1 else 0.0

        return {
            "city": self.city_key,
            "city_name": self.city_name,
            "center": self.center,
            "nodes": list(self.nodes.values()),
            "edges": self.edges,
            "adjacency_list": {
                nid: [
                    {
                        "to_id": item["neighbor_id"],
                        "to_label": item["neighbor_label"],
                        "weight_km": item["weight_km"],
                        "road": item["road"]
                    }
                    for item in items
                ]
                for nid, items in self.adj_list.items()
            },
            "adjacency_matrix": {
                "nodes": [
                    {"id": nid, "label": self.nodes[nid]["label"]}
                    for nid in node_ids
                ],
                "matrix": matrix
            },
            "metrics": {
                "num_vertices": n_count,
                "num_edges": e_count,
                "density": round(density, 4),
                "avg_degree": round(avg_deg, 2),
                "max_degree": max_deg,
                "min_degree": min_deg,
                "is_connected": self._check_connectivity()
            }
        }

    def _check_connectivity(self) -> bool:
        if not self.nodes:
            return True
        start = next(iter(self.nodes.keys()))
        visited = set([start])
        q = deque([start])
        while q:
            curr = q.popleft()
            for item in self.adj_list.get(curr, []):
                v = item["neighbor_id"]
                if v not in visited:
                    visited.add(v)
                    q.append(v)
        return len(visited) == len(self.nodes)

    def dijkstra(self, start_id: str, dest_id: str, penalty_edges: Optional[set] = None) -> dict:
        """
        Dijkstra's Algorithm implemented from first principles.
        Calculates shortest path, total distance, relaxed edges, and step logs.
        """
        if start_id not in self.nodes or dest_id not in self.nodes:
            return {"error": "Invalid start or destination node ID", "success": False}

        penalty_edges = penalty_edges or set()
        distances = {nid: float("inf") for nid in self.nodes}
        distances[start_id] = 0.0
        previous = {nid: None for nid in self.nodes}
        edge_used = {nid: None for nid in self.nodes}
        
        # Priority queue stores (cost, node_id)
        pq = [(0.0, start_id)]
        visited = set()
        visited_order = []
        steps_log = []
        step_num = 1

        while pq:
            curr_dist, u = heapq.heappop(pq)
            
            if u in visited:
                continue
            visited.add(u)
            visited_order.append(u)

            steps_log.append({
                "step": step_num,
                "action": f"Settled vertex {self.nodes[u]['label']}",
                "vertex_id": u,
                "vertex_label": self.nodes[u]["label"],
                "cumulative_cost_km": round(curr_dist, 3),
                "pq_size": len(pq)
            })
            step_num += 1

            if u == dest_id:
                break

            for neighbor in self.adj_list.get(u, []):
                v = neighbor["neighbor_id"]
                w = neighbor["weight_km"]
                
                # Apply penalty for alternative path computation if specified
                edge_key = tuple(sorted([u, v]))
                if edge_key in penalty_edges:
                    w = w * 3.5 # penalty factor to divert path

                new_dist = curr_dist + w
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    previous[v] = u
                    edge_used[v] = neighbor
                    heapq.heappush(pq, (new_dist, v))
                    steps_log.append({
                        "step": step_num,
                        "action": f"Relaxed edge ({self.nodes[u]['label']} → {self.nodes[v]['label']}) via {neighbor['road']}",
                        "vertex_id": v,
                        "vertex_label": self.nodes[v]["label"],
                        "cumulative_cost_km": round(new_dist, 3),
                        "pq_size": len(pq)
                    })
                    step_num += 1

        # Path reconstruction
        path = []
        curr = dest_id
        if distances[dest_id] != float("inf"):
            while curr is not None:
                path.append(curr)
                curr = previous[curr]
            path.reverse()

        path_edges = []
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            e = self.edge_map.get((u, v))
            if e:
                path_edges.append(e)

        return {
            "success": bool(path),
            "algorithm": "Dijkstra's Shortest Path",
            "start": {"id": start_id, "label": self.nodes[start_id]["label"]},
            "destination": {"id": dest_id, "label": self.nodes[dest_id]["label"]},
            "path": path,
            "path_labels": [self.nodes[nid]["label"] for nid in path],
            "total_distance_km": round(distances[dest_id], 3) if distances[dest_id] != float("inf") else None,
            "path_edges": path_edges,
            "visited_order": visited_order,
            "visited_count": len(visited_order),
            "steps_log": steps_log[:30], # keep top readable steps
            "cost_table": {
                nid: (round(distances[nid], 3) if distances[nid] != float("inf") else "∞")
                for nid in visited_order
            }
        }

    def find_shortest_with_alternatives(self, start_id: str, dest_id: str) -> dict:
        """
        Compute primary Dijkstra shortest path and 1-2 alternative paths
        by penalizing edges from the shortest path.
        """
        primary = self.dijkstra(start_id, dest_id)
        if not primary.get("success") or len(primary.get("path", [])) < 3:
            return {"primary": primary, "alternatives": []}

        # Select middle edges to penalize for alternative routes
        path = primary["path"]
        penalized_edges = set()
        mid_idx = len(path) // 2
        penalized_edges.add(tuple(sorted([path[mid_idx-1], path[mid_idx]])))

        alt = self.dijkstra(start_id, dest_id, penalty_edges=penalized_edges)
        alternatives = []
        if alt.get("success") and alt.get("path") != primary.get("path"):
            alternatives.append(alt)

        return {
            "primary": primary,
            "alternatives": alternatives
        }

    def bfs(self, start_id: str) -> dict:
        """
        Breadth-First Search (BFS) Traversal from first principles.
        Demonstrates queue-based exploration and level sets.
        """
        if start_id not in self.nodes:
            return {"error": "Invalid start node ID", "success": False}

        visited = set([start_id])
        q = deque([(start_id, 0)]) # (node, depth)
        visited_order = []
        levels = {start_id: 0}
        tree_edges = []
        steps_log = []
        step_num = 1

        while q:
            u, depth = q.popleft()
            visited_order.append(u)
            
            steps_log.append({
                "step": step_num,
                "action": f"Dequeued vertex {self.nodes[u]['label']} at level {depth}",
                "vertex_id": u,
                "vertex_label": self.nodes[u]["label"],
                "level": depth,
                "queue_size": len(q)
            })
            step_num += 1

            for neighbor in self.adj_list.get(u, []):
                v = neighbor["neighbor_id"]
                if v not in visited:
                    visited.add(v)
                    levels[v] = depth + 1
                    tree_edges.append({
                        "from": u,
                        "to": v,
                        "road": neighbor["road"],
                        "weight_km": neighbor["weight_km"],
                        "coords": neighbor["coords"]
                    })
                    q.append((v, depth + 1))
                    steps_log.append({
                        "step": step_num,
                        "action": f"Enqueued vertex {self.nodes[v]['label']} (level {depth + 1})",
                        "vertex_id": v,
                        "vertex_label": self.nodes[v]["label"],
                        "level": depth + 1,
                        "queue_size": len(q)
                    })
                    step_num += 1

        return {
            "success": True,
            "algorithm": "Breadth-First Search (BFS)",
            "start": {"id": start_id, "label": self.nodes[start_id]["label"]},
            "visited_order": visited_order,
            "visited_labels": [self.nodes[nid]["label"] for nid in visited_order],
            "visited_count": len(visited_order),
            "levels": levels,
            "tree_edges": tree_edges,
            "steps_log": steps_log[:30]
        }

    def dfs(self, start_id: str) -> dict:
        """
        Depth-First Search (DFS) Traversal from first principles.
        Demonstrates stack / recursion, discovery, and finish times.
        """
        if start_id not in self.nodes:
            return {"error": "Invalid start node ID", "success": False}

        visited = set()
        visited_order = []
        discovery_time = {}
        finish_time = {}
        time_counter = 0
        tree_edges = []
        steps_log = []
        step_num = 1

        def dfs_visit(u):
            nonlocal time_counter, step_num
            time_counter += 1
            discovery_time[u] = time_counter
            visited.add(u)
            visited_order.append(u)

            steps_log.append({
                "step": step_num,
                "action": f"Discovered vertex {self.nodes[u]['label']} (time: {time_counter})",
                "vertex_id": u,
                "vertex_label": self.nodes[u]["label"],
                "discovery_time": time_counter
            })
            step_num += 1

            for neighbor in self.adj_list.get(u, []):
                v = neighbor["neighbor_id"]
                if v not in visited:
                    tree_edges.append({
                        "from": u,
                        "to": v,
                        "road": neighbor["road"],
                        "weight_km": neighbor["weight_km"],
                        "coords": neighbor["coords"]
                    })
                    dfs_visit(v)

            time_counter += 1
            finish_time[u] = time_counter
            steps_log.append({
                "step": step_num,
                "action": f"Finished vertex {self.nodes[u]['label']} (time: {time_counter})",
                "vertex_id": u,
                "vertex_label": self.nodes[u]["label"],
                "finish_time": time_counter
            })
            step_num += 1

        dfs_visit(start_id)

        return {
            "success": True,
            "algorithm": "Depth-First Search (DFS)",
            "start": {"id": start_id, "label": self.nodes[start_id]["label"]},
            "visited_order": visited_order,
            "visited_labels": [self.nodes[nid]["label"] for nid in visited_order],
            "visited_count": len(visited_order),
            "discovery_time": discovery_time,
            "finish_time": finish_time,
            "tree_edges": tree_edges,
            "steps_log": steps_log[:30]
        }


# ---------------------------------------------------------------------------
# Global Graph Repository & Overpass Live Loader
# ---------------------------------------------------------------------------

_GRAPH_CACHE: Dict[str, RoadNetworkGraph] = {}

CITY_COORDINATES = {
    "pune": {"lat": 18.5204, "lng": 73.8567, "name": "Pune"},
    "mumbai": {"lat": 18.9388, "lng": 72.8354, "name": "Mumbai"},
    "delhi": {"lat": 28.6448, "lng": 77.2167, "name": "Delhi"},
    "chennai": {"lat": 13.0827, "lng": 80.2707, "name": "Chennai"},
    "hyderabad": {"lat": 17.3850, "lng": 78.4867, "name": "Hyderabad"},
}

OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]

def fetch_road_network_from_overpass(city_key: str, lat: float = None, lng: float = None, radius_m: int = 2200) -> Optional[RoadNetworkGraph]:
    """
    Fetch live OpenStreetMap road network data using Overpass API for the city.
    Extract road intersections as vertices and road segments as weighted edges.
    """
    import urllib.request
    import urllib.parse
    import time
    
    city_key = city_key.lower().strip()
    c_info = CITY_COORDINATES.get(city_key, {"lat": 18.5204, "lng": 73.8567, "name": city_key.title()})
    c_lat = lat if lat is not None else c_info["lat"]
    c_lng = lng if lng is not None else c_info["lng"]
    city_name = c_info.get("name", city_key.title())

    overpass_query = f"""[out:json][timeout:12];
(
  way["highway"~"^(primary|secondary|tertiary|trunk)$"](around:{radius_m},{c_lat},{c_lng});
);
out body geom;"""

    data = None
    for server in OVERPASS_SERVERS:
        try:
            req = urllib.request.Request(
                server,
                data=urllib.parse.urlencode({"data": overpass_query}).encode("utf-8"),
                headers={"User-Agent": "TouristGuideAssistant/2.0 (DiscreteMathAnalyzer)"}
            )
            with urllib.request.urlopen(req, timeout=14) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    if data and "elements" in data and len(data["elements"]) > 0:
                        break
        except Exception:
            continue

    if not data or "elements" not in data or not data["elements"]:
        return None

    ways = [el for el in data["elements"] if el.get("type") == "way" and el.get("geometry")]
    if len(ways) < 3:
        return None

    # Count coordinate occurrences to locate intersections
    coord_usage: Dict[Tuple[float, float], List[str]] = {}
    for w in ways:
        road_name = w.get("tags", {}).get("name", "Unnamed Road")
        geom = w.get("geometry", [])
        if not geom:
            continue
        # Mark endpoints
        for pt in [geom[0], geom[-1]]:
            key = (round(pt["lat"], 5), round(pt["lon"], 5))
            if key not in coord_usage:
                coord_usage[key] = []
            if road_name not in coord_usage[key]:
                coord_usage[key].append(road_name)
        # Mark interior points
        for pt in geom[1:-1]:
            key = (round(pt["lat"], 5), round(pt["lon"], 5))
            if key not in coord_usage:
                coord_usage[key] = []
            if road_name not in coord_usage[key]:
                coord_usage[key].append(road_name)

    # Junctions are coords shared by multiple roads or 2+ ways
    junction_coords = {c: roads for c, roads in coord_usage.items() if len(roads) >= 2 or len(coord_usage[c]) > 1}
    
    # If too few, include endpoints of major ways
    if len(junction_coords) < 10:
        for w in ways:
            geom = w.get("geometry", [])
            if geom:
                for pt in [geom[0], geom[-1]]:
                    key = (round(pt["lat"], 5), round(pt["lon"], 5))
                    road_name = w.get("tags", {}).get("name", "Road")
                    if key not in junction_coords:
                        junction_coords[key] = [road_name]

    # Limit to top 40 best-connected junctions for clear visualization
    sorted_junctions = sorted(junction_coords.items(), key=lambda item: len(item[1]), reverse=True)[:45]
    
    nodes_list = []
    coord_to_id: Dict[Tuple[float, float], str] = {}
    for idx, ((j_lat, j_lng), r_names) in enumerate(sorted_junctions):
        nid = str(100000 + idx)
        coord_to_id[(j_lat, j_lng)] = nid
        label_text = f"Junction ({' & '.join(r_names[:2])})" if r_names else f"Junction #{idx+1}"
        nodes_list.append({
            "id": nid,
            "osm_id": 100000 + idx,
            "label": label_text,
            "lat": j_lat,
            "lng": j_lng,
            "degree": 0
        })

    # Build road segments between junctions
    edges_list = []
    edge_seen = set()
    node_id_set = {n["id"] for n in nodes_list}

    for w in ways:
        road_name = w.get("tags", {}).get("name", "Connecting Road")
        geom = w.get("geometry", [])
        if len(geom) < 2:
            continue

        # Find all junction points on this way
        matched_on_way = []
        for pt in geom:
            k = (round(pt["lat"], 5), round(pt["lon"], 5))
            if k in coord_to_id:
                matched_on_way.append((coord_to_id[k], pt["lat"], pt["lon"]))

        # Create edges between consecutive matched junctions
        for i in range(len(matched_on_way) - 1):
            u_id, u_lat, u_lng = matched_on_way[i]
            v_id, v_lat, v_lng = matched_on_way[i + 1]
            if u_id == v_id:
                continue

            edge_key = tuple(sorted([u_id, v_id]))
            if edge_key in edge_seen:
                continue
            edge_seen.add(edge_key)

            dist_km = haversine_km(u_lat, u_lng, v_lat, v_lng)
            if dist_km < 0.02:
                dist_km = 0.05

            edges_list.append({
                "id": f"e_{u_id}_{v_id}",
                "u": u_id,
                "v": v_id,
                "road": road_name,
                "weight_km": dist_km,
                "coords": [[u_lat, u_lng], [v_lat, v_lng]]
            })

    # Update degrees
    deg_map = {n["id"]: 0 for n in nodes_list}
    for e in edges_list:
        if e["u"] in deg_map: deg_map[e["u"]] += 1
        if e["v"] in deg_map: deg_map[e["v"]] += 1
    for n in nodes_list:
        n["degree"] = deg_map.get(n["id"], 0)

    # Filter out disconnected nodes if plenty exist
    connected_nodes = [n for n in nodes_list if n["degree"] > 0]
    if len(connected_nodes) >= 8:
        nodes_list = connected_nodes

    network_data = {
        "city_name": city_name,
        "center": {"lat": c_lat, "lng": c_lng},
        "nodes": nodes_list,
        "edges": edges_list
    }

    graph = RoadNetworkGraph(city_key, network_data)
    _GRAPH_CACHE[city_key] = graph
    
    # Save to disk cache
    try:
        all_data = {}
        if os.path.exists(NETWORKS_FILE):
            with open(NETWORKS_FILE, "r", encoding="utf-8") as f:
                all_data = json.load(f)
        all_data[city_key] = network_data
        with open(NETWORKS_FILE, "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=2)
    except Exception as e:
        print("Disk cache write error:", e)

    return graph


def get_network_graph(city_key: str, force_refresh: bool = False) -> Optional[RoadNetworkGraph]:
    """Retrieve or initialize the RoadNetworkGraph for a city."""
    city_key = city_key.lower().strip()
    
    if force_refresh:
        live_g = fetch_road_network_from_overpass(city_key)
        if live_g:
            return live_g

    if city_key in _GRAPH_CACHE:
        return _GRAPH_CACHE[city_key]

    if os.path.exists(NETWORKS_FILE):
        try:
            with open(NETWORKS_FILE, "r", encoding="utf-8") as f:
                all_data = json.load(f)
                if city_key in all_data:
                    graph = RoadNetworkGraph(city_key, all_data[city_key])
                    _GRAPH_CACHE[city_key] = graph
                    return graph
        except Exception as e:
            print(f"Error loading road network for {city_key}:", e)

    # If not in file, try live Overpass fetch
    return fetch_road_network_from_overpass(city_key)


def list_available_network_cities() -> List[dict]:
    """Return available cities with road networks."""
    if not os.path.exists(NETWORKS_FILE):
        return []
    try:
        with open(NETWORKS_FILE, "r", encoding="utf-8") as f:
            all_data = json.load(f)
            return [
                {
                    "city": k,
                    "name": v.get("city_name", k.title()),
                    "nodes_count": len(v.get("nodes", [])),
                    "edges_count": len(v.get("edges", [])),
                    "center": v.get("center", {})
                }
                for k, v in all_data.items()
            ]
    except Exception:
        return []

