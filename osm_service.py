"""
Open-Source Mapping Services — Tourist Guide Assistant
=======================================================
All services are FREE, require no API keys and no billing account.

Services:
  - Nominatim (OpenStreetMap geocoding)      https://nominatim.openstreetmap.org
  - Overpass API (OSM place search)          https://overpass.openstreetmap.fr
  - OSRM (Open Source Routing Machine)       http://router.project-osrm.org

Attribution required (OSM licence: ODbL 1.0):
  © OpenStreetMap contributors
"""

import time
import requests
from typing import Optional, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from cache_manager import geo_cache, places_cache, routes_cache

# ---------------------------------------------------------------------------
# Constants & Configuration
# ---------------------------------------------------------------------------

USER_AGENT = "TouristGuideAssistant/1.0 (educational project; non-commercial)"

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OVERPASS_URL = "https://overpass.openstreetmap.fr/api/interpreter"
OSRM_BASE_URL = "http://router.project-osrm.org"

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

# Pre-warmed landmark geocache to make sample queries instantaneous (<1ms)
PRE_WARMED_LANDMARKS = {
    "gateway of india": {"lat": 18.9220, "lng": 72.8347, "display_name": "Gateway of India, Colaba, Mumbai, Maharashtra, India"},
    "red fort": {"lat": 28.6562, "lng": 77.2410, "display_name": "Red Fort, Netaji Subhash Marg, Chandni Chowk, Old Delhi, Delhi, India"},
    "shaniwar wada": {"lat": 18.5194, "lng": 73.8553, "display_name": "Shaniwar Wada, Bajirao Road, Shaniwar Peth, Pune, Maharashtra, India"},
    "aga khan palace": {"lat": 18.5524, "lng": 73.9015, "display_name": "Aga Khan Palace, Nagar Road, Kalyani Nagar, Pune, Maharashtra, India"},
    "charminar": {"lat": 17.3616, "lng": 78.4747, "display_name": "Charminar, Char Kaman, Ghansi Bazaar, Hyderabad, Telangana, India"},
    "marina beach": {"lat": 13.0499, "lng": 80.2824, "display_name": "Marina Beach, Kamarajar Salai, Triplicane, Chennai, Tamil Nadu, India"},
    "india gate": {"lat": 28.6129, "lng": 77.2295, "display_name": "India Gate, Rajpath, New Delhi, Delhi, India"},
    "qutub minar": {"lat": 28.5244, "lng": 77.1855, "display_name": "Qutub Minar, Mehrauli, New Delhi, Delhi, India"},
    "golconda fort": {"lat": 17.3833, "lng": 78.4011, "display_name": "Golconda Fort, Ibrahim Bagh, Hyderabad, Telangana, India"},
    "fort st george": {"lat": 13.0797, "lng": 80.2874, "display_name": "Fort St. George, Rajaji Salai, Chennai, Tamil Nadu, India"}
}
for name, data in PRE_WARMED_LANDMARKS.items():
    geo_cache.set(name, data)
    geo_cache.set(f"{name}, india", data)

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
# Internal Helpers
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
                           radius: int, limit: int = 15) -> str:
    effective_radius = min(max(radius, 1000), 3000)
    filters = OVERPASS_FILTERS.get(place_type, [("tourism", "attraction")])

    lines = []
    for key, value in filters[:3]:
        lines.append(f'  node["{key}"="{value}"]["name"](around:{effective_radius},{lat},{lng});')

    return (
        f"[out:json][timeout:5];\n"
        f"(\n"
        + "\n".join(lines) +
        f"\n);\n"
        f"out {limit};"
    )


def format_osm_place(element: dict) -> dict:
    """Normalize an Overpass OSM element into a plain dict for the frontend."""
    tags = element.get("tags", {})
    lat, lng = _get_lat_lng(element)

    name    = tags.get("name:en") or tags.get("name") or "Unnamed Place"
    address = _get_address(tags)
    cat     = _get_category(tags)

    hours   = (tags.get("opening_hours") or
               tags.get("opening_hours:en") or "")
    phone   = (tags.get("phone") or tags.get("contact:phone") or
               tags.get("contact:mobile") or "")
    website = (tags.get("website") or tags.get("contact:website") or
               tags.get("url") or "")
    cuisine = (tags.get("cuisine") or tags.get("diet:vegetarian") or "")

    osm_type = element.get("type", "node")
    osm_id   = element.get("id", "")
    osm_url  = f"https://www.openstreetmap.org/{osm_type}/{osm_id}" if osm_id else ""

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


# ---------------------------------------------------------------------------
# Public API with Caching & Fast Failovers
# ---------------------------------------------------------------------------

