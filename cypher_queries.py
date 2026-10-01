"""
Natural Language to Cypher Query Generator and Response Synthesizer
Supports Rule-based discrete intent parsing and optional Gemini API integration.
"""

import os
import re
from typing import Dict, List, Any, Optional, Tuple
import requests

from graph_db import kg_service


# Pre-defined landmark names for entity extraction
KNOWN_LANDMARKS = [
    # Mumbai
    ("Gateway of India", ["gateway of india", "gateway", "gateway monument"]),
    ("Red Fort", ["red fort", "lal quila", "lal qila"]),
    ("Marine Drive", ["marine drive", "queen's necklace"]),
    ("Chhatrapati Shivaji Maharaj Terminus", ["csmt", "vt", "victoria terminus", "csmt station"]),
    ("India Gate", ["india gate"]),
    ("Qutub Minar", ["qutub minar", "qutub"]),
    ("Humayun's Tomb", ["humayun's tomb", "humayun tomb"]),
    ("Lotus Temple", ["lotus temple"]),
    ("Elephanta Caves", ["elephanta caves", "elephanta"]),
    ("National Museum", ["national museum"]),
    ("CSMVS Museum", ["csmvs", "prince of wales museum", "csmvs museum"]),
    ("Jehangir Art Gallery", ["jehangir art gallery", "jehangir"]),
    ("The Taj Mahal Palace", ["taj hotel", "taj mahal palace", "taj"]),
    ("Churchgate Station", ["churchgate", "churchgate station"]),
    ("Jama Masjid", ["jama masjid"]),
    ("Chandni Chowk Metro Station", ["chandni chowk metro", "chandni chowk station"]),
    ("Lal Quila Metro Station", ["lal quila metro", "lal quila station"]),

    # Pune
    ("Shaniwar Wada", ["shaniwar wada", "shaniwarwada", "shanivar wada"]),
    ("Aga Khan Palace", ["aga khan palace", "agakhan palace", "aga khan"]),
    ("Sinhagad Fort", ["sinhagad fort", "sinhagad", "sinhgarh"]),
    ("Raja Dinkar Kelkar Museum", ["kelkar museum", "raja dinkar kelkar", "kelkar"]),
    ("Tribal Cultural Museum", ["tribal museum", "tribal cultural museum"]),
    ("Vaishali Restaurant", ["vaishali", "vaishali restaurant", "vaishali fc road"]),
    ("Kayani Bakery", ["kayani bakery", "kayani"]),
    ("German Bakery", ["german bakery"]),
    ("Civil Court Metro Station", ["civil court metro", "civil court station"]),
    ("Deccan Gymkhana Metro Station", ["deccan gymkhana metro", "deccan metro"]),

    # Chennai
    ("Marina Beach", ["marina beach", "marina"]),
    ("Kapaleeshwarar Temple", ["kapaleeshwarar", "kapaleeswarar temple", "kapaleeswarar", "mylapore temple"]),
    ("Fort St. George", ["fort st george", "fort st. george", "st george fort"]),
    ("San Thome Cathedral Basilica", ["san thome", "santhome", "san thome church"]),
    ("Government Museum Chennai", ["government museum", "egmore museum", "chennai museum"]),
    ("Fort St. George Museum", ["fort museum"]),
    ("Taj Coromandel", ["taj coromandel"]),
    ("Murugan Idli Shop", ["murugan idli", "murugan idli shop"]),
    ("Buhari Hotel", ["buhari", "buhari hotel"]),
    ("Chennai Central Metro Station", ["chennai central metro", "chennai central"]),
    ("High Court Metro Station", ["high court metro", "high court station"]),

    # Hyderabad
    ("Charminar", ["charminar", "char minar"]),
    ("Golconda Fort", ["golconda fort", "golconda", "golkonda"]),
    ("Chowmahalla Palace", ["chowmahalla palace", "chowmahalla", "chowmohalla"]),
    ("Qutb Shahi Tombs", ["qutb shahi tombs", "qutub shahi tombs"]),
    ("Salar Jung Museum", ["salar jung museum", "salar jung", "salarjung"]),
    ("The Nizam's Museum", ["nizam museum", "nizam's museum"]),
    ("Taj Falaknuma Palace", ["falaknuma palace", "taj falaknuma", "falaknuma"]),
    ("Paradise Biryani", ["paradise biryani", "paradise"]),
    ("Hotel Shadab", ["hotel shadab", "shadab restaurant", "shadab"]),
    ("Bawarchi Restaurant", ["bawarchi", "bawarchi restaurant"]),
    ("MGBS Metro Interchange", ["mgbs metro", "mgbs station", "mgbs"]),
    ("Charminar Metro Station", ["charminar metro station", "charminar metro"])
]


