# 🧭 Tourist Guide Knowledge Graph Chatbot

> **Discrete Mathematics Academic Project**  
> Demonstrating **Graph Theory**, **Binary Relations**, **BFS/DFS Traversal**, **Dijkstra's Algorithm**, and **Set Theory** using **Neo4j** & **Python Flask**.

---

## 🌟 Project Overview

The **Tourist Guide Knowledge Graph Chatbot** is a complete, modern web application that helps tourists discover attractions, hotels, dining, and transit options across **5 major Indian cities: Mumbai, Delhi, Pune, Chennai, and Hyderabad**.

The application models the tourist domain as an interconnected **Knowledge Graph** $G = (V, E)$ stored in Neo4j, converts natural-language queries into Cypher queries, executes them, and returns structured recommendations alongside mathematical explanations.

---

## 📐 Discrete Mathematics Core Demonstrations

This project is explicitly structured around core Discrete Mathematics concepts:

### 1. Graph Theory ($G = (V, E)$)
* **Vertices ($V$):** Categorized tourist entities (91+ vertices):
  * `City` (Mumbai, Delhi, Pune, Chennai, Hyderabad)
  * `Monument` (Gateway of India, Red Fort, Shaniwar Wada, Marina Beach, Charminar, Golconda Fort, etc.)
  * `Museum` (CSMVS Museum, National Museum, Kelkar Museum, Government Museum Chennai, Salar Jung Museum, etc.)
  * `Hotel` (The Taj Mahal Palace, Haveli Dharampura, The Ritz-Carlton Pune, Taj Coromandel, Taj Falaknuma Palace, etc.)
  * `Restaurant` (Karim's, Bademiya, Vaishali, Murugan Idli Shop, Paradise Biryani, Hotel Shadab, etc.)
  * `MetroStation` (CSMT, Lal Quila, Civil Court Metro, Chennai Central, Charminar Metro, MGBS, etc.)
* **Edges ($E$):** Labeled, directed, and undirected relationships:
  * `LOCATED_IN`: Directed hierarchical relationship $(p) \to (c)$.
  * `NEAR`: Undirected/Symmetric spatial proximity weighted by distance in kilometers.
  * `CONNECTED_TO`: Transit and pedestrian navigation routes with distance ($km$) and mode (Metro, Walk, Ferry).
  * `HAS_PRICE`: Categorical price tier relationship (Free, Budget, Moderate, Luxury).
* **Graph Representations:**
  * **Adjacency List:** $Adj[u] = \{v \in V \mid (u, v) \in E\}$
  * **Adjacency Matrix:** $A \in \{0, 1\}^{n \times n}$ where $A_{ij} = 1$ if $(v_i, v_j) \in E$
  * **Vertex Degrees:** In-degree $\text{deg}^-(v)$, Out-degree $\text{deg}^+(v)$, and Total Degree $\text{deg}(v)$.

### 2. Binary Relations on Sets ($R \subseteq A \times B$)
* **Reflexivity:** $\forall x \in V, (x, x) \in R$.  
  * `NEAR` is *Irreflexive* in tourist navigation (landmarks are not listed as near themselves).
* **Symmetry:** $\forall x, y \in V, (x, y) \in R \implies (y, x) \in R$.  
  * `NEAR` and `CONNECTED_TO` are *Symmetric* (Euclidean distance is symmetric: $d(x, y) = d(y, x)$).
* **Transitivity:** $\forall x, y, z \in V, ((x, y) \in R \land (y, z) \in R) \implies (x, z) \in R$.  
  * `LOCATED_IN` is *Transitive* ($A$ in South Mumbai $\land$ South Mumbai in Mumbai $\implies A$ in Mumbai).
  * `NEAR` is *Non-transitive* due to distance thresholds (Triangle Inequality).
* **Equivalence Relation:** Evaluated and explained in the interactive Relation Inspector.

### 3. Breadth-First Search (BFS)
* **Concept:** Explores vertices in order of their distance from the source vertex using a **FIFO Queue**.
* **Application:** Finds $k$-hop neighborhood places (e.g., immediate 1st-hop restaurants and 2nd-hop hotels).
* **Time Complexity:** $O(|V| + |E|)$.
* **Feature:** Interactive step-by-step visualizer with queue state, visited set, and exploration tree.

### 4. Depth-First Search (DFS)
* **Concept:** Explores as deep as possible along each branch before backtracking using a **LIFO Stack**.
* **Application:** Discovers deep walking itineraries and topological paths.
* **Feature:** Tracks vertex discovery timestamp $d[u]$ and finishing timestamp $f[u]$ with backtrack logs.

### 5. Dijkstra's Shortest Path Algorithm
* **Concept:** Greedy shortest path on non-negative weighted graphs using a Min-Heap priority queue.
* **Application:** Finds optimal walking/metro route between transit stations and attractions.
* **Edge Relaxation Formula:**
  $$d[v] = \min(d[v], d[u] + w(u, v))$$
* **Feature:** Displays exact step-by-step edge relaxation table showing tentative distance updates and predecessor decisions.

### 6. Set Theory Operations
* Let universe $U = \text{All Places}$:
  * $M = \text{Museums}$, $N = \text{Monuments}$, $H = \text{Hotels}$, $R = \text{Restaurants}$
  * $S_{\text{Mumbai}}, S_{\text{Delhi}}$
* **Union ($A \cup B$):** $\{x \mid x \in A \lor x \in B\}$ (e.g., "Show museums and monuments").
* **Intersection ($A \cap B$):** $\{x \mid x \in A \land x \in B\}$ (e.g., Heritage sites that are also Museums).
* **Relative Complement / Difference ($A \setminus B$):** $\{x \mid x \in A \land x \notin B\}$.
* **Principle of Inclusion-Exclusion (PIE):**
  $$|A \cup B| = |A| + |B| - |A \cap B|$$
  Verified dynamically with live cardinality badges and Venn diagram partition cards.

---

## 💬 Chatbot Queries & Cypher Mapping

The chatbot automatically translates tourist questions to Cypher:

| Natural Language Query | Discrete Math Intent | Generated Cypher Pattern |
|------------------------|----------------------|---------------------------|
| *"Which restaurants are near Gateway of India?"* | 1st-degree Adjacency $N(u)$ | `MATCH (m:Place {name: 'Gateway of India'})-[r:NEAR]-(res:Restaurant) RETURN res.name, res.cuisine, res.rating, r.distance_km ORDER BY r.distance_km` |
| *"Find hotels near Red Fort."* | Proximity Relation $R_{NEAR}$ | `MATCH (m:Place {name: 'Red Fort'})-[r:NEAR]-(h:Hotel) RETURN h.name, h.price_inr, h.rating, r.distance_km ORDER BY r.distance_km` |
| *"Show museums in Mumbai."* | Relation $R_{LOCATED\_IN}$ | `MATCH (mus:Museum)-[:LOCATED_IN]->(c:City {name: 'Mumbai'}) RETURN mus.name, mus.description, mus.rating, mus.entry_fee` |
| *"How can I reach Gateway of India from the nearest station?"* | Shortest Transit Route | `MATCH (m:Place {name: 'Gateway of India'})-[r:CONNECTED_TO\|NEAR]-(s:MetroStation) RETURN s.name, r.distance_km, r.mode ORDER BY r.distance_km LIMIT 1` |
| *"Find the cheapest hotel near Red Fort."* | Min-Cost Optimization | `MATCH (m:Place {name: 'Red Fort'})-[r:NEAR]-(h:Hotel) RETURN h.name, h.price_inr, h.rating, r.distance_km ORDER BY h.price_inr ASC LIMIT 1` |
| *"Show museums and monuments."* | Set Union $A \cup B$ | `MATCH (p:Place) WHERE (p:Museum OR p:Monument) RETURN p.name, p.category, p.city, p.rating` |

---

## 🛠️ Architecture & Tech Stack

```
   ┌────────────────────────────────────────────────────────┐
   │             Modern Frontend Web Interface              │
   │  HTML5 + Vanilla CSS (Glassmorphism) + JavaScript      │
   │  vis-network.js Graph Canvas + Discrete Math Studio   │
   └───────────────────────────▲────────────────────────────┘
                               │ HTTP / JSON REST APIs
   ┌───────────────────────────▼────────────────────────────┐
   │                   Flask Backend (app.py)               │
   │  - REST API Routing & Controllers                     │
   │  - Discrete Math Engine (algorithms.py)                │
   │  - Cypher Query Processor (cypher_queries.py)          │
   └───────────────────────────▲────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
   ┌────────────────────────┐      ┌────────────────────────┐
   │   Neo4j Database       │      │ In-Memory Graph Engine │
   │   (Bolt Protocol:7687) │ (or) │ (Zero-Setup Fallback)  │
   │   Native Cypher Query  │      │ Full Graph Algorithms  │
   └────────────────────────┘      └────────────────────────┘
```

* **Dual-Mode Graph Engine:**
  * **Live Neo4j:** When Neo4j is running, connects via official `neo4j` Python driver and executes queries on port 7687.
  * **In-Memory Fallback:** When Neo4j is not running, the application seamlessly runs on its built-in Python In-Memory Knowledge Graph Engine, ensuring **100% functionality out-of-the-box** with zero external dependencies.

---

## 🚀 Quickstart Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Web Application
```bash
python app.py
```
Open your browser and navigate to:
```
http://localhost:5000
```

### 3. (Optional) Connect to Neo4j
If you have Neo4j running locally (via Neo4j Desktop or Docker):
```bash
docker run -d --name neo4j-tourist -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
```
1. Click the status badge in the top navbar (`In-Memory Graph Engine`).
2. Enter your Neo4j Bolt URI (`bolt://localhost:7687`), username, and password.
3. Click **Connect Neo4j**, then click **Seed Cypher Data**.
4. The system will execute all Cypher statements and switch to **Neo4j Connected** mode!

---

## 📁 Project Structure

```
tourist-guide-kg/
├── app.py                     # Flask application & REST endpoints
├── graph_db.py                # Neo4j driver + In-Memory graph engine
├── algorithms.py              # Discrete Math (BFS, DFS, Dijkstra, Sets, Relations)
├── cypher_queries.py          # NL-to-Cypher translator & chatbot synthesizer
├── seed_data.py               # 40+ nodes & relationships for Mumbai & Delhi
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── data/
│   └── seed_graph.cypher      # Standalone Cypher script for Neo4j Browser
├── static/
│   ├── css/
│   │   └── style.css          # Glassmorphic dark UI stylesheet
│   └── js/
│       ├── chat.js            # Chatbot interaction & Cypher inspector
│       ├── graph_viz.js       # vis-network physics graph visualizer
│       ├── discrete_math.js   # Interactive BFS/DFS, Dijkstra & Sets visualizer
│       └── explorer.js        # Tourist places directory & filtering
└── templates/
    ├── base.html              # Base HTML template with navbar & modal
    ├── index.html             # Chatbot home page
    ├── graph.html             # Knowledge Graph visualizer page
    ├── discrete_math.html     # Discrete Mathematics algorithms studio
    └── explorer.html          # Tourist places directory page
```

---

## 🎯 Verification & Evaluation Checklist

- [x] **Graph Theory:** Nodes (Places) and Edges (Relationships) represented and visualized.
- [x] **Relations:** Mathematical breakdown of `NEAR`, `LOCATED_IN`, `CONNECTED_TO`, and `HAS_PRICE`.
- [x] **BFS & DFS:** Interactive step-by-step queue and stack animators with discovery timestamps.
- [x] **Dijkstra:** Shortest path route between locations with distance matrix and relaxation table.
- [x] **Set Theory:** Interactive Union, Intersection, and Inclusion-Exclusion calculations.
- [x] **Mumbai & Delhi:** Over 40 realistic nodes across Monuments, Museums, Hotels, Restaurants, and Metro Stations.
- [x] **Chatbot:** Converts natural questions to Cypher and returns natural answers.
- [x] **Fully Runnable:** Runs out-of-the-box with in-memory graph engine or connects to live Neo4j.
