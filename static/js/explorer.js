/**
 * Tourist Places Directory Explorer
 */

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('placeSearch');
  const citySelect = document.getElementById('cityFilter');
  const categoryChips = document.querySelectorAll('.cat-chip');
  const placesGrid = document.getElementById('placesGrid');
  const countBadge = document.getElementById('placesCount');

  let activeCategory = '';
  let activeCity = '';
  let searchQuery = '';

  categoryChips.forEach(chip => {
    chip.addEventListener('click', () => {
      categoryChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeCategory = chip.getAttribute('data-cat') || '';
      filterAndRender();
    });
  });

  if (citySelect) {
    citySelect.addEventListener('change', () => {
      activeCity = citySelect.value;
      filterAndRender();
    });
  }

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.toLowerCase().trim();
      filterAndRender();
    });
  }

  async function filterAndRender() {
    try {
      let url = '/api/places/list?';
      if (activeCategory) url += `category=${encodeURIComponent(activeCategory)}&`;
      if (activeCity) url += `city=${encodeURIComponent(activeCity)}&`;

      const res = await fetch(url);
      const data = await res.json();
      let places = data.places || [];

      if (searchQuery) {
        places = places.filter(p => 
          (p.name && p.name.toLowerCase().includes(searchQuery)) ||
          (p.area && p.area.toLowerCase().includes(searchQuery)) ||
          (p.description && p.description.toLowerCase().includes(searchQuery)) ||
          (p.cuisine && p.cuisine.toLowerCase().includes(searchQuery))
        );
      }

      if (countBadge) countBadge.innerText = `${places.length} Places Found`;
      renderCards(places);
    } catch (err) {
      console.error('Error fetching places:', err);
    }
  }

  function renderCards(places) {
    if (!placesGrid) return;

    if (places.length === 0) {
      placesGrid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 4rem 1rem; color: var(--text-dim);">
          <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
          <h3>No tourist places match your filters</h3>
          <p>Try resetting the category filter or searching for another location.</p>
        </div>
      `;
      return;
    }

    placesGrid.innerHTML = places.map(p => {
      const cat = p.category || 'Place';
      const badgeClass = `badge-${cat.toLowerCase()}`;
      
      let priceInfo = '';
      if (p.price_inr !== undefined) {
        priceInfo = `<div class="place-price">₹${p.price_inr}/night</div>`;
      } else if (p.entry_fee !== undefined) {
        priceInfo = `<div class="place-price">${p.entry_fee === 0 ? 'Free Entry' : 'Entry: ₹' + p.entry_fee}</div>`;
      } else if (p.line) {
        priceInfo = `<div style="color: #38bdf8; font-size: 0.85rem;">🚇 ${escapeHtml(p.line)}</div>`;
      }

      return `
        <div class="place-card" style="display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <span class="place-badge ${badgeClass}">${escapeHtml(cat)}</span>
              <span style="font-size: 0.8rem; color: #fbbf24; font-weight: 600;">⭐ ${p.rating || 4.5}</span>
            </div>

            <h4 class="place-title" style="font-size: 1.1rem;">${escapeHtml(p.name)}</h4>
            
            <div class="place-meta">
              <span>📍 ${escapeHtml(p.area || p.city)}</span>
              <span>• ${escapeHtml(p.city)}</span>
              ${p.is_unesco ? '<span style="color: #a78bfa;">• UNESCO</span>' : ''}
            </div>

            <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 1rem; line-height: 1.45; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;">
              ${escapeHtml(p.description || '')}
            </p>
          </div>

          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.85rem; padding-top: 0.75rem; border-top: 1px solid rgba(255,255,255,0.05);">
              ${priceInfo}
              <span style="font-size: 0.75rem; color: var(--text-dim); text-transform: uppercase;">${p.price_tier || 'Moderate'}</span>
            </div>

            <button onclick="window.location.href='/?q=${encodeURIComponent('Which restaurants are near ' + p.name)}'" class="btn-primary" style="padding: 0.5rem; font-size: 0.8rem;">
              <span>💬</span> Query in Chatbot
            </button>
          </div>
        </div>
      `;
    }).join('');
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  // Initial load
  filterAndRender();
});
