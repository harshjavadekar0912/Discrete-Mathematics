"""
Open-Source Mapping Services — Tourist Guide Assistant
=======================================================
All services are FREE, require no API keys and no billing account.

Services:
  - Nominatim (OpenStreetMap geocoding)      https://nominatim.openstreetmap.org
  - Overpass API (OSM place search)          https://overpass-api.de
  - OSRM (Open Source Routing Machine)       http://router.project-osrm.org

Attribution required (OSM licence: ODbL 1.0):
  © OpenStreetMap contributors
"""
import requests
import time
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

USER_AGENT = "TouristGuideAssistant/1.0 (educational project; non-commercial)"

NOMINATIM_URL  = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL   = "https://overpass.openstreetmap.fr/api/interpreter"
OVERPASS_ENDPOINTS = [
    "https://overpass.openstreetmap.fr/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
]
OSRM_BASE_URL  = "http://router.project-osrm.org"

DEFAULT_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en",
}

# Hardcoded city centres — used so Explorer/Map can search without geocoding
CITY_CENTERS = {
    "mumbai":    {"lat": 18.9388, "lng": 72.8354},
    "delhi":     {"lat": 28.6448, "lng": 77.2167},
    "pune":      {"lat": 18.5204, "lng": 73.8567},
    "chennai":   {"lat": 13.0827, "lng": 80.2707},
    "hyderabad": {"lat": 17.3850, "lng": 78.4867},
}

# Map intent place-type keys → lists of (OSM-tag-key, OSM-tag-value) pairs
OVERPASS_FILTERS = {
    "restaurant": [
        ("amenity", "restaurant"),
        ("amenity", "cafe"),
        ("amenity", "fast_food"),
        ("amenity", "food_court"),
    ],
    "hotel": [
        ("tourism", "hotel"),
        ("tourism", "motel"),
        ("tourism", "hostel"),
        ("tourism", "guest_house"),
        ("tourism", "resort"),
    ],
    "museum": [
        ("tourism", "museum"),
        ("tourism", "gallery"),
    ],
    "tourist_attraction": [
        ("tourism", "attraction"),
        ("tourism", "viewpoint"),
        ("tourism", "zoo"),
        ("historic", "monument"),
        ("historic", "memorial"),
        ("historic", "fort"),
        ("historic", "ruins"),
        ("historic", "archaeological_site"),
        ("historic", "temple"),
    ],
    "subway_station": [
        ("station", "subway"),
        ("railway",  "station"),
    ],
    "transit_station": [
        ("railway",  "station"),
        ("amenity",  "bus_station"),
        ("amenity",  "ferry_terminal"),
    ],
}

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_category(tags: dict) -> str:
    amenity = tags.get("amenity", "")
    tourism  = tags.get("tourism", "")
    historic = tags.get("historic", "")
    railway  = tags.get("railway", "")
    station  = tags.get("station", "")

    if amenity in ("restaurant", "cafe", "fast_food", "bar", "pub",
                   "food_court", "biergarten", "ice_cream"):
        return "Restaurant"
    if tourism in ("hotel", "motel", "hostel", "guest_house", "resort", "apartment"):
        return "Hotel"
    if tourism in ("museum", "gallery"):
        return "Museum"
    if (tourism in ("attraction", "artwork", "viewpoint", "theme_park", "zoo", "aquarium") or
        historic in ("monument", "memorial", "ruins", "castle", "fort", "temple",
                     "mosque", "church", "archaeological_site", "manor")):
        return "Attraction"
    if station == "subway" or railway in ("station", "halt") or amenity in ("bus_station", "ferry_terminal"):
        return "Transit"
    return "Place"


def _get_address(tags: dict) -> str:
    parts = []
    for key in ("addr:housenumber", "addr:street", "addr:suburb",
                "addr:city", "addr:state"):
        v = tags.get(key)
        if v:
            parts.append(v)
    if parts:
        return ", ".join(parts)
    return (tags.get("addr:city") or tags.get("addr:place") or
            tags.get("addr:district") or "")


def _get_lat_lng(element: dict) -> tuple:
    if element.get("type") == "node":
        return element.get("lat"), element.get("lon")
    center = element.get("center", {})
    return center.get("lat"), center.get("lon")


