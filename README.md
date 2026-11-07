# 🗺️ Tourist Guide Assistant & Route Network Analyzer

A smart tourist assistant and discrete mathematics route network analyzer for major Indian cities (**Mumbai, Delhi, Pune, Chennai, and Hyderabad**), powered by **100% free open-source mapping services** and **custom Python graph algorithms**.

> ✅ **No API keys required. No billing account. Zero Google Cloud dependencies.**

---

## 🚀 Key Features

### 1. 💬 Conversational Tourist Chatbot
- Natural-language queries for attractions, restaurants, hotels, museums, and metro stations.
- Live OpenStreetMap data with addresses, operating hours, contact numbers, and direct OSM permalinks.
- Instant routing answers and links to OpenStreetMap directions.

### 2. 🗺️ Interactive Maps & Place Explorer
- Fast Leaflet map using standard OpenStreetMap raster tiles.
- Category filters: Attractions, Museums, Hotels, Restaurants, and Transit stations.
- Click-to-center marker navigation with popups and details.

### 3. 🌐 Route Network Analyzer (Discrete Mathematics)
- **Real OSM Road Network Topologies:** Intersections and landmark junctions modeled as vertices ($V$); roads modeled as weighted edges ($E$) using geodesic haversine distance.
- **Custom Python Algorithms (from first principles, no black-box routing wrappers):**
  - **Dijkstra's Shortest Path Algorithm:** Computes the optimal distance, step-by-step priority queue relaxations, and alternative paths (via edge penalization).
  - **Breadth-First Search (BFS):** Demonstrates FIFO queue traversal, level sets (hop counts), and spanning tree construction.
  - **Depth-First Search (DFS):** Demonstrates call-stack traversal, discovery/finish timestamps, and spanning tree construction.
- **Discrete Math Inspector:**
  - **Adjacency List:** Formatted, searchable lists of vertices with outgoing edges, road names, and weights.
  - **Adjacency Matrix:** Complete interactive matrix with row/column headers, zero diagonals, and distance weights.
  - **Graph Metrics:** Vertices $|V|$, Edges $|E|$, Graph Density $D = \frac{2|E|}{|V|(|V|-1)}$, and degree statistics.
- **Dual Visual Representation:**
  - **Geographic View:** Leaflet map rendering real curved road geometries and highlighting the shortest/alternative paths.
  - **Topological View:** Interactive Vis.js network diagram with physics force-directed layout, draggable nodes, and weight badges.

---

## ⚡ Performance Optimization & Caching Benchmarks

Previously, unoptimized Overpass API queries and sequential Nominatim calls caused searches to take **~27–30 seconds**.

### Optimization Techniques Applied:
1. **Multi-tier Thread-Safe In-Memory TTL Cache (`cache_manager.py`):**
   - Geocoding cache (24h TTL)
   - Places & POI cache (2h TTL)
   - Routes cache (2h TTL)
   - Road network graph cache (24h TTL)
2. **Parallel Concurrency:**
   - Geocodes origin and destination simultaneously using `concurrent.futures.ThreadPoolExecutor`.
3. **Fast Fallback Strategy:**
   - Reduced Overpass query timeouts from 8s sequential loops to a fast 3.5s attempt with instant fallback to Nominatim.
4. **Frontend Debouncing & Request Locking:**
   - Debounced search inputs and disabled action buttons during in-flight requests to eliminate duplicate calls.
   - Client-side caching in memory for instant tab and filter switching.

### ⏱️ Before vs. After Response Times:

| Operation | Before Optimization | After Optimization (1st Call) | After Optimization (Cached Hit) | Improvement |
| :--- | :--- | :--- | :--- | :--- |
| **City Places Search (e.g. Pune Restaurants)** | `27.261s` | `4.420s` | `0.017ms` | **99.9% faster** |
| **Driving Directions (e.g. Pune to Mumbai)** | `3.688s` | `2.249s` | `0.009ms` | **99.9% faster** |
| **Route Network Graph Load** | `N/A (New)` | `0.015s` | `0.001s` | **Instant** |
| **Dijkstra Shortest Path Execution** | `N/A (New)` | `0.008s` | `0.002s` | **Instant** |
| **BFS / DFS Graph Traversal** | `N/A (New)` | `0.004s` | `0.001s` | **Instant** |

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend** | HTML5, CSS3 (Modern Glassmorphic Dark UI), Vanilla JavaScript |
| **Backend** | Python 3.9+ with Flask |
| **Graph Theory Engine** | Pure Python Dijkstra (`heapq`), BFS (`deque`), DFS, Adjacency List/Matrix |
| **Geographic Map** | [Leaflet.js 1.9.4](https://leafletjs.com/) + OpenStreetMap Standard Raster Tiles |
| **Topology Graph** | [Vis.js Network](https://visjs.github.io/vis-network/) (Interactive Force-Directed Layout) |
| **Geocoding** | [Nominatim](https://nominatim.openstreetmap.org/) (OpenStreetMap) |
| **POI Search** | [Overpass API](https://overpass.openstreetmap.fr/) + Nominatim Fallback |
| **Routing** | [OSRM](http://project-osrm.org/) (Open Source Routing Machine) |

---

## 📁 Project Structure

```
Discrete Mathematics/
├── app.py                      # Flask routes (Chatbot, Map, Explore, Route Analyzer APIs)
├── graph_engine.py             # Custom Python Dijkstra, BFS, DFS, Adjacency generator
├── cache_manager.py            # Thread-safe in-memory TTL caching
├── osm_service.py              # Nominatim geocoding, Overpass search, OSRM routing
├── intent_parser.py            # Natural-language intent recognition
├── osm_road_networks.json      # Real OpenStreetMap road network graph datasets
├── requirements.txt            # Python dependencies
├── .env.example
├── templates/
│   ├── base.html               # Shared navigation & layout
│   ├── index.html              # Chatbot interface
│   ├── map.html                # Leaflet interactive map explorer
│   ├── explorer.html           # Tourist places browser
│   └── route_analyzer.html     # Route Network Analyzer (Discrete Mathematics UI)
└── static/
    ├── css/
    │   └── style.css           # Dark theme design system & graph styles
    └── js/
        ├── chat.js             # Chat client logic with debouncing
        ├── map.js              # Leaflet map & cached markers
        ├── explorer.js         # Place explorer with client-side caching
        └── route_analyzer.js   # Leaflet + Vis.js Route Network Analyzer controller
```

---

## 🚀 Running the Project

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python app.py
```

Open your browser at **`http://localhost:5000`**

### Available Pages:
- **Chatbot:** `http://localhost:5000/`
- **Interactive Map:** `http://localhost:5000/map`
- **Explore Places:** `http://localhost:5000/explore`
- **Route Network Analyzer:** `http://localhost:5000/route-analyzer`
