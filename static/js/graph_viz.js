/**
 * Knowledge Graph Visualizer using vis-network
 */

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('network-container');
  const inspector = document.getElementById('nodeInspector');
  const cityFilterBtns = document.querySelectorAll('.filter-btn');
  const searchInput = document.getElementById('graphSearchInput');
  const nodeCountElem = document.getElementById('graphNodeCount');
  const edgeCountElem = document.getElementById('graphEdgeCount');

  let network = null;
  let allNodes = [];
  let allEdges = [];

  loadGraphData();

  cityFilterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      cityFilterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const city = btn.getAttribute('data-city') || '';
      loadGraphData(city);
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const term = e.target.value.toLowerCase().trim();
      if (!term || !network) return;

      const matched = allNodes.find(n => n.raw_data && n.raw_data.name && n.raw_data.name.toLowerCase().includes(term));
      if (matched) {
        network.focus(matched.id, {
          scale: 1.2,
          animation: { duration: 800, easingFunction: 'easeInOutQuad' }
        });
        network.selectNodes([matched.id]);
        showNodeInspector(matched.raw_data);
      }
    });
  }

  async function loadGraphData(city = '') {
    try {
      const url = city ? `/api/graph/data?city=${encodeURIComponent(city)}` : '/api/graph/data';
      const res = await fetch(url);
      const data = await res.json();

      allNodes = data.nodes;
      allEdges = data.edges;

      if (nodeCountElem) nodeCountElem.innerText = `${data.total_nodes} Nodes`;
      if (edgeCountElem) edgeCountElem.innerText = `${data.total_edges} Edges`;

      renderNetwork(data.nodes, data.edges);
    } catch (err) {
      console.error('Failed to load graph data:', err);
    }
  }

  function renderNetwork(nodes, edges) {
    const data = {
      nodes: new vis.DataSet(nodes),
      edges: new vis.DataSet(edges)
    };

    const options = {
      nodes: {
        shape: 'box',
        borderWidth: 2,
        shadow: true,
        font: { color: '#ffffff', face: 'Outfit, Inter, sans-serif', size: 13 }
      },
      edges: {
        smooth: { type: 'continuous', roundness: 0.2 },
        font: { align: 'middle', size: 10, color: '#94a3b8', strokeWidth: 0 }
      },
      physics: {
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {
          gravitationalConstant: -70,
          centralGravity: 0.015,
          springLength: 120,
          springConstant: 0.06,
          damping: 0.6
        },
        stabilization: { iterations: 150 }
      },
      interaction: {
        hover: true,
        tooltipDelay: 150,
        navigationButtons: true,
        keyboard: true
      }
    };

    if (network) {
      network.destroy();
    }

    network = new vis.Network(container, data, options);

    network.on('click', (params) => {
      if (params.nodes.length > 0) {
        const selectedId = params.nodes[0];
        const selectedNode = allNodes.find(n => n.id === selectedId);
        if (selectedNode && selectedNode.raw_data) {
          showNodeInspector(selectedNode.raw_data);
        }
      } else {
        hideNodeInspector();
      }
    });
  }

  function showNodeInspector(node) {
    if (!inspector) return;
    inspector.style.display = 'block';

    const cat = node.category || 'Place';
    let extra = '';
    if (node.price_inr !== undefined) {
      extra += `<div class="metric-row"><span class="metric-label">Price / Tariff</span><span class="metric-value">₹${node.price_inr}</span></div>`;
    }
    if (node.entry_fee !== undefined) {
      extra += `<div class="metric-row"><span class="metric-label">Entry Fee</span><span class="metric-value">${node.entry_fee === 0 ? 'Free' : '₹' + node.entry_fee}</span></div>`;
    }
    if (node.cuisine) {
      extra += `<div class="metric-row"><span class="metric-label">Cuisine</span><span class="metric-value">${escapeHtml(node.cuisine)}</span></div>`;
    }
    if (node.line) {
      extra += `<div class="metric-row"><span class="metric-label">Metro Line</span><span class="metric-value">${escapeHtml(node.line)}</span></div>`;
    }
    if (node.is_unesco !== undefined) {
      extra += `<div class="metric-row"><span class="metric-label">UNESCO Site</span><span class="metric-value">${node.is_unesco ? 'Yes 🏛️' : 'No'}</span></div>`;
    }

    inspector.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
        <div>
          <span class="place-badge badge-${cat.toLowerCase()}">${escapeHtml(cat)}</span>
          <h3 style="font-family: var(--font-heading); font-size: 1.25rem; font-weight: 700; color: #fff; margin-top: 0.3rem;">
            ${escapeHtml(node.name)}
          </h3>
        </div>
        <button id="closeInspectorBtn" style="background: none; border: none; color: var(--text-muted); font-size: 1.25rem; cursor: pointer;">&times;</button>
      </div>

      <div style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.25rem; line-height: 1.5;">
        ${escapeHtml(node.description || 'Knowledge graph tourist entity.')}
      </div>

      <div style="background: rgba(0,0,0,0.25); border-radius: var(--radius-sm); padding: 0.75rem 1rem; margin-bottom: 1.25rem;">
        <div class="metric-row"><span class="metric-label">City</span><span class="metric-value">${escapeHtml(node.city || 'India')}</span></div>
        <div class="metric-row"><span class="metric-label">Area</span><span class="metric-value">${escapeHtml(node.area || 'N/A')}</span></div>
        <div class="metric-row"><span class="metric-label">Rating</span><span class="metric-value">⭐ ${node.rating || 4.5}</span></div>
        <div class="metric-row"><span class="metric-label">Price Tier</span><span class="metric-value">${node.price_tier || 'Moderate'}</span></div>
        ${extra}
      </div>

      <button onclick="window.location.href='/?q=${encodeURIComponent('Which restaurants are near ' + node.name)}'" class="btn-primary" style="font-size: 0.85rem; padding: 0.6rem;">
        <span>🔍</span> Ask Chatbot About Place
      </button>
    `;

    const closeBtn = document.getElementById('closeInspectorBtn');
    if (closeBtn) closeBtn.addEventListener('click', hideNodeInspector);
  }

  function hideNodeInspector() {
    if (inspector) {
      inspector.innerHTML = `
        <div style="text-align: center; color: var(--text-dim); padding: 3rem 1rem;">
          <div style="font-size: 2.5rem; margin-bottom: 0.75rem;">👆</div>
          <p>Click on any node in the graph to inspect its properties and relationships.</p>
        </div>
      `;
    }
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
});
