# 🗺️ Tourist Guide Assistant

A conversational AI chatbot that helps tourists explore **Mumbai, Delhi, Pune, Chennai, and Hyderabad** using **Google Maps Platform** as the exclusive real-time data source.

---

## ✨ Features

- 💬 **Chatbot** — Ask natural-language questions; get real Google Maps results
- 🗺️ **Interactive Map** — Browse and search places on a live Google Map
- 📍 **Explore** — Browse attractions, restaurants, hotels and transit by city & category
- 🔍 **Real-Time Data** — All results fetched live from Google Maps APIs (no hardcoded data)
- 🔒 **Secure Keys** — API key stored in `.env`, never exposed to the client

---

## 🏗️ Tech Stack

| Layer     | Technology                              |
|-----------|-----------------------------------------|
| Frontend  | HTML, CSS, JavaScript                   |
| Backend   | Python 3.11+, Flask 3.x                 |
| Data      | Google Maps Platform (Places & Routes)  |
| Map Embed | Google Maps JavaScript API              |

### Google Maps APIs Used

| API | Purpose |
|-----|---------|
| **Places API (New)** — `searchText` | Chatbot & Explorer search |
| **Places API (New)** — `searchNearby` | Nearby places search |
| **Routes API** — `computeRoutes` | Directions & travel time |
| **Maps JavaScript API** | Interactive map page |

---

## 🚀 Quick Setup

### 1. Prerequisites

- Python 3.11+ installed
- A Google Cloud account with billing enabled
- pip or virtualenv

### 2. Get Your Google Maps API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or use an existing one)
3. Enable these APIs:
   - **Maps JavaScript API**
   - **Places API (New)**
   - **Routes API**
4. Go to **Credentials** → **Create Credentials** → **API Key**
5. Copy your API key

### 3. Configure Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and paste your key
# GOOGLE_MAPS_API_KEY=AIzaSy...your_key_here...
```

### 4. Install Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 5. Run the App

```bash
python app.py
```

Open **http://localhost:5000** in your browser.

---

## 💬 Sample Chatbot Queries

| Query | What it does |
|-------|-------------|
| `Find tourist attractions near Pune.` | Searches Places API for attractions in Pune |
| `Show restaurants near Gateway of India.` | Nearby restaurant search |
| `Find hotels near Red Fort.` | Hotel search around Red Fort, Delhi |
| `Find museums in Chennai.` | Museum search in Chennai |
| `Show highly rated restaurants in Hyderabad.` | Restaurant search in Hyderabad |
| `Directions from Shaniwar Wada to Aga Khan Palace.` | Routes API directions |
| `Find hotels near Charminar.` | Hotel search near Charminar, Hyderabad |

---

## 📁 Project Structure

```
tourist-guide/
├── app.py                  # Flask app — all routes & API endpoints
├── google_maps_service.py  # Google Maps API service layer
├── intent_parser.py        # Natural language intent parser
├── requirements.txt
├── .env                    # Your secrets (never commit!)
├── .env.example            # Template for .env
├── .gitignore
├── templates/
│   ├── base.html           # Navbar, layout
│   ├── index.html          # Chatbot page
│   ├── map.html            # Interactive map page
│   └── explorer.html       # Places explorer page
└── static/
    ├── css/style.css       # Dark glassmorphic design
    └── js/
        ├── chat.js         # Chatbot UI logic
        ├── map.js          # Google Maps JS integration
        └── explorer.js     # Places explorer UI
```

---

## 🔌 REST API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| `GET` | `/` | Chatbot page |
| `GET` | `/map` | Interactive map page |
| `GET` | `/explore` | Places explorer page |
| `POST` | `/api/chat` | Main chatbot endpoint |
| `GET/POST` | `/api/places/search` | Places text search |
| `POST` | `/api/places/nearby` | Nearby places search |
| `POST` | `/api/routes/directions` | Driving directions |
| `GET` | `/api/cities` | City center coordinates |
| `GET` | `/api/status` | Health check |

---

## 🔒 API Key Security

- The API key is **only** stored in `.env` — never committed to git
- Backend (Flask) makes server-side calls to Places API and Routes API (key never reaches browser)
- For Maps JavaScript API (frontend embed), restrict the key by **HTTP referrer** in Google Cloud Console
- `.env` is listed in `.gitignore`

---

## ⚠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| `GOOGLE_MAPS_API_KEY not configured` | Add key to `.env` and restart Flask |
| `API key invalid or Places API not enabled` | Enable Places API (New) in Google Cloud Console |
| `API quota exceeded` | Wait or increase quota in Cloud Console |
| Map page shows "API Key Required" | Same as above — key must be in `.env` |
| No results for a query | Try a more specific or differently phrased query |

---

## 📝 Notes

- All tourism data is **fetched live** from Google Maps — no hardcoded data
- Results vary based on Google Maps availability for each location
- Requires an active internet connection
- Google Maps APIs are **paid** after free tier quotas ($200/month free credit)
