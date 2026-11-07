/**
 * Route Network Analyzer - Discrete Mathematics Graph Engine Client
 * Powered by Leaflet + Vis.js + Python Graph Theory Backend
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const citySelect = document.getElementById('analyzerCitySelect');
  const startSelect = document.getElementById('startNodeSelect');
  const destSelect = document.getElementById('destNodeSelect');
  const destGroup = document.getElementById('destNodeGroup');
  const algoSelect = document.getElementById('algorithmSelect');
  const runBtn = document.getElementById('runAlgorithmBtn');
  const resetBtn = document.getElementById('resetViewBtn');
  const statusIndicator = document.getElementById('statusIndicator');

  // Metrics
  const metricV = document.getElementById('metricVertices');
  const metricE = document.getElementById('metricEdges');
  const metricDensity = document.getElementById('metricDensity');
  const metricDegree = document.getElementById('metricAvgDegree');

  // Summary Banner & Breakdown
  const summaryBanner = document.getElementById('resultSummaryBanner');
  const resultTitle = document.getElementById('resultTitle');
  const resultSubtitle = document.getElementById('resultSubtitle');
  const resultBadges = document.getElementById('resultBadges');
  const pathBreakdownList = document.getElementById('pathBreakdownList');
  const altBox = document.getElementById('alternativeRoutesBox');
  const altContent = document.getElementById('alternativeRoutesContent');

  // Steps log
  const stepsLogBody = document.getElementById('stepsLogBody');

  // Subtabs for Adjacency
  const subtabListBtn = document.getElementById('subtabListBtn');
  const subtabMatrixBtn = document.getElementById('subtabMatrixBtn');
  const panelAdjList = document.getElementById('panelAdjList');
  const panelAdjMatrix = document.getElementById('panelAdjMatrix');
  const adjListGrid = document.getElementById('adjListGrid');
  const matrixTable = document.getElementById('matrixTable');

  // State
  let currentGraphData = null;
  let leafletMap = null;
  let mapMarkers = {};
  let mapEdges = [];
  let pathPolylines = [];
  let visNetwork = null;
  let visNodesDataSet = null;
  let visEdgesDataSet = null;

  // Initialize Leaflet Map
  function initLeafletMap() {
    if (leafletMap) return;
    const mapContainer = document.getElementById('analyzerMap');
    if (!mapContainer) return;

    leafletMap = L.map('analyzerMap').setView([18.5204, 73.8567], 14);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19
    }).addTo(leafletMap);
  }

  // Handle View Mode Tabs
  const tabBtns = document.querySelectorAll('.view-tab-btn');
  const tabPanels = document.querySelectorAll('.tab-panel');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanels.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetId = btn.getAttribute('data-tab');
      const panel = document.getElementById(targetId);
      if (panel) panel.classList.add('active');

      if (targetId === 'tabMap' && leafletMap) {
        setTimeout(() => leafletMap.invalidateSize(), 150);
      } else if (targetId === 'tabTopology' && visNetwork) {
        setTimeout(() => visNetwork.fit(), 150);
      }
    });
  });

  // Handle Adjacency Subtabs
  if (subtabListBtn && subtabMatrixBtn) {
    subtabListBtn.addEventListener('click', () => {
      subtabListBtn.classList.add('active');
      subtabMatrixBtn.classList.remove('active');
      panelAdjList.style.display = 'block';
      panelAdjMatrix.style.display = 'none';
    });
    subtabMatrixBtn.addEventListener('click', () => {
      subtabMatrixBtn.classList.add('active');
      subtabListBtn.classList.remove('active');
      panelAdjList.style.display = 'none';
      panelAdjMatrix.style.display = 'block';
    });
  }

  // Toggle destination field on algorithm change
  if (algoSelect) {
    algoSelect.addEventListener('change', () => {
      const isDijkstra = algoSelect.value === 'dijkstra';
      if (destGroup) {
        destGroup.style.display = isDijkstra ? 'block' : 'none';
      }
    });
  }

  // Fetch & Load Road Network Graph for Selected City
  async function loadCityGraph(cityKey) {
    statusIndicator.innerText = `Loading ${cityKey} road network...`;
    runBtn.disabled = true;

    try {
      const res = await fetch(`/api/network/graph?city=${encodeURIComponent(cityKey)}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      currentGraphData = data;

      // Update Metrics
      const m = data.metrics || {};
      metricV.innerText = m.num_vertices || 0;
      metricE.innerText = m.num_edges || 0;
      metricDensity.innerText = m.density || 0;
      metricAvgDegree.innerText = m.avg_degree || 0;

      // Update Dropdowns
      populateNodeSelectors(data.nodes);

      // Render on Leaflet Map
      renderLeafletGraph(data);

      // Render on Vis.js Topology
      renderVisTopology(data);

      // Render Adjacency Structures
      renderAdjacencyList(data.adjacency_list, data.nodes);
      renderAdjacencyMatrix(data.adjacency_matrix);

      // Center map
      if (leafletMap && data.center) {
        leafletMap.setView([data.center.lat, data.center.lng], 14);
      }

      clearResultsUI();
      statusIndicator.innerText = `Loaded ${data.city_name} (${m.num_vertices} vertices, ${m.num_edges} edges)`;
    } catch (err) {
      statusIndicator.innerText = `Error: ${err.message}`;
    } finally {
      runBtn.disabled = false;
    }
  }

  // Populate Dropdown Options
  function populateNodeSelectors(nodes) {
    startSelect.innerHTML = '';
    destSelect.innerHTML = '';

    nodes.forEach((n, idx) => {
      const opt1 = document.createElement('option');
      opt1.value = n.id;
      opt1.textContent = `${n.label} (deg: ${n.degree})`;
      if (idx === 0) opt1.selected = true;
      startSelect.appendChild(opt1);

      const opt2 = document.createElement('option');
      opt2.value = n.id;
      opt2.textContent = `${n.label} (deg: ${n.degree})`;
      if (idx === nodes.length - 1) opt2.selected = true;
      destSelect.appendChild(opt2);
    });
  }

  // Render Road Network on Leaflet
  function renderLeafletGraph(data) {
    initLeafletMap();
    if (!leafletMap) return;

    // Clear previous markers & edges
    Object.values(mapMarkers).forEach(m => leafletMap.removeLayer(m));
    mapMarkers = {};
    mapEdges.forEach(e => leafletMap.removeLayer(e));
    mapEdges = [];
    clearPathPolylines();

    // Render Edges as Road Polylines
    data.edges.forEach(e => {
      if (e.coords && e.coords.length > 0) {
        const poly = L.polyline(e.coords, {
          color: '#475569',
          weight: 3,
          opacity: 0.65,
          lineJoin: 'round'
        }).bindTooltip(`${e.road} (${e.weight_km} km)`, { sticky: true });
        poly.addTo(leafletMap);
        mapEdges.push(poly);
      }
    });

    // Render Vertices (Nodes)
    data.nodes.forEach(n => {
      const marker = L.circleMarker([n.lat, n.lng], {
        radius: 6,
        fillColor: '#38bdf8',
        color: '#ffffff',
        weight: 2,
        opacity: 0.9,
        fillOpacity: 0.9
      });

      marker.bindPopup(`
        <div style="font-family:Inter,sans-serif; padding:4px;">
          <strong style="color:#0f172a; font-size:13px;">${escapeHtml(n.label)}</strong><br>
          <span style="font-size:11px; color:#64748b;">OSM ID: ${n.osm_id} | Degree: ${n.degree}</span><br>
          <div style="margin-top:6px; display:flex; gap:4px;">
            <button onclick="window.setStartFromMap('${n.id}')" style="background:#0284c7; color:#fff; border:none; padding:2px 8px; border-radius:4px; font-size:11px; cursor:pointer;">Set Start</button>
            <button onclick="window.setDestFromMap('${n.id}')" style="background:#f43f5e; color:#fff; border:none; padding:2px 8px; border-radius:4px; font-size:11px; cursor:pointer;">Set Dest</button>
          </div>
        </div>
      `);

      marker.addTo(leafletMap);
      mapMarkers[n.id] = marker;
    });
  }

  // Expose global helper for popup buttons
  window.setStartFromMap = (nid) => {
    startSelect.value = nid;
    leafletMap.closePopup();
    statusIndicator.innerText = `Start set to ${currentGraphData.nodes.find(n=>n.id===nid)?.label}`;
  };
  window.setDestFromMap = (nid) => {
    destSelect.value = nid;
    leafletMap.closePopup();
    statusIndicator.innerText = `Destination set to ${currentGraphData.nodes.find(n=>n.id===nid)?.label}`;
  };

  // Render Vis.js Topology Graph
  function renderVisTopology(data) {
    const container = document.getElementById('topologyNetwork');
    if (!container || typeof vis === 'undefined') return;

    const visNodes = data.nodes.map(n => ({
      id: n.id,
      label: n.label.replace('Junction (', '').replace(')', ''),
      title: `${n.label}\nDegree: ${n.degree}\nLat: ${n.lat}, Lng: ${n.lng}`,
      color: {
        background: '#0f172a',
        border: '#38bdf8',
        highlight: { background: '#0284c7', border: '#ffffff' }
      },
      font: { color: '#f8fafc', size: 11, face: 'Inter' },
      shape: 'dot',
      size: 14 + (n.degree * 2),
      borderWidth: 2
    }));

    const visEdges = data.edges.map(e => ({
      id: e.id,
      from: e.u,
      to: e.v,
      label: `${e.weight_km}km`,
      title: `${e.road}: ${e.weight_km} km`,
      color: { color: 'rgba(255,255,255,0.25)', highlight: '#38bdf8' },
      font: { color: '#94a3b8', size: 9, align: 'top', background: '#0a0f1d' },
      width: 1.5,
      smooth: { type: 'continuous' }
    }));

    visNodesDataSet = new vis.DataSet(visNodes);
    visEdgesDataSet = new vis.DataSet(visEdges);

    const options = {
      physics: {
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {
          gravitationalConstant: -40,
          centralGravity: 0.008,
          springLength: 90,
          springConstant: 0.08
        },
        stabilization: { iterations: 120 }
      },
      interaction: { hover: true, tooltipDelay: 100 }
    };

    visNetwork = new vis.Network(container, { nodes: visNodesDataSet, edges: visEdgesDataSet }, options);

    visNetwork.on('selectNode', (params) => {
      if (params.nodes.length > 0) {
        const nid = params.nodes[0];
        const nObj = currentGraphData.nodes.find(x => x.id === nid);
        if (nObj && leafletMap) {
          leafletMap.setView([nObj.lat, nObj.lng], 16);
          if (mapMarkers[nid]) mapMarkers[nid].openPopup();
        }
      }
    });

    const fitBtn = document.getElementById('fitTopologyBtn');
    if (fitBtn) fitBtn.onclick = () => visNetwork.fit();
  }

  // Render Adjacency List
  function renderAdjacencyList(adjList, nodes) {
    if (!adjListGrid) return;
    const nodeMap = {};
    if (nodes && Array.isArray(nodes)) {
      nodes.forEach(n => { nodeMap[n.id] = n; });
    }
    adjListGrid.innerHTML = '';

    Object.keys(adjList).forEach(nid => {
      const neighbors = adjList[nid] || [];
      const nodeObj = nodeMap[nid] || { label: nid, degree: neighbors.length };

      const card = document.createElement('div');
      card.className = 'adj-node-card';

      const itemsHtml = neighbors.map(nb => `
        <div class="adj-edge-item">
          <div>
            <strong>${escapeHtml(nb.to_label)}</strong>
            <div class="edge-road">${escapeHtml(nb.road)}</div>
          </div>
          <span class="edge-weight">${nb.weight_km} km</span>
        </div>
      `).join('');

      card.innerHTML = `
        <div class="adj-node-header">
          <span>${escapeHtml(nodeObj.label)}</span>
          <span style="font-size:0.75rem; color:#38bdf8;">deg: ${neighbors.length}</span>
        </div>
        <div>${itemsHtml || '<span style="color:var(--text-dim);">No outgoing edges</span>'}</div>
      `;

      adjListGrid.appendChild(card);
    });
  }

  // Render Adjacency Matrix
  function renderAdjacencyMatrix(matrixData) {
    if (!matrixTable || !matrixData) return;
    const { nodes, matrix } = matrixData;

    let thead = '<thead><tr><th>Vertex</th>';
    nodes.forEach(n => {
      const short = n.label.replace('Junction (', '').slice(0, 10);
      thead += `<th title="${escapeHtml(n.label)}">${escapeHtml(short)}</th>`;
    });
    thead += '</tr></thead>';

    let tbody = '<tbody>';
    matrix.forEach((row, i) => {
      const n = nodes[i];
      tbody += `<tr><th class="row-header" title="${escapeHtml(n.label)}">${escapeHtml(n.label)}</th>`;
      row.forEach(val => {
        if (val === 0.0) {
          tbody += '<td class="zero-val">0</td>';
        } else if (val === null) {
          tbody += '<td class="inf-val">∞</td>';
        } else {
          tbody += `<td class="weight-val">${val}</td>`;
        }
      });
      tbody += '</tr>';
    });
    tbody += '</tbody>';

    matrixTable.innerHTML = thead + tbody;
  }

  // Clear Path Polylines
  function clearPathPolylines() {
    pathPolylines.forEach(p => leafletMap && leafletMap.removeLayer(p));
    pathPolylines = [];
  }

  // Clear Results UI
  function clearResultsUI() {
    clearPathPolylines();
    summaryBanner.style.display = 'none';
    pathBreakdownList.innerHTML = `
      <p style="text-align: center; padding: 2rem 0; color: var(--text-muted);">
        Select a Start and Destination vertex, then click <strong>Run</strong> to compute shortest path or traversal.
      </p>
    `;
    altBox.style.display = 'none';
    stepsLogBody.innerHTML = `
      <tr>
        <td colspan="4" style="text-align:center; padding:2rem; color:var(--text-muted);">
          Run an algorithm to inspect the step-by-step Discrete Mathematics progression.
        </td>
      </tr>
    `;
  }

  // Run Selected Algorithm
  async function runAlgorithm() {
    if (!currentGraphData) return;
    const algo = algoSelect.value;
    const startId = startSelect.value;
    const destId = destSelect.value;
    const city = citySelect.value;

    if (!startId) return alert('Please select a start vertex');
    if (algo === 'dijkstra' && !destId) return alert('Please select a destination vertex');
    if (algo === 'dijkstra' && startId === destId) return alert('Start and destination vertices must be distinct');

    runBtn.disabled = true;
    runBtn.innerHTML = '<span>Computing...</span> <span>⏳</span>';
    statusIndicator.innerText = `Executing ${algo.toUpperCase()} algorithm...`;

    try {
      if (algo === 'dijkstra') {
        const res = await fetch('/api/network/dijkstra', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ city, start_id: startId, dest_id: destId })
        });
        const data = await res.json();
        handleDijkstraResult(data);
      } else if (algo === 'bfs') {
        const res = await fetch('/api/network/bfs', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ city, start_id: startId })
        });
        const data = await res.json();
        handleBfsResult(data);
      } else if (algo === 'dfs') {
        const res = await fetch('/api/network/dfs', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ city, start_id: startId })
        });
        const data = await res.json();
        handleDfsResult(data);
      }
    } catch (err) {
      alert(`Execution error: ${err.message}`);
    } finally {
      runBtn.disabled = false;
      runBtn.innerHTML = '<span>Run</span> <span>⚡</span>';
    }
  }

  // Handle Dijkstra Result
  function handleDijkstraResult(data) {
    const primary = data.primary;
    if (!primary || !primary.success) {
      alert('No path found between selected vertices');
      return;
    }

    clearPathPolylines();
    statusIndicator.innerText = `Dijkstra completed: ${primary.total_distance_km} km (${primary.path.length} vertices)`;

    // Summary Banner
    summaryBanner.style.display = 'block';
    resultTitle.innerText = `🚀 Shortest Path: ${primary.total_distance_km} km`;
    resultSubtitle.innerText = `${primary.start.label} ➔ ${primary.destination.label}`;
    resultBadges.innerHTML = `
      <span class="hero-pill" style="margin:0; background:rgba(2,132,199,0.2); color:#38bdf8;">Vertices: ${primary.path.length}</span>
      <span class="hero-pill" style="margin:0; background:rgba(16,185,129,0.2); color:#34d399;">Distance: ${primary.total_distance_km} km</span>
      <span class="hero-pill" style="margin:0; background:rgba(139,92,246,0.2); color:#c084fc;">Settled: ${primary.visited_count}</span>
    `;

    // Highlight on Leaflet
    const allCoords = [];
    primary.path_edges.forEach(e => {
      if (e.coords && e.coords.length > 0) {
        const poly = L.polyline(e.coords, {
          color: '#38bdf8',
          weight: 6,
          opacity: 0.95
        }).addTo(leafletMap);
        pathPolylines.push(poly);
        e.coords.forEach(c => allCoords.push(c));
      }
    });

    // Render Alternative path if available
    const alts = data.alternatives || [];
    if (alts.length > 0 && alts[0].success) {
      const alt1 = alts[0];
      alt1.path_edges.forEach(e => {
        if (e.coords && e.coords.length > 0) {
          const altPoly = L.polyline(e.coords, {
            color: '#c084fc',
            weight: 4,
            dashArray: '6, 8',
            opacity: 0.85
          }).addTo(leafletMap);
          pathPolylines.push(altPoly);
        }
      });

      altBox.style.display = 'block';
      altContent.innerHTML = `
        <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem;">
          <span>Alternative Distance:</span>
          <strong style="color:#c084fc;">${alt1.total_distance_km} km</strong>
        </div>
        <div style="font-size:0.75rem; color:var(--text-dim);">
          +${Math.round((alt1.total_distance_km - primary.total_distance_km)*1000)}m longer via ${alt1.path_labels[1] || 'alternative road'}
        </div>
      `;
    } else {
      altBox.style.display = 'none';
    }

    if (allCoords.length > 0 && leafletMap) {
      leafletMap.fitBounds(L.latLngBounds(allCoords), { padding: [40, 40] });
    }

    // Path Breakdown list in sidebar
    let breakdownHtml = `<div style="font-weight:700; color:#38bdf8; margin-bottom:0.75rem;">Step-by-step Road Path:</div>`;
    primary.path_edges.forEach((e, idx) => {
      breakdownHtml += `
        <div style="padding:0.4rem 0; border-bottom:1px solid rgba(255,255,255,0.05);">
          <div style="display:flex; justify-content:space-between; font-weight:600;">
            <span>${idx + 1}. ${escapeHtml(e.road)}</span>
            <span style="color:#34d399;">${e.weight_km} km</span>
          </div>
          <div style="font-size:0.75rem; color:var(--text-dim);">
            ${escapeHtml(currentGraphData.nodes.find(n=>n.id===e.u)?.label || '')} → ${escapeHtml(currentGraphData.nodes.find(n=>n.id===e.v)?.label || '')}
          </div>
        </div>
      `;
    });
    pathBreakdownList.innerHTML = breakdownHtml;

    // Steps Log
    renderStepsLog(primary.steps_log, 'Dijkstra Priority Queue Relaxations');

    // Highlight on Vis.js Topology
    if (visNodesDataSet && visEdgesDataSet) {
      const pathSet = new Set(primary.path);
      const edgeIds = new Set(primary.path_edges.map(e => e.id));

      visNodesDataSet.forEach(node => {
        if (node.id === primary.start.id) {
          visNodesDataSet.update({ id: node.id, color: { background: '#10b981', border: '#ffffff' }, size: 24 });
        } else if (node.id === primary.destination.id) {
          visNodesDataSet.update({ id: node.id, color: { background: '#f43f5e', border: '#ffffff' }, size: 24 });
        } else if (pathSet.has(node.id)) {
          visNodesDataSet.update({ id: node.id, color: { background: '#0284c7', border: '#38bdf8' }, size: 20 });
        } else {
          visNodesDataSet.update({ id: node.id, color: { background: '#0f172a', border: 'rgba(255,255,255,0.2)' }, size: 12 });
        }
      });

      visEdgesDataSet.forEach(edge => {
        if (edgeIds.has(edge.id)) {
          visEdgesDataSet.update({ id: edge.id, color: { color: '#38bdf8' }, width: 4 });
        } else {
          visEdgesDataSet.update({ id: edge.id, color: { color: 'rgba(255,255,255,0.1)' }, width: 1 });
        }
      });
    }
  }

  // Handle BFS Result
  function handleBfsResult(data) {
    clearPathPolylines();
    statusIndicator.innerText = `BFS traversal finished: ${data.visited_count} vertices explored`;

    summaryBanner.style.display = 'block';
    resultTitle.innerText = `🌊 Breadth-First Search (BFS) Traversal`;
    resultSubtitle.innerText = `Explored from ${data.start.label}`;
    resultBadges.innerHTML = `
      <span class="hero-pill" style="margin:0; background:rgba(2,132,199,0.2); color:#38bdf8;">Vertices: ${data.visited_count}</span>
      <span class="hero-pill" style="margin:0; background:rgba(16,185,129,0.2); color:#34d399;">Max Depth: ${Math.max(...Object.values(data.levels))} hops</span>
    `;

    // Render tree edges on Leaflet
    const allCoords = [];
    data.tree_edges.forEach(e => {
      if (e.coords && e.coords.length > 0) {
        const poly = L.polyline(e.coords, {
          color: '#10b981',
          weight: 4,
          opacity: 0.8
        }).addTo(leafletMap);
        pathPolylines.push(poly);
        e.coords.forEach(c => allCoords.push(c));
      }
    });

    if (allCoords.length > 0 && leafletMap) {
      leafletMap.fitBounds(L.latLngBounds(allCoords), { padding: [40, 40] });
    }

    // Breakdown
    pathBreakdownList.innerHTML = `
      <div style="font-weight:700; color:#10b981; margin-bottom:0.75rem;">BFS Level Sets (Hops from Start):</div>
      ${data.visited_order.slice(0, 15).map(nid => {
        const nObj = currentGraphData.nodes.find(x => x.id === nid);
        return `
          <div style="padding:0.35rem 0; border-bottom:1px solid rgba(255,255,255,0.05); display:flex; justify-content:space-between;">
            <span>${escapeHtml(nObj ? nObj.label : nid)}</span>
            <span style="color:#38bdf8; font-weight:bold;">Level ${data.levels[nid]}</span>
          </div>
        `;
      }).join('')}
    `;

    renderStepsLog(data.steps_log, 'BFS FIFO Queue Transitions');
  }

  // Handle DFS Result
  function handleDfsResult(data) {
    clearPathPolylines();
    statusIndicator.innerText = `DFS traversal finished: ${data.visited_count} vertices explored`;

    summaryBanner.style.display = 'block';
    resultTitle.innerText = `🌲 Depth-First Search (DFS) Traversal`;
    resultSubtitle.innerText = `Explored from ${data.start.label}`;
    resultBadges.innerHTML = `
      <span class="hero-pill" style="margin:0; background:rgba(139,92,246,0.2); color:#c084fc;">Vertices: ${data.visited_count}</span>
      <span class="hero-pill" style="margin:0; background:rgba(245,158,11,0.2); color:#fbbf24;">Edges in Spanning Tree: ${data.tree_edges.length}</span>
    `;

    // Render tree edges on Leaflet
    const allCoords = [];
    data.tree_edges.forEach(e => {
      if (e.coords && e.coords.length > 0) {
        const poly = L.polyline(e.coords, {
          color: '#8b5cf6',
          weight: 4,
          opacity: 0.85
        }).addTo(leafletMap);
        pathPolylines.push(poly);
        e.coords.forEach(c => allCoords.push(c));
      }
    });

    if (allCoords.length > 0 && leafletMap) {
      leafletMap.fitBounds(L.latLngBounds(allCoords), { padding: [40, 40] });
    }

    pathBreakdownList.innerHTML = `
      <div style="font-weight:700; color:#c084fc; margin-bottom:0.75rem;">DFS Discovery & Finish Timestamps:</div>
      ${data.visited_order.slice(0, 15).map(nid => {
        const nObj = currentGraphData.nodes.find(x => x.id === nid);
        return `
          <div style="padding:0.35rem 0; border-bottom:1px solid rgba(255,255,255,0.05); display:flex; justify-content:space-between;">
            <span>${escapeHtml(nObj ? nObj.label : nid)}</span>
            <span style="color:#fbbf24; font-size:0.78rem;">d: ${data.discovery_time[nid]} / f: ${data.finish_time[nid]}</span>
          </div>
        `;
      }).join('')}
    `;

    renderStepsLog(data.steps_log, 'DFS Call Stack Transitions');
  }

  // Render Steps Log Table
  function renderStepsLog(steps, title) {
    if (!stepsLogBody || !steps) return;
    stepsLogBody.innerHTML = steps.map(s => `
      <tr>
        <td style="color:#38bdf8; font-weight:bold;">${s.step}</td>
        <td>${escapeHtml(s.action)}</td>
        <td>${escapeHtml(s.vertex_label || s.vertex_id || '--')}</td>
        <td style="color:#34d399; font-weight:600;">${s.cumulative_cost_km !== undefined ? s.cumulative_cost_km + ' km' : (s.level !== undefined ? 'Level ' + s.level : '--')}</td>
      </tr>
    `).join('');
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  // Event Listeners
  citySelect.addEventListener('change', () => loadCityGraph(citySelect.value));
  runBtn.addEventListener('click', runAlgorithm);
  resetBtn.addEventListener('click', () => {
    clearResultsUI();
    if (currentGraphData) {
      renderLeafletGraph(currentGraphData);
      renderVisTopology(currentGraphData);
      statusIndicator.innerText = 'Reset view';
    }
  });

  // Check query parameter ?city=
  const urlParams = new URLSearchParams(window.location.search);
  const initialCity = urlParams.get('city') || 'pune';
  citySelect.value = initialCity;

  // Initial Load
  loadCityGraph(initialCity);
});

