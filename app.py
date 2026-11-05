"""
Tourist Guide Assistant
Flask Backend - Google Maps Platform Integration
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

from google_maps_service import (
    search_places, get_nearby_places, get_directions,
    format_place, CITY_CENTERS, get_api_key
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
    """Interactive Google Maps page."""
    maps_key = get_api_key()
    return render_template("map.html", page="map", maps_key=maps_key)


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
    """Main chatbot endpoint — parses intent and calls Google Maps APIs."""
    data = request.get_json() or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Empty message"}), 400

    api_key = get_api_key()
    if not api_key:
        return jsonify({
            "answer": "⚠️ **Google Maps API key not configured.** Please add `GOOGLE_MAPS_API_KEY` to your `.env` file and restart the server. See `.env.example` for instructions.",
            "places": [],
            "intent": "NO_KEY"
        })

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
            elif result.get("routes"):
                route = result["routes"][0]
                legs = route.get("legs", [])
                dist_m = route.get("distanceMeters", 0)
                dur = route.get("localizedValues", {}).get("duration", {}).get("text", "")
                dist_km = round(dist_m / 1000, 1) if dist_m else "?"
                steps_text = ""
                if legs:
                    leg = legs[0]
                    steps = leg.get("steps", [])
                    step_list = []
                    for s in steps[:8]:
                        nav = s.get("navigationInstruction", {})
                        instr = nav.get("instructions", "")
                        s_dist = s.get("localizedValues", {}).get("distance", {}).get("text", "")
                        if instr:
                            step_list.append(f"• {instr} ({s_dist})")
                    steps_text = "\n".join(step_list)
                answer = (
                    f"🗺️ **Directions from {origin.title()} to {dest.title()}**\n\n"
                    f"📏 Distance: **{dist_km} km** | ⏱️ Estimated Time: **{dur}**\n\n"
                    + (f"**Step-by-step:**\n{steps_text}" if steps_text else "")
                )
                extra = {"route_distance_km": dist_km, "route_duration": dur}
            else:
                answer = f"I couldn't find a route from **{origin}** to **{dest}**. Please check the place names and try again."

        elif intent["intent"] in ("NEARBY_LANDMARK", "CITY_TYPE_SEARCH", "CITY_ATTRACTIONS", "LANDMARK_INFO", "GENERAL_SEARCH"):
            query = intent["query"]
            result = search_places(query)
            if "error" in result and not result.get("places"):
                answer = f"❌ {result['error']}"
            else:
                raw_places = result.get("places", [])
                places = [format_place(p) for p in raw_places]

                if not places:
                    answer = f"I searched for **{query}** but found no results. Try rephrasing or being more specific."
                else:
                    type_label = intent.get("place_type_label") or "places"
                    landmark = intent.get("landmark")
                    city_full = intent.get("city_full")

                    if landmark:
                        answer = f"🗺️ Found **{len(places)} {type_label}** near **{landmark}**:"
                    elif city_full:
                        answer = f"🏙️ Found **{len(places)} {type_label}** in **{city_full.replace(', India', '')}**:"
                    else:
                        answer = f"🔍 Found **{len(places)} results** for your search:"

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

@app.route("/api/places/search", methods=["GET", "POST"])
def api_places_search():
    """Search places by text query."""
    if request.method == "POST":
        data = request.get_json() or {}
        query = data.get("query", "")
        location_bias = data.get("location_bias")
    else:
        query = request.args.get("query", "")
        location_bias = None

    if not query:
        return jsonify({"error": "query param required", "places": []}), 400

    result = search_places(query, location_bias=location_bias)
    if "error" in result and not result.get("places"):
        return jsonify(result), 503

    raw_places = result.get("places", [])
    formatted = [format_place(p) for p in raw_places]
    return jsonify({"places": formatted, "count": len(formatted)})


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

    result = get_nearby_places(float(lat), float(lng), place_type, radius)
    if "error" in result and not result.get("places"):
        return jsonify(result), 503

    raw_places = result.get("places", [])
    formatted = [format_place(p) for p in raw_places]
    return jsonify({"places": formatted, "count": len(formatted)})


@app.route("/api/routes/directions", methods=["POST"])
def api_routes_directions():
    """Get driving directions between two places."""
    data = request.get_json() or {}
    origin = data.get("origin", "")
    destination = data.get("destination", "")

    if not origin or not destination:
        return jsonify({"error": "origin and destination required"}), 400

    result = get_directions(origin, destination)
    return jsonify(result)


@app.route("/api/cities", methods=["GET"])
def api_cities():
    """Return city center coordinates."""
    return jsonify(CITY_CENTERS)


@app.route("/api/status", methods=["GET"])
def api_status():
    """Health check."""
    return jsonify({
        "status": "ok",
        "google_maps_configured": bool(get_api_key()),
        "app": "Tourist Guide Assistant"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Tourist Guide Assistant on http://localhost:{port}")
    if not get_api_key():
        print("WARNING: GOOGLE_MAPS_API_KEY not set in .env — API calls will fail!")
    app.run(host="0.0.0.0", port=port, debug=True)