def _build_overpass_query(place_type: str, lat: float, lng: float,
                           radius: int, limit: int = 20) -> str:
    effective_radius = min(max(radius, 1000), 4000)
    filters = OVERPASS_FILTERS.get(place_type, [("tourism", "attraction")])

    lines = []
    for key, value in filters[:4]:
        # Target named nodes for fast, reliable spatial querying
        lines.append(f'  node["{key}"="{value}"]["name"](around:{effective_radius},{lat},{lng});')

    return (
        f"[out:json][timeout:25];\n"
        f"(\n"
        + "\n".join(lines) +
        f"\n);\n"
        f"out {limit};"
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def format_osm_place(element: dict) -> dict:
    """Normalize an Overpass OSM element into a plain dict for the frontend."""
    tags = element.get("tags", {})
    lat, lng = _get_lat_lng(element)

    name    = tags.get("name:en") or tags.get("name") or "Unnamed Place"
    address = _get_address(tags)
    cat     = _get_category(tags)

    phone   = (tags.get("phone") or tags.get("contact:phone") or
               tags.get("contact:mobile"))
    website = (tags.get("website") or tags.get("contact:website") or
               tags.get("url"))
    hours   = tags.get("opening_hours")
    cuisine = tags.get("cuisine", "").replace(";", ", ").strip() or None

    osm_type = element.get("type", "node")
    osm_id   = element.get("id")
    osm_url  = (f"https://www.openstreetmap.org/{osm_type}/{osm_id}"
                if osm_id else None)

    return {
        "name":          name,
        "address":       address,
        "category":      cat,
        "lat":           lat,
        "lng":           lng,
        "phone":         phone,
        "website":       website,
        "opening_hours": hours,
        "cuisine":       cuisine,
        "osm_url":       osm_url,
        "osm_id":        osm_id,
        "osm_type":      osm_type,
    }


def search_nominatim(query: str, limit: int = 15, country: str = "in") -> list:
    """
    Search places via Nominatim text query.
    Used for instant text search and as a reliable fallback when Overpass is busy.
    """
    try:
        time.sleep(0.6)
        params = {
            "q": query,
            "format": "json",
            "limit": limit,
            "countrycodes": country,
            "addressdetails": 0,
        }
        resp = requests.get(NOMINATIM_URL, params=params, headers=DEFAULT_HEADERS, timeout=8)
        if resp.status_code != 200:
            return []

        places = []
        for it in resp.json():
            name = it.get("name") or it.get("display_name", "").split(",")[0].strip()
            osm_type = it.get("osm_type", "node")
            osm_id = it.get("osm_id", "")
            places.append({
                "name": name,
                "address": it.get("display_name", ""),
                "category": it.get("type", "Place").replace("_", " ").title(),
                "lat": float(it["lat"]),
                "lng": float(it["lon"]),
                "opening_hours": "",
                "phone": "",
                "website": "",
                "cuisine": "",
                "osm_url": f"https://www.openstreetmap.org/{osm_type}/{osm_id}" if osm_id else "",
                "osm_id": osm_id,
                "osm_type": osm_type,
            })
        return places
    except Exception:
        return []


def search_nearby(lat: float, lng: float,
                  place_type: str = "tourist_attraction",
                  radius: int = 3000) -> dict:
    """
    Search OSM places near (lat, lng) of given type within radius metres.
    Uses public Overpass API with automatic Nominatim fallback.
    """
    query = _build_overpass_query(place_type, lat, lng, radius)

    for ep in OVERPASS_ENDPOINTS:
        try:
            resp = requests.post(
                ep,
                data={"data": query},
                headers=DEFAULT_HEADERS,
                timeout=8,
            )
            if resp.status_code != 200:
                continue
            data = resp.json()
            elements = data.get("elements", [])

            places = []
            for el in elements:
                tags = el.get("tags", {})
                if not tags.get("name"):
                    continue
                lat_v, lng_v = _get_lat_lng(el)
                if lat_v is None or lng_v is None:
                    continue
                places.append(format_osm_place(el))

            if places:
                return {"places": places, "count": len(places)}

        except Exception:
            continue

    # Fallback to Nominatim if Overpass is temporarily busy or returns 0 results
    label_map = {
        "restaurant": "restaurants",
        "hotel": "hotels",
        "museum": "museums",
        "tourist_attraction": "attractions",
        "subway_station": "metro station",
        "transit_station": "transit station",
    }
    label = label_map.get(place_type, "attractions")
    for city_name, coords in CITY_CENTERS.items():
        if abs(coords["lat"] - lat) < 0.6 and abs(coords["lng"] - lng) < 0.6:
            nom_places = search_nominatim(f"{label} in {city_name.title()} India")
            if nom_places:
                return {"places": nom_places, "count": len(nom_places)}
            break

    # If not near a city center, search around coordinates
    nom_places = search_nominatim(f"{label} near {lat},{lng}")
    if nom_places:
        return {"places": nom_places, "count": len(nom_places)}

    return {"places": [], "count": 0}


def geocode(query: str, country: str = "in") -> Optional[dict]:
    """
    Geocode a free-form query via Nominatim (OpenStreetMap).
    Returns {lat, lng, display_name} or None.

    Policy: 1 request/second max; include User-Agent header; no bulk requests.
    """
    try:
        time.sleep(0.6)   # Respect Nominatim 1 req/s limit

        params = {
            "q":            query,
            "format":       "json",
            "limit":        1,
            "countrycodes": country,
            "addressdetails": 0,
        }
        resp = requests.get(NOMINATIM_URL, params=params,
                            headers=DEFAULT_HEADERS, timeout=10)
        resp.raise_for_status()
        results = resp.json()

        if not results:
            # Retry without country restriction
            params.pop("countrycodes", None)
            time.sleep(0.6)
            resp = requests.get(NOMINATIM_URL, params=params,
                                headers=DEFAULT_HEADERS, timeout=10)
            resp.raise_for_status()
            results = resp.json()

        if results:
            r = results[0]
            return {
                "lat":          float(r["lat"]),
                "lng":          float(r["lon"]),
                "display_name": r.get("display_name", query),
            }
        return None

    except requests.exceptions.ConnectionError:
        return None
    except Exception:
        return None


def get_directions(origin: str, destination: str) -> dict:
    """
    Geocode both endpoints via Nominatim, then route via OSRM.
    Returns a dict with distance_km, duration_str, steps list, osm_route_url.
    """
    orig_loc = geocode(origin)
    if not orig_loc:
        return {"error": f"Could not locate '{origin}'. Try a more specific name."}

    dest_loc = geocode(destination)
    if not dest_loc:
        return {"error": f"Could not locate '{destination}'. Try a more specific name."}

    # OSRM public routing server (free, no key)
    url = (
        f"{OSRM_BASE_URL}/route/v1/driving/"
        f"{orig_loc['lng']},{orig_loc['lat']};"
        f"{dest_loc['lng']},{dest_loc['lat']}"
        f"?overview=simplified&steps=true&geometries=geojson"
    )

    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        if data.get("code") != "Ok" or not data.get("routes"):
            return {"error": "No route found between those locations."}

        route      = data["routes"][0]
        dist_m     = route.get("distance", 0)
        dur_s      = route.get("duration", 0)
        dist_km    = round(dist_m / 1000, 1)
        dur_min    = max(1, round(dur_s / 60))

        if dur_min >= 60:
            h, m = divmod(dur_min, 60)
            dur_str = f"{h}h {m}m" if m else f"{h}h"
        else:
            dur_str = f"{dur_min} min"

        # Build human-readable steps from OSRM maneuver types
        steps = []
        legs = route.get("legs", [])
        if legs:
            for s in legs[0].get("steps", [])[:10]:
                name     = s.get("name", "")
                dist_s   = s.get("distance", 0)
                dist_txt = (f"{round(dist_s)}m" if dist_s < 1000
                            else f"{round(dist_s / 1000, 1)}km")
                mv       = s.get("maneuver", {})
                mtype    = mv.get("type", "")
                mod      = mv.get("modifier", "")

                if mtype == "depart":
                    instr = f"Start on {name}" if name else "Depart"
                elif mtype == "arrive":
                    instr = "Arrive at destination"
                elif mtype == "turn":
                    instr = f"Turn {mod} onto {name}" if name else f"Turn {mod}"
                elif mtype in ("new name", "continue"):
                    instr = f"Continue on {name}" if name else "Continue straight"
                elif mtype == "roundabout":
                    instr = f"Take roundabout onto {name}" if name else "Enter roundabout"
                else:
                    instr = f"{mtype.replace('_', ' ').title()} {name}".strip()

                if instr:
                    steps.append(f"• {instr} ({dist_txt})")

        # OSM routing permalink
        osm_url = (
            f"https://www.openstreetmap.org/directions"
            f"?engine=fossgis_osrm_car"
            f"&route={orig_loc['lat']},{orig_loc['lng']}"
            f";{dest_loc['lat']},{dest_loc['lng']}"
        )

        return {
            "origin": {
                "name": orig_loc["display_name"].split(",")[0].strip(),
                **orig_loc,
            },
            "destination": {
                "name": dest_loc["display_name"].split(",")[0].strip(),
                **dest_loc,
            },
            "distance_km":    dist_km,
            "duration_str":   dur_str,
            "steps":          steps,
            "osm_route_url":  osm_url,
        }

    except requests.exceptions.ConnectionError:
        return {"error": "Network error. Check your internet connection."}
    except requests.exceptions.Timeout:
        return {"error": "OSRM routing timed out. Please try again."}
    except Exception as e:
        return {"error": f"Routing error: {str(e)}"}

