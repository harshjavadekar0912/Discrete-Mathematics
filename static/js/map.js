/**
 * Tourist Guide Assistant - Interactive Map Page
 * Powered by Leaflet + OpenStreetMap Standard Raster Tiles
 */

let map = null;
const markers = [];
window.markers = markers;

// City centers matching osm_service.py CITY_CENTERS
const CITY_CENTERS = {
  mumbai:    [18.9388, 72.8354],
  delhi:     [28.6448, 77.2167],
  pune:      [18.5204, 73.8567],
  chennai:   [13.0827, 80.2707],
  hyderabad: [17.3850, 78.4867],
};

// Custom cyan divIcon to match dark UI theme
function makeDivIcon() {
  return L.divIcon({
    className: '',
    html: `<div style="
      width: 16px; height: 16px;
      background: #38bdf8;
      border: 2px solid #ffffff;
      border-radius: 50%;
      box-shadow: 0 0 8px rgba(56,189,248,0.7);
    "></div>`,
    iconSize: [16, 16],
    iconAnchor: [8, 8],
    popupAnchor: [0, -10],
  });
}

function initMap() {
  if (!document.getElementById('map')) return;

  map = L.map('map').setView([20.5937, 78.9629], 5);
  window.map = map;

  L.tileLayer(
    'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19
    }
  ).addTo(map);
}

function clearMarkers() {
  markers.forEach(m => map && map.removeLayer(m));
  markers.length = 0;
}

function addMarker(place) {
  if (!place.lat || !place.lng || !map) return;

  const osmLink = place.osm_url
    ? `<br><a href="${escapeHtml(place.osm_url)}" target="_blank" rel="noopener" style="color:#0284c7; font-size:12px; font-weight:600; text-decoration:none;">View on OpenStreetMap ↗</a>`
    : '';
  const hours = place.opening_hours ? `<br><span style="font-size:11px; color:#475569;">🕐 ${escapeHtml(place.opening_hours)}</span>` : '';
  const phone = place.phone ? `<br><span style="font-size:11px; color:#475569;">📞 ${escapeHtml(place.phone)}</span>` : '';

  const popup = L.popup({ maxWidth: 260 }).setContent(`
    <div style="font-family: Inter, sans-serif; padding: 4px;">
      <strong style="font-size:14px; color:#0f172a;">${escapeHtml(place.name || 'Unknown')}</strong><br>
      <span style="font-size:12px; color:#475569;">${escapeHtml(place.address || '')}</span>
      ${hours}${phone}${osmLink}
    </div>
  `);

  const marker = L.marker([place.lat, place.lng], { icon: makeDivIcon() })
    .bindPopup(popup)
    .addTo(map);

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
    const badgeClass = `badge-${cat.toLowerCase().replace(/[^a-z0-9]/g, '')}`;
    const osmLink = p.osm_url
      ? `<a href="${escapeHtml(p.osm_url)}" target="_blank" rel="noopener" style="font-size:0.72rem; color:#38bdf8; text-decoration:none;">OSM ↗</a>`
      : '';

    return `
      <div class="place-card" style="margin-bottom:0.75rem; cursor:pointer;" onclick="focusPlace(${p.lat || 'null'}, ${p.lng || 'null'})">
        <span class="place-badge ${badgeClass}">${escapeHtml(cat)}</span>
        <div class="place-title" style="font-size:0.95rem;">${escapeHtml(p.name || '')}</div>
        <div style="font-size:0.78rem; color:var(--text-muted); margin-top:0.2rem;">${escapeHtml(p.address || '')}</div>
        <div style="font-size:0.8rem; margin-top:0.3rem; display:flex; gap:0.5rem; align-items:center; flex-wrap:wrap;">
          ${osmLink}
        </div>
      </div>
    `;
  }).join('');
}

function focusPlace(lat, lng) {
  if (!map || !lat || !lng) return;
  map.setView([lat, lng], 16);
  const matched = markers.find(m => {
    const pos = m.getLatLng();
    return Math.abs(pos.lat - lat) < 0.0001 && Math.abs(pos.lng - lng) < 0.0001;
  });
  if (matched) {
    matched.openPopup();
  }
}

async function searchPlaces(query) {
  const resultsDiv = document.getElementById('mapResults');
  resultsDiv.innerHTML = `<p style="color:var(--text-muted); font-size:0.88rem; text-align:center; padding:2rem 0;">⏳ Searching OpenStreetMap...</p>`;

  try {
    const res = await fetch(`/api/places/search?query=${encodeURIComponent(query)}`);
    const data = await res.json();
    const places = data.places || [];

    clearMarkers();
    renderResults(places);
    places.forEach(addMarker);

    // Fit map to result bounds
    if (places.length > 0 && map) {
      const validPlaces = places.filter(p => p.lat && p.lng);
      if (validPlaces.length > 0) {
        const bounds = L.latLngBounds(validPlaces.map(p => [p.lat, p.lng]));
        map.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 });
      }
    }
  } catch (err) {
    if (resultsDiv) resultsDiv.innerHTML = `<p style="color:#f87171; font-size:0.88rem;">Error: ${escapeHtml(err.message)}</p>`;
  }
}

async function searchCity(cityKey) {
  const center = CITY_CENTERS[cityKey];
  if (!center || !map) return;
  map.setView(center, 12);

  const resultsDiv = document.getElementById('mapResults');
  resultsDiv.innerHTML = `<p style="color:var(--text-muted); font-size:0.88rem; text-align:center; padding:2rem 0;">⏳ Loading OpenStreetMap data...</p>`;

  try {
    const res = await fetch(`/api/places/citytype?city=${encodeURIComponent(cityKey)}&type=tourist_attraction`);
    const data = await res.json();
    const places = data.places || [];

    clearMarkers();
    renderResults(places);
    places.forEach(addMarker);
  } catch (err) {
    if (resultsDiv) resultsDiv.innerHTML = `<p style="color:#f87171; font-size:0.88rem;">Error: ${escapeHtml(err.message)}</p>`;
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// DOM event binding
document.addEventListener('DOMContentLoaded', () => {
  // Init Leaflet map safely
  if (typeof L !== 'undefined' && document.getElementById('map')) {
    initMap();
  } else if (document.getElementById('map')) {
    console.error('Leaflet library (L) is not loaded.');
    document.getElementById('map').innerHTML = `
      <div style="display:flex; align-items:center; justify-content:center; height:100%; color:var(--text-muted); text-align:center; padding:2rem;">
        <div>
          <div style="font-size:2.5rem; margin-bottom:1rem;">⚠️</div>
          <p>Unable to load map library. Please check your internet connection and refresh.</p>
        </div>
      </div>
    `;
  }

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
          searchCity(cityKey);
        } else if (!cityKey && map) {
          map.setView([20.5937, 78.9629], 5);
          clearMarkers();
          document.getElementById('mapResults').innerHTML =
            `<p style="color:var(--text-muted); font-size:0.88rem; text-align:center; padding:2rem 0;">Select a city or search to see results.</p>`;
        }
      });
    });
  }
});
