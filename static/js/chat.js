/**
 * Tourist Guide Knowledge Graph Chatbot - Chat Client Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  const chatMessages = document.getElementById('chatMessages');
  const chatForm = document.getElementById('chatForm');
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');
  const queryChips = document.querySelectorAll('.chip-btn');
  const statusBadge = document.getElementById('statusBadge');
  const neo4jModal = document.getElementById('neo4jModal');
  const closeModalBtn = document.getElementById('closeModalBtn');
  const neo4jForm = document.getElementById('neo4jForm');
  const seedBtn = document.getElementById('seedBtn');

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

    // Append user message
    appendUserMessage(message);
    chatInput.value = '';
    chatInput.focus();

    // Show bot typing indicator
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
        appendBotMessage({
          answer: `Error: ${data.error}`,
          cypher_query: null,
          discrete_math_concept: null,
          records: []
        });
      } else {
        appendBotMessage(data);
      }
    } catch (err) {
      typingElem.remove();
      appendBotMessage({
        answer: `Connection error: ${err.message}. Please verify the Flask server is running.`,
        cypher_query: null,
        discrete_math_concept: null,
        records: []
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
      <div class="avatar bot-avatar">🧭</div>
      <div class="message-bubble" style="color: var(--text-muted); font-style: italic;">
        Querying Knowledge Graph with Cypher...
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
    if (data.records && data.records.length > 0) {
      cardsHtml = `
        <div class="cards-grid">
          ${data.records.slice(0, 6).map(r => renderPlaceCard(r)).join('')}
        </div>
      `;
    }

    let cypherHtml = '';
    if (data.cypher_query) {
      cypherHtml = `
        <div class="cypher-preview">
          <div class="cypher-header">
            <span>⚡ Executed Cypher Query (${escapeHtml(data.execution_engine || 'Graph Engine')})</span>
            <button class="copy-btn" onclick="navigator.clipboard.writeText(\`${escapeJsString(data.cypher_query)}\`); this.innerText='Copied!'; setTimeout(()=>this.innerText='Copy', 1500)" style="background: none; border: none; color: #38bdf8; cursor: pointer; font-size: 0.75rem;">Copy</button>
          </div>
          <pre class="cypher-code"><code>${escapeHtml(data.cypher_query)}</code></pre>
        </div>
      `;
    }

    let mathHtml = '';
    if (data.discrete_math_concept) {
      mathHtml = `
        <div class="math-concept-card">
          <div class="math-concept-title">
            <span>📐</span> Discrete Mathematics Mapping
          </div>
          <div>${escapeHtml(data.discrete_math_concept)}</div>
        </div>
      `;
    }

    // Format markdown bolding in answer
    const formattedAnswer = formatMarkdown(data.answer);

    msgDiv.innerHTML = `
      <div class="avatar bot-avatar">🧭</div>
      <div class="message-bubble">
        <div>${formattedAnswer}</div>
        ${cardsHtml}
        ${cypherHtml}
        ${mathHtml}
      </div>
    `;

    chatMessages.appendChild(msgDiv);
    scrollToBottom();
  }

  function renderPlaceCard(record) {
    const cat = record.category || 'Place';
    const badgeClass = `badge-${cat.toLowerCase()}`;
    const name = record.name || record.station_name || 'Location';
    const area = record.area ? `📍 ${record.area}` : '';
    const rating = record.rating ? `⭐ ${record.rating}` : '';
    const dist = record.distance_km !== undefined ? `🚶 ${record.distance_km} km` : '';
    
    let extra = '';
    if (record.price_inr !== undefined) {
      extra = `<div class="place-price">₹${record.price_inr}</div>`;
    } else if (record.entry_fee !== undefined) {
      extra = `<div class="place-price">${record.entry_fee === 0 ? 'Free Entry' : 'Entry: ₹' + record.entry_fee}</div>`;
    } else if (record.cuisine) {
      extra = `<div style="font-size: 0.8rem; color: #cbd5e1;">🍲 ${record.cuisine}</div>`;
    } else if (record.line) {
      extra = `<div style="font-size: 0.8rem; color: #38bdf8;">🚇 ${record.line}</div>`;
    }

    return `
      <div class="place-card">
        <span class="place-badge ${badgeClass}">${escapeHtml(cat)}</span>
        <div class="place-title">${escapeHtml(name)}</div>
        <div class="place-meta">
          ${area ? `<span>${escapeHtml(area)}</span>` : ''}
          ${rating ? `<span>${rating}</span>` : ''}
          ${dist ? `<span>${dist}</span>` : ''}
        </div>
        ${extra}
      </div>
    `;
  }

  function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function escapeJsString(str) {
    if (!str) return '';
    return str.replace(/`/g, '\\`').replace(/\$/g, '\\$');
  }

  function formatMarkdown(text) {
    if (!text) return '';
    // Format bold **text** -> <strong>text</strong>
    let out = escapeHtml(text)
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>');
    return out;
  }

  // Neo4j Modal Handlers
  if (statusBadge && neo4jModal) {
    statusBadge.addEventListener('click', () => {
      neo4jModal.classList.add('active');
    });
  }

  if (closeModalBtn) {
    closeModalBtn.addEventListener('click', () => {
      neo4jModal.classList.remove('active');
    });
  }

  if (neo4jModal) {
    neo4jModal.addEventListener('click', (e) => {
      if (e.target === neo4jModal) {
        neo4jModal.classList.remove('active');
      }
    });
  }

  if (neo4jForm) {
    neo4jForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const uri = document.getElementById('neo4jUri').value.trim();
      const user = document.getElementById('neo4jUser').value.trim();
      const password = document.getElementById('neo4jPass').value.trim();
      const resultElem = document.getElementById('neo4jResult');

      resultElem.innerText = 'Connecting to Neo4j...';
      try {
        const res = await fetch('/api/neo4j/connect', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ uri, user, password })
        });
        const data = await res.json();
        resultElem.innerText = data.message;
        if (data.connected) {
          resultElem.style.color = '#34d399';
          setTimeout(() => location.reload(), 1200);
        } else {
          resultElem.style.color = '#f87171';
        }
      } catch (err) {
        resultElem.innerText = `Error: ${err.message}`;
        resultElem.style.color = '#f87171';
      }
    });
  }

  if (seedBtn) {
    seedBtn.addEventListener('click', async () => {
      const resultElem = document.getElementById('neo4jResult');
      resultElem.innerText = 'Seeding Neo4j database...';
      try {
        const res = await fetch('/api/neo4j/seed', { method: 'POST' });
        const data = await res.json();
        resultElem.innerText = data.message || data.error;
        resultElem.style.color = data.success ? '#34d399' : '#f87171';
      } catch (err) {
        resultElem.innerText = `Error: ${err.message}`;
        resultElem.style.color = '#f87171';
      }
    });
  }
});
