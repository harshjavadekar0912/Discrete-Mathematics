/**
 * Tourist Places Explorer
 * Powered by OpenStreetMap — Overpass API via /api/places/citytype
 */

document.addEventListener('DOMContentLoaded', () => {
  const citySelect = document.getElementById('cityFilter');
  const categoryChips = document.querySelectorAll('.cat-chip');
  const placesGrid = document.getElementById('placesGrid');
  const countBadge = document.getElementById('placesCount');

  let activeCity = 'mumbai';
  let activePlaceType = 'tourist_attraction';

  categoryChips.forEach(chip => {
    chip.addEventListener('click', () => {
      categoryChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activePlaceType = chip.getAttribute('data-type') || 'tourist_attraction';
      fetchAndRender();
    });
  });

  if (citySelect) {
    citySelect.addEventListener('change', () => {
      activeCity = citySelect.value;
      fetchAndRender();
    });
  }

  async function fetchAndRender() {
    if (countBadge) countBadge.innerText = 'Loading...';
    if (placesGrid) placesGrid.innerHTML = `
      <div style="grid-column: 1/-1; text-align:center; padding:3rem; color:var(--text-muted);">
        <div style="font-size:2rem; margin-bottom:0.75rem;">⏳</div>
        <p>Fetching from OpenStreetMap...</p>
      </div>
    `;

    try {
      const url = `/api/places/citytype?city=${encodeURIComponent(activeCity)}&type=${encodeURIComponent(activePlaceType)}`;
      const res = await fetch(url);
      const data = await res.json();

      if (data.error && (!data.places || data.places.length === 0)) {
        if (countBadge) countBadge.innerText = 'Error';
        placesGrid.innerHTML = `
          <div style="grid-column:1/-1; text-align:center; padding:3rem; color:var(--text-muted);">
            <div style="font-size:2.5rem; margin-bottom:1rem;">⚠️</div>
            <h3 style="color:#f87171; margin-bottom:0.5rem;">Search Error</h3>
            <p style="max-width:500px; margin:0 auto;">${escapeHtml(data.error)}</p>
          </div>
        `;
        return;
      }

      const places = data.places || [];
      if (countBadge) countBadge.innerText = `${places.length} Places Found`;
      renderCards(places);
    } catch (err) {
      if (countBadge) countBadge.innerText = 'Error';
      if (placesGrid) placesGrid.innerHTML = `<div style="grid-column:1/-1; color:#f87171; text-align:center; padding:3rem;">Error: ${escapeHtml(err.message)}</div>`;
    }
  }

  function renderCards(places) {
    if (!placesGrid) return;

    if (places.length === 0) {
      placesGrid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 4rem 1rem; color: var(--text-dim);">
          <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
          <h3>No places found</h3>
          <p>OpenStreetMap may have sparse data here. Try a different category or city.</p>
        </div>
      `;
      return;
    }

    placesGrid.innerHTML = places.map(p => {
      const cat = p.category || 'Place';
      const badgeClass = `badge-${cat.toLowerCase()}`;
      const hours = p.opening_hours ? `<div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.5rem;">🕐 ${escapeHtml(p.opening_hours)}</div>` : '';
      const phone = p.phone ? `<div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.5rem;">📞 ${escapeHtml(p.phone)}</div>` : '';
      const cuisine = p.cuisine ? `<div style="font-size:0.78rem; color:var(--text-muted); margin-bottom:0.5rem;">🍴 ${escapeHtml(p.cuisine)}</div>` : '';

      const osmLink = p.osm_url
        ? `<a href="${escapeHtml(p.osm_url)}" target="_blank" rel="noopener" class="btn-primary" style="padding:0.5rem; font-size:0.8rem; text-decoration:none; display:flex; align-items:center; justify-content:center; gap:0.4rem;"><span>📍</span> View on OpenStreetMap</a>`
        : `<button onclick="window.location.href='/?q=${encodeURIComponent('Tell me about ' + (p.name || ''))}';" class="btn-primary" style="padding:0.5rem; font-size:0.8rem; cursor:pointer;"><span>💬</span> Ask Chatbot</button>`;

      const webLink = p.website
        ? `<a href="${escapeHtml(p.website)}" target="_blank" rel="noopener" style="font-size:0.75rem; color:#a78bfa; text-decoration:none; display:block; margin-top:0.3rem; text-align:center;">🌐 Website ↗</a>`
        : '';

      return `
        <div class="place-card" style="display:flex; flex-direction:column; justify-content:space-between;">
          <div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
              <span class="place-badge ${badgeClass}">${escapeHtml(cat)}</span>
            </div>
            <h4 class="place-title" style="font-size:1.05rem;">${escapeHtml(p.name || 'Unknown')}</h4>
            <div class="place-meta">
              <span>📍 ${escapeHtml(p.address || '')}</span>
            </div>
            ${hours}${phone}${cuisine}
          </div>
          <div>
            ${osmLink}
            ${webLink}
          </div>
        </div>
      `;
    }).join('');
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  // Initial load
  fetchAndRender();
});
