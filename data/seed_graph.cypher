// ===============================================
// Neo4j Seed Script: Tourist Guide Knowledge Graph
// Discrete Mathematics Project
// ===============================================

// 1. Clear existing database graph
MATCH (n) DETACH DELETE n;

// 2. Create Constraints & Indexes
CREATE CONSTRAINT place_id IF NOT EXISTS FOR (p:Place) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT city_id IF NOT EXISTS FOR (c:City) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT tier_id IF NOT EXISTS FOR (t:PriceTier) REQUIRE t.id IS UNIQUE;

// 3. Create City Nodes
CREATE (:City {id: 'city_mumbai', name: 'Mumbai', state: 'Maharashtra', country: 'India', description: 'Financial capital of India, known for colonial architecture, seaside promenades, and Bollywood.'});
CREATE (:City {id: 'city_delhi', name: 'Delhi', state: 'Delhi NCR', country: 'India', description: 'Historical capital of India, home to Mughal monuments, ancient heritage, and vibrant bazaars.'});

// 4. Create Price Tier Nodes
CREATE (:PriceTier {id: 'price_free', name: 'Free Entry', tier: 'Free', max_inr: 0});
CREATE (:PriceTier {id: 'price_budget', name: 'Budget Friendly', tier: 'Budget', max_inr: 1000});
CREATE (:PriceTier {id: 'price_moderate', name: 'Moderate Comfort', tier: 'Moderate', max_inr: 5000});
CREATE (:PriceTier {id: 'price_luxury', name: 'Luxury & Heritage', tier: 'Luxury', max_inr: 50000});

