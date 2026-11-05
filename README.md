# 🗺️ Tourist Guide Assistant

A conversational chatbot that helps tourists find attractions, restaurants, hotels, and transit stations across five major Indian cities — **Mumbai, Delhi, Pune, Chennai, and Hyderabad** — using **100% free, open-source location services**.

> ✅ **No API keys required. No billing account. No Google Cloud.**

---

## Tech Stack

| Layer     | Technology                                                        |
|-----------|-------------------------------------------------------------------|
| Frontend  | HTML, CSS, JavaScript (Vanilla)                                   |
| Backend   | Python + Flask                                                    |
| Map UI    | [Leaflet.js](https://leafletjs.com/) + CartoDB Dark Matter tiles  |
| Geocoding | [Nominatim](https://nominatim.openstreetmap.org/) (OpenStreetMap) |
| Search    | [Overpass API](https://overpass-api.de/) (OSM POI data)           |
| Routing   | [OSRM](http://router.project-osrm.org/) (open-source routing)    |

---

## Features

- 💬 **Natural-language chatbot** — ask about restaurants, hotels, monuments, museums, metro stations
- 🗺️ **Interactive Leaflet map** — dark-themed map with clickable place markers
- 🔍 **Place Explorer** — browse places by city and category
- 🛣️ **Turn-by-turn directions** — OSRM routing with step-by-step instructions
- 📍 **OpenStreetMap links** — every result links back to its OSM page
- 🏙️ **5 cities covered** — Mumbai, Delhi, Pune, Chennai, Hyderabad

---

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- Internet connection (all data is fetched live from OSM services)

### 2. Install Dependencies

```bash
cd "Discrete Mathematics"
pip install -r requirements.txt
```

### 3. Environment (Optional)

No API key is required. You can optionally create a `.env` file for Flask settings:

```bash
cp .env.example .env
```

### 4. Run the Server

```bash
python app.py
```

The app starts at **http://localhost:5000**

---

## Project Structure

```
Discrete Mathematics/
├── app.py                  ← Flask backend (all routes)
├── osm_service.py          ← Nominatim, Overpass API, OSRM wrappers
├── intent_parser.py        ← Natural-language intent detection
├── requirements.txt
├── .env.example
├── .gitignore
├── templates/
│   ├── base.html           ← Shared navbar & layout
│   ├── index.html          ← Chatbot page
│   ├── map.html            ← Leaflet interactive map
│   └── explorer.html       ← Place browser grid
└── static/
    ├── css/style.css       ← Dark glassmorphic theme
    └── js/
        ├── chat.js         ← Chatbot UI logic
        ├── map.js          ← Leaflet map + markers
        └── explorer.js     ← Place explorer grid
```

---

## Chatbot Examples

| Query | What it does |
|-------|--------------|
| `Find tourist attractions near Pune` | Overpass search around Pune centre |
| `Show restaurants near Gateway of India` | Geocodes landmark → nearby restaurants |
| `Find hotels near Red Fort` | Geocodes landmark → nearby hotels |
| `Museums in Chennai` | City-centre Overpass search |
| `Directions from Shaniwar Wada to Aga Khan Palace` | OSRM routing |
| `Find hotels near Charminar` | Geocodes Charminar → nearby hotels |

---

## OSM Attribution

This project uses data from **OpenStreetMap** (© OpenStreetMap contributors), licensed under the [Open Database Licence (ODbL) 1.0](https://opendatacommons.org/licenses/odbl/1-0/).

Map tiles are provided by **CARTO** under the [CartoDB attribution](https://carto.com/attributions).

Routing is provided by **OSRM** (the Open Source Routing Machine).

---

## Usage Policy Notes

- **Nominatim** — max 1 request/second; this app enforces a 0.6 s sleep between calls. Do not use for high-volume or bulk requests.
- **Overpass API** — free public instance at `overpass-api.de`; heavy queries time out after 25 s.
- **OSRM public server** — free but no SLA; handle timeouts gracefully (the app does).

---

## Requirements

```
Flask>=3.0.0
requests>=2.31.0
python-dotenv>=1.0.0
```
