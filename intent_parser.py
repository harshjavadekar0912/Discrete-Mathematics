"""
Natural Language Intent Parser
Converts user queries into structured search intents for Google Maps APIs
"""
import re

# City name aliases
CITIES = {
    "mumbai": "Mumbai, India",
    "delhi": "Delhi, India",
    "new delhi": "New Delhi, India",
    "pune": "Pune, India",
    "chennai": "Chennai, India",
    "hyderabad": "Hyderabad, India",
}

CITY_SHORT = {
    "mumbai": "mumbai",
    "delhi": "delhi",
    "new delhi": "delhi",
    "pune": "pune",
    "chennai": "chennai",
    "hyderabad": "hyderabad",
}

# Famous Indian landmarks
LANDMARKS = [
    "gateway of india", "india gate", "red fort", "qutub minar", "taj mahal hotel",
    "marine drive", "colaba", "bandra", "juhu", "worli", "dadar",
    "connaught place", "lodi garden", "humayun's tomb", "akshardham",
    "shaniwar wada", "aga khan palace", "pataleshwar", "dagdusheth",
    "kapaleeshwarar temple", "marina beach", "fort st george", "government museum",
    "charminar", "golconda fort", "hussain sagar", "birla mandir",
    "elephanta caves", "cst station", "victoria terminus",
    "chhatrapati shivaji terminus", "nehru planetarium", "nehru museum",
    "national gallery of modern art", "national museum",
]

# Place type keywords
PLACE_TYPE_MAP = {
    "restaurant": ("restaurant", "Restaurant"),
    "restaurants": ("restaurant", "Restaurants"),
    "food": ("restaurant", "restaurants"),
    "eat": ("restaurant", "restaurants"),
    "dine": ("restaurant", "restaurants"),
    "hotel": ("hotel", "Hotel"),
    "hotels": ("hotel", "Hotels"),
    "stay": ("hotel", "hotels"),
    "accommodation": ("hotel", "hotels"),
    "museum": ("museum", "Museum"),
    "museums": ("museum", "Museums"),
    "monument": ("tourist_attraction", "Attractions & Monuments"),
    "monuments": ("tourist_attraction", "Attractions & Monuments"),
    "attraction": ("tourist_attraction", "Attractions"),
    "attractions": ("tourist_attraction", "Attractions"),
    "tourist": ("tourist_attraction", "tourist attractions"),
    "metro": ("subway_station", "Metro Stations"),
    "station": ("transit_station", "Transit Stations"),
    "transport": ("transit_station", "Transport"),
}

def parse_intent(text: str) -> dict:
    """
    Parse natural language query into a structured intent.
    Returns a dict with keys: intent, query, place_type, city_key, city_full, landmark, origin, destination
    """
    lowered = text.lower().strip()
    
    # Detect origin/destination for directions
    direction_patterns = [
        r"(?:directions?|route|how (?:to|can i) (?:reach|get to|go to)|navigate|from)\s+(.+?)\s+(?:to|toward)\s+(.+)",
        r"(.+?)\s+to\s+(.+?)(?:\s+route|\s+directions?|$)",
    ]
    for pat in direction_patterns:
        m = re.search(pat, lowered)
        if m and ("direction" in lowered or "route" in lowered or "how" in lowered or "reach" in lowered or "navigate" in lowered):
            origin = m.group(1).strip()
            dest = m.group(2).strip()
            # clean up
            for pfx in ["from", "get to", "go to", "reach"]:
                origin = origin.replace(pfx, "").strip()
                dest = dest.replace(pfx, "").strip()
            return {
                "intent": "DIRECTIONS",
                "origin": origin,
                "destination": dest,
                "query": text,
                "place_type": None,
                "city_key": None,
                "city_full": None,
                "landmark": None,
            }
    
    # Detect city
    city_key = None
    city_full = None
    for name, full in CITIES.items():
        if name in lowered:
            city_key = CITY_SHORT[name]
            city_full = full
            break
    
    # Detect landmark
    landmark = None
    for lm in LANDMARKS:
        if lm in lowered:
            landmark = lm.title()
            break
    
    # Detect place type
    place_type_api = None
    place_type_label = None
    for kw, (api_type, label) in PLACE_TYPE_MAP.items():
        if kw in lowered:
            place_type_api = api_type
            place_type_label = label
            break
    
    # Determine intent
    if landmark and place_type_api:
        # nearby landmark search
        return {
            "intent": "NEARBY_LANDMARK",
            "landmark": landmark,
            "place_type": place_type_api,
            "place_type_label": place_type_label,
            "city_key": city_key,
            "city_full": city_full,
            "query": f"{place_type_label} near {landmark}" + (f" {city_full}" if city_full else ""),
            "origin": None,
            "destination": None,
        }
    elif city_key and place_type_api:
        return {
            "intent": "CITY_TYPE_SEARCH",
            "city_key": city_key,
            "city_full": city_full,
            "place_type": place_type_api,
            "place_type_label": place_type_label,
            "query": f"{place_type_label} in {city_full}",
            "landmark": None,
            "origin": None,
            "destination": None,
        }
    elif city_key:
        return {
            "intent": "CITY_ATTRACTIONS",
            "city_key": city_key,
            "city_full": city_full,
            "query": f"tourist attractions in {city_full}",
            "place_type": "tourist_attraction",
            "place_type_label": "Tourist Attractions",
            "landmark": None,
            "origin": None,
            "destination": None,
        }
    elif landmark:
        return {
            "intent": "LANDMARK_INFO",
            "landmark": landmark,
            "query": f"{landmark} tourist information India",
            "place_type": None,
            "place_type_label": None,
            "city_key": None,
            "city_full": None,
            "origin": None,
            "destination": None,
        }
    else:
        # Generic text search
        cleaned = text.strip().rstrip('.?!')
        if "india" not in lowered:
            cleaned = f"{cleaned} India"
        return {
            "intent": "GENERAL_SEARCH",
            "query": cleaned,
            "place_type": place_type_api,
            "place_type_label": place_type_label,
            "city_key": city_key,
            "city_full": city_full,
            "landmark": None,
            "origin": None,
            "destination": None,
        }
