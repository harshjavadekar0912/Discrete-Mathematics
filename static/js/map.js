/**
 * Tourist Guide Assistant - Interactive Map Page
 * Powered by Google Maps JavaScript API
 */

let map = null;
let markers = [];
let infoWindow = null;

// City centers for India
const CITY_CENTERS = {
  mumbai:    { lat: 18.9388, lng: 72.8354 },
  delhi:     { lat: 28.6448, lng: 77.2167 },
  pune:      { lat: 18.5204, lng: 73.8567 },
  chennai:   { lat: 13.0827, lng: 80.2707 },
  hyderabad: { lat: 17.3850, lng: 78.4867 },
};

// Called by Maps JS API loader callback
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: { lat: 20.5937, lng: 78.9629 }, // Center of India
    zoom: 5,
    styles: [
      { elementType: 'geometry', stylers: [{ color: '#0a0f1d' }] },
      { elementType: 'labels.text.fill', stylers: [{ color: '#94a3b8' }] },
      { elementType: 'labels.text.stroke', stylers: [{ color: '#0a0f1d' }] },
      { featureType: 'road', elementType: 'geometry', stylers: [{ color: '#1e293b' }] },
      { featureType: 'water', elementType: 'geometry', stylers: [{ color: '#0f172a' }] },
      { featureType: 'poi', elementType: 'geometry', stylers: [{ color: '#0f172a' }] },
    ],
    disableDefaultUI: false,
  });
  infoWindow = new google.maps.InfoWindow();
}

function clearMarkers() {
  markers.forEach(m => m.setMap(null));
  markers = [];
}

function addMarker(place) {
  if (!place.lat || !place.lng || !map) return;
  const marker = new google.maps.Marker({
    position: { lat: place.lat, lng: place.lng },
    map: map,
    title: place.name,
    icon: {
      path: google.maps.SymbolPath.CIRCLE,
      scale: 10,
      fillColor: '#38bdf8',
      fillOpacity: 0.9,
      strokeColor: '#fff',
      strokeWeight: 2,
    }
  });

  marker.addListener('click', () => {
    const rating = place.rating ? `⭐ ${place.rating}` : '';
    const hours = place.opening_hours ? `🕐 ${place.opening_hours}` : '';
    const mapsLink = place.maps_uri
      ? `<br><a href="${place.maps_uri}" target="_blank" style="color:#38bdf8;">Open in Google Maps ↗</a>`
      : '';

    infoWindow.setContent(`
      <div style="font-family: Inter, sans-serif; padding: 4px;">
        <strong style="font-size:14px;">${place.name}</strong><br>
        <span style="font-size:12px; color:#555;">${place.address || ''}</span><br>
        <span style="font-size:12px;">${rating} ${hours}</span>
        ${mapsLink}
      </div>
    `);
    infoWindow.open(map, marker);
  });

  markers.push(marker);
}

function renderResults(places) {
  const resultsDiv = document.getElementById('mapResults');
  if (!places || places.length === 0) {
    resultsDiv.innerHTML = `<p style="color:var(--text-muted); font-size:0.88rem; text-align:center; padding:2rem 0;">No results found. Try a different search.</p>`;
    return;
  }

  resultsDiv.innerHTML = places.map(p => {
    const cat = p.category || 'Place';
    const badgeClass = `badge-${cat.toLowerCase()}`;
    const rating = p.rating ? `⭐ ${p.rating}` : '';
    const mapsLink = p.maps_uri
      ? `<a href="${p.maps_uri}" target="_blank" rel="noopener" style="font-size:0.72rem; color:#38bdf8; text-decoration:none;">Open Maps ↗</a>`
      : '';

    return `
      <div class="place-card" style="margin-bottom:0.75rem; cursor:pointer;" onclick="focusPlace(${p.lat || 'null'}, ${p.lng || 'null'})">
        <span class="place-badge ${badgeClass}">${cat}</span>
        <div class="place-title" style="font-size:0.95rem;">${p.name}</div>
        <div style="font-size:0.78rem; color:var(--text-muted); margin-top:0.2rem;">${p.address || ''}</div>
        <div style="font-size:0.8rem; margin-top:0.3rem; display:flex; gap:0.5rem; align-items:center; flex-wrap:wrap;">
          <span style="color:#fbbf24;">${rating}</span>
          ${mapsLink}
        </div>
      </div>
    `;
  }).join('');
}

function focusPlace(lat, lng) {
  if (!map || !lat || !lng) return;
  map.setCenter({ lat, lng });
  map.setZoom(16);
}

async function searchPlaces(query) {
  try {
    const res = await fetch(`/api/places/search?query=${encodeURIComponent(query)}`);
    const data = await res.json();
    const places = data.places || [];

    clearMarkers();
    renderResults(places);
    places.forEach(addMarker);

    // Fit map bounds
    if (places.length > 0 && map) {
      const bounds = new google.maps.LatLngBounds();
      places.forEach(p => {
        if (p.lat && p.lng) bounds.extend({ lat: p.lat, lng: p.lng });
      });
      if (!bounds.isEmpty()) map.fitBounds(bounds);
    }
  } catch (err) {
    document.getElementById('mapResults').innerHTML =
      `<p style="color:#f87171; font-size:0.88rem;">Error: ${err.message}</p>`;
  }
}

// DOM event binding (runs before Maps API is loaded)
document.addEventListener('DOMContentLoaded', () => {
  const searchBtn = document.getElementById('mapSearchBtn');
  const searchInput = document.getElementById('mapSearchInput');
  const cityBtns = document.querySelectorAll('.city-btn');

  if (searchBtn && searchInput) {
    searchBtn.addEventListener('click', () => {
      const q = searchInput.value.trim();
      if (q) searchPlaces(q);
    });
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const q = searchInput.value.trim();
        if (q) searchPlaces(q);
      }
    });
  }

  if (cityBtns) {
    cityBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        cityBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const cityKey = btn.getAttribute('data-city');
        if (cityKey && CITY_CENTERS[cityKey]) {
          if (map) {
            map.setCenter(CITY_CENTERS[cityKey]);
            map.setZoom(12);
          }
          searchPlaces(`tourist attractions in ${cityKey} India`);
        } else if (!cityKey && map) {
          map.setCenter({ lat: 20.5937, lng: 78.9629 });
          map.setZoom(5);
          clearMarkers();
          document.getElementById('mapResults').innerHTML =
            `<p style="color:var(--text-muted); font-size:0.88rem; text-align:center; padding:2rem 0;">Select a city or search to see results.</p>`;
        }
      });
    });
  }
});
