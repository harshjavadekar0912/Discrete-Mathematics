"""
Tourist Guide Assistant
Flask Backend - OpenStreetMap Integration
(Nominatim + Overpass API + OSRM — no API key required)
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

from osm_service import (
    search_nearby, geocode, get_directions, search_nominatim,
    format_osm_place, CITY_CENTERS, OVERPASS_FILTERS
)
from intent_parser import parse_intent

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["JSON_AS_ASCII"] = False


# ---------------------------------------------------------------------------
# HTML PAGE ROUTES
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Chatbot Home Interface."""
    return render_template("index.html", page="chat")


@app.route("/map")
def map_page():
    """Interactive Leaflet map page."""
    return render_template("map.html", page="map")


@app.route("/explore")
def explore_page():
    """Places Explorer page."""
    return render_template("explorer.html", page="places")


@app.route("/places")
def places_redirect():
    """Backwards compatibility redirect to /explore."""
    return explore_page()


# ---------------------------------------------------------------------------
# CHAT API
# ---------------------------------------------------------------------------

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Main chatbot endpoint — parses intent and calls OSM APIs."""
    data = request.get_json() or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Empty message"}), 400

    intent = parse_intent(message)
    answer = ""
    places = []
    extra = {}

    try:
        if intent["intent"] == "DIRECTIONS":
            origin = intent["origin"]
            dest = intent["destination"]
            result = get_directions(origin, dest)

            if "error" in result:
                answer = f"❌ {result['error']}"
            else:
                dist_km = result.get("distance_km", "?")
                dur_str = result.get("duration_str", "?")
                steps = result.get("steps", [])
                osm_route_url = result.get("osm_route_url", "")
                steps_text = "\n".join(steps[:8]) if steps else ""
                orig_name = result.get("origin", {}).get("name", origin.title())
                dest_name = result.get("destination", {}).get("name", dest.title())
                answer = (
                    f"🗺️ **Directions from {orig_name} to {dest_name}**\n\n"
                    f"📍 Distance: **{dist_km} km** | ⏱️ Estimated Time: **{dur_str}**\n\n"
                    + (f"**Step-by-step:**\n{steps_text}\n\n" if steps_text else "")
                    + (f"[📍 View on OpenStreetMap ↗]({osm_route_url})" if osm_route_url else "")
                )
                extra = {
                    "route_distance_km": dist_km,
                    "route_duration": dur_str,
                    "osm_route_url": osm_route_url,
                }

        elif intent["intent"] in ("NEARBY_LANDMARK", "CITY_TYPE_SEARCH", "CITY_ATTRACTIONS",
                                   "LANDMARK_INFO", "GENERAL_SEARCH"):
            place_type = intent.get("place_type") or "tourist_attraction"
            place_type_label = intent.get("place_type_label") or "Places"
            landmark = intent.get("landmark")
            city_key = intent.get("city_key")
            city_full = intent.get("city_full")

            loc = None

            # Priority 1: geocode landmark
            if landmark:
                query_str = landmark + (f", {city_full}" if city_full else ", India")
                loc = geocode(query_str)

            # Priority 2: use city center
            if not loc and city_key and city_key in CITY_CENTERS:
                c = CITY_CENTERS[city_key]
                loc = {"lat": c["lat"], "lng": c["lng"]}

            # Priority 3: geocode the query string
            if not loc:
                query_str = intent.get("query", message)
                loc = geocode(query_str)

            if not loc:
                nom_fallback = search_nominatim(f"{place_type_label} in {message}")
                if nom_fallback:
                    places = nom_fallback
                    answer = f"🔍 Found **{len(places)} {place_type_label}** from OpenStreetMap:"
                else:
                    answer = (
                        f"I couldn't locate **{landmark or city_full or message}**. "
                        "Try a more specific place name or city."
                    )
            else:
                radius = 3000 if landmark else 4000
                res = search_nearby(
                    loc["lat"], loc["lng"], place_type, radius
                )
                places = res.get("places", [])

                if not places and landmark:
                    places = search_nominatim(f"{place_type_label} near {landmark} India")

                if not places:
                    if res.get("error"):
                        answer = f"⚠️ {res['error']}"
                    else:
                        answer = (
                            f"I searched OpenStreetMap but found no **{place_type_label}** "
                            f"near **{landmark or city_full or message}**. "
                            "OSM data may be sparse in that area — try a different category."
                        )
                elif landmark:
                    answer = f"🗺️ Found **{len(places)} {place_type_label}** near **{landmark}**:"
                elif city_full:
                    city_display = city_full.replace(", India", "")
                    answer = f"🏙️ Found **{len(places)} {place_type_label}** in **{city_display}**:"
                else:
                    answer = f"🔍 Found **{len(places)} results** from OpenStreetMap:"

        return jsonify({
            "answer": answer,
            "places": places,
            "intent": intent["intent"],
            **extra,
        })

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}", "places": []}), 500


# ---------------------------------------------------------------------------
# PLACES API ENDPOINTS
# ---------------------------------------------------------------------------

@app.route("/api/places/citytype", methods=["GET"])
def api_places_citytype():
    """Get places for a city + type using hardcoded city centres."""
    city = (request.args.get("city") or "mumbai").lower()
    place_type = request.args.get("type", "tourist_attraction")
    radius = int(request.args.get("radius", 4000))

    if city not in CITY_CENTERS:
        return jsonify({"error": f"Unknown city '{city}'", "places": []}), 400

    c = CITY_CENTERS[city]
    res = search_nearby(c["lat"], c["lng"], place_type, radius)
    places = res.get("places", [])
    return jsonify({"places": places, "count": len(places), "city": city, "type": place_type})


@app.route("/api/places/search", methods=["GET", "POST"])
def api_places_search():
    """Search places by text query (geocode then nearby search)."""
    if request.method == "POST":
        data = request.get_json() or {}
        query = data.get("query", "")
        place_type = data.get("type", "tourist_attraction")
        radius = int(data.get("radius", 4000))
    else:
        query = request.args.get("query", "")
        place_type = request.args.get("type", "tourist_attraction")
        radius = int(request.args.get("radius", 4000))

    if not query:
        return jsonify({"error": "query param required", "places": []}), 400

    loc = geocode(query)
    if not loc:
        return jsonify({"error": f"Could not geocode '{query}'", "places": []}), 404

    res = search_nearby(loc["lat"], loc["lng"], place_type, radius)
    places = res.get("places", [])
    return jsonify({"places": places, "count": len(places)})


@app.route("/api/places/nearby", methods=["POST"])
def api_places_nearby():
    """Get nearby places by lat/lng and type."""
    data = request.get_json() or {}
    lat = data.get("lat")
    lng = data.get("lng")
    place_type = data.get("type", "tourist_attraction")
    radius = int(data.get("radius", 5000))

    if lat is None or lng is None:
        return jsonify({"error": "lat and lng required", "places": []}), 400

    res = search_nearby(float(lat), float(lng), place_type, radius)
    places = res.get("places", [])
    return jsonify({"places": places, "count": len(places)})


@app.route("/api/routes/directions", methods=["POST"])
def api_routes_directions():
    """Get driving directions between two places via OSRM."""
    data = request.get_json() or {}
    origin = data.get("origin", "")
    destination = data.get("destination", "")

    if not origin or not destination:
        return jsonify({"error": "origin and destination required"}), 400

    result = get_directions(origin, destination)
    return jsonify(result)


@app.route("/api/geocode", methods=["GET"])
def api_geocode():
    """Geocode a place name via Nominatim."""
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"error": "q param required"}), 400
    loc = geocode(q)
    if not loc:
        return jsonify({"error": f"Could not geocode '{q}'"}), 404
    return jsonify(loc)


@app.route("/api/cities", methods=["GET"])
def api_cities():
    """Return city center coordinates."""
    return jsonify(CITY_CENTERS)


@app.route("/api/status", methods=["GET"])
def api_status():
    """Health check."""
    return jsonify({
        "status": "ok",
        "data_source": "OpenStreetMap (Nominatim + Overpass API + OSRM)",
        "api_key_required": False,
        "app": "Tourist Guide Assistant"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🗺️  Tourist Guide Assistant starting on http://localhost:{port}")
    print("📡 Data source: OpenStreetMap — no API key required!")
    app.run(host="0.0.0.0", port=port, debug=True)