// 5. Create Place Nodes (Monument, Museum, Restaurant, Hotel, MetroStation)
CREATE (:Place:Monument {id: 'mumbai_gateway', name: 'Gateway of India', category: 'Monument', city: 'Mumbai', area: 'Colaba', rating: 4.7, description: 'Iconic arch monument built in the 20th century overlooking the Arabian Sea.', price_tier: 'Free', entry_fee: 0, is_unesco: false});
CREATE (:Place:Monument {id: 'mumbai_csmt', name: 'Chhatrapati Shivaji Maharaj Terminus', category: 'Monument', city: 'Mumbai', area: 'Fort', rating: 4.8, description: 'Historic railway terminus and UNESCO World Heritage Site with Victorian Gothic architecture.', price_tier: 'Free', entry_fee: 0, is_unesco: true});
CREATE (:Place:Monument {id: 'mumbai_marine_drive', name: 'Marine Drive', category: 'Monument', city: 'Mumbai', area: 'Marine Lines', rating: 4.8, description: '3.6 km long arc-shaped boulevard along the coast, famously known as the Queen\'s Necklace.', price_tier: 'Free', entry_fee: 0, is_unesco: false});
CREATE (:Place:Monument {id: 'mumbai_elephanta', name: 'Elephanta Caves', category: 'Monument', city: 'Mumbai', area: 'Gharapuri Island', rating: 4.5, description: 'UNESCO World Heritage site with collection of cave temples predominantly dedicated to Hindu god Shiva.', price_tier: 'Budget', entry_fee: 40, is_unesco: true});
CREATE (:Place:Museum {id: 'mumbai_csmvs_museum', name: 'CSMVS Museum', category: 'Museum', city: 'Mumbai', area: 'Fort', rating: 4.8, description: 'Premier art and history museum in Mumbai showcasing ancient Indian history and artwork.', price_tier: 'Budget', entry_fee: 150, is_unesco: false});
CREATE (:Place:Museum {id: 'mumbai_jehangir_art', name: 'Jehangir Art Gallery', category: 'Museum', city: 'Mumbai', area: 'Kala Ghoda', rating: 4.6, description: 'Famous contemporary art gallery in Kala Ghoda founded by Sir Cowasji Jehangir.', price_tier: 'Free', entry_fee: 0, is_unesco: false});
CREATE (:Place:Museum {id: 'mumbai_nehru_centre', name: 'Nehru Science Centre', category: 'Museum', city: 'Mumbai', area: 'Worli', rating: 4.6, description: 'India\'s largest interactive science centre with hundreds of hands-on science exhibits.', price_tier: 'Budget', entry_fee: 70, is_unesco: false});
CREATE (:Place:Hotel {id: 'mumbai_taj_hotel', name: 'The Taj Mahal Palace', category: 'Hotel', city: 'Mumbai', area: 'Colaba', rating: 4.9, description: 'Legendary five-star heritage hotel standing proudly opposite the Gateway of India.', price_tier: 'Luxury', price_inr: 24000, stars: 5});
CREATE (:Place:Hotel {id: 'mumbai_hotel_diplomat', name: 'Hotel Diplomat', category: 'Hotel', city: 'Mumbai', area: 'Colaba', rating: 4.2, description: 'Comfortable boutique hotel located just 300 meters from Gateway of India.', price_tier: 'Moderate', price_inr: 3800, stars: 3});
CREATE (:Place:Hotel {id: 'mumbai_sea_green_hotel', name: 'Sea Green Hotel', category: 'Hotel', city: 'Mumbai', area: 'Marine Drive', rating: 4.1, description: 'Historic sea-facing hotel situated right on Marine Drive.', price_tier: 'Moderate', price_inr: 3200, stars: 3});
CREATE (:Place:Hotel {id: 'mumbai_oberoi', name: 'The Oberoi Mumbai', category: 'Hotel', city: 'Mumbai', area: 'Nariman Point', rating: 4.8, description: 'Luxury hotel offering panoramic views of Marine Drive and Queen\'s Necklace.', price_tier: 'Luxury', price_inr: 21000, stars: 5});
CREATE (:Place:Hotel {id: 'mumbai_abode_colaba', name: 'Abode Bombay', category: 'Hotel', city: 'Mumbai', area: 'Colaba', rating: 4.6, description: 'Vintage luxury boutique hotel in Colaba within walking distance of the Gateway.', price_tier: 'Moderate', price_inr: 4500, stars: 3});
CREATE (:Place:Restaurant {id: 'mumbai_sea_lounge', name: 'Sea Lounge', category: 'Restaurant', city: 'Mumbai', area: 'Colaba', rating: 4.7, description: 'Opulent seaside lounge in Taj Mahal Palace famed for afternoon English teas and harbour views.', price_tier: 'Luxury', price_inr: 2800, cuisine: 'Continental & High Tea'});
CREATE (:Place:Restaurant {id: 'mumbai_bademiya', name: 'Bademiya', category: 'Restaurant', city: 'Mumbai', area: 'Colaba', rating: 4.3, description: 'Iconic late-night street food restaurant legendary for seekh kebabs and chicken baida roti.', price_tier: 'Budget', price_inr: 450, cuisine: 'Kebabs & Mughlai'});
CREATE (:Place:Restaurant {id: 'mumbai_leopold', name: 'Leopold Cafe', category: 'Restaurant', city: 'Mumbai', area: 'Colaba', rating: 4.4, description: 'Historic cafe established in 1871, popular among international tourists and backpackers.', price_tier: 'Moderate', price_inr: 900, cuisine: 'Cafe, Continental & Beer'});
CREATE (:Place:Restaurant {id: 'mumbai_pizza_by_bay', name: 'Pizza By The Bay', category: 'Restaurant', city: 'Mumbai', area: 'Marine Drive', rating: 4.5, description: 'Art-deco waterfront restaurant serving gourmet pizzas with views of the Arabian sea.', price_tier: 'Moderate', price_inr: 1300, cuisine: 'Italian & Pizzeria'});
CREATE (:Place:Restaurant {id: 'mumbai_cafe_mondegar', name: 'Cafe Mondegar', category: 'Restaurant', city: 'Mumbai', area: 'Colaba', rating: 4.4, description: 'Vintage Irani cafe featuring famous murals painted by cartoonist Mario Miranda.', price_tier: 'Budget', price_inr: 750, cuisine: 'Continental, Parsi & Draught Beer'});
CREATE (:Place:MetroStation {id: 'mumbai_metro_csmt', name: 'CSMT Metro Station', category: 'MetroStation', city: 'Mumbai', area: 'Fort', rating: 4.5, description: 'Major multimodal transit hub connecting suburban rail and upcoming underground Aqua Line.', price_tier: 'Transit', line: 'Aqua Line 3 / Central Railway'});
CREATE (:Place:MetroStation {id: 'mumbai_metro_churchgate', name: 'Churchgate Station', category: 'MetroStation', city: 'Mumbai', area: 'Churchgate', rating: 4.4, description: 'Southern terminus of the Western suburban rail network and key junction near Marine Drive.', price_tier: 'Transit', line: 'Western Railway / Aqua Line 3'});
CREATE (:Place:MetroStation {id: 'mumbai_metro_colaba', name: 'Colaba Metro Station', category: 'MetroStation', city: 'Mumbai', area: 'Colaba', rating: 4.6, description: 'Cuffe Parade & Colaba underground metro terminal serving South Mumbai tourist quarter.', price_tier: 'Transit', line: 'Aqua Line 3'});
CREATE (:Place:Monument {id: 'delhi_red_fort', name: 'Red Fort', category: 'Monument', city: 'Delhi', area: 'Old Delhi', rating: 4.6, description: 'Historic red sandstone fortress served as main residence of Mughal Emperors, UNESCO World Heritage.', price_tier: 'Budget', entry_fee: 50, is_unesco: true});
CREATE (:Place:Monument {id: 'delhi_jama_masjid', name: 'Jama Masjid', category: 'Monument', city: 'Delhi', area: 'Old Delhi', rating: 4.6, description: 'One of India\'s largest mosques built by Mughal Emperor Shah Jahan between 1650 and 1656.', price_tier: 'Free', entry_fee: 0, is_unesco: false});
CREATE (:Place:Monument {id: 'delhi_india_gate', name: 'India Gate', category: 'Monument', city: 'Delhi', area: 'Central Delhi', rating: 4.7, description: 'War memorial arch dedicated to soldiers of the British Indian Army who died in World War I.', price_tier: 'Free', entry_fee: 0, is_unesco: false});
CREATE (:Place:Monument {id: 'delhi_qutub_minar', name: 'Qutub Minar', category: 'Monument', city: 'Delhi', area: 'Mehrauli', rating: 4.7, description: '73-meter tall minaret of victory built in 1192, a UNESCO World Heritage site with intricate carvings.', price_tier: 'Budget', entry_fee: 50, is_unesco: true});
CREATE (:Place:Monument {id: 'delhi_humayuns_tomb', name: 'Humayun\'s Tomb', category: 'Monument', city: 'Delhi', area: 'Nizamuddin', rating: 4.7, description: 'First garden-tomb on the Indian subcontinent, precursor to the Taj Mahal and UNESCO Heritage Site.', price_tier: 'Budget', entry_fee: 50, is_unesco: true});
CREATE (:Place:Monument {id: 'delhi_lotus_temple', name: 'Lotus Temple', category: 'Monument', city: 'Delhi', area: 'Kalkaji', rating: 4.6, description: 'Bahá\'í House of Worship notable for its flower-like lotus shape and open prayer sanctuary.', price_tier: 'Free', entry_fee: 0, is_unesco: false});
CREATE (:Place:Museum {id: 'delhi_national_museum', name: 'National Museum', category: 'Museum', city: 'Delhi', area: 'Janpath', rating: 4.7, description: 'India\'s premier museum holding over 200,000 works of art covering 5,000 years of cultural heritage.', price_tier: 'Budget', entry_fee: 20, is_unesco: false});
CREATE (:Place:Museum {id: 'delhi_ngma', name: 'National Gallery of Modern Art', category: 'Museum', city: 'Delhi', area: 'India Gate Circle', rating: 4.6, description: 'Premier modern and contemporary Indian art museum housed in historic Jaipur House near India Gate.', price_tier: 'Budget', entry_fee: 20, is_unesco: false});
CREATE (:Place:Museum {id: 'delhi_crafts_museum', name: 'National Crafts Museum', category: 'Museum', city: 'Delhi', area: 'Pragati Maidan', rating: 4.6, description: 'Celebration of traditional Indian crafts, village architecture, handloom textiles, and living folk artists.', price_tier: 'Budget', entry_fee: 20, is_unesco: false});
CREATE (:Place:Hotel {id: 'delhi_haveli_dharampura', name: 'Haveli Dharampura', category: 'Hotel', city: 'Delhi', area: 'Chandni Chowk', rating: 4.6, description: 'Award-winning restored UNESCO heritage haveli nestled in the heart of Old Delhi near Red Fort.', price_tier: 'Luxury', price_inr: 8500, stars: 4});
CREATE (:Place:Hotel {id: 'delhi_hotel_tara_palace', name: 'Hotel Tara Palace', category: 'Hotel', city: 'Delhi', area: 'Chandni Chowk', rating: 4.2, description: 'Affordable budget hotel located just 500 meters from the Red Fort in Old Delhi.', price_tier: 'Budget', price_inr: 1800, stars: 3});
CREATE (:Place:Hotel {id: 'delhi_hotel_delhi_heart', name: 'Hotel City Star', category: 'Hotel', city: 'Delhi', area: 'Paharganj', rating: 4.1, description: 'Popular budget hotel with modern rooms near New Delhi Railway Station.', price_tier: 'Budget', price_inr: 2200, stars: 3});
CREATE (:Place:Hotel {id: 'delhi_imperial_hotel', name: 'The Imperial Hotel', category: 'Hotel', city: 'Delhi', area: 'Janpath', rating: 4.8, description: 'Grand historic 5-star hotel built in 1936 during the British Raj near Connaught Place.', price_tier: 'Luxury', price_inr: 18500, stars: 5});
CREATE (:Place:Hotel {id: 'delhi_le_meridien', name: 'Le Meridien New Delhi', category: 'Hotel', city: 'Delhi', area: 'Windsor Place', rating: 4.7, description: 'High-end contemporary hotel located within 2 km of India Gate and National Museum.', price_tier: 'Luxury', price_inr: 14000, stars: 5});
CREATE (:Place:Restaurant {id: 'delhi_karims', name: 'Karim\'s', category: 'Restaurant', city: 'Delhi', area: 'Old Delhi', rating: 4.5, description: 'Legendary historic restaurant established in 1913 near Jama Masjid and Red Fort, famous for mutton korma.', price_tier: 'Budget', price_inr: 600, cuisine: 'Royal Mughlai'});
CREATE (:Place:Restaurant {id: 'delhi_moti_mahal', name: 'Moti Mahal Delux', category: 'Restaurant', city: 'Delhi', area: 'Daryaganj', rating: 4.4, description: 'Birthplace of the legendary Butter Chicken and Tandoori Chicken, located near Red Fort.', price_tier: 'Moderate', price_inr: 850, cuisine: 'North Indian & Butter Chicken'});
CREATE (:Place:Restaurant {id: 'delhi_saravana_bhavan', name: 'Saravana Bhavan', category: 'Restaurant', city: 'Delhi', area: 'Connaught Place', rating: 4.5, description: 'Renowned South Indian chain serving crispy dosas, filter coffee, and traditional thalis.', price_tier: 'Budget', price_inr: 350, cuisine: 'South Indian Vegetarian'});
CREATE (:Place:Restaurant {id: 'delhi_gulati', name: 'Gulati Restaurant', category: 'Restaurant', city: 'Delhi', area: 'Pandara Road', rating: 4.6, description: 'Iconic fine-dining establishment on Pandara Road near India Gate, famous for rich dal makhani.', price_tier: 'Moderate', price_inr: 1100, cuisine: 'North Indian & Mughlai'});
CREATE (:Place:Restaurant {id: 'delhi_lakhori', name: 'Lakhori at Haveli Dharampura', category: 'Restaurant', city: 'Delhi', area: 'Chandni Chowk', rating: 4.6, description: 'Rooftop dining with classical kathak dance and panoramic views of Red Fort and Jama Masjid.', price_tier: 'Luxury', price_inr: 2500, cuisine: 'Mughlai & Chaat Tasting'});
CREATE (:Place:MetroStation {id: 'delhi_metro_lal_quila', name: 'Lal Quila Metro Station', category: 'MetroStation', city: 'Delhi', area: 'Old Delhi', rating: 4.6, description: 'Direct metro station gate opening right outside the Red Fort entry.', price_tier: 'Transit', line: 'Violet Line (Heritage Line)'});
CREATE (:Place:MetroStation {id: 'delhi_metro_chandni_chowk', name: 'Chandni Chowk Metro Station', category: 'MetroStation', city: 'Delhi', area: 'Chandni Chowk', rating: 4.4, description: 'Major station connecting Delhi\'s bustling spice markets and Old Delhi monuments.', price_tier: 'Transit', line: 'Yellow Line'});
CREATE (:Place:MetroStation {id: 'delhi_metro_central_sec', name: 'Central Secretariat Metro Station', category: 'MetroStation', city: 'Delhi', area: 'Rajpath', rating: 4.7, description: 'Interchange station located near National Museum, Kartavya Path, and India Gate.', price_tier: 'Transit', line: 'Yellow Line & Violet Line interchange'});
CREATE (:Place:MetroStation {id: 'delhi_metro_qutub_minar', name: 'Qutab Minar Metro Station', category: 'MetroStation', city: 'Delhi', area: 'Mehrauli', rating: 4.5, description: 'Yellow Line station providing swift access to the Qutub Minar complex.', price_tier: 'Transit', line: 'Yellow Line'});

