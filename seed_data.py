"""
Sample Knowledge Graph Data for Mumbai and Delhi
Tourist Guide Knowledge Graph Chatbot - Discrete Mathematics Project
"""

CITIES = [
    {
        "id": "city_mumbai",
        "name": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "description": "Financial capital of India, known for colonial architecture, seaside promenades, and Bollywood.",
        "type": "City"
    },
    {
        "id": "city_delhi",
        "name": "Delhi",
        "state": "Delhi NCR",
        "country": "India",
        "description": "Historical capital of India, home to Mughal monuments, ancient heritage, and vibrant bazaars.",
        "type": "City"
    },
    {
        "id": "city_pune",
        "name": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "description": "Cultural city known for Maratha history, museums, and its vibrant food scene.",
        "type": "City"
    },
    {
        "id": "city_chennai",
        "name": "Chennai",
        "state": "Tamil Nadu",
        "country": "India",
        "description": "Coastal capital of Tamil Nadu known for temples, museums, and South Indian culture.",
        "type": "City"
    },
    {
        "id": "city_hyderabad",
        "name": "Hyderabad",
        "state": "Telangana",
        "country": "India",
        "description": "Historic city known for the Charminar, Deccan heritage, and Hyderabadi cuisine.",
        "type": "City"
    }
]

