"""
Sample Knowledge Graph Data for 5 Major Indian Cities:
1. Mumbai
2. Delhi
3. Pune
4. Chennai
5. Hyderabad

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
        "description": "Oxford of the East, historic capital of the Maratha Empire, cultural and IT hub of Maharashtra.",
        "type": "City"
    },
    {
        "id": "city_chennai",
        "name": "Chennai",
        "state": "Tamil Nadu",
        "country": "India",
        "description": "Gateway to South India, famed for Dravidian temple architecture, classical Carnatic music, and Marina Beach.",
        "type": "City"
    },
    {
        "id": "city_hyderabad",
        "name": "Hyderabad",
        "state": "Telangana",
        "country": "India",
        "description": "City of Pearls and Nizams, celebrated for Charminar, Golconda Fort, aromatic biryani, and HITEC City.",
        "type": "City"
    }
]

PLACES = [
    # =========================================================================
    # 1. MUMBAI PLACES
    # =========================================================================
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
        "description": "UNESCO World Heritage site with collection of cave temples predominantly dedicated to Shiva.",
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
        "description": "Opulent seaside lounge in Taj Mahal Palace famed for afternoon teas and harbour views."
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
        "description": "Historic cafe established in 1871, popular among international tourists."
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
    # Metro Stations
    {
        "id": "mumbai_metro_csmt",
        "name": "CSMT Metro Station",
        "city": "Mumbai",
        "category": "MetroStation",
        "area": "Fort",
        "rating": 4.5,
        "line": "Aqua Line 3 / Central Railway",
        "price_tier": "Transit",
        "description": "Major multimodal transit hub connecting suburban rail and underground Aqua Line."
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
        "description": "Southern terminus of Western suburban network and key junction near Marine Drive."
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

    # =========================================================================
    # 2. DELHI PLACES
    # =========================================================================
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
        "description": "Legendary historic restaurant established in 1913 near Jama Masjid and Red Fort."
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
        "description": "Iconic dining establishment on Pandara Road near India Gate, famous for butter chicken."
    },
    # Metro Stations
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
        "description": "Major station connecting Delhi's bustling markets and Old Delhi monuments."
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

    # =========================================================================
    # 3. PUNE PLACES
    # =========================================================================
    # Monuments
    {
        "id": "pune_shaniwar_wada",
        "name": "Shaniwar Wada",
        "city": "Pune",
        "category": "Monument",
        "area": "Shaniwar Peth",
        "rating": 4.5,
        "entry_fee": 25,
        "description": "Historic 18th-century fortified palace of the Peshwa rulers, celebrated for its massive Delhi Gate.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    {
        "id": "pune_aga_khan_palace",
        "name": "Aga Khan Palace",
        "city": "Pune",
        "category": "Monument",
        "area": "Yerwada",
        "rating": 4.6,
        "entry_fee": 25,
        "description": "Historic palace built in 1892 where Mahatma Gandhi and Kasturba Gandhi were interned during Quit India.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    {
        "id": "pune_sinhagad_fort",
        "name": "Sinhagad Fort",
        "city": "Pune",
        "category": "Monument",
        "area": "Sinhagad",
        "rating": 4.6,
        "entry_fee": 50,
        "description": "Hill fortress perched on a cliff in the Sahyadri mountains, famous for the battle led by Tanaji Malusare.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    # Museums
    {
        "id": "pune_kelkar_museum",
        "name": "Raja Dinkar Kelkar Museum",
        "city": "Pune",
        "category": "Museum",
        "area": "Shukrawar Peth",
        "rating": 4.7,
        "entry_fee": 100,
        "description": "Spectacular museum housing over 20,000 priceless Indian artifacts, musical instruments, and sculptures.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    {
        "id": "pune_tribal_museum",
        "name": "Tribal Cultural Museum",
        "city": "Pune",
        "category": "Museum",
        "area": "Koregaon Park / Bund Garden",
        "rating": 4.5,
        "entry_fee": 20,
        "description": "Museum preserving and exhibiting indigenous heritage, masks, and weapons of Maharashtra tribes.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    # Hotels
    {
        "id": "pune_ritz_carlton",
        "name": "The Ritz-Carlton Pune",
        "city": "Pune",
        "category": "Hotel",
        "area": "Yerwada",
        "rating": 4.9,
        "price_inr": 19000,
        "price_tier": "Luxury",
        "stars": 5,
        "description": "Opulent luxury hotel offering golf course views, fine dining, and close proximity to Aga Khan Palace."
    },
    {
        "id": "pune_hotel_shreyas",
        "name": "Hotel Shreyas",
        "city": "Pune",
        "category": "Hotel",
        "area": "Deccan Gymkhana",
        "rating": 4.3,
        "price_inr": 2600,
        "price_tier": "Budget",
        "stars": 3,
        "description": "Classic Maharashtrian hospitality hotel famous for traditional vegetarian dining and central location."
    },
    {
        "id": "pune_marriott_sb_road",
        "name": "JW Marriott Hotel Pune",
        "city": "Pune",
        "category": "Hotel",
        "area": "Senapati Bapat Road",
        "rating": 4.8,
        "price_inr": 14500,
        "price_tier": "Luxury",
        "stars": 5,
        "description": "Premier five-star hotel with rooftop cocktail lounge, tranquil spa, and upscale shopping pavilion."
    },
    # Restaurants
    {
        "id": "pune_vaishali",
        "name": "Vaishali Restaurant",
        "city": "Pune",
        "category": "Restaurant",
        "area": "FC Road",
        "rating": 4.7,
        "cuisine": "South Indian, Dosas & Filter Coffee",
        "price_inr": 350,
        "price_tier": "Budget",
        "description": "Cult classic cafe on Fergusson College Road loved for Mysore Masala Dosa and filter coffee."
    },
    {
        "id": "pune_kayani_bakery",
        "name": "Kayani Bakery",
        "city": "Pune",
        "category": "Restaurant",
        "area": "Camp",
        "rating": 4.6,
        "cuisine": "Parsi Bakery & Shrewsbury Biscuits",
        "price_inr": 400,
        "price_tier": "Budget",
        "description": "Historic bakery founded in 1955, world-renowned for melt-in-mouth Shrewsbury butter biscuits."
    },
    {
        "id": "pune_german_bakery",
        "name": "German Bakery",
        "city": "Pune",
        "category": "Restaurant",
        "area": "Koregaon Park",
        "rating": 4.4,
        "cuisine": "Continental, Bakes & Coffee",
        "price_inr": 850,
        "price_tier": "Moderate",
        "description": "Iconic bohemian cafe in Koregaon Park famous for cheesecakes and relaxed traveler ambiance."
    },
    {
        "id": "pune_shabree",
        "name": "Shabree Restaurant",
        "city": "Pune",
        "category": "Restaurant",
        "area": "FC Road",
        "rating": 4.5,
        "cuisine": "Authentic Maharashtrian Thali",
        "price_inr": 650,
        "price_tier": "Budget",
        "description": "Beloved traditional restaurant serving unlimited Maharashtrian thalis with Puran Poli and Pitla Bhakri."
    },
    # Metro Stations
    {
        "id": "pune_metro_civil_court",
        "name": "Civil Court Metro Station",
        "city": "Pune",
        "category": "MetroStation",
        "area": "Shivajinagar",
        "rating": 4.6,
        "line": "Purple & Aqua Line Interchange",
        "price_tier": "Transit",
        "description": "Major underground & elevated junction connecting Pune Metro's Purple and Aqua Lines."
    },
    {
        "id": "pune_metro_deccan",
        "name": "Deccan Gymkhana Metro Station",
        "city": "Pune",
        "category": "MetroStation",
        "area": "Deccan / FC Road",
        "rating": 4.5,
        "line": "Aqua Line",
        "price_tier": "Transit",
        "description": "Elevated metro station serving Fergusson College Road dining, colleges, and commercial zones."
    },
    {
        "id": "pune_metro_pune_station",
        "name": "Pune Railway Station Metro",
        "city": "Pune",
        "category": "MetroStation",
        "area": "Pune Station",
        "rating": 4.4,
        "line": "Purple Line",
        "price_tier": "Transit",
        "description": "Key multimodal terminal integrating Indian Railways mainline trains with Pune Metro."
    },

    # =========================================================================
    # 4. CHENNAI PLACES
    # =========================================================================
    # Monuments
    {
        "id": "chennai_marina_beach",
        "name": "Marina Beach",
        "city": "Chennai",
        "category": "Monument",
        "area": "Triplicane",
        "rating": 4.7,
        "entry_fee": 0,
        "description": "World's second-longest natural urban beach, stretching along the Bay of Bengal with historic memorials.",
        "is_unesco": False,
        "price_tier": "Free"
    },
    {
        "id": "chennai_kapaleeshwarar",
        "name": "Kapaleeshwarar Temple",
        "city": "Chennai",
        "category": "Monument",
        "area": "Mylapore",
        "rating": 4.8,
        "entry_fee": 0,
        "description": "7th-century Dravidian architectural masterpiece dedicated to Lord Shiva with towering rainbow gopuram.",
        "is_unesco": False,
        "price_tier": "Free"
    },
    {
        "id": "chennai_fort_st_george",
        "name": "Fort St. George",
        "city": "Chennai",
        "category": "Monument",
        "area": "George Town",
        "rating": 4.5,
        "entry_fee": 25,
        "description": "First British fortress in India built in 1644, now home to the Fort Museum and state administration.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    {
        "id": "chennai_san_thome",
        "name": "San Thome Cathedral Basilica",
        "city": "Chennai",
        "category": "Monument",
        "area": "Santhome",
        "rating": 4.6,
        "entry_fee": 0,
        "description": "Neo-Gothic Roman Catholic minor basilica built over the tomb of St. Thomas the Apostle.",
        "is_unesco": False,
        "price_tier": "Free"
    },
    # Museums
    {
        "id": "chennai_govt_museum",
        "name": "Government Museum Chennai",
        "city": "Chennai",
        "category": "Museum",
        "area": "Egmore",
        "rating": 4.7,
        "entry_fee": 50,
        "description": "Second-oldest museum in India established in 1851, housing world-famous Chola bronzes including Nataraja.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    {
        "id": "chennai_fort_museum",
        "name": "Fort St. George Museum",
        "city": "Chennai",
        "category": "Museum",
        "area": "George Town",
        "rating": 4.5,
        "entry_fee": 25,
        "description": "Colonial-era museum exhibiting British Raj uniforms, manuscripts, silver coins, and battlefield cannons.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    # Hotels
    {
        "id": "chennai_taj_coromandel",
        "name": "Taj Coromandel",
        "city": "Chennai",
        "category": "Hotel",
        "area": "Nungambakkam",
        "rating": 4.9,
        "price_inr": 16000,
        "price_tier": "Luxury",
        "stars": 5,
        "description": "Legendary luxury hotel blending rich South Indian design with international hospitality and fine dining."
    },
    {
        "id": "chennai_hotel_savera",
        "name": "Savera Hotel",
        "city": "Chennai",
        "category": "Hotel",
        "area": "Mylapore",
        "rating": 4.4,
        "price_inr": 4200,
        "price_tier": "Moderate",
        "stars": 4,
        "description": "Contemporary hotel situated close to Kapaleeshwarar Temple, music sabhas, and shopping streets."
    },
    {
        "id": "chennai_grand_chennai",
        "name": "Grand Chennai by GRT Hotels",
        "city": "Chennai",
        "category": "Hotel",
        "area": "T. Nagar",
        "rating": 4.6,
        "price_inr": 6800,
        "price_tier": "Moderate",
        "stars": 4,
        "description": "Modern upscale hotel situated in the heart of T. Nagar shopping hub with chic multi-cuisine diners."
    },
    {
        "id": "chennai_broad_lands",
        "name": "Broad Lands Hotel",
        "city": "Chennai",
        "category": "Hotel",
        "area": "Triplicane",
        "rating": 4.1,
        "price_inr": 1500,
        "price_tier": "Budget",
        "stars": 2,
        "description": "Heritage courtyard lodge in Triplicane offering tranquil budget accommodations near Marina Beach."
    },
    # Restaurants
    {
        "id": "chennai_murugan_idli",
        "name": "Murugan Idli Shop",
        "city": "Chennai",
        "category": "Restaurant",
        "area": "T. Nagar",
        "rating": 4.6,
        "cuisine": "Traditional South Indian & Idlis",
        "price_inr": 300,
        "price_tier": "Budget",
        "description": "Iconic culinary stop celebrated for fluffy soft idlis, spicy podi ghee, and four signature chutneys."
    },
    {
        "id": "chennai_saravana_mylapore",
        "name": "Saravana Bhavan Mylapore",
        "city": "Chennai",
        "category": "Restaurant",
        "area": "Mylapore",
        "rating": 4.5,
        "cuisine": "Pure Vegetarian South Indian",
        "price_inr": 350,
        "price_tier": "Budget",
        "description": "Legendary vegetarian institution opposite Kapaleeshwarar temple serving rich thalis and crisp ghee roast."
    },
    {
        "id": "chennai_buhari",
        "name": "Buhari Hotel",
        "city": "Chennai",
        "category": "Restaurant",
        "area": "Anna Salai",
        "rating": 4.4,
        "cuisine": "Mughlai, Biryani & Chicken 65",
        "price_inr": 650,
        "price_tier": "Budget",
        "description": "Historic restaurant established in 1951, world-famous as the original creator of Chicken 65."
    },
    {
        "id": "chennai_dakshin",
        "name": "Dakshin Restaurant",
        "city": "Chennai",
        "category": "Restaurant",
        "area": "Alwarpet",
        "rating": 4.8,
        "cuisine": "Fine Dining South Indian Coastal",
        "price_inr": 3200,
        "price_tier": "Luxury",
        "description": "Acclaimed restaurant showcasing gourmet delicacies from Tamil Nadu, Kerala, Karnataka, and Andhra."
    },
    # Metro Stations
    {
        "id": "chennai_metro_central",
        "name": "Chennai Central Metro Station",
        "city": "Chennai",
        "category": "MetroStation",
        "area": "Park Town",
        "rating": 4.6,
        "line": "Blue & Green Line Interchange",
        "price_tier": "Transit",
        "description": "Massive underground transit hub linking intercity trains, suburban rail, and Chennai Metro."
    },
    {
        "id": "chennai_metro_high_court",
        "name": "High Court Metro Station",
        "city": "Chennai",
        "category": "MetroStation",
        "area": "George Town",
        "rating": 4.5,
        "line": "Blue Line",
        "price_tier": "Transit",
        "description": "Key station providing direct access to Madras High Court, Fort St. George, and Broadway."
    },
    {
        "id": "chennai_metro_lic",
        "name": "LIC Metro Station",
        "city": "Chennai",
        "category": "MetroStation",
        "area": "Anna Salai",
        "rating": 4.4,
        "line": "Blue Line",
        "price_tier": "Transit",
        "description": "Arterial station on Anna Salai providing swift connections to Triplicane and Marina Beach."
    },

    # =========================================================================
    # 5. HYDERABAD PLACES
    # =========================================================================
    # Monuments
    {
        "id": "hyd_charminar",
        "name": "Charminar",
        "city": "Hyderabad",
        "category": "Monument",
        "area": "Old City",
        "rating": 4.7,
        "entry_fee": 25,
        "description": "Magnificent 1591 monument with four soaring minarets, the timeless global symbol of Hyderabad.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    {
        "id": "hyd_golconda_fort",
        "name": "Golconda Fort",
        "city": "Hyderabad",
        "category": "Monument",
        "area": "Ibrahim Bagh",
        "rating": 4.7,
        "entry_fee": 25,
        "description": "Colossal medieval citadel and historic diamond trading seat, renowned for its acoustic engineering.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    {
        "id": "hyd_chowmahalla",
        "name": "Chowmahalla Palace",
        "city": "Hyderabad",
        "category": "Monument",
        "area": "Motigalli",
        "rating": 4.7,
        "entry_fee": 100,
        "description": "Exquisite palace complex of the Nizams of Hyderabad, boasting the Grand Khilwat Mubarak hall.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    {
        "id": "hyd_qutb_shahi_tombs",
        "name": "Qutb Shahi Tombs",
        "city": "Hyderabad",
        "category": "Monument",
        "area": "Ibrahim Bagh",
        "rating": 4.6,
        "entry_fee": 40,
        "description": "Splendid domed mausoleums set in landscaped gardens honoring the seven Qutb Shahi sultans.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    # Museums
    {
        "id": "hyd_salar_jung",
        "name": "Salar Jung Museum",
        "city": "Hyderabad",
        "category": "Museum",
        "area": "Darulshifa",
        "rating": 4.8,
        "entry_fee": 50,
        "description": "One of India's three National Museums, holding Nawab Salar Jung III's world art treasures and Veiled Rebecca.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    {
        "id": "hyd_nizams_museum",
        "name": "The Nizam's Museum",
        "city": "Hyderabad",
        "category": "Museum",
        "area": "Purani Haveli",
        "rating": 4.5,
        "entry_fee": 100,
        "description": "Houses gold tiffin boxes, diamond-studded daggers, and personal mementos of the Seventh Nizam.",
        "is_unesco": False,
        "price_tier": "Budget"
    },
    # Hotels
    {
        "id": "hyd_falaknuma_palace",
        "name": "Taj Falaknuma Palace",
        "city": "Hyderabad",
        "category": "Hotel",
        "area": "Falaknuma",
        "rating": 4.9,
        "price_inr": 38000,
        "price_tier": "Luxury",
        "stars": 5,
        "description": "Grand hilltop palace hotel offering royal Nizam suite experiences, horse carriages, and heritage dinners."
    },
    {
        "id": "hyd_the_park",
        "name": "The Park Hyderabad",
        "city": "Hyderabad",
        "category": "Hotel",
        "area": "Somajiguda",
        "rating": 4.6,
        "price_inr": 8200,
        "price_tier": "Moderate",
        "stars": 5,
        "description": "Boutique luxury hotel with glistening jeweled facade overlooking the scenic Hussain Sagar Lake."
    },
    {
        "id": "hyd_hotel_shadab_inn",
        "name": "Hotel Shadab Lodge",
        "city": "Hyderabad",
        "category": "Hotel",
        "area": "Ghansi Bazaar",
        "rating": 4.1,
        "price_inr": 1600,
        "price_tier": "Budget",
        "stars": 2,
        "description": "Convenient budget hotel located right in the vibrant heritage shopping district of Charminar."
    },
    {
        "id": "hyd_marigold",
        "name": "Marigold Hotel",
        "city": "Hyderabad",
        "category": "Hotel",
        "area": "Begumpet",
        "rating": 4.5,
        "price_inr": 5200,
        "price_tier": "Moderate",
        "stars": 4,
        "description": "Elegant business & tourist hotel featuring contemporary rooms, swimming pool, and central metro access."
    },
    # Restaurants
    {
        "id": "hyd_paradise_biryani",
        "name": "Paradise Biryani",
        "city": "Hyderabad",
        "category": "Restaurant",
        "area": "Secunderabad",
        "rating": 4.6,
        "cuisine": "World-Famous Hyderabadi Dum Biryani",
        "price_inr": 650,
        "price_tier": "Budget",
        "description": "Legendary institution founded in 1953, celebrated globally for fragrant saffron dum biryani."
    },
    {
        "id": "hyd_shadab_restaurant",
        "name": "Hotel Shadab",
        "city": "Hyderabad",
        "category": "Restaurant",
        "area": "Charminar (Madina)",
        "rating": 4.6,
        "cuisine": "Hyderabadi Mughlai, Biryani & Haleem",
        "price_inr": 500,
        "price_tier": "Budget",
        "description": "Cult foodie hotspot near Charminar famous for aromatic mutton biryani, paya, and Zafrani tea."
    },
    {
        "id": "hyd_bawarchi",
        "name": "Bawarchi Restaurant",
        "city": "Hyderabad",
        "category": "Restaurant",
        "area": "RTC X Roads",
        "rating": 4.5,
        "cuisine": "Authentic Hyderabadi Biryani & Kebabs",
        "price_inr": 550,
        "price_tier": "Budget",
        "description": "Hugely popular restaurant praised for massive, flavour-packed portions of spicy chicken and mutton biryani."
    },
    {
        "id": "hyd_chutneys",
        "name": "Chutneys",
        "city": "Hyderabad",
        "category": "Restaurant",
        "area": "Banjara Hills",
        "rating": 4.5,
        "cuisine": "South Indian Vegetarian & Steamed Dosa",
        "price_inr": 450,
        "price_tier": "Budget",
        "description": "Renowned South Indian chain famous for Guntur Steamed Dosa served with six varieties of flavorful chutneys."
    },
    # Metro Stations
    {
        "id": "hyd_metro_mgbs",
        "name": "MGBS Metro Interchange",
        "city": "Hyderabad",
        "category": "MetroStation",
        "area": "Imlibun",
        "rating": 4.7,
        "line": "Red & Green Line Interchange",
        "price_tier": "Transit",
        "description": "Major multimodal transit hub beside Salar Jung Museum and Mahatma Gandhi Bus Station."
    },
    {
        "id": "hyd_metro_charminar",
        "name": "Charminar Metro Station",
        "city": "Hyderabad",
        "category": "MetroStation",
        "area": "Sultan Bazaar",
        "rating": 4.5,
        "line": "Green Line",
        "price_tier": "Transit",
        "description": "Underground metro station providing swift transit access to Charminar and Old City markets."
    },
    {
        "id": "hyd_metro_hitec",
        "name": "HITEC City Metro Station",
        "city": "Hyderabad",
        "category": "MetroStation",
        "area": "Madhapur",
        "rating": 4.6,
        "line": "Blue Line",
        "price_tier": "Transit",
        "description": "Terminal metro station connecting the heritage city to Hyderabad's modern IT and financial district."
    }
]

# =============================================================================
# RELATIONSHIPS
# =============================================================================

NEAR_RELATIONSHIPS = [
    # --- Mumbai: Gateway Cluster ---
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

    # --- Mumbai: Marine Drive Cluster ---
    ("mumbai_marine_drive", "mumbai_oberoi", 0.5),
    ("mumbai_marine_drive", "mumbai_sea_green_hotel", 0.3),
    ("mumbai_marine_drive", "mumbai_pizza_by_bay", 0.2),
    ("mumbai_csmt", "mumbai_csmvs_museum", 1.2),
    ("mumbai_marine_drive", "mumbai_csmt", 2.2),

    # --- Delhi: Red Fort Cluster ---
    ("delhi_red_fort", "delhi_hotel_tara_palace", 0.5),
    ("delhi_red_fort", "delhi_karims", 0.6),
    ("delhi_red_fort", "delhi_jama_masjid", 0.7),
    ("delhi_red_fort", "delhi_haveli_dharampura", 0.8),
    ("delhi_jama_masjid", "delhi_karims", 0.2),
    ("delhi_jama_masjid", "delhi_haveli_dharampura", 0.4),

    # --- Delhi: Central Secretariat & India Gate Cluster ---
    ("delhi_india_gate", "delhi_ngma", 0.3),
    ("delhi_india_gate", "delhi_gulati", 0.9),
    ("delhi_national_museum", "delhi_imperial_hotel", 1.1),
    ("delhi_imperial_hotel", "delhi_saravana_bhavan", 0.7),
    ("delhi_india_gate", "delhi_national_museum", 1.4),

    # --- Pune: Shaniwar Wada & Deccan Cluster ---
    ("pune_shaniwar_wada", "pune_kelkar_museum", 0.9),
    ("pune_shaniwar_wada", "pune_hotel_shreyas", 1.8),
    ("pune_shaniwar_wada", "pune_vaishali", 2.1),
    ("pune_vaishali", "pune_shabree", 0.1),
    ("pune_vaishali", "pune_hotel_shreyas", 1.2),
    ("pune_hotel_shreyas", "pune_kelkar_museum", 1.4),

    # --- Pune: Yerwada & Koregaon Park Cluster ---
    ("pune_aga_khan_palace", "pune_ritz_carlton", 0.8),
    ("pune_aga_khan_palace", "pune_german_bakery", 2.4),
    ("pune_aga_khan_palace", "pune_tribal_museum", 2.2),
    ("pune_tribal_museum", "pune_german_bakery", 1.5),
    ("pune_german_bakery", "pune_kayani_bakery", 2.5),
    ("pune_marriott_sb_road", "pune_vaishali", 1.8),

    # --- Chennai: Marina Beach & Triplicane Cluster ---
    ("chennai_marina_beach", "chennai_broad_lands", 0.9),
    ("chennai_marina_beach", "chennai_san_thome", 1.2),
    ("chennai_marina_beach", "chennai_buhari", 1.8),
    ("chennai_marina_beach", "chennai_fort_st_george", 2.5),
    ("chennai_san_thome", "chennai_kapaleeshwarar", 1.5),

    # --- Chennai: Mylapore & T. Nagar Cluster ---
    ("chennai_kapaleeshwarar", "chennai_saravana_mylapore", 0.1),
    ("chennai_kapaleeshwarar", "chennai_hotel_savera", 1.4),
    ("chennai_hotel_savera", "chennai_dakshin", 0.9),
    ("chennai_murugan_idli", "chennai_grand_chennai", 0.6),
    ("chennai_taj_coromandel", "chennai_govt_museum", 1.6),
    ("chennai_fort_st_george", "chennai_fort_museum", 0.1),

    # --- Hyderabad: Charminar & Old City Cluster ---
    ("hyd_charminar", "hyd_hotel_shadab_inn", 0.4),
    ("hyd_charminar", "hyd_shadab_restaurant", 0.5),
    ("hyd_charminar", "hyd_chowmahalla", 0.9),
    ("hyd_charminar", "hyd_salar_jung", 1.4),
    ("hyd_charminar", "hyd_nizams_museum", 1.6),
    ("hyd_chowmahalla", "hyd_hotel_shadab_inn", 0.6),
    ("hyd_chowmahalla", "hyd_shadab_restaurant", 0.7),
    ("hyd_salar_jung", "hyd_nizams_museum", 0.9),
    ("hyd_salar_jung", "hyd_shadab_restaurant", 1.1),
    ("hyd_falaknuma_palace", "hyd_charminar", 4.2),

    # --- Hyderabad: Golconda & Banjara Hills Cluster ---
    ("hyd_golconda_fort", "hyd_qutb_shahi_tombs", 1.2),
    ("hyd_the_park", "hyd_chutneys", 1.5),
    ("hyd_the_park", "hyd_marigold", 2.1),
    ("hyd_paradise_biryani", "hyd_marigold", 2.8),
    ("hyd_bawarchi", "hyd_chutneys", 3.2),
]

CONNECTED_TO_RELATIONSHIPS = [
    # --- Mumbai Transit Routes ---
    ("mumbai_metro_colaba", "mumbai_gateway", 1.1, "Walk / Shuttle"),
    ("mumbai_metro_colaba", "mumbai_taj_hotel", 1.0, "Walk"),
    ("mumbai_metro_churchgate", "mumbai_marine_drive", 0.6, "Walk"),
    ("mumbai_metro_churchgate", "mumbai_csmvs_museum", 0.9, "Walk"),
    ("mumbai_metro_csmt", "mumbai_csmt", 0.1, "Direct Entry"),
    ("mumbai_metro_csmt", "mumbai_csmvs_museum", 1.1, "Taxi / Walk"),
    ("mumbai_metro_colaba", "mumbai_metro_churchgate", 2.4, "Aqua Line 3"),
    ("mumbai_metro_churchgate", "mumbai_metro_csmt", 1.8, "Suburban Rail / Bus"),
    ("mumbai_gateway", "mumbai_elephanta", 10.0, "Ferry Boat"),

    # --- Delhi Transit Routes ---
    ("delhi_metro_lal_quila", "delhi_red_fort", 0.2, "Walk (Gate 1)"),
    ("delhi_metro_chandni_chowk", "delhi_red_fort", 0.7, "Walk / E-Rickshaw"),
    ("delhi_metro_chandni_chowk", "delhi_jama_masjid", 0.8, "Walk / E-Rickshaw"),
    ("delhi_metro_chandni_chowk", "delhi_hotel_tara_palace", 0.5, "Walk"),
    ("delhi_metro_central_sec", "delhi_national_museum", 0.6, "Walk"),
    ("delhi_metro_central_sec", "delhi_india_gate", 1.2, "Walk / Shuttle"),
    ("delhi_metro_central_sec", "delhi_imperial_hotel", 0.8, "Walk"),
    ("delhi_metro_chandni_chowk", "delhi_metro_central_sec", 4.5, "Yellow Line"),
    ("delhi_metro_lal_quila", "delhi_metro_central_sec", 4.2, "Violet Line"),

    # --- Pune Transit Routes ---
    ("pune_metro_civil_court", "pune_shaniwar_wada", 1.1, "Walk / Auto"),
    ("pune_metro_civil_court", "pune_kelkar_museum", 1.4, "Auto / Walk"),
    ("pune_metro_deccan", "pune_vaishali", 0.5, "Walk (FC Road)"),
    ("pune_metro_deccan", "pune_shabree", 0.6, "Walk"),
    ("pune_metro_deccan", "pune_hotel_shreyas", 0.8, "Walk"),
    ("pune_metro_pune_station", "pune_kayani_bakery", 1.5, "Auto / Walk"),
    ("pune_metro_pune_station", "pune_metro_civil_court", 1.9, "Purple Line"),
    ("pune_metro_civil_court", "pune_metro_deccan", 2.3, "Aqua Line"),

    # --- Chennai Transit Routes ---
    ("chennai_metro_high_court", "chennai_fort_st_george", 0.8, "Walk"),
    ("chennai_metro_high_court", "chennai_fort_museum", 0.9, "Walk"),
    ("chennai_metro_lic", "chennai_marina_beach", 1.4, "Walk / Auto"),
    ("chennai_metro_lic", "chennai_buhari", 0.4, "Walk"),
    ("chennai_metro_central", "chennai_govt_museum", 1.8, "Walk / Shuttle"),
    ("chennai_metro_central", "chennai_metro_high_court", 2.1, "Blue Line"),
    ("chennai_metro_central", "chennai_metro_lic", 2.7, "Blue Line"),

    # --- Hyderabad Transit Routes ---
    ("hyd_metro_charminar", "hyd_charminar", 1.1, "Walk / E-Rickshaw"),
    ("hyd_metro_charminar", "hyd_shadab_restaurant", 0.8, "Walk"),
    ("hyd_metro_charminar", "hyd_hotel_shadab_inn", 0.9, "Walk"),
    ("hyd_metro_mgbs", "hyd_salar_jung", 0.6, "Walk (Bridge)"),
    ("hyd_metro_mgbs", "hyd_nizams_museum", 1.1, "Walk / Auto"),
    ("hyd_metro_mgbs", "hyd_metro_charminar", 1.8, "Green Line"),
    ("hyd_metro_mgbs", "hyd_metro_hitec", 16.5, "Red Line to Ameerpet, Blue Line"),
    ("hyd_metro_hitec", "hyd_the_park", 7.5, "Blue Line"),
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
    """Generates pure Cypher statements to seed a Neo4j database for all 5 cities."""
    statements = []
    statements.append("// ===============================================")
    statements.append("// Neo4j Seed Script: Tourist Guide Knowledge Graph")
    statements.append("// 5 Cities: Mumbai, Delhi, Pune, Chennai, Hyderabad")
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
    statements.append("// 5. Create Place Nodes")
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
    city_map = {
        "Mumbai": "city_mumbai",
        "Delhi": "city_delhi",
        "Pune": "city_pune",
        "Chennai": "city_chennai",
        "Hyderabad": "city_hyderabad"
    }
    statements.append("// 6. Create LOCATED_IN Relations (Place -> City)")
    for p in PLACES:
        city_id = city_map.get(p["city"], "city_mumbai")
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
