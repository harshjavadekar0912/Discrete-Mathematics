/**
 * Tourist Guide Assistant - Chat Client Logic
 * Powered by OpenStreetMap (Nominatim + Overpass API + OSRM)
 */

document.addEventListener('DOMContentLoaded', () => {
  const chatMessages = document.getElementById('chatMessages');
  const chatForm = document.getElementById('chatForm');
  const chatInput = document.getElementById('chatInput');
  const queryChips = document.querySelectorAll('.chip-btn');

  // Handle Quick Chips
  queryChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const queryText = chip.getAttribute('data-query');
      if (queryText) {
        chatInput.value = queryText;
        chatForm.dispatchEvent(new Event('submit'));
      }
    });
  });

  // Handle Form Submit
  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = chatInput.value.trim();
    if (!message) return;

    appendUserMessage(message);
    chatInput.value = '';
    chatInput.focus();

    const typingElem = appendTypingIndicator();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });

      const data = await response.json();
      typingElem.remove();

      if (data.error) {
        appendBotMessage({ answer: `❌ ${data.error}`, places: [] });
      } else {
        appendBotMessage(data);
      }
    } catch (err) {
      typingElem.remove();
      appendBotMessage({
        answer: `Connection error: ${err.message}. Please verify the Flask server is running.`,
        places: []
      });
    }
  });

  function appendUserMessage(text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message user';
    msgDiv.innerHTML = `
      <div class="avatar user-avatar">👤</div>
      <div class="message-bubble">${escapeHtml(text)}</div>
    `;
    chatMessages.appendChild(msgDiv);
    scrollToBottom();
  }

  function appendTypingIndicator() {
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot typing-msg';
    typingDiv.innerHTML = `
      <div class="avatar bot-avatar">🗺️</div>
      <div class="message-bubble" style="color: var(--text-muted); font-style: italic;">
        Searching OpenStreetMap...
      </div>
    `;
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
    return typingDiv;
  }

  function appendBotMessage(data) {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message bot';

    let cardsHtml = '';
    const places = data.places || [];
    if (places.length > 0) {
      cardsHtml = `
        <div class="cards-grid" style="margin-top: 1rem;">
          ${places.slice(0, 8).map(p => renderPlaceCard(p)).join('')}
        </div>
      `;
    }

    // Route info
    let routeHtml = '';
    if (data.route_distance_km || data.route_duration) {
      const osmRouteLink = data.osm_route_url
        ? `&nbsp;|&nbsp; <a href="${escapeHtml(data.osm_route_url)}" target="_blank" rel="noopener" style="color:#38bdf8; font-size:0.82rem;">📍 View route on OSM ↗</a>`
        : '';
      routeHtml = `
        <div class="route-info-box" style="margin-top: 0.75rem; padding: 0.75rem 1rem; background: rgba(2,132,199,0.08); border-left: 3px solid #0284c7; border-radius: 0 var(--radius-sm) var(--radius-sm) 0; font-size: 0.85rem;">
          <strong>📍 ${data.route_distance_km} km</strong> &nbsp;|&nbsp; <strong>⏱️ ${data.route_duration}</strong>${osmRouteLink}
        </div>
      `;
    }

    const formattedAnswer = formatMarkdown(data.answer || '');

    msgDiv.innerHTML = `
      <div class="avatar bot-avatar">🗺️</div>
      <div class="message-bubble">
        <div>${formattedAnswer}</div>
        ${routeHtml}
        ${cardsHtml}
      </div>
    `;

    chatMessages.appendChild(msgDiv);
    scrollToBottom();
  }

  function renderPlaceCard(p) {
    const cat = p.category || 'Place';
    const badgeClass = `badge-${cat.toLowerCase()}`;
    const name = p.name || 'Unknown Place';
    const address = p.address || '';
    const hours = p.opening_hours ? `🕐 ${p.opening_hours}` : '';
    const phone = p.phone ? `📞 ${p.phone}` : '';
    const cuisine = p.cuisine ? `🍴 ${p.cuisine}` : '';
    const website = p.website
      ? `<a href="${escapeHtml(p.website)}" target="_blank" rel="noopener" style="font-size: 0.75rem; color: #a78bfa; text-decoration: none; display: inline-block; margin-top: 0.3rem;">🌐 Website ↗</a>`
      : '';
    const osmLink = p.osm_url
      ? `<a href="${escapeHtml(p.osm_url)}" target="_blank" rel="noopener" style="font-size: 0.75rem; color: #38bdf8; text-decoration: none; display: inline-block; margin-top: 0.4rem;">📍 View on OpenStreetMap ↗</a>`
      : '';

    const metaItems = [hours, phone, cuisine].filter(Boolean);

    return `
      <div class="place-card">
        <span class="place-badge ${badgeClass}">${escapeHtml(cat)}</span>
        <div class="place-title">${escapeHtml(name)}</div>
        <div class="place-meta">
          ${address ? `<span style="font-size:0.78rem; color: var(--text-muted);">📍 ${escapeHtml(address)}</span>` : ''}
        </div>
        ${metaItems.length > 0 ? `<div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; font-size: 0.78rem; margin-top: 0.3rem; color: var(--text-muted);">${metaItems.map(i => `<span>${escapeHtml(i)}</span>`).join('')}</div>` : ''}
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.3rem;">
          ${osmLink}
          ${website}
        </div>
      </div>
    `;
  }

  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function formatMarkdown(text) {
    if (!text) return '';
    // Don't double-escape — the text from the server may contain markdown links [label](url)
    return text
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener" style="color:#38bdf8;">$1</a>')
      .replace(/\n/g, '<br>');
  }
});