PLACES = [
    # ================= MUMBAI PLACES =================
    # Monuments
    {
        "id": "mumbai_gateway",
        "name": "Gateway of India",
        "city": "Mumbai",
        "category": "Monument",
        "area": "Colaba",
        "rating": 4.7,
        "entry_fee": 0,
        "description": "Iconic arch monument built in the 20th century overlooking the Arabian Sea.",
        "is_unesco": False,
        "price_tier": "Free"
    },
    {
        "id": "mumbai_csmt",
        "name": "Chhatrapati Shivaji Maharaj Terminus",
        "city": "Mumbai",
        "category": "Monument",
        "area": "Fort",
        "rating": 4.8,
        "entry_fee": 0,
        "description": "Historic railway terminus and UNESCO World Heritage Site with Victorian Gothic architecture.",
        "is_unesco": True,
        "price_tier": "Free"
    },
    {
        "id": "mumbai_marine_drive",
        "name": "Marine Drive",
        "city": "Mumbai",
        "category": "Monument",
        "area": "Marine Lines",
        "rating": 4.8,
        "entry_fee": 0,
        "description": "3.6 km long arc-shaped boulevard along the coast, famously known as the Queen's Necklace.",
        "is_unesco": False,
        "price_tier": "Free"
    },
    {
        "id": "mumbai_elephanta",
        "name": "Elephanta Caves",
        "city": "Mumbai",
        "category": "Monument",
        "area": "Gharapuri Island",
        "rating": 4.5,
        "entry_fee": 40,
        "description": "UNESCO World Heritage site with collection of cave temples predominantly dedicated to Hindu god Shiva.",
        "is_unesco": True,
        "price_tier": "Budget"
    },
    
    # Museums
    {
        "id": "mumbai_csmvs_museum",
        "name": "CSMVS Museum",
        "alt_name": "Chhatrapati Shivaji Maharaj Vastu Sangrahalaya",
        "city": "Mumbai",
        "category": "Museum",
        "area": "Fort",
        "rating": 4.8,
        "entry_fee": 150,
        "description": "Premier art and history museum in Mumbai showcasing ancient Indian history and artwork.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    {
        "id": "mumbai_jehangir_art",
        "name": "Jehangir Art Gallery",
        "city": "Mumbai",
        "category": "Museum",
        "area": "Kala Ghoda",
        "rating": 4.6,
        "entry_fee": 0,
        "description": "Famous contemporary art gallery in Kala Ghoda founded by Sir Cowasji Jehangir.",
        "is_unesco": False,
        "price_tier": "Free"
    },
    {
        "id": "mumbai_nehru_centre",
        "name": "Nehru Science Centre",
        "city": "Mumbai",
        "category": "Museum",
        "area": "Worli",
        "rating": 4.6,
        "entry_fee": 70,
        "description": "India's largest interactive science centre with hundreds of hands-on science exhibits.",
        "is_unesco": False,
        "price_tier": "Budget"
    },

    # Hotels
    {
        "id": "mumbai_taj_hotel",
        "name": "The Taj Mahal Palace",
        "city": "Mumbai",
        "category": "Hotel",
        "area": "Colaba",
        "rating": 4.9,
        "price_inr": 24000,
        "price_tier": "Luxury",
        "stars": 5,
        "description": "Legendary five-star heritage hotel standing proudly opposite the Gateway of India."
    },
    {
        "id": "mumbai_hotel_diplomat",
        "name": "Hotel Diplomat",
        "city": "Mumbai",
        "category": "Hotel",
        "area": "Colaba",
        "rating": 4.2,
        "price_inr": 3800,
        "price_tier": "Moderate",
        "stars": 3,
        "description": "Comfortable boutique hotel located just 300 meters from Gateway of India."
    },
    {
        "id": "mumbai_sea_green_hotel",
        "name": "Sea Green Hotel",
        "city": "Mumbai",
        "category": "Hotel",
        "area": "Marine Drive",
        "rating": 4.1,
        "price_inr": 3200,
        "price_tier": "Moderate",
        "stars": 3,
        "description": "Historic sea-facing hotel situated right on Marine Drive."
    },
    {
        "id": "mumbai_oberoi",
        "name": "The Oberoi Mumbai",
        "city": "Mumbai",
        "category": "Hotel",
        "area": "Nariman Point",
        "rating": 4.8,
        "price_inr": 21000,
        "price_tier": "Luxury",
        "stars": 5,
        "description": "Luxury hotel offering panoramic views of Marine Drive and Queen's Necklace."
    },
    {
        "id": "mumbai_abode_colaba",
        "name": "Abode Bombay",
        "city": "Mumbai",
        "category": "Hotel",
        "area": "Colaba",
        "rating": 4.6,
        "price_inr": 4500,
        "price_tier": "Moderate",
        "stars": 3,
        "description": "Vintage luxury boutique hotel in Colaba within walking distance of the Gateway."
    },

    # Restaurants
    {
        "id": "mumbai_sea_lounge",
        "name": "Sea Lounge",
        "city": "Mumbai",
        "category": "Restaurant",
        "area": "Colaba",
        "rating": 4.7,
        "cuisine": "Continental & High Tea",
        "price_inr": 2800,
        "price_tier": "Luxury",
        "description": "Opulent seaside lounge in Taj Mahal Palace famed for afternoon English teas and harbour views."
    },
    {
        "id": "mumbai_bademiya",
        "name": "Bademiya",
        "city": "Mumbai",
        "category": "Restaurant",
        "area": "Colaba",
        "rating": 4.3,
        "cuisine": "Kebabs & Mughlai",
        "price_inr": 450,
        "price_tier": "Budget",
        "description": "Iconic late-night street food restaurant legendary for seekh kebabs and chicken baida roti."
    },
    {
        "id": "mumbai_leopold",
        "name": "Leopold Cafe",
        "city": "Mumbai",
        "category": "Restaurant",
        "area": "Colaba",
        "rating": 4.4,
        "cuisine": "Cafe, Continental & Beer",
        "price_inr": 900,
        "price_tier": "Moderate",
        "description": "Historic cafe established in 1871, popular among international tourists and backpackers."
    },
    {
        "id": "mumbai_pizza_by_bay",
        "name": "Pizza By The Bay",
        "city": "Mumbai",
        "category": "Restaurant",
        "area": "Marine Drive",
        "rating": 4.5,
        "cuisine": "Italian & Pizzeria",
        "price_inr": 1300,
        "price_tier": "Moderate",
        "description": "Art-deco waterfront restaurant serving gourmet pizzas with views of the Arabian sea."
    },
    {
        "id": "mumbai_cafe_mondegar",
        "name": "Cafe Mondegar",
        "city": "Mumbai",
        "category": "Restaurant",
        "area": "Colaba",
        "rating": 4.4,
        "cuisine": "Continental, Parsi & Draught Beer",
        "price_inr": 750,
        "price_tier": "Budget",
        "description": "Vintage Irani cafe featuring famous murals painted by cartoonist Mario Miranda."
    },

    # Metro / Transit Stations
    {
        "id": "mumbai_metro_csmt",
        "name": "CSMT Metro Station",
        "city": "Mumbai",
        "category": "MetroStation",
        "area": "Fort",
        "rating": 4.5,
        "line": "Aqua Line 3 / Central Railway",
        "price_tier": "Transit",
        "description": "Major multimodal transit hub connecting suburban rail and upcoming underground Aqua Line."
    },
    {
        "id": "mumbai_metro_churchgate",
        "name": "Churchgate Station",
        "city": "Mumbai",
        "category": "MetroStation",
        "area": "Churchgate",
        "rating": 4.4,
        "line": "Western Railway / Aqua Line 3",
        "price_tier": "Transit",
        "description": "Southern terminus of the Western suburban rail network and key junction near Marine Drive."
    },
    {
        "id": "mumbai_metro_colaba",
        "name": "Colaba Metro Station",
        "city": "Mumbai",
        "category": "MetroStation",
        "area": "Colaba",
        "rating": 4.6,
        "line": "Aqua Line 3",
        "price_tier": "Transit",
        "description": "Cuffe Parade & Colaba underground metro terminal serving South Mumbai tourist quarter."
    },


    # ================= DELHI PLACES =================
    # Monuments
    {
        "id": "delhi_red_fort",
        "name": "Red Fort",
        "city": "Delhi",
        "category": "Monument",
        "area": "Old Delhi",
        "rating": 4.6,
        "entry_fee": 50,
        "description": "Historic red sandstone fortress served as main residence of Mughal Emperors, UNESCO World Heritage.",
        "is_unesco": True,
        "price_tier": "Budget"
    },
    {
        "id": "delhi_jama_masjid",
        "name": "Jama Masjid",
        "city": "Delhi",
        "category": "Monument",
        "area": "Old Delhi",
        "rating": 4.6,
        "entry_fee": 0,
        "description": "One of India's largest mosques built by Mughal Emperor Shah Jahan between 1650 and 1656.",
        "is_unesco": False,
        "price_tier": "Free"
    },
    {
        "id": "delhi_india_gate",
        "name": "India Gate",
        "city": "Delhi",
        "category": "Monument",
        "area": "Central Delhi",
        "rating": 4.7,
        "entry_fee": 0,
        "description": "War memorial arch dedicated to soldiers of the British Indian Army who died in World War I.",
        "is_unesco": False,
        "price_tier": "Free"
    },
    {
        "id": "delhi_qutub_minar",
        "name": "Qutub Minar",
        "city": "Delhi",
        "category": "Monument",
        "area": "Mehrauli",
        "rating": 4.7,
        "entry_fee": 50,
        "description": "73-meter tall minaret of victory built in 1192, a UNESCO World Heritage site with intricate carvings.",
        "is_unesco": True,
        "price_tier": "Budget"
    },
    {
        "id": "delhi_humayuns_tomb",
        "name": "Humayun's Tomb",
        "city": "Delhi",
        "category": "Monument",
        "area": "Nizamuddin",
        "rating": 4.7,
        "entry_fee": 50,
        "description": "First garden-tomb on the Indian subcontinent, precursor to the Taj Mahal and UNESCO Heritage Site.",
        "is_unesco": True,
        "price_tier": "Budget"
    },
    {
        "id": "delhi_lotus_temple",
        "name": "Lotus Temple",
        "city": "Delhi",
        "category": "Monument",
        "area": "Kalkaji",
        "rating": 4.6,
        "entry_fee": 0,
        "description": "Bahá'í House of Worship notable for its flower-like lotus shape and open prayer sanctuary.",
        "is_unesco": False,
        "price_tier": "Free"
    },

    # Museums
    {
        "id": "delhi_national_museum",
        "name": "National Museum",
        "city": "Delhi",
        "category": "Museum",
        "area": "Janpath",
        "rating": 4.7,
        "entry_fee": 20,
        "description": "India's premier museum holding over 200,000 works of art covering 5,000 years of cultural heritage.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    {
        "id": "delhi_ngma",
        "name": "National Gallery of Modern Art",
        "city": "Delhi",
        "category": "Museum",
        "area": "India Gate Circle",
        "rating": 4.6,
        "entry_fee": 20,
        "description": "Premier modern and contemporary Indian art museum housed in historic Jaipur House near India Gate.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    {
        "id": "delhi_crafts_museum",
        "name": "National Crafts Museum",
        "city": "Delhi",
        "category": "Museum",
        "area": "Pragati Maidan",
        "rating": 4.6,
        "entry_fee": 20,
        "description": "Celebration of traditional Indian crafts, village architecture, handloom textiles, and living folk artists.",
        "is_unesco": False,
        "price_tier": "Budget"
    },

    # Hotels
    {
        "id": "delhi_haveli_dharampura",
        "name": "Haveli Dharampura",
        "city": "Delhi",
        "category": "Hotel",
        "area": "Chandni Chowk",
        "rating": 4.6,
        "price_inr": 8500,
        "price_tier": "Luxury",
        "stars": 4,
        "description": "Award-winning restored UNESCO heritage haveli nestled in the heart of Old Delhi near Red Fort."
    },
    {
        "id": "delhi_hotel_tara_palace",
        "name": "Hotel Tara Palace",
        "city": "Delhi",
        "category": "Hotel",
        "area": "Chandni Chowk",
        "rating": 4.2,
        "price_inr": 1800,
        "price_tier": "Budget",
        "stars": 3,
        "description": "Affordable budget hotel located just 500 meters from the Red Fort in Old Delhi."
    },
    {
        "id": "delhi_hotel_delhi_heart",
        "name": "Hotel City Star",
        "city": "Delhi",
        "category": "Hotel",
        "area": "Paharganj",
        "rating": 4.1,
        "price_inr": 2200,
        "price_tier": "Budget",
        "stars": 3,
        "description": "Popular budget hotel with modern rooms near New Delhi Railway Station."
    },
    {
        "id": "delhi_imperial_hotel",
        "name": "The Imperial Hotel",
        "city": "Delhi",
        "category": "Hotel",
        "area": "Janpath",
        "rating": 4.8,
        "price_inr": 18500,
        "price_tier": "Luxury",
        "stars": 5,
        "description": "Grand historic 5-star hotel built in 1936 during the British Raj near Connaught Place."
    },
    {
        "id": "delhi_le_meridien",
        "name": "Le Meridien New Delhi",
        "city": "Delhi",
        "category": "Hotel",
        "area": "Windsor Place",
        "rating": 4.7,
        "price_inr": 14000,
        "price_tier": "Luxury",
        "stars": 5,
        "description": "High-end contemporary hotel located within 2 km of India Gate and National Museum."
    },

    # Restaurants
    {
        "id": "delhi_karims",
        "name": "Karim's",
        "city": "Delhi",
        "category": "Restaurant",
        "area": "Old Delhi",
        "rating": 4.5,
        "cuisine": "Royal Mughlai",
        "price_inr": 600,
        "price_tier": "Budget",
        "description": "Legendary historic restaurant established in 1913 near Jama Masjid and Red Fort, famous for mutton korma."
    },
    {
        "id": "delhi_moti_mahal",
        "name": "Moti Mahal Delux",
        "city": "Delhi",
        "category": "Restaurant",
        "area": "Daryaganj",
        "rating": 4.4,
        "cuisine": "North Indian & Butter Chicken",
        "price_inr": 850,
        "price_tier": "Moderate",
        "description": "Birthplace of the legendary Butter Chicken and Tandoori Chicken, located near Red Fort."
    },
    {
        "id": "delhi_saravana_bhavan",
        "name": "Saravana Bhavan",
        "city": "Delhi",
        "category": "Restaurant",
        "area": "Connaught Place",
        "rating": 4.5,
        "cuisine": "South Indian Vegetarian",
        "price_inr": 350,
        "price_tier": "Budget",
        "description": "Renowned South Indian chain serving crispy dosas, filter coffee, and traditional thalis."
    },
    {
        "id": "delhi_gulati",
        "name": "Gulati Restaurant",
        "city": "Delhi",
        "category": "Restaurant",
        "area": "Pandara Road",
        "rating": 4.6,
        "cuisine": "North Indian & Mughlai",
        "price_inr": 1100,
        "price_tier": "Moderate",
        "description": "Iconic fine-dining establishment on Pandara Road near India Gate, famous for rich dal makhani."
    },
    {
        "id": "delhi_lakhori",
        "name": "Lakhori at Haveli Dharampura",
        "city": "Delhi",
        "category": "Restaurant",
        "area": "Chandni Chowk",
        "rating": 4.6,
        "cuisine": "Mughlai & Chaat Tasting",
        "price_inr": 2500,
        "price_tier": "Luxury",
        "description": "Rooftop dining with classical kathak dance and panoramic views of Red Fort and Jama Masjid."
    },

    # Metro / Transit Stations
    {
        "id": "delhi_metro_lal_quila",
        "name": "Lal Quila Metro Station",
        "city": "Delhi",
        "category": "MetroStation",
        "area": "Old Delhi",
        "rating": 4.6,
        "line": "Violet Line (Heritage Line)",
        "price_tier": "Transit",
        "description": "Direct metro station gate opening right outside the Red Fort entry."
    },
    {
        "id": "delhi_metro_chandni_chowk",
        "name": "Chandni Chowk Metro Station",
        "city": "Delhi",
        "category": "MetroStation",
        "area": "Chandni Chowk",
        "rating": 4.4,
        "line": "Yellow Line",
        "price_tier": "Transit",
        "description": "Major station connecting Delhi's bustling spice markets and Old Delhi monuments."
    },
    {
        "id": "delhi_metro_central_sec",
        "name": "Central Secretariat Metro Station",
        "city": "Delhi",
        "category": "MetroStation",
        "area": "Rajpath",
        "rating": 4.7,
        "line": "Yellow Line & Violet Line interchange",
        "price_tier": "Transit",
        "description": "Interchange station located near National Museum, Kartavya Path, and India Gate."
    },
    {
        "id": "delhi_metro_qutub_minar",
        "name": "Qutab Minar Metro Station",
        "city": "Delhi",
        "category": "MetroStation",
        "area": "Mehrauli",
        "rating": 4.5,
        "line": "Yellow Line",
        "price_tier": "Transit",
        "description": "Yellow Line station providing swift access to the Qutub Minar complex."
    },
    # ================= PUNE PLACES =================
    {"id": "pune_shaniwar_wada", "name": "Shaniwar Wada", "city": "Pune", "category": "Monument", "area": "Shaniwar Peth", "rating": 4.5, "entry_fee": 25, "price_tier": "Budget", "description": "Historic Peshwa fortification and palace in the heart of Pune."},
    {"id": "pune_dagdusheth", "name": "Dagdusheth Halwai Ganpati Temple", "city": "Pune", "category": "Monument", "area": "Budhwar Peth", "rating": 4.8, "entry_fee": 0, "price_tier": "Free", "description": "Famous Ganesh temple known for its ornate shrine and long-standing tradition."},
    {"id": "pune_raja_dinkar_kelkar", "name": "Raja Dinkar Kelkar Museum", "city": "Pune", "category": "Museum", "area": "Shukrawar Peth", "rating": 4.5, "entry_fee": 100, "price_tier": "Budget", "description": "Museum displaying an extensive collection of Indian art and everyday objects."},
    {"id": "pune_shabree", "name": "Shabree", "city": "Pune", "category": "Restaurant", "area": "Deccan Gymkhana", "rating": 4.3, "price_inr": 500, "price_tier": "Budget", "cuisine": "Maharashtrian" , "description": "Popular restaurant serving traditional Maharashtrian thalis."},
    {"id": "pune_fern", "name": "The Fern Residency Pune", "city": "Pune", "category": "Hotel", "area": "Shivajinagar", "rating": 4.2, "price_inr": 4500, "price_tier": "Moderate", "stars": 4, "description": "Contemporary hotel with convenient access to central Pune."},
    {"id": "pune_pmc_metro", "name": "PMC Metro Station", "city": "Pune", "category": "MetroStation", "area": "Shivajinagar", "rating": 4.3, "line": "Pune Metro Aqua Line", "price_tier": "Transit", "description": "Pune Metro station serving the central business district."},
    # ================= CHENNAI PLACES =================
    {"id": "chennai_marina", "name": "Marina Beach", "city": "Chennai", "category": "Monument", "area": "Marina", "rating": 4.5, "entry_fee": 0, "price_tier": "Free", "description": "Landmark urban beach along the Bay of Bengal and a popular city promenade."},
    {"id": "chennai_kapaleeshwarar", "name": "Kapaleeshwarar Temple", "city": "Chennai", "category": "Monument", "area": "Mylapore", "rating": 4.7, "entry_fee": 0, "price_tier": "Free", "description": "Historic Dravidian-style Shiva temple in the Mylapore neighbourhood."},
    {"id": "chennai_government_museum", "name": "Government Museum Chennai", "city": "Chennai", "category": "Museum", "area": "Egmore", "rating": 4.5, "entry_fee": 15, "price_tier": "Budget", "description": "Major museum complex with archaeology, art, and natural history collections."},
    {"id": "chennai_murugan_idli", "name": "Murugan Idli Shop", "city": "Chennai", "category": "Restaurant", "area": "T. Nagar", "rating": 4.3, "price_inr": 350, "price_tier": "Budget", "cuisine": "South Indian", "description": "Well-known eatery serving idli, dosa, and traditional Tamil dishes."},
    {"id": "chennai_savera", "name": "Savera Hotel", "city": "Chennai", "category": "Hotel", "area": "Mylapore", "rating": 4.2, "price_inr": 6000, "price_tier": "Moderate", "stars": 4, "description": "Established city hotel close to Chennai's central cultural districts."},
    {"id": "chennai_egmore_metro", "name": "Egmore Metro Station", "city": "Chennai", "category": "MetroStation", "area": "Egmore", "rating": 4.3, "line": "Chennai Metro Blue Line", "price_tier": "Transit", "description": "Metro station serving Egmore railway station and nearby attractions."},
    # ================= HYDERABAD PLACES =================
    {"id": "hyderabad_charminar", "name": "Charminar", "city": "Hyderabad", "category": "Monument", "area": "Old City", "rating": 4.6, "entry_fee": 25, "price_tier": "Budget", "description": "Four-minaret monument and defining landmark of Hyderabad's Old City."},
    {"id": "hyderabad_golconda", "name": "Golconda Fort", "city": "Hyderabad", "category": "Monument", "area": "Ibrahim Bagh", "rating": 4.6, "entry_fee": 25, "price_tier": "Budget", "description": "Hilltop fort complex renowned for its history and acoustic design."},
    {"id": "hyderabad_salar_jung", "name": "Salar Jung Museum", "city": "Hyderabad", "category": "Museum", "area": "Darulshifa", "rating": 4.6, "entry_fee": 50, "price_tier": "Budget", "description": "Art museum with collections spanning India, Europe, and Asia."},
    {"id": "hyderabad_paradise", "name": "Paradise Biryani", "city": "Hyderabad", "category": "Restaurant", "area": "Secunderabad", "rating": 4.2, "price_inr": 500, "price_tier": "Budget", "cuisine": "Hyderabadi", "description": "Popular restaurant known for Hyderabadi biryani and local dishes."},
    {"id": "hyderabad_taj_deccan", "name": "Taj Deccan", "city": "Hyderabad", "category": "Hotel", "area": "Banjara Hills", "rating": 4.5, "price_inr": 12000, "price_tier": "Luxury", "stars": 5, "description": "Full-service hotel in the Banjara Hills neighbourhood."},
    {"id": "hyderabad_charminar_metro", "name": "MGBS Metro Station", "city": "Hyderabad", "category": "MetroStation", "area": "Gowliguda", "rating": 4.3, "line": "Hyderabad Metro Green Line", "price_tier": "Transit", "description": "Metro station connecting the Mahatma Gandhi Bus Station and Old City."},
]

