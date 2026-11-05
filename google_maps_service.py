"""
Google Maps Platform Service Layer
Handles all calls to Places API (New) and Routes API
"""
import os
import requests
from typing import Optional

MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")

PLACES_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
PLACES_NEARBY_URL = "https://places.googleapis.com/v1/places:searchNearby"
ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"

# City center coordinates for 5 Indian cities
CITY_CENTERS = {
    "mumbai": {"latitude": 18.9388, "longitude": 72.8354},
    "delhi": {"latitude": 28.6448, "longitude": 77.2167},
    "pune": {"latitude": 18.5204, "longitude": 73.8567},
    "chennai": {"latitude": 13.0827, "longitude": 80.2707},
    "hyderabad": {"latitude": 17.3850, "longitude": 78.4867},
}

def get_api_key() -> str:
    """Return the active Google Maps API key from environment."""
    return os.environ.get("GOOGLE_MAPS_API_KEY", "").strip()

def _headers(field_mask: str) -> dict:
    return {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": get_api_key(),
        "X-Goog-FieldMask": field_mask,
    }

def search_places(query: str, location_bias: Optional[dict] = None) -> dict:
    """Search for places using Places API (New) searchText."""
    api_key = get_api_key()
    if not api_key:
        return {"error": "GOOGLE_MAPS_API_KEY not configured. Please set it in your .env file.", "places": []}
    
    payload = {
        "textQuery": query,
        "languageCode": "en",
        "maxResultCount": 10,
    }
    if location_bias:
        payload["locationBias"] = location_bias
    
    field_mask = "places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.types,places.location,places.regularOpeningHours,places.googleMapsUri,places.photos,places.priceLevel,places.editorialSummary"
    
    try:
        resp = requests.post(PLACES_SEARCH_URL, json=payload, headers=_headers(field_mask), timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Network error — check your internet connection.", "places": []}
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 403:
            return {"error": "API key invalid or Places API not enabled. Enable Places API (New) in Google Cloud Console.", "places": []}
        if resp.status_code == 429:
            return {"error": "API quota exceeded. Please try again later.", "places": []}
        return {"error": f"Places API error: {resp.status_code}", "places": []}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "places": []}

def get_nearby_places(lat: float, lng: float, place_type: str = "tourist_attraction", radius_meters: int = 5000) -> dict:
    """Get nearby places using Places API (New) searchNearby."""
    if not get_api_key():
        return {"error": "GOOGLE_MAPS_API_KEY not configured.", "places": []}
    
    payload = {
        "includedTypes": [place_type],
        "maxResultCount": 10,
        "locationRestriction": {
            "circle": {
                "center": {"latitude": lat, "longitude": lng},
                "radius": float(radius_meters)
            }
        }
    }
    
    field_mask = "places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount,places.types,places.location,places.regularOpeningHours,places.googleMapsUri,places.priceLevel"
    
    try:
        resp = requests.post(PLACES_NEARBY_URL, json=payload, headers=_headers(field_mask), timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Network error — check your internet connection.", "places": []}
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 403:
            return {"error": "API key invalid or Places API not enabled.", "places": []}
        if resp.status_code == 429:
            return {"error": "API quota exceeded. Please try again later.", "places": []}
        return {"error": f"Places API error: {resp.status_code}", "places": []}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "places": []}

def get_directions(origin: str, destination: str) -> dict:
    """Get route between two places using Routes API."""
    if not get_api_key():
        return {"error": "GOOGLE_MAPS_API_KEY not configured.", "routes": []}
    
    payload = {
        "origin": {"address": origin},
        "destination": {"address": destination},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "computeAlternativeRoutes": False,
        "languageCode": "en",
        "units": "METRIC"
    }
    
    field_mask = "routes.duration,routes.distanceMeters,routes.legs,routes.description,routes.localizedValues"
    
    try:
        resp = requests.post(ROUTES_URL, json=payload, headers=_headers(field_mask), timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Network error — check your internet connection.", "routes": []}
    except requests.exceptions.HTTPError as e:
        if resp.status_code == 403:
            return {"error": "API key invalid or Routes API not enabled.", "routes": []}
        if resp.status_code == 429:
            return {"error": "API quota exceeded. Please try again later.", "routes": []}
        return {"error": f"Routes API error: {resp.status_code}", "routes": []}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "routes": []}

def format_place(p: dict) -> dict:
    """Normalize a Places API (New) place object into a simple dict for the frontend."""
    name = p.get("displayName", {}).get("text", "Unknown Place")
    address = p.get("formattedAddress", "")
    rating = p.get("rating")
    review_count = p.get("userRatingCount")
    types = p.get("types", [])
    maps_uri = p.get("googleMapsUri", "")
    location = p.get("location", {})
    price_level = p.get("priceLevel", "")
    summary = p.get("editorialSummary", {}).get("text", "")
    
    # Determine category from types
    category = "Place"
    if any(t in types for t in ["restaurant", "food", "cafe", "bakery"]):
        category = "Restaurant"
    elif any(t in types for t in ["lodging", "hotel", "motel", "resort_hotel"]):
        category = "Hotel"
    elif any(t in types for t in ["museum"]):
        category = "Museum"
    elif any(t in types for t in ["tourist_attraction", "monument", "historical_place", "cultural_landmark"]):
        category = "Attraction"
    elif any(t in types for t in ["transit_station", "subway_station", "train_station", "bus_station"]):
        category = "Transit"
    
    # Opening hours
    opening_hours = None
    oh = p.get("regularOpeningHours", {})
    if oh:
        opening_hours = "Open Now" if oh.get("openNow") else "Closed Now"
        weekday_desc = oh.get("weekdayDescriptions", [])
        if weekday_desc:
            opening_hours = weekday_desc[0] if len(weekday_desc) == 1 else opening_hours
    
    # Price label
    price_map = {
        "PRICE_LEVEL_FREE": "Free",
        "PRICE_LEVEL_INEXPENSIVE": "Budget (₹)",
        "PRICE_LEVEL_MODERATE": "Moderate (₹₹)",
        "PRICE_LEVEL_EXPENSIVE": "Premium (₹₹₹)",
        "PRICE_LEVEL_VERY_EXPENSIVE": "Luxury (₹₹₹₹)",
    }
    price_label = price_map.get(price_level, "")
    
    return {
        "name": name,
        "address": address,
        "category": category,
        "rating": rating,
        "review_count": review_count,
        "opening_hours": opening_hours,
        "maps_uri": maps_uri,
        "lat": location.get("latitude"),
        "lng": location.get("longitude"),
        "price_label": price_label,
        "summary": summary,
        "types": types[:3],
    }
