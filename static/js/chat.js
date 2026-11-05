/**
 * Tourist Guide Assistant - Chat Client Logic
 * Powered by Google Maps Platform
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
        Searching Google Maps...
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
      routeHtml = `
        <div class="route-info-box" style="margin-top: 0.75rem; padding: 0.75rem 1rem; background: rgba(2,132,199,0.08); border-left: 3px solid #0284c7; border-radius: 0 var(--radius-sm) var(--radius-sm) 0; font-size: 0.85rem;">
          <strong>📏 ${data.route_distance_km} km</strong> &nbsp;|&nbsp; <strong>⏱️ ${data.route_duration}</strong>
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
    const rating = p.rating ? `⭐ ${p.rating}` : '';
    const reviews = p.review_count ? `(${p.review_count.toLocaleString()})` : '';
    const hours = p.opening_hours ? `🕐 ${p.opening_hours}` : '';
    const price = p.price_label || '';
    const mapsUri = p.maps_uri || '';
    const summary = p.summary || '';

    const mapsLink = mapsUri
      ? `<a href="${escapeHtml(mapsUri)}" target="_blank" rel="noopener" style="font-size: 0.75rem; color: #38bdf8; text-decoration: none; display: inline-block; margin-top: 0.4rem;">📍 Open in Google Maps ↗</a>`
      : '';

    return `
      <div class="place-card">
        <span class="place-badge ${badgeClass}">${escapeHtml(cat)}</span>
        <div class="place-title">${escapeHtml(name)}</div>
        <div class="place-meta">
          ${address ? `<span style="font-size:0.78rem; color: var(--text-muted);">📍 ${escapeHtml(address)}</span>` : ''}
        </div>
        <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; font-size: 0.8rem; margin-top: 0.3rem; color: var(--text-muted);">
          ${rating ? `<span style="color:#fbbf24;">${escapeHtml(rating)}</span>` : ''}
          ${reviews ? `<span>${escapeHtml(reviews)}</span>` : ''}
          ${hours ? `<span>${escapeHtml(hours)}</span>` : ''}
        </div>
        ${price ? `<div class="place-price" style="margin-top: 0.3rem; font-size: 0.8rem;">${escapeHtml(price)}</div>` : ''}
        ${summary ? `<div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 0.4rem; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">${escapeHtml(summary)}</div>` : ''}
        ${mapsLink}
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
    return escapeHtml(text)
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>');
  }
});