# ================= RELATIONSHIPS =================
# 1. LOCATED_IN: (Place)-[:LOCATED_IN]->(City)
# 2. NEAR: (PlaceA)-[:NEAR {distance_km: float}]->(PlaceB) [Symmetric in nature]
# 3. CONNECTED_TO: (Station/Place)-[:CONNECTED_TO {distance_km: float, mode: str}]->(Station/Place)
# 4. HAS_PRICE: (Place)-[:HAS_PRICE {amount_inr: int, tier: str}]->(PriceTierNode)

NEAR_RELATIONSHIPS = [
    # --- Gateway of India Cluster (Mumbai) ---
    ("mumbai_gateway", "mumbai_taj_hotel", 0.1),
    ("mumbai_gateway", "mumbai_sea_lounge", 0.1),
    ("mumbai_gateway", "mumbai_hotel_diplomat", 0.3),
    ("mumbai_gateway", "mumbai_bademiya", 0.4),
    ("mumbai_gateway", "mumbai_leopold", 0.5),
    ("mumbai_gateway", "mumbai_cafe_mondegar", 0.6),
    ("mumbai_gateway", "mumbai_abode_colaba", 0.4),
    ("mumbai_gateway", "mumbai_csmvs_museum", 0.8),
    ("mumbai_gateway", "mumbai_jehangir_art", 0.9),
    ("mumbai_taj_hotel", "mumbai_sea_lounge", 0.05),
    ("mumbai_hotel_diplomat", "mumbai_bademiya", 0.2),
    ("mumbai_csmvs_museum", "mumbai_jehangir_art", 0.2),

    # --- Marine Drive / CSMT Cluster (Mumbai) ---
    ("mumbai_marine_drive", "mumbai_oberoi", 0.5),
    ("mumbai_marine_drive", "mumbai_sea_green_hotel", 0.3),
    ("mumbai_marine_drive", "mumbai_pizza_by_bay", 0.2),
    ("mumbai_csmt", "mumbai_csmvs_museum", 1.2),
    ("mumbai_marine_drive", "mumbai_csmt", 2.2),

    # --- Red Fort Cluster (Delhi) ---
    ("delhi_red_fort", "delhi_hotel_tara_palace", 0.5),
    ("delhi_red_fort", "delhi_karims", 0.6),
    ("delhi_red_fort", "delhi_moti_mahal", 1.0),
    ("delhi_red_fort", "delhi_jama_masjid", 0.7),
    ("delhi_red_fort", "delhi_haveli_dharampura", 0.8),
    ("delhi_red_fort", "delhi_lakhori", 0.8),
    ("delhi_jama_masjid", "delhi_karims", 0.2),
    ("delhi_jama_masjid", "delhi_haveli_dharampura", 0.4),
    ("delhi_haveli_dharampura", "delhi_lakhori", 0.05),

    # --- India Gate / Central Delhi Cluster (Delhi) ---
    ("delhi_india_gate", "delhi_ngma", 0.3),
    ("delhi_india_gate", "delhi_gulati", 0.9),
    ("delhi_national_museum", "delhi_imperial_hotel", 1.1),
    ("delhi_national_museum", "delhi_le_meridien", 1.2),
    ("delhi_imperial_hotel", "delhi_saravana_bhavan", 0.7),
    ("delhi_india_gate", "delhi_national_museum", 1.4),
    # --- Pune Cluster ---
    ("pune_shaniwar_wada", "pune_dagdusheth", 0.8),
    ("pune_shaniwar_wada", "pune_raja_dinkar_kelkar", 1.5),
    ("pune_shaniwar_wada", "pune_shabree", 2.0),
    ("pune_raja_dinkar_kelkar", "pune_shabree", 1.2),
    # --- Chennai Cluster ---
    ("chennai_marina", "chennai_kapaleeshwarar", 3.0),
    ("chennai_marina", "chennai_savera", 4.0),
    ("chennai_government_museum", "chennai_egmore_metro", 0.5),
    ("chennai_government_museum", "chennai_murugan_idli", 4.0),
    # --- Hyderabad Cluster ---
    ("hyderabad_charminar", "hyderabad_salar_jung", 2.0),
    ("hyderabad_charminar", "hyderabad_paradise", 6.0),
    ("hyderabad_charminar", "hyderabad_charminar_metro", 2.5),
    ("hyderabad_golconda", "hyderabad_taj_deccan", 8.0),
]