def search_nominatim(query: str, limit: int = 15, country: str = "in") -> list:
    """
    Search places via Nominatim text query.
    Cached for high speed and instant responses.
    """
    cache_key = f"nom_{query.lower().strip()}_{limit}_{country}"
    cached = places_cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        params = {
            "q": query,
            "format": "json",
            "limit": limit,
            "countrycodes": country,
            "addressdetails": 0,
        }
        resp = requests.get(NOMINATIM_URL, params=params, headers=DEFAULT_HEADERS, timeout=5)
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

        places_cache.set(cache_key, places)
        return places
    except Exception:
        return []


def search_nearby(lat: float, lng: float,
                  place_type: str = "tourist_attraction",
                  radius: int = 3000) -> dict:
    """
    Search OSM places near (lat, lng) of given type within radius metres.
    Features instant caching, fast Overpass check with immediate Nominatim fallback.
    """
    cache_key = f"nearby_{round(lat, 3)}_{round(lng, 3)}_{place_type}_{radius}"
    cached = places_cache.get(cache_key)
    if cached is not None:
        return cached

    # Attempt fast Overpass check (timeout=3.5s)
    query = _build_overpass_query(place_type, lat, lng, radius)
    try:
        resp = requests.post(
            OVERPASS_URL,
            data={"data": query},
            headers=DEFAULT_HEADERS,
            timeout=3.5,
        )
        if resp.status_code == 200:
            elements = resp.json().get("elements", [])
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
                res = {"places": places, "count": len(places)}
                places_cache.set(cache_key, res)
                return res
    except Exception:
        pass # Immediately proceed to fast Nominatim fallback

    # Fast Nominatim fallback
    label_map = {
        "restaurant": "restaurants",
        "hotel": "hotels",
        "museum": "museums",
        "tourist_attraction": "attractions",
        "subway_station": "metro station",
        "transit_station": "transit station",
    }
    label = label_map.get(place_type, "attractions")

    # Match to city name if near known center
    for city_name, coords in CITY_CENTERS.items():
        if abs(coords["lat"] - lat) < 0.6 and abs(coords["lng"] - lng) < 0.6:
            nom_places = search_nominatim(f"{label} in {city_name.title()} India")
            if nom_places:
                res = {"places": nom_places, "count": len(nom_places)}
                places_cache.set(cache_key, res)
                return res
            break

    # Search around coords if not near recognized city center
    nom_places = search_nominatim(f"{label} near {round(lat, 4)},{round(lng, 4)}")
    if nom_places:
        res = {"places": nom_places, "count": len(nom_places)}
        places_cache.set(cache_key, res)
        return res

    res = {"places": [], "count": 0}
    places_cache.set(cache_key, res, ttl=300) # short TTL for empty
    return res


def geocode(query: str, country: str = "in") -> Optional[dict]:
    """
    Geocode a free-form query via Nominatim (OpenStreetMap).
    Caches results to eliminate repetitive 1s delays.
    """
    cache_key = query.lower().strip()
    cached = geo_cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        params = {
            "q":            query,
            "format":       "json",
            "limit":        1,
            "countrycodes": country,
            "addressdetails": 0,
        }
        resp = requests.get(NOMINATIM_URL, params=params,
                            headers=DEFAULT_HEADERS, timeout=5)
        if resp.status_code == 200:
            results = resp.json()
            if not results:
                # Retry without country restriction
                params.pop("countrycodes", None)
                resp = requests.get(NOMINATIM_URL, params=params,
                                    headers=DEFAULT_HEADERS, timeout=5)
                results = resp.json() if resp.status_code == 200 else []

            if results:
                r = results[0]
                loc = {
                    "lat":          float(r["lat"]),
                    "lng":          float(r["lon"]),
                    "display_name": r.get("display_name", query),
                }
                geo_cache.set(cache_key, loc)
                return loc
        return None
    except Exception:
        return None


def get_directions(origin: str, destination: str) -> dict:
    """
    Geocode both endpoints concurrently via ThreadPoolExecutor, then route via OSRM.
    Caches route results to make repeated directions queries instant (<5ms).
    """
    cache_key = f"dir_{origin.lower().strip()}_{destination.lower().strip()}"
    cached = routes_cache.get(cache_key)
    if cached is not None:
        return cached

    # Geocode origin and destination in parallel threads
    with ThreadPoolExecutor(max_workers=2) as executor:
        f_orig = executor.submit(geocode, origin)
        f_dest = executor.submit(geocode, destination)
        orig_loc = f_orig.result()
        dest_loc = f_dest.result()

    if not orig_loc:
        return {"error": f"Could not locate '{origin}'. Try a more specific name."}
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
        resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=8)
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
            for s in legs[0].get("steps", [])[:8]:
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

        res = {
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
        routes_cache.set(cache_key, res)
        return res

    except requests.exceptions.ConnectionError:
        return {"error": "Network error. Check your internet connection."}
    except requests.exceptions.Timeout:
        return {"error": "OSRM routing timed out. Please try again."}
    except Exception as e:
        return {"error": f"Routing error: {str(e)}"}
