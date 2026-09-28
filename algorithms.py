"""
Discrete Mathematics Algorithms & Concepts Engine
Tourist Guide Knowledge Graph Chatbot

Demonstrates:
1. Graph Theory (Adjacency Matrix, Adjacency List, Degrees, Components)
2. Relations (Reflexive, Symmetric, Transitive, Equivalence Relation)
3. Breadth-First Search (BFS) with step-by-step queue trace
4. Depth-First Search (DFS) with step-by-step stack trace & timestamps
5. Dijkstra's Algorithm with step-by-step edge relaxation table
6. Set Theory (Union, Intersection, Difference, Symmetric Difference, Inclusion-Exclusion)
"""

import heapq
from collections import deque
from typing import Dict, List, Set, Tuple, Any, Optional


class DiscreteMathEngine:
    def __init__(self, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]):
        """
        nodes: list of dicts with 'id', 'name', 'category', 'city', etc.
        edges: list of dicts with 'source', 'target', 'type', 'distance_km', etc.
        """
        self.nodes = {n["id"]: n for n in nodes}
        self.edges = edges
        
        # Build adjacency structures
        self.adj_list_directed: Dict[str, List[Dict[str, Any]]] = {n_id: [] for n_id in self.nodes}
        self.adj_list_undirected: Dict[str, List[Dict[str, Any]]] = {n_id: [] for n_id in self.nodes}
        
        for edge in edges:
            src = edge["source"]
            tgt = edge["target"]
            if src in self.nodes and tgt in self.nodes:
                self.adj_list_directed[src].append(edge)
                
                # For undirected view (traversals across NEAR and CONNECTED_TO)
                self.adj_list_undirected[src].append(edge)
                rev_edge = dict(edge)
                rev_edge["source"] = tgt
                rev_edge["target"] = src
                self.adj_list_undirected[tgt].append(rev_edge)

    # =========================================================================
    # 1. GRAPH THEORY REPRESENTATIONS
    # =========================================================================
    def get_graph_metrics(self) -> Dict[str, Any]:
        """Calculates vertex degrees, density, and basic graph theory metrics."""
        degrees = {}
        in_degrees = {n_id: 0 for n_id in self.nodes}
        out_degrees = {n_id: 0 for n_id in self.nodes}

        for edge in self.edges:
            s, t = edge["source"], edge["target"]
            if s in out_degrees:
                out_degrees[s] += 1
            if t in in_degrees:
                in_degrees[t] += 1

        for n_id in self.nodes:
            degrees[n_id] = {
                "name": self.nodes[n_id].get("name", n_id),
                "in_degree": in_degrees[n_id],
                "out_degree": out_degrees[n_id],
                "total_degree": in_degrees[n_id] + out_degrees[n_id],
                "category": self.nodes[n_id].get("category", "Place")
            }

        num_vertices = len(self.nodes)
        num_edges = len(self.edges)
        max_possible_edges = num_vertices * (num_vertices - 1) if num_vertices > 1 else 1
        density = round(num_edges / max_possible_edges, 4)

        return {
            "num_vertices": num_vertices,
            "num_edges": num_edges,
            "graph_density": density,
            "degrees": degrees
        }

    def get_adjacency_matrix(self, filter_city: Optional[str] = None, max_nodes: int = 15) -> Dict[str, Any]:
        """Generates an adjacency matrix A where A[i][j] = 1 if edge exists, else 0."""
        target_nodes = [
            n for n in self.nodes.values()
            if (not filter_city or n.get("city") == filter_city) and n.get("category") != "City"
        ][:max_nodes]

        node_ids = [n["id"] for n in target_nodes]
        node_names = [n["name"] for n in target_nodes]
        id_to_idx = {nid: idx for idx, nid in enumerate(node_ids)}

        n = len(node_ids)
        matrix = [[0] * n for _ in range(n)]

        for edge in self.edges:
            s = edge["source"]
            t = edge["target"]
            if s in id_to_idx and t in id_to_idx:
                matrix[id_to_idx[s]][id_to_idx[t]] = 1
                # If relationship is symmetric (NEAR / CONNECTED_TO)
                if edge.get("type") in ["NEAR", "CONNECTED_TO"]:
                    matrix[id_to_idx[t]][id_to_idx[s]] = 1

        return {
            "node_names": node_names,
            "node_ids": node_ids,
            "matrix": matrix,
            "size": n
        }

    # =========================================================================
    # 2. RELATIONS (MATHEMATICAL PROPERTIES OF BINARY RELATIONS)
    # =========================================================================
    def analyze_relation_properties(self, relation_type: str = "NEAR", city: str = "Mumbai") -> Dict[str, Any]:
        """
        Analyzes a binary relation R on set of places V for:
        - Reflexivity: (x, x) in R for all x in V
        - Symmetry: (x, y) in R => (y, x) in R
        - Transitivity: (x, y) in R and (y, z) in R => (x, z) in R
        - Equivalence relation check
        """
        # Filter places in chosen city
        places = [
            n["id"] for n in self.nodes.values()
            if n.get("city") == city and n.get("category") not in ["City", "PriceTier"]
        ]
        place_set = set(places)

        # Build relation pair set R = {(u, v)}
        R: Set[Tuple[str, str]] = set()
        for edge in self.edges:
            if edge.get("type") == relation_type:
                u, v = edge["source"], edge["target"]
                if u in place_set and v in place_set:
                    R.add((u, v))
                    # NEAR and CONNECTED_TO are inherently bidirectional in geography
                    if relation_type in ["NEAR", "CONNECTED_TO"]:
                        R.add((v, u))

        # 1. Reflexivity: Is (x, x) in R for all x in V?
        is_reflexive = all((x, x) in R for x in places)
        reflexive_counterexample = next((x for x in places if (x, x) not in R), None)
        reflexive_explanation = (
            "Reflexive: Every place is related to itself (distance 0)." if is_reflexive else
            f"Not Reflexive: Places are not listed as NEAR themselves (e.g., ({self.nodes[reflexive_counterexample]['name']}, {self.nodes[reflexive_counterexample]['name']}) ∉ R)."
        )

        # 2. Symmetry: If (x, y) in R, is (y, x) in R?
        is_symmetric = True
        symmetric_counterexample = None
        for (u, v) in R:
            if (v, u) not in R:
                is_symmetric = False
                symmetric_counterexample = (u, v)
                break

        symmetric_explanation = (
            "Symmetric: If Place A is NEAR Place B, then Place B is NEAR Place A by Euclidean spatial symmetry." if is_symmetric else
            f"Not Symmetric: Found ({self.nodes[symmetric_counterexample[0]]['name']}, {self.nodes[symmetric_counterexample[1]]['name']}) ∈ R but reverse ∉ R."
        )

        # 3. Transitivity: If (x, y) in R and (y, z) in R, is (x, z) in R?
        is_transitive = True
        transitive_counterexample = None
        for (x, y) in R:
            for (y2, z) in R:
                if y == y2 and x != z:
                    if (x, z) not in R:
                        is_transitive = False
                        transitive_counterexample = (x, y, z)
                        break
            if not is_transitive:
                break

        if relation_type == "LOCATED_IN":
            transitive_explanation = "Transitive: If Place A is located in Area B, and Area B is in City C, Place A is in City C."
        else:
            transitive_explanation = (
                "Transitive: Holds universally for all pairs." if is_transitive else
                f"Not Transitive: Proximity does not chain! E.g., {self.nodes[transitive_counterexample[0]]['name']} is NEAR {self.nodes[transitive_counterexample[1]]['name']}, and {self.nodes[transitive_counterexample[1]]['name']} is NEAR {self.nodes[transitive_counterexample[2]]['name']}, but {self.nodes[transitive_counterexample[0]]['name']} is NOT NEAR {self.nodes[transitive_counterexample[2]]['name']} (Triangle inequality distance threshold)."
            )

        is_equivalence = is_reflexive and is_symmetric and is_transitive

        return {
            "relation_type": relation_type,
            "city": city,
            "set_cardinality": len(places),
            "relation_cardinality": len(R),
            "is_reflexive": is_reflexive,
            "reflexive_explanation": reflexive_explanation,
            "is_symmetric": is_symmetric,
            "symmetric_explanation": symmetric_explanation,
            "is_transitive": is_transitive,
            "transitive_explanation": transitive_explanation,
            "is_equivalence": is_equivalence
        }

    # =========================================================================
    # 3. BREADTH-FIRST SEARCH (BFS)
    # =========================================================================
    def run_bfs(self, start_id: str, target_category: Optional[str] = None, max_depth: int = 3) -> Dict[str, Any]:
        """
        Executes Breadth-First Search (BFS) using a FIFO queue.
        Explores vertices level-by-level (nearest neighborhood expansion).
        Returns step-by-step trace showing queue state, visited set, and current depth.
        """
        if start_id not in self.nodes:
            return {"error": f"Start node '{start_id}' not found."}

        queue = deque([(start_id, 0, [start_id])])  # (node_id, depth, path)
        visited = {start_id}
        traversal_order = []
        steps = []
        matching_places = []
        tree_edges = []

        step_num = 1
        steps.append({
            "step": step_num,
            "action": "INITIALIZE",
            "current_node": self.nodes[start_id]["name"],
            "queue": [self.nodes[start_id]["name"]],
            "visited": [self.nodes[start_id]["name"]],
            "description": f"Initialize FIFO Queue with start vertex '{self.nodes[start_id]['name']}' at depth 0."
        })

        while queue:
            curr_id, depth, path = queue.popleft()
            curr_node = self.nodes[curr_id]
            traversal_order.append(curr_id)

            if target_category and curr_node.get("category") == target_category and curr_id != start_id:
                matching_places.append({
                    "id": curr_id,
                    "name": curr_node["name"],
                    "category": curr_node.get("category"),
                    "depth": depth,
                    "path": [self.nodes[p]["name"] for p in path]
                })

            if depth < max_depth:
                # Get neighbors via NEAR and CONNECTED_TO
                neighbors = []
                for edge in self.adj_list_undirected.get(curr_id, []):
                    rel_type = edge.get("type")
                    if rel_type in ["NEAR", "CONNECTED_TO"]:
                        nbr = edge["target"] if edge["source"] == curr_id else edge["source"]
                        if nbr in self.nodes and nbr not in visited:
                            neighbors.append((nbr, edge.get("distance_km", 1.0), rel_type))

                # Sort by distance for deterministic exploration
                neighbors.sort(key=lambda x: x[1])

                for nbr_id, dist, rtype in neighbors:
                    if nbr_id not in visited:
                        visited.add(nbr_id)
                        queue.append((nbr_id, depth + 1, path + [nbr_id]))
                        tree_edges.append({
                            "from": curr_id,
                            "to": nbr_id,
                            "from_name": curr_node["name"],
                            "to_name": self.nodes[nbr_id]["name"],
                            "depth": depth + 1,
                            "relation": rtype,
                            "distance_km": dist
                        })

                        step_num += 1
                        steps.append({
                            "step": step_num,
                            "action": "ENQUEUE",
                            "current_node": curr_node["name"],
                            "neighbor": self.nodes[nbr_id]["name"],
                            "queue": [self.nodes[q[0]]["name"] for q in queue],
                            "visited": [self.nodes[v]["name"] for v in visited],
                            "description": f"Discovered neighbor '{self.nodes[nbr_id]['name']}' via {rtype} ({dist} km). Enqueued at depth {depth + 1}."
                        })

        return {
            "start_node": self.nodes[start_id]["name"],
            "total_visited": len(visited),
            "traversal_order": [self.nodes[nid]["name"] for nid in traversal_order],
            "tree_edges": tree_edges,
            "matching_places": matching_places,
            "steps": steps,
            "algorithm": "Breadth-First Search (Queue FIFO)",
            "complexity": "O(V + E)"
        }

    # =========================================================================
    # 4. DEPTH-FIRST SEARCH (DFS)
    # =========================================================================
    def run_dfs(self, start_id: str, max_depth: int = 4) -> Dict[str, Any]:
        """
        Executes Depth-First Search (DFS) using a LIFO call stack.
        Explores branches to their maximum depth before backtracking.
        Includes discovery/finish timestamps and backtrack steps.
        """
        if start_id not in self.nodes:
            return {"error": f"Start node '{start_id}' not found."}

        visited: Set[str] = set()
        stack: List[str] = []
        steps = []
        discovery_time = {}
        finish_time = {}
        tree_edges = []
        timer = [0]
        step_num = [0]

        def dfs_visit(u: str, depth: int):
            if depth > max_depth:
                return

            visited.add(u)
            stack.append(u)
            timer[0] += 1
            discovery_time[u] = timer[0]
            step_num[0] += 1

            steps.append({
                "step": step_num[0],
                "action": "PUSH",
                "current_node": self.nodes[u]["name"],
                "stack": [self.nodes[sid]["name"] for sid in stack],
                "visited": [self.nodes[v]["name"] for v in visited],
                "timestamp": f"d[{self.nodes[u]['name']}] = {timer[0]}",
                "description": f"Push '{self.nodes[u]['name']}' onto LIFO stack at depth {depth}. Discovery timestamp d = {timer[0]}."
            })

            # Inspect neighbors
            neighbors = []
            for edge in self.adj_list_undirected.get(u, []):
                if edge.get("type") in ["NEAR", "CONNECTED_TO"]:
                    nbr = edge["target"] if edge["source"] == u else edge["source"]
                    if nbr in self.nodes:
                        neighbors.append((nbr, edge.get("distance_km", 1.0), edge.get("type")))

            neighbors.sort(key=lambda x: x[1])

            for nbr, dist, rtype in neighbors:
                if nbr not in visited:
                    tree_edges.append({
                        "from": u,
                        "to": nbr,
                        "from_name": self.nodes[u]["name"],
                        "to_name": self.nodes[nbr]["name"],
                        "relation": rtype
                    })
                    dfs_visit(nbr, depth + 1)

            # Backtracking (Pop from stack)
            timer[0] += 1
            finish_time[u] = timer[0]
            popped = stack.pop()
            step_num[0] += 1
            steps.append({
                "step": step_num[0],
                "action": "POP (BACKTRACK)",
                "current_node": self.nodes[popped]["name"],
                "stack": [self.nodes[sid]["name"] for sid in stack],
                "visited": [self.nodes[v]["name"] for v in visited],
                "timestamp": f"f[{self.nodes[u]['name']}] = {timer[0]}",
                "description": f"Finished exploring all branches from '{self.nodes[popped]['name']}'. Backtrack and pop from stack. Finish timestamp f = {timer[0]}."
            })

        dfs_visit(start_id, 0)

        return {
            "start_node": self.nodes[start_id]["name"],
            "total_visited": len(visited),
            "discovery_times": {self.nodes[k]["name"]: v for k, v in discovery_time.items()},
            "finish_times": {self.nodes[k]["name"]: v for k, v in finish_time.items()},
            "tree_edges": tree_edges,
            "steps": steps,
            "algorithm": "Depth-First Search (Stack LIFO)",
            "complexity": "O(V + E)"
        }

    # =========================================================================
    # 5. DIJKSTRA'S SHORTEST PATH ALGORITHM
    # =========================================================================
    def run_dijkstra(self, start_id: str, end_id: str) -> Dict[str, Any]:
        """
        Executes Dijkstra's Shortest Path Algorithm on weighted edges (distance_km).
        Demonstrates edge relaxation: d[v] = min(d[v], d[u] + w(u, v)).
        Returns shortest route, total distance, and step-by-step relaxation table.
        """
        if start_id not in self.nodes or end_id not in self.nodes:
            return {"error": "Invalid start or destination node ID."}

        distances = {nid: float("inf") for nid in self.nodes}
        distances[start_id] = 0.0
        previous = {nid: None for nid in self.nodes}
        
        # Priority Queue: (distance, node_id)
        pq = [(0.0, start_id)]
        visited = set()
        relaxation_steps = []
        step_counter = 0

        while pq:
            curr_dist, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)

            if u == end_id:
                break

            u_name = self.nodes[u]["name"]

            # Explore outgoing/undirected travel edges (NEAR or CONNECTED_TO)
            for edge in self.adj_list_undirected.get(u, []):
                rel_type = edge.get("type")
                if rel_type in ["NEAR", "CONNECTED_TO"]:
                    v = edge["target"] if edge["source"] == u else edge["source"]
                    weight = float(edge.get("distance_km", 1.0))
                    v_name = self.nodes[v]["name"]

                    old_dist = distances[v]
                    new_dist = curr_dist + weight
                    step_counter += 1

                    relaxed = False
                    if new_dist < old_dist:
                        distances[v] = round(new_dist, 2)
                        previous[v] = u
                        heapq.heappush(pq, (new_dist, v))
                        relaxed = True

                    relaxation_steps.append({
                        "step": step_counter,
                        "current_node": u_name,
                        "neighbor": v_name,
                        "edge_type": rel_type,
                        "weight_km": weight,
                        "old_distance": "∞" if old_dist == float("inf") else round(old_dist, 2),
                        "tentative_distance": round(new_dist, 2),
                        "relaxed": relaxed,
                        "decision": f"d[{v_name}] updated to {round(new_dist, 2)} km" if relaxed else f"Keep existing d[{v_name}] = {round(old_dist, 2)} km"
                    })

        # Reconstruct path
        path_ids = []
        curr = end_id
        while curr is not None:
            path_ids.append(curr)
            curr = previous[curr]
        path_ids.reverse()

        if len(path_ids) == 1 and path_ids[0] != start_id:
            return {
                "found": False,
                "message": f"No connected route found between {self.nodes[start_id]['name']} and {self.nodes[end_id]['name']}."
            }

        path_details = []
        for i in range(len(path_ids)):
            nid = path_ids[i]
            node = self.nodes[nid]
            leg_info = {"name": node["name"], "category": node.get("category"), "area": node.get("area")}
            if i > 0:
                prev_id = path_ids[i - 1]
                # find connecting edge
                dist_val = 0.0
                mode_val = "Transit"
                for edge in self.adj_list_undirected.get(prev_id, []):
                    target_candidate = edge["target"] if edge["source"] == prev_id else edge["source"]
                    if target_candidate == nid:
                        dist_val = edge.get("distance_km", 0.0)
                        mode_val = edge.get("mode", edge.get("type", "Near"))
                        break
                leg_info["travel_from_prev"] = f"{dist_val} km via {mode_val}"
            path_details.append(leg_info)

        return {
            "found": True,
            "start_node": self.nodes[start_id]["name"],
            "end_node": self.nodes[end_id]["name"],
            "total_distance_km": round(distances[end_id], 2),
            "shortest_path": [self.nodes[nid]["name"] for nid in path_ids],
            "path_details": path_details,
            "relaxation_steps": relaxation_steps,
            "algorithm": "Dijkstra's Shortest Path Algorithm (Greedy Min-Heap)",
            "complexity": "O((V + E) log V)"
        }

    # =========================================================================
    # 6. SET THEORY OPERATIONS (SETS, UNION, INTERSECTION, DIFFERENCE)
    # =========================================================================
    def run_set_operation(self, set_a_query: Dict[str, Any], set_b_query: Dict[str, Any], operation: str = "UNION") -> Dict[str, Any]:
        r"""
        Executes discrete set operations on the universe of tourist places U.
        Demonstrates:
        - Union: A ∪ B
        - Intersection: A ∩ B
        - Difference: A \ B
        - Symmetric Difference: A Δ B = (A \ B) ∪ (B \ A)
        - Inclusion-Exclusion Principle: |A ∪ B| = |A| + |B| - |A ∩ B|
        """
        def filter_places(criteria: Dict[str, Any]) -> Set[str]:
            res = set()
            for nid, node in self.nodes.items():
                if node.get("category") == "City":
                    continue
                match = True
                if "city" in criteria and criteria["city"] and node.get("city") != criteria["city"]:
                    match = False
                if "category" in criteria and criteria["category"] and node.get("category") != criteria["category"]:
                    match = False
                if "price_tier" in criteria and criteria["price_tier"] and node.get("price_tier") != criteria["price_tier"]:
                    match = False
                if "is_unesco" in criteria and node.get("is_unesco") != criteria["is_unesco"]:
                    match = False
                if "max_price" in criteria and (node.get("price_inr", node.get("entry_fee", 0)) > criteria["max_price"]):
                    match = False
                if match:
                    res.add(nid)
            return res

        Set_A = filter_places(set_a_query)
        Set_B = filter_places(set_b_query)

        op = operation.upper()
        if op == "UNION":
            Result_Set = Set_A.union(Set_B)
            symbol = "A ∪ B"
            formula = "A ∪ B = { x | x ∈ A ∨ x ∈ B }"
        elif op == "INTERSECTION":
            Result_Set = Set_A.intersection(Set_B)
            symbol = "A ∩ B"
            formula = "A ∩ B = { x | x ∈ A ∧ x ∈ B }"
        elif op == "DIFFERENCE":
            Result_Set = Set_A.difference(Set_B)
            symbol = "A \\ B"
            formula = "A \\ B = { x | x ∈ A ∧ x ∉ B }"
        elif op == "SYM_DIFFERENCE":
            Result_Set = Set_A.symmetric_difference(Set_B)
            symbol = "A Δ B"
            formula = "A Δ B = (A \\ B) ∪ (B \\ A)"
        else:
            Result_Set = Set_A.union(Set_B)
            symbol = "A ∪ B"
            formula = "A ∪ B"

        # Inclusion-Exclusion check
        card_A = len(Set_A)
        card_B = len(Set_B)
        card_intersection = len(Set_A.intersection(Set_B))
        card_union = len(Set_A.union(Set_B))
        pie_verified = (card_union == card_A + card_B - card_intersection)

        def node_list(id_set):
            return [
                {
                    "id": nid,
                    "name": self.nodes[nid]["name"],
                    "category": self.nodes[nid].get("category"),
                    "city": self.nodes[nid].get("city"),
                    "rating": self.nodes[nid].get("rating")
                }
                for nid in sorted(id_set, key=lambda x: self.nodes[x]["name"])
            ]

        return {
            "operation": op,
            "symbol": symbol,
            "mathematical_definition": formula,
            "set_A_description": set_a_query.get("label", str(set_a_query)),
            "set_B_description": set_b_query.get("label", str(set_b_query)),
            "cardinality_A": card_A,
            "cardinality_B": card_B,
            "cardinality_Intersection": card_intersection,
            "cardinality_Union": card_union,
            "cardinality_Result": len(Result_Set),
            "inclusion_exclusion_principle": {
                "formula": "|A ∪ B| = |A| + |B| - |A ∩ B|",
                "calculation": f"{card_union} = {card_A} + {card_B} - {card_intersection}",
                "holds": pie_verified
            },
            "result_items": node_list(Result_Set),
            "set_A_only": node_list(Set_A - Set_B),
            "set_B_only": node_list(Set_B - Set_A),
            "intersection_items": node_list(Set_A.intersection(Set_B))
        }