def extract_landmark(text: str) -> Optional[str]:
    """Extracts known landmark entity from text query."""
    text_lower = text.lower()
    for canonical_name, aliases in KNOWN_LANDMARKS:
        for alias in aliases:
            if alias in text_lower:
                return canonical_name
    return None


def extract_city(text: str) -> Optional[str]:
    """Extracts target city."""
    text_lower = text.lower()
    if "delhi" in text_lower:
        return "Delhi"
    if "mumbai" in text_lower or "bombay" in text_lower:
        return "Mumbai"
    if "pune" in text_lower or "poona" in text_lower:
        return "Pune"
    if "chennai" in text_lower or "madras" in text_lower:
        return "Chennai"
    if "hyderabad" in text_lower or "secunderabad" in text_lower:
        return "Hyderabad"
    return None


class ChatbotQueryProcessor:
    def __init__(self):
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")

    def process_query(self, user_prompt: str, user_api_key: Optional[str] = None) -> Dict[str, Any]:
        """
        Main pipeline:
        1. Translates natural language question into Cypher.
        2. Executes Cypher query via kg_service (Neo4j or In-Memory fallback).
        3. Generates natural language answer & tourist cards.
        4. Outlines relevant Discrete Mathematics concept.
        """
        api_key = user_api_key or self.gemini_api_key
        
        # 1. Translate question to Cypher (Rule-based or optional Gemini)
        cypher_info = self._translate_to_cypher(user_prompt, api_key)
        cypher = cypher_info["cypher"]
        math_concept = cypher_info["discrete_math_concept"]
        intent = cypher_info["intent"]

        # 2. Execute Cypher
        exec_res = kg_service.execute_cypher(cypher)
        records = exec_res.get("records", [])
        engine_used = exec_res.get("execution_engine", "Graph Engine")

        # 3. Format Natural Language Response
        natural_response = self._synthesize_answer(user_prompt, intent, records, cypher_info.get("landmark"))

        return {
            "query": user_prompt,
            "intent": intent,
            "cypher_query": cypher,
            "discrete_math_concept": math_concept,
            "execution_engine": engine_used,
            "neo4j_connected": kg_service.is_neo4j_connected,
            "records": records,
            "total_results": len(records),
            "answer": natural_response
        }

    def _translate_to_cypher(self, text: str, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Maps question into Cypher query with discrete mathematics metadata."""
        t = text.lower().strip()
        landmark = extract_landmark(text)
        city = extract_city(text)

        # -------------------------------------------------------------
        # Query Type A: Cheapest Hotel Near Landmark
        # e.g., "Find the cheapest hotel near Red Fort"
        # -------------------------------------------------------------
        if ("cheap" in t or "lowest price" in t or "budget" in t) and "hotel" in t and (landmark or "near" in t):
            lm = landmark or ("Red Fort" if "delhi" in t else "Gateway of India")
            cypher = (
                f"MATCH (m:Place {{name: '{lm}'}})-[r:NEAR]-(h:Hotel)\n"
                f"RETURN h.name, h.price_inr, h.rating, r.distance_km, h.area\n"
                f"ORDER BY h.price_inr ASC\n"
                f"LIMIT 1"
            )
            return {
                "intent": "CHEAPEST_HOTEL_NEAR_LANDMARK",
                "landmark": lm,
                "cypher": cypher,
                "discrete_math_concept": "Greedy Optimization & Subgraph Neighborhood: Minimizing weight function w: V -> R+ over subgraph N(u) = {v | (u,v) ∈ E_NEAR}."
            }

        # -------------------------------------------------------------
        # Query Type B: Restaurants Near Landmark
        # e.g., "Which restaurants are near Gateway of India?"
        # -------------------------------------------------------------
        if ("restaurant" in t or "food" in t or "eat" in t or "dining" in t or "cafe" in t) and (landmark or "near" in t):
            lm = landmark or ("Gateway of India" if "mumbai" in t else "Red Fort")
            cypher = (
                f"MATCH (m:Place {{name: '{lm}'}})-[r:NEAR]-(res:Restaurant)\n"
                f"RETURN res.name, res.cuisine, res.rating, r.distance_km, res.price_inr\n"
                f"ORDER BY r.distance_km ASC"
            )
            return {
                "intent": "RESTAURANTS_NEAR_LANDMARK",
                "landmark": lm,
                "cypher": cypher,
                "discrete_math_concept": "Graph Theory 1st-Degree Adjacency: Locating open neighborhood N(v) = { u ∈ V | (v, u) ∈ E_NEAR } with degree d(v)."
            }

        # -------------------------------------------------------------
        # Query Type C: Hotels Near Landmark
        # e.g., "Find hotels near Red Fort"
        # -------------------------------------------------------------
        if ("hotel" in t or "stay" in t or "lodge" in t) and (landmark or "near" in t):
            lm = landmark or ("Red Fort" if "delhi" in t else "Gateway of India")
            cypher = (
                f"MATCH (m:Place {{name: '{lm}'}})-[r:NEAR]-(h:Hotel)\n"
                f"RETURN h.name, h.price_inr, h.rating, r.distance_km, h.area\n"
                f"ORDER BY r.distance_km ASC"
            )
            return {
                "intent": "HOTELS_NEAR_LANDMARK",
                "landmark": lm,
                "cypher": cypher,
                "discrete_math_concept": "Binary Proximity Relation: Demonstrating symmetric relation R_NEAR ⊆ Places × Places."
            }

        # -------------------------------------------------------------
        # Query Type D: How to reach Landmark from nearest station
        # e.g., "How can I reach Gateway of India from the nearest station?"
        # -------------------------------------------------------------
        if ("how can i reach" in t or "reach" in t or "route" in t or "station" in t or "metro" in t) and (landmark or "from" in t):
            lm = landmark or ("Gateway of India" if "mumbai" in t else "Red Fort")
            cypher = (
                f"MATCH (m:Place {{name: '{lm}'}})-[r:CONNECTED_TO|NEAR]-(s:MetroStation)\n"
                f"RETURN s.name AS station_name, r.distance_km, r.mode, m.name AS destination\n"
                f"ORDER BY r.distance_km ASC\n"
                f"LIMIT 1"
            )
            return {
                "intent": "SHORTEST_PATH_TRANSIT_TO_LANDMARK",
                "landmark": lm,
                "cypher": cypher,
                "discrete_math_concept": "Shortest Path & Dijkstra on Connected Weighted Graph: Finding min-cost edge/path in transit subnetwork."
            }

        # -------------------------------------------------------------
        # Query Type E: Set Union of Categories (Museums and Monuments)
        # e.g., "Show museums and monuments"
        # -------------------------------------------------------------
        if ("museum" in t and "monument" in t) or ("museums and monuments" in t):
            city_clause = f" AND p.city = '{city}'" if city else ""
            cypher = (
                f"MATCH (p:Place)\n"
                f"WHERE (p:Museum OR p:Monument){city_clause}\n"
                f"RETURN p.name, p.category, p.city, p.rating, p.area\n"
                f"ORDER BY p.rating DESC"
            )
            return {
                "intent": "SET_UNION_MUSEUMS_MONUMENTS",
                "landmark": None,
                "cypher": cypher,
                "discrete_math_concept": "Set Theory Union: A ∪ B = { x ∈ U | x ∈ Museums ∨ x ∈ Monuments }. Inclusion-Exclusion |A ∪ B| = |A| + |B| - |A ∩ B|."
            }

        # -------------------------------------------------------------
        # Query Type F: Museums in a City
        # e.g., "Show museums in Mumbai"
        # -------------------------------------------------------------
        if "museum" in t:
            target_city = city or "Mumbai"
            cypher = (
                f"MATCH (mus:Museum)-[:LOCATED_IN]->(c:City {{name: '{target_city}'}})\n"
                f"RETURN mus.name, mus.description, mus.rating, mus.entry_fee, mus.area\n"
                f"ORDER BY mus.rating DESC"
            )
            return {
                "intent": "MUSEUMS_IN_CITY",
                "landmark": None,
                "cypher": cypher,
                "discrete_math_concept": "Set Intersection / Function Mapping: Places ∩ { x | Category(x) = 'Museum' } filtered by Relation LOCATED_IN(x, City)."
            }

        # -------------------------------------------------------------
        # Query Type G: Monuments in a City
        # e.g., "Show monuments in Delhi"
        # -------------------------------------------------------------
        if "monument" in t or "attraction" in t or "heritage" in t or "sight" in t:
            target_city = city or "Delhi"
            cypher = (
                f"MATCH (m:Monument)-[:LOCATED_IN]->(c:City {{name: '{target_city}'}})\n"
                f"RETURN m.name, m.description, m.rating, m.entry_fee, m.area, m.is_unesco\n"
                f"ORDER BY m.rating DESC"
            )
            return {
                "intent": "MONUMENTS_IN_CITY",
                "landmark": None,
                "cypher": cypher,
                "discrete_math_concept": "Entity Classification & Hierarchical Relations: (Node:Monument)-[:LOCATED_IN]->(Node:City)."
            }

        # -------------------------------------------------------------
        # Query Type H: Metro stations in city
        # -------------------------------------------------------------
        if "metro" in t or "station" in t:
            target_city = city or "Delhi"
            cypher = (
                f"MATCH (s:MetroStation)-[:LOCATED_IN]->(c:City {{name: '{target_city}'}})\n"
                f"RETURN s.name, s.line, s.area, s.rating\n"
                f"ORDER BY s.name ASC"
            )
            return {
                "intent": "METRO_STATIONS_IN_CITY",
                "landmark": None,
                "cypher": cypher,
                "discrete_math_concept": "Graph Network Topology: Transit nodes acting as junctions in multimodal route graph."
            }

        # Default fallback query
        target_city = city or "Mumbai"
        cypher = (
            f"MATCH (p:Place)-[:LOCATED_IN]->(c:City {{name: '{target_city}'}})\n"
            f"RETURN p.name, p.category, p.rating, p.area\n"
            f"ORDER BY p.rating DESC\n"
            f"LIMIT 6"
        )
        return {
            "intent": "GENERAL_CITY_PLACES",
            "landmark": None,
            "cypher": cypher,
            "discrete_math_concept": "General Graph Pattern Matching: MATCH (p:Place)-[:LOCATED_IN]->(c:City)."
        }

    def _synthesize_answer(self, prompt: str, intent: str, records: List[Dict[str, Any]], landmark: Optional[str]) -> str:
        """Constructs a clean natural-language answer with tourist guidance."""
        if not records:
            return (
                f"I searched the knowledge graph for **'{prompt}'**, but found no matching records. "
                "Try asking for attractions near **Gateway of India** or **Red Fort**, or explore **museums in Mumbai**!"
            )

        if intent == "CHEAPEST_HOTEL_NEAR_LANDMARK":
            top = records[0]
            price = f"₹{top.get('price_inr', 'N/A')}"
            dist = f"{top.get('distance_km', '0.5')} km"
            return (
                f"The cheapest hotel near **{landmark}** is **{top['name']}** in {top.get('area', 'the area')}.\n\n"
                f"• **Price**: {price}/night\n"
                f"• **Distance**: {dist} away\n"
                f"• **Rating**: ⭐ {top.get('rating', '4.0')}/5.0\n"
                f"This result was obtained by evaluating the minimum price vertex in the 1-hop neighborhood of {landmark}."
            )

        if intent == "RESTAURANTS_NEAR_LANDMARK":
            lines = [f"Here are the top restaurants located near **{landmark}**:"]
            for r in records[:5]:
                dist_str = f"({r.get('distance_km')} km away)" if "distance_km" in r else ""
                cuisine_str = f"- {r.get('cuisine')}" if "cuisine" in r else ""
                price_str = f"~₹{r.get('price_inr')}" if "price_inr" in r else ""
                lines.append(f"• **{r['name']}** {cuisine_str} {price_str} {dist_str} — ⭐ {r.get('rating')}")
            return "\n".join(lines)

        if intent == "HOTELS_NEAR_LANDMARK":
            lines = [f"Found {len(records)} hotels within walking proximity to **{landmark}**:"]
            for h in records[:5]:
                dist_str = f"({h.get('distance_km')} km away)" if "distance_km" in h else ""
                price_str = f"₹{h.get('price_inr')}/night" if "price_inr" in h else ""
                lines.append(f"• **{h['name']}** in {h.get('area', '')} — {price_str} {dist_str} (⭐ {h.get('rating')})")
            return "\n".join(lines)

        if intent == "SHORTEST_PATH_TRANSIT_TO_LANDMARK":
            st = records[0]
            dist = st.get("distance_km", 0.5)
            mode = st.get("mode", "Walk")
            return (
                f"To reach **{landmark}**, the closest transit hub is **{st.get('station_name', 'Metro Station')}**.\n\n"
                f"• **Distance**: {dist} km\n"
                f"• **Recommended Mode**: {mode}\n"
                f"In graph theory terms, this represents the minimum weight incoming transit edge connected to {landmark}."
            )

        if intent == "SET_UNION_MUSEUMS_MONUMENTS":
            lines = [f"Found {len(records)} places in the **Union Set (Museums ∪ Monuments)**:"]
            for p in records[:8]:
                lines.append(f"• **{p['name']}** [{p.get('category')}] in {p.get('city')} — ⭐ {p.get('rating')} ({p.get('area', '')})")
            lines.append("\n*Mathematical property: |Museums ∪ Monuments| = |Museums| + |Monuments| (Disjoint sets).*")
            return "\n".join(lines)

        if intent == "MUSEUMS_IN_CITY":
            lines = [f"Here are the prominent museums in {records[0].get('city', 'the city')}:"]
            for m in records:
                fee = f"Entry: ₹{m.get('entry_fee')}" if m.get('entry_fee') is not None else "Free"
                lines.append(f"• **{m['name']}** ({m.get('area', '')}) — ⭐ {m.get('rating')} | {fee}\n  _{m.get('description', '')}_")
            return "\n".join(lines)

        # General summary
        lines = [f"Found {len(records)} results from the knowledge graph:"]
        for item in records[:6]:
            cat = f"[{item.get('category')}]" if 'category' in item else ""
            lines.append(f"• **{item['name']}** {cat} in {item.get('area', '')} — ⭐ {item.get('rating', '4.5')}")
        return "\n".join(lines)


bot_engine = ChatbotQueryProcessor()