CONNECTED_TO_RELATIONSHIPS = [
    # --- Mumbai Metro & Transit Network ---
    # Transit to Place connections (Walk/Cab)
    ("mumbai_metro_colaba", "mumbai_gateway", 1.1, "Walk / Shuttle"),
    ("mumbai_metro_colaba", "mumbai_taj_hotel", 1.0, "Walk"),
    ("mumbai_metro_churchgate", "mumbai_marine_drive", 0.6, "Walk"),
    ("mumbai_metro_churchgate", "mumbai_csmvs_museum", 0.9, "Walk"),
    ("mumbai_metro_csmt", "mumbai_csmt", 0.1, "Direct Entry"),
    ("mumbai_metro_csmt", "mumbai_csmvs_museum", 1.1, "Taxi / Walk"),

    # Metro inter-station connections (Graph edges for Dijkstra)
    ("mumbai_metro_colaba", "mumbai_metro_churchgate", 2.4, "Aqua Line 3"),
    ("mumbai_metro_churchgate", "mumbai_metro_csmt", 1.8, "Suburban Rail / Bus"),
    ("mumbai_gateway", "mumbai_elephanta", 10.0, "Ferry Boat"),

    # --- Delhi Metro & Transit Network ---
    # Transit to Place connections
    ("delhi_metro_lal_quila", "delhi_red_fort", 0.2, "Walk (Gate 1)"),
    ("delhi_metro_chandni_chowk", "delhi_red_fort", 0.7, "Walk / E-Rickshaw"),
    ("delhi_metro_chandni_chowk", "delhi_jama_masjid", 0.8, "Walk / E-Rickshaw"),
    ("delhi_metro_chandni_chowk", "delhi_hotel_tara_palace", 0.5, "Walk"),
    ("delhi_metro_central_sec", "delhi_national_museum", 0.6, "Walk"),
    ("delhi_metro_central_sec", "delhi_india_gate", 1.2, "Walk / Shuttle"),
    ("delhi_metro_central_sec", "delhi_imperial_hotel", 0.8, "Walk"),
    ("delhi_metro_qutub_minar", "delhi_qutub_minar", 0.9, "Feeder Bus / Walk"),

    # Delhi Metro inter-station connections
    ("delhi_metro_chandni_chowk", "delhi_metro_central_sec", 4.5, "Yellow Line"),
    ("delhi_metro_lal_quila", "delhi_metro_central_sec", 4.2, "Violet Line"),
    ("delhi_metro_chandni_chowk", "delhi_metro_lal_quila", 0.9, "Heritage Walkway"),
    ("delhi_metro_central_sec", "delhi_metro_qutub_minar", 12.0, "Yellow Line"),
    ("pune_pmc_metro", "pune_shaniwar_wada", 1.5, "Walk / Pune Metro"),
    ("chennai_egmore_metro", "chennai_government_museum", 0.5, "Walk"),
    ("chennai_egmore_metro", "chennai_marina", 5.0, "Blue Line / Bus"),
    ("hyderabad_charminar_metro", "hyderabad_charminar", 2.5, "Green Line / Bus"),
    ("hyderabad_charminar_metro", "hyderabad_salar_jung", 2.0, "Green Line / Walk"),
]