// 6. Create LOCATED_IN Relations (Place -> City)
MATCH (p:Place {id: 'mumbai_gateway'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_csmt'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_marine_drive'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_elephanta'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_csmvs_museum'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_jehangir_art'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_nehru_centre'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_taj_hotel'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_hotel_diplomat'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_sea_green_hotel'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_oberoi'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_abode_colaba'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_sea_lounge'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_bademiya'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_leopold'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_pizza_by_bay'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_cafe_mondegar'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_metro_csmt'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_metro_churchgate'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'mumbai_metro_colaba'}), (c:City {id: 'city_mumbai'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_red_fort'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_jama_masjid'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_india_gate'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_qutub_minar'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_humayuns_tomb'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_lotus_temple'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_national_museum'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_ngma'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_crafts_museum'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_haveli_dharampura'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_hotel_tara_palace'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_hotel_delhi_heart'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_imperial_hotel'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_le_meridien'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_karims'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_moti_mahal'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_saravana_bhavan'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_gulati'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_lakhori'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_metro_lal_quila'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_metro_chandni_chowk'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_metro_central_sec'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);
MATCH (p:Place {id: 'delhi_metro_qutub_minar'}), (c:City {id: 'city_delhi'}) CREATE (p)-[:LOCATED_IN]->(c);

// 7. Create HAS_PRICE Relations (Place -> PriceTier)
MATCH (p:Place {id: 'mumbai_gateway'}), (t:PriceTier {id: 'price_free'}) CREATE (p)-[:HAS_PRICE {amount_inr: 0, tier: 'Free'}]->(t);
MATCH (p:Place {id: 'mumbai_csmt'}), (t:PriceTier {id: 'price_free'}) CREATE (p)-[:HAS_PRICE {amount_inr: 0, tier: 'Free'}]->(t);
MATCH (p:Place {id: 'mumbai_marine_drive'}), (t:PriceTier {id: 'price_free'}) CREATE (p)-[:HAS_PRICE {amount_inr: 0, tier: 'Free'}]->(t);
MATCH (p:Place {id: 'mumbai_elephanta'}), (t:PriceTier {id: 'price_budget'}) CREATE (p)-[:HAS_PRICE {amount_inr: 40, tier: 'Budget'}]->(t);
MATCH (p:Place {id: 'mumbai_csmvs_museum'}), (t:PriceTier {id: 'price_budget'}) CREATE (p)-[:HAS_PRICE {amount_inr: 150, tier: 'Budget'}]->(t);
MATCH (p:Place {id: 'mumbai_jehangir_art'}), (t:PriceTier {id: 'price_free'}) CREATE (p)-[:HAS_PRICE {amount_inr: 0, tier: 'Free'}]->(t);
MATCH (p:Place {id: 'mumbai_nehru_centre'}), (t:PriceTier {id: 'price_budget'}) CREATE (p)-[:HAS_PRICE {amount_inr: 70, tier: 'Budget'}]->(t);
MATCH (p:Place {id: 'mumbai_taj_hotel'}), (t:PriceTier {id: 'price_luxury'}) CREATE (p)-[:HAS_PRICE {amount_inr: 24000, tier: 'Luxury'}]->(t);
MATCH (p:Place {id: 'mumbai_hotel_diplomat'}), (t:PriceTier {id: 'price_moderate'}) CREATE (p)-[:HAS_PRICE {amount_inr: 3800, tier: 'Moderate'}]->(t);
MATCH (p:Place {id: 'mumbai_sea_green_hotel'}), (t:PriceTier {id: 'price_moderate'}) CREATE (p)-[:HAS_PRICE {amount_inr: 3200, tier: 'Moderate'}]->(t);
MATCH (p:Place {id: 'mumbai_oberoi'}), (t:PriceTier {id: 'price_luxury'}) CREATE (p)-[:HAS_PRICE {amount_inr: 21000, tier: 'Luxury'}]->(t);
MATCH (p:Place {id: 'mumbai_abode_colaba'}), (t:PriceTier {id: 'price_moderate'}) CREATE (p)-[:HAS_PRICE {amount_inr: 4500, tier: 'Moderate'}]->(t);
MATCH (p:Place {id: 'mumbai_sea_lounge'}), (t:PriceTier {id: 'price_luxury'}) CREATE (p)-[:HAS_PRICE {amount_inr: 2800, tier: 'Luxury'}]->(t);
MATCH (p:Place {id: 'mumbai_bademiya'}), (t:PriceTier {id: 'price_budget'}) CREATE (p)-[:HAS_PRICE {amount_inr: 450, tier: 'Budget'}]->(t);
MATCH (p:Place {id: 'mumbai_leopold'}), (t:PriceTier {id: 'price_moderate'}) CREATE (p)-[:HAS_PRICE {amount_inr: 900, tier: 'Moderate'}]->(t);
MATCH (p:Place {id: 'mumbai_pizza_by_bay'}), (t:PriceTier {id: 'price_moderate'}) CREATE (p)-[:HAS_PRICE {amount_inr: 1300, tier: 'Moderate'}]->(t);
MATCH (p:Place {id: 'mumbai_cafe_mondegar'}), (t:PriceTier {id: 'price_budget'}) CREATE (p)-[:HAS_PRICE {amount_inr: 750, tier: 'Budget'}]->(t);
MATCH (p:Place {id: 'mumbai_metro_csmt'}), (t:PriceTier {id: 'price_moderate'}) CREATE (p)-[:HAS_PRICE {amount_inr: 0, tier: 'Transit'}]->(t);
MATCH (p:Place {id: 'mumbai_metro_churchgate'}), (t:PriceTier {id: 'price_moderate'}) CREATE (p)-[:HAS_PRICE {amount_inr: 0, tier: 'Transit'}]->(t);
MATCH (p:Place {id: 'mumbai_metro_colaba'}), (t:PriceTier {id: 'price_moderate'}) CREATE (p)-[:HAS_PRICE {amount_inr: 0, tier: 'Transit'}]->(t);
MATCH (p:Place {id: 'delhi_red_fort'}), (t:PriceTier {id: 'price_budget'}) CREATE (p)-[:HAS_PRICE {amount_inr: 50, tier: 'Budget'}]->(t);
MATCH (p:Place {id: 'delhi_jama_masjid'}), (t:PriceTier {id: 'price_free'}) CREATE (p)-[:HAS_PRICE {amount_inr: 0, tier: 'Free'}]->(t);
MATCH (p:Place {id: 'delhi_india_gate'}), (t:PriceTier {id: 'price_free'}) CREATE (p)-[:HAS_PRICE {amount_inr: 0, tier: 'Free'}]->(t);
MATCH (p:Place {id: 'delhi_qutub_minar'}), (t:PriceTier {id: 'price_budget'}) CREATE (p)-[:HAS_PRICE {amount_inr: 50, tier: 'Budget'}]->(t);
MATCH (p:Place {id: 'delhi_humayuns_tomb'}), (t:PriceTier {id: 'price_budget'}) CREATE (p)-[:HAS_PRICE {amount_inr: 50, tier: 'Budget'}]->(t);
MATCH (p:Place {id: 'delhi_lotus_temple'}), (t:PriceTier {id: 'price_free'}) CREATE (p)-[:HAS_PRICE {amount_inr: 0, tier: 'Free'}]->(t);
MATCH (p:Place {id: 'delhi_national_museum'}), (t:PriceTier {id: 'price_budget'}) CREATE (p)-[:HAS_PRICE {amount_inr: 20, tier: 'Budget'}]->(t);
MATCH (p:Place {id: 'delhi_ngma'}), (t:PriceTier {id: 'price_budget'}) CREATE (p)-[:HAS_PRICE {amount_inr: 20, tier: 'Budget'}]->(t);
MATCH (p:Place {id: 'delhi_crafts_museum'}), (t:PriceTier {id: 'price_budget'}) CREATE (p)-[:HAS_PRICE {amount_inr: 20, tier: 'Budget'}]->(t);
MATCH (p:Place {id: 'delhi_haveli_dharampura'}), (t:PriceTier {id: 'price_luxury'}) CREATE (p)-[:HAS_PRICE {amount_inr: 8500, tier: 'Luxury'}]->(t);
MATCH (p:Place {id: 'delhi_hotel_tara_palace'}), (t:PriceTier {id: 'price_budget'}) CREATE (p)-[:HAS_PRICE {amount_inr: 1800, tier: 'Budget'}]->(t);
MATCH (p:Place {id: 'delhi_hotel_delhi_heart'}), (t:PriceTier {id: 'price_budget'}) CREATE (p)-[:HAS_PRICE {amount_inr: 2200, tier: 'Budget'}]->(t);
MATCH (p:Place {id: 'delhi_imperial_hotel'}), (t:PriceTier {id: 'price_luxury'}) CREATE (p)-[:HAS_PRICE {amount_inr: 18500, tier: 'Luxury'}]->(t);
MATCH (p:Place {id: 'delhi_le_meridien'}), (t:PriceTier {id: 'price_luxury'}) CREATE (p)-[:HAS_PRICE {amount_inr: 14000, tier: 'Luxury'}]->(t);
MATCH (p:Place {id: 'delhi_karims'}), (t:PriceTier {id: 'price_budget'}) CREATE (p)-[:HAS_PRICE {amount_inr: 600, tier: 'Budget'}]->(t);
MATCH (p:Place {id: 'delhi_moti_mahal'}), (t:PriceTier {id: 'price_moderate'}) CREATE (p)-[:HAS_PRICE {amount_inr: 850, tier: 'Moderate'}]->(t);
MATCH (p:Place {id: 'delhi_saravana_bhavan'}), (t:PriceTier {id: 'price_budget'}) CREATE (p)-[:HAS_PRICE {amount_inr: 350, tier: 'Budget'}]->(t);
MATCH (p:Place {id: 'delhi_gulati'}), (t:PriceTier {id: 'price_moderate'}) CREATE (p)-[:HAS_PRICE {amount_inr: 1100, tier: 'Moderate'}]->(t);
MATCH (p:Place {id: 'delhi_lakhori'}), (t:PriceTier {id: 'price_luxury'}) CREATE (p)-[:HAS_PRICE {amount_inr: 2500, tier: 'Luxury'}]->(t);
MATCH (p:Place {id: 'delhi_metro_lal_quila'}), (t:PriceTier {id: 'price_moderate'}) CREATE (p)-[:HAS_PRICE {amount_inr: 0, tier: 'Transit'}]->(t);
MATCH (p:Place {id: 'delhi_metro_chandni_chowk'}), (t:PriceTier {id: 'price_moderate'}) CREATE (p)-[:HAS_PRICE {amount_inr: 0, tier: 'Transit'}]->(t);
MATCH (p:Place {id: 'delhi_metro_central_sec'}), (t:PriceTier {id: 'price_moderate'}) CREATE (p)-[:HAS_PRICE {amount_inr: 0, tier: 'Transit'}]->(t);
MATCH (p:Place {id: 'delhi_metro_qutub_minar'}), (t:PriceTier {id: 'price_moderate'}) CREATE (p)-[:HAS_PRICE {amount_inr: 0, tier: 'Transit'}]->(t);

// 8. Create NEAR Relations (Symmetric Binary Relation)
MATCH (a:Place {id: 'mumbai_gateway'}), (b:Place {id: 'mumbai_taj_hotel'}) CREATE (a)-[:NEAR {distance_km: 0.1}]->(b), (b)-[:NEAR {distance_km: 0.1}]->(a);
MATCH (a:Place {id: 'mumbai_gateway'}), (b:Place {id: 'mumbai_sea_lounge'}) CREATE (a)-[:NEAR {distance_km: 0.1}]->(b), (b)-[:NEAR {distance_km: 0.1}]->(a);
MATCH (a:Place {id: 'mumbai_gateway'}), (b:Place {id: 'mumbai_hotel_diplomat'}) CREATE (a)-[:NEAR {distance_km: 0.3}]->(b), (b)-[:NEAR {distance_km: 0.3}]->(a);
MATCH (a:Place {id: 'mumbai_gateway'}), (b:Place {id: 'mumbai_bademiya'}) CREATE (a)-[:NEAR {distance_km: 0.4}]->(b), (b)-[:NEAR {distance_km: 0.4}]->(a);
MATCH (a:Place {id: 'mumbai_gateway'}), (b:Place {id: 'mumbai_leopold'}) CREATE (a)-[:NEAR {distance_km: 0.5}]->(b), (b)-[:NEAR {distance_km: 0.5}]->(a);
MATCH (a:Place {id: 'mumbai_gateway'}), (b:Place {id: 'mumbai_cafe_mondegar'}) CREATE (a)-[:NEAR {distance_km: 0.6}]->(b), (b)-[:NEAR {distance_km: 0.6}]->(a);
MATCH (a:Place {id: 'mumbai_gateway'}), (b:Place {id: 'mumbai_abode_colaba'}) CREATE (a)-[:NEAR {distance_km: 0.4}]->(b), (b)-[:NEAR {distance_km: 0.4}]->(a);
MATCH (a:Place {id: 'mumbai_gateway'}), (b:Place {id: 'mumbai_csmvs_museum'}) CREATE (a)-[:NEAR {distance_km: 0.8}]->(b), (b)-[:NEAR {distance_km: 0.8}]->(a);
MATCH (a:Place {id: 'mumbai_gateway'}), (b:Place {id: 'mumbai_jehangir_art'}) CREATE (a)-[:NEAR {distance_km: 0.9}]->(b), (b)-[:NEAR {distance_km: 0.9}]->(a);
MATCH (a:Place {id: 'mumbai_taj_hotel'}), (b:Place {id: 'mumbai_sea_lounge'}) CREATE (a)-[:NEAR {distance_km: 0.05}]->(b), (b)-[:NEAR {distance_km: 0.05}]->(a);
MATCH (a:Place {id: 'mumbai_hotel_diplomat'}), (b:Place {id: 'mumbai_bademiya'}) CREATE (a)-[:NEAR {distance_km: 0.2}]->(b), (b)-[:NEAR {distance_km: 0.2}]->(a);
MATCH (a:Place {id: 'mumbai_csmvs_museum'}), (b:Place {id: 'mumbai_jehangir_art'}) CREATE (a)-[:NEAR {distance_km: 0.2}]->(b), (b)-[:NEAR {distance_km: 0.2}]->(a);
MATCH (a:Place {id: 'mumbai_marine_drive'}), (b:Place {id: 'mumbai_oberoi'}) CREATE (a)-[:NEAR {distance_km: 0.5}]->(b), (b)-[:NEAR {distance_km: 0.5}]->(a);
MATCH (a:Place {id: 'mumbai_marine_drive'}), (b:Place {id: 'mumbai_sea_green_hotel'}) CREATE (a)-[:NEAR {distance_km: 0.3}]->(b), (b)-[:NEAR {distance_km: 0.3}]->(a);
MATCH (a:Place {id: 'mumbai_marine_drive'}), (b:Place {id: 'mumbai_pizza_by_bay'}) CREATE (a)-[:NEAR {distance_km: 0.2}]->(b), (b)-[:NEAR {distance_km: 0.2}]->(a);
MATCH (a:Place {id: 'mumbai_csmt'}), (b:Place {id: 'mumbai_csmvs_museum'}) CREATE (a)-[:NEAR {distance_km: 1.2}]->(b), (b)-[:NEAR {distance_km: 1.2}]->(a);
MATCH (a:Place {id: 'mumbai_marine_drive'}), (b:Place {id: 'mumbai_csmt'}) CREATE (a)-[:NEAR {distance_km: 2.2}]->(b), (b)-[:NEAR {distance_km: 2.2}]->(a);
MATCH (a:Place {id: 'delhi_red_fort'}), (b:Place {id: 'delhi_hotel_tara_palace'}) CREATE (a)-[:NEAR {distance_km: 0.5}]->(b), (b)-[:NEAR {distance_km: 0.5}]->(a);
MATCH (a:Place {id: 'delhi_red_fort'}), (b:Place {id: 'delhi_karims'}) CREATE (a)-[:NEAR {distance_km: 0.6}]->(b), (b)-[:NEAR {distance_km: 0.6}]->(a);
MATCH (a:Place {id: 'delhi_red_fort'}), (b:Place {id: 'delhi_moti_mahal'}) CREATE (a)-[:NEAR {distance_km: 1.0}]->(b), (b)-[:NEAR {distance_km: 1.0}]->(a);
MATCH (a:Place {id: 'delhi_red_fort'}), (b:Place {id: 'delhi_jama_masjid'}) CREATE (a)-[:NEAR {distance_km: 0.7}]->(b), (b)-[:NEAR {distance_km: 0.7}]->(a);
MATCH (a:Place {id: 'delhi_red_fort'}), (b:Place {id: 'delhi_haveli_dharampura'}) CREATE (a)-[:NEAR {distance_km: 0.8}]->(b), (b)-[:NEAR {distance_km: 0.8}]->(a);
MATCH (a:Place {id: 'delhi_red_fort'}), (b:Place {id: 'delhi_lakhori'}) CREATE (a)-[:NEAR {distance_km: 0.8}]->(b), (b)-[:NEAR {distance_km: 0.8}]->(a);
MATCH (a:Place {id: 'delhi_jama_masjid'}), (b:Place {id: 'delhi_karims'}) CREATE (a)-[:NEAR {distance_km: 0.2}]->(b), (b)-[:NEAR {distance_km: 0.2}]->(a);
MATCH (a:Place {id: 'delhi_jama_masjid'}), (b:Place {id: 'delhi_haveli_dharampura'}) CREATE (a)-[:NEAR {distance_km: 0.4}]->(b), (b)-[:NEAR {distance_km: 0.4}]->(a);
MATCH (a:Place {id: 'delhi_haveli_dharampura'}), (b:Place {id: 'delhi_lakhori'}) CREATE (a)-[:NEAR {distance_km: 0.05}]->(b), (b)-[:NEAR {distance_km: 0.05}]->(a);
MATCH (a:Place {id: 'delhi_india_gate'}), (b:Place {id: 'delhi_ngma'}) CREATE (a)-[:NEAR {distance_km: 0.3}]->(b), (b)-[:NEAR {distance_km: 0.3}]->(a);
MATCH (a:Place {id: 'delhi_india_gate'}), (b:Place {id: 'delhi_gulati'}) CREATE (a)-[:NEAR {distance_km: 0.9}]->(b), (b)-[:NEAR {distance_km: 0.9}]->(a);
MATCH (a:Place {id: 'delhi_national_museum'}), (b:Place {id: 'delhi_imperial_hotel'}) CREATE (a)-[:NEAR {distance_km: 1.1}]->(b), (b)-[:NEAR {distance_km: 1.1}]->(a);
MATCH (a:Place {id: 'delhi_national_museum'}), (b:Place {id: 'delhi_le_meridien'}) CREATE (a)-[:NEAR {distance_km: 1.2}]->(b), (b)-[:NEAR {distance_km: 1.2}]->(a);
MATCH (a:Place {id: 'delhi_imperial_hotel'}), (b:Place {id: 'delhi_saravana_bhavan'}) CREATE (a)-[:NEAR {distance_km: 0.7}]->(b), (b)-[:NEAR {distance_km: 0.7}]->(a);
MATCH (a:Place {id: 'delhi_india_gate'}), (b:Place {id: 'delhi_national_museum'}) CREATE (a)-[:NEAR {distance_km: 1.4}]->(b), (b)-[:NEAR {distance_km: 1.4}]->(a);

// 9. Create CONNECTED_TO Relations (Transit and Navigation Routes)
MATCH (a:Place {id: 'mumbai_metro_colaba'}), (b:Place {id: 'mumbai_gateway'}) CREATE (a)-[:CONNECTED_TO {distance_km: 1.1, mode: 'Walk / Shuttle'}]->(b), (b)-[:CONNECTED_TO {distance_km: 1.1, mode: 'Walk / Shuttle'}]->(a);
MATCH (a:Place {id: 'mumbai_metro_colaba'}), (b:Place {id: 'mumbai_taj_hotel'}) CREATE (a)-[:CONNECTED_TO {distance_km: 1.0, mode: 'Walk'}]->(b), (b)-[:CONNECTED_TO {distance_km: 1.0, mode: 'Walk'}]->(a);
MATCH (a:Place {id: 'mumbai_metro_churchgate'}), (b:Place {id: 'mumbai_marine_drive'}) CREATE (a)-[:CONNECTED_TO {distance_km: 0.6, mode: 'Walk'}]->(b), (b)-[:CONNECTED_TO {distance_km: 0.6, mode: 'Walk'}]->(a);
MATCH (a:Place {id: 'mumbai_metro_churchgate'}), (b:Place {id: 'mumbai_csmvs_museum'}) CREATE (a)-[:CONNECTED_TO {distance_km: 0.9, mode: 'Walk'}]->(b), (b)-[:CONNECTED_TO {distance_km: 0.9, mode: 'Walk'}]->(a);
MATCH (a:Place {id: 'mumbai_metro_csmt'}), (b:Place {id: 'mumbai_csmt'}) CREATE (a)-[:CONNECTED_TO {distance_km: 0.1, mode: 'Direct Entry'}]->(b), (b)-[:CONNECTED_TO {distance_km: 0.1, mode: 'Direct Entry'}]->(a);
MATCH (a:Place {id: 'mumbai_metro_csmt'}), (b:Place {id: 'mumbai_csmvs_museum'}) CREATE (a)-[:CONNECTED_TO {distance_km: 1.1, mode: 'Taxi / Walk'}]->(b), (b)-[:CONNECTED_TO {distance_km: 1.1, mode: 'Taxi / Walk'}]->(a);
MATCH (a:Place {id: 'mumbai_metro_colaba'}), (b:Place {id: 'mumbai_metro_churchgate'}) CREATE (a)-[:CONNECTED_TO {distance_km: 2.4, mode: 'Aqua Line 3'}]->(b), (b)-[:CONNECTED_TO {distance_km: 2.4, mode: 'Aqua Line 3'}]->(a);
MATCH (a:Place {id: 'mumbai_metro_churchgate'}), (b:Place {id: 'mumbai_metro_csmt'}) CREATE (a)-[:CONNECTED_TO {distance_km: 1.8, mode: 'Suburban Rail / Bus'}]->(b), (b)-[:CONNECTED_TO {distance_km: 1.8, mode: 'Suburban Rail / Bus'}]->(a);
MATCH (a:Place {id: 'mumbai_gateway'}), (b:Place {id: 'mumbai_elephanta'}) CREATE (a)-[:CONNECTED_TO {distance_km: 10.0, mode: 'Ferry Boat'}]->(b), (b)-[:CONNECTED_TO {distance_km: 10.0, mode: 'Ferry Boat'}]->(a);
MATCH (a:Place {id: 'delhi_metro_lal_quila'}), (b:Place {id: 'delhi_red_fort'}) CREATE (a)-[:CONNECTED_TO {distance_km: 0.2, mode: 'Walk (Gate 1)'}]->(b), (b)-[:CONNECTED_TO {distance_km: 0.2, mode: 'Walk (Gate 1)'}]->(a);
MATCH (a:Place {id: 'delhi_metro_chandni_chowk'}), (b:Place {id: 'delhi_red_fort'}) CREATE (a)-[:CONNECTED_TO {distance_km: 0.7, mode: 'Walk / E-Rickshaw'}]->(b), (b)-[:CONNECTED_TO {distance_km: 0.7, mode: 'Walk / E-Rickshaw'}]->(a);
MATCH (a:Place {id: 'delhi_metro_chandni_chowk'}), (b:Place {id: 'delhi_jama_masjid'}) CREATE (a)-[:CONNECTED_TO {distance_km: 0.8, mode: 'Walk / E-Rickshaw'}]->(b), (b)-[:CONNECTED_TO {distance_km: 0.8, mode: 'Walk / E-Rickshaw'}]->(a);
MATCH (a:Place {id: 'delhi_metro_chandni_chowk'}), (b:Place {id: 'delhi_hotel_tara_palace'}) CREATE (a)-[:CONNECTED_TO {distance_km: 0.5, mode: 'Walk'}]->(b), (b)-[:CONNECTED_TO {distance_km: 0.5, mode: 'Walk'}]->(a);
MATCH (a:Place {id: 'delhi_metro_central_sec'}), (b:Place {id: 'delhi_national_museum'}) CREATE (a)-[:CONNECTED_TO {distance_km: 0.6, mode: 'Walk'}]->(b), (b)-[:CONNECTED_TO {distance_km: 0.6, mode: 'Walk'}]->(a);
MATCH (a:Place {id: 'delhi_metro_central_sec'}), (b:Place {id: 'delhi_india_gate'}) CREATE (a)-[:CONNECTED_TO {distance_km: 1.2, mode: 'Walk / Shuttle'}]->(b), (b)-[:CONNECTED_TO {distance_km: 1.2, mode: 'Walk / Shuttle'}]->(a);
MATCH (a:Place {id: 'delhi_metro_central_sec'}), (b:Place {id: 'delhi_imperial_hotel'}) CREATE (a)-[:CONNECTED_TO {distance_km: 0.8, mode: 'Walk'}]->(b), (b)-[:CONNECTED_TO {distance_km: 0.8, mode: 'Walk'}]->(a);
MATCH (a:Place {id: 'delhi_metro_qutub_minar'}), (b:Place {id: 'delhi_qutub_minar'}) CREATE (a)-[:CONNECTED_TO {distance_km: 0.9, mode: 'Feeder Bus / Walk'}]->(b), (b)-[:CONNECTED_TO {distance_km: 0.9, mode: 'Feeder Bus / Walk'}]->(a);
MATCH (a:Place {id: 'delhi_metro_chandni_chowk'}), (b:Place {id: 'delhi_metro_central_sec'}) CREATE (a)-[:CONNECTED_TO {distance_km: 4.5, mode: 'Yellow Line'}]->(b), (b)-[:CONNECTED_TO {distance_km: 4.5, mode: 'Yellow Line'}]->(a);
MATCH (a:Place {id: 'delhi_metro_lal_quila'}), (b:Place {id: 'delhi_metro_central_sec'}) CREATE (a)-[:CONNECTED_TO {distance_km: 4.2, mode: 'Violet Line'}]->(b), (b)-[:CONNECTED_TO {distance_km: 4.2, mode: 'Violet Line'}]->(a);
MATCH (a:Place {id: 'delhi_metro_chandni_chowk'}), (b:Place {id: 'delhi_metro_lal_quila'}) CREATE (a)-[:CONNECTED_TO {distance_km: 0.9, mode: 'Heritage Walkway'}]->(b), (b)-[:CONNECTED_TO {distance_km: 0.9, mode: 'Heritage Walkway'}]->(a);
MATCH (a:Place {id: 'delhi_metro_central_sec'}), (b:Place {id: 'delhi_metro_qutub_minar'}) CREATE (a)-[:CONNECTED_TO {distance_km: 12.0, mode: 'Yellow Line'}]->(b), (b)-[:CONNECTED_TO {distance_km: 12.0, mode: 'Yellow Line'}]->(a);