PRICE_TIERS = [
    {"id": "price_free", "name": "Free Entry", "tier": "Free", "max_inr": 0},
    {"id": "price_budget", "name": "Budget Friendly", "tier": "Budget", "max_inr": 1000},
    {"id": "price_moderate", "name": "Moderate Comfort", "tier": "Moderate", "max_inr": 5000},
    {"id": "price_luxury", "name": "Luxury & Heritage", "tier": "Luxury", "max_inr": 50000},
]


def escape_cypher_str(val):
    if not isinstance(val, str):
        return str(val)
    return val.replace("'", "\\'")


def generate_cypher_seed_script():
    """Generates pure Cypher statements to seed a Neo4j database."""
    statements = []
    statements.append("// ===============================================")
    statements.append("// Neo4j Seed Script: Tourist Guide Knowledge Graph")
    statements.append("// Discrete Mathematics Project")
    statements.append("// ===============================================\n")
    statements.append("// 1. Clear existing database graph")
    statements.append("MATCH (n) DETACH DELETE n;\n")

    statements.append("// 2. Create Constraints & Indexes")
    statements.append("CREATE CONSTRAINT place_id IF NOT EXISTS FOR (p:Place) REQUIRE p.id IS UNIQUE;")
    statements.append("CREATE CONSTRAINT city_id IF NOT EXISTS FOR (c:City) REQUIRE c.id IS UNIQUE;")
    statements.append("CREATE CONSTRAINT tier_id IF NOT EXISTS FOR (t:PriceTier) REQUIRE t.id IS UNIQUE;\n")

    # Create Cities
    statements.append("// 3. Create City Nodes")
    for city in CITIES:
        desc = escape_cypher_str(city['description'])
        stmt = (
            f"CREATE (:City {{id: '{city['id']}', name: '{city['name']}', "
            f"state: '{city['state']}', country: '{city['country']}', "
            f"description: '{desc}'}});"
        )
        statements.append(stmt)
    statements.append("")

    # Create Price Tier nodes
    statements.append("// 4. Create Price Tier Nodes")
    for pt in PRICE_TIERS:
        stmt = f"CREATE (:PriceTier {{id: '{pt['id']}', name: '{pt['name']}', tier: '{pt['tier']}', max_inr: {pt['max_inr']}}});"
        statements.append(stmt)
    statements.append("")

    # Create Places
    statements.append("// 5. Create Place Nodes (Monument, Museum, Restaurant, Hotel, MetroStation)")
    for p in PLACES:
        labels = f":Place:{p['category']}"
        name = escape_cypher_str(p['name'])
        area = escape_cypher_str(p['area'])
        desc = escape_cypher_str(p.get('description', ''))
        tier = escape_cypher_str(p.get('price_tier', 'Moderate'))
        props = [
            f"id: '{p['id']}'",
            f"name: '{name}'",
            f"category: '{p['category']}'",
            f"city: '{p['city']}'",
            f"area: '{area}'",
            f"rating: {p.get('rating', 4.0)}",
            f"description: '{desc}'",
            f"price_tier: '{tier}'"
        ]
        if "price_inr" in p:
            props.append(f"price_inr: {p['price_inr']}")
        if "entry_fee" in p:
            props.append(f"entry_fee: {p['entry_fee']}")
        if "cuisine" in p:
            props.append(f"cuisine: '{escape_cypher_str(p['cuisine'])}'")
        if "stars" in p:
            props.append(f"stars: {p['stars']}")
        if "is_unesco" in p:
            props.append(f"is_unesco: {str(p['is_unesco']).lower()}")
        if "line" in p:
            props.append(f"line: '{escape_cypher_str(p['line'])}'")

        stmt = f"CREATE ({labels} {{{', '.join(props)}}});"
        statements.append(stmt)
    statements.append("")

    # LOCATED_IN relationships
    statements.append("// 6. Create LOCATED_IN Relations (Place -> City)")
    for p in PLACES:
        city_id = next(city["id"] for city in CITIES if city["name"] == p["city"])
        stmt = f"MATCH (p:Place {{id: '{p['id']}'}}), (c:City {{id: '{city_id}'}}) CREATE (p)-[:LOCATED_IN]->(c);"
        statements.append(stmt)
    statements.append("")

    # HAS_PRICE relationships
    statements.append("// 7. Create HAS_PRICE Relations (Place -> PriceTier)")
    for p in PLACES:
        tier = p.get("price_tier", "Moderate").lower()
        tier_id = f"price_{tier}" if f"price_{tier}" in ["price_free", "price_budget", "price_moderate", "price_luxury"] else "price_moderate"
        price_val = p.get("price_inr", p.get("entry_fee", 0))
        stmt = f"MATCH (p:Place {{id: '{p['id']}'}}), (t:PriceTier {{id: '{tier_id}'}}) CREATE (p)-[:HAS_PRICE {{amount_inr: {price_val}, tier: '{p.get('price_tier', 'Moderate')}'}}]->(t);"
        statements.append(stmt)
    statements.append("")

    # NEAR relationships
    statements.append("// 8. Create NEAR Relations (Symmetric Binary Relation)")
    for src, dst, dist in NEAR_RELATIONSHIPS:
        stmt = (
            f"MATCH (a:Place {{id: '{src}'}}), (b:Place {{id: '{dst}'}}) "
            f"CREATE (a)-[:NEAR {{distance_km: {dist}}}]->(b), "
            f"(b)-[:NEAR {{distance_km: {dist}}}]->(a);"
        )
        statements.append(stmt)
    statements.append("")

    # CONNECTED_TO relationships
    statements.append("// 9. Create CONNECTED_TO Relations (Transit and Navigation Routes)")
    for item in CONNECTED_TO_RELATIONSHIPS:
        src, dst, dist, mode = item
        stmt = (
            f"MATCH (a:Place {{id: '{src}'}}), (b:Place {{id: '{dst}'}}) "
            f"CREATE (a)-[:CONNECTED_TO {{distance_km: {dist}, mode: '{mode}'}}]->(b), "
            f"(b)-[:CONNECTED_TO {{distance_km: {dist}, mode: '{mode}'}}]->(a);"
        )
        statements.append(stmt)
    statements.append("")

    return "\n".join(statements)
