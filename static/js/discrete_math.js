/**
 * Discrete Mathematics Interactive Algorithms Client Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  // Navigation Tabs
  const tabBtns = document.querySelectorAll('.tab-btn');
  const sections = document.querySelectorAll('.math-section');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      sections.forEach(s => s.classList.remove('active'));

      btn.classList.add('active');
      const targetId = btn.getAttribute('data-target');
      const targetSection = document.getElementById(targetId);
      if (targetSection) targetSection.classList.add('active');
    });
  });

  // =========================================================================
  // 1. BFS & DFS TRAVERSAL
  // =========================================================================
  const bfsForm = document.getElementById('bfsForm');
  const bfsResultCard = document.getElementById('bfsResultCard');
  let currentSteps = [];
  let currentStepIdx = 0;
  let playInterval = null;

  if (bfsForm) {
    bfsForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const startId = document.getElementById('bfsStartNode').value;
      const algoType = document.getElementById('traversalAlgoType').value;
      const maxDepth = document.getElementById('bfsDepth').value;

      const endpoint = algoType === 'BFS' ? '/api/algorithms/bfs' : '/api/algorithms/dfs';

      try {
        const res = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ start_id: startId, max_depth: parseInt(maxDepth) })
        });
        const data = await res.json();
        renderTraversalResults(data, algoType);
      } catch (err) {
        alert('Failed to execute traversal: ' + err.message);
      }
    });
  }

  function renderTraversalResults(data, algoType) {
    if (!bfsResultCard) return;
    currentSteps = data.steps || [];
    currentStepIdx = 0;
    clearInterval(playInterval);

    const isBfs = algoType === 'BFS';
    const queueLabel = isBfs ? 'FIFO Queue' : 'LIFO Stack';

    bfsResultCard.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
        <div>
          <h3 style="font-family: var(--font-heading); font-size: 1.25rem; font-weight: 700; color: #fff;">
            ${escapeHtml(data.algorithm)}
          </h3>
          <p style="color: var(--text-muted); font-size: 0.85rem;">
            Start: <strong>${escapeHtml(data.start_node)}</strong> | Total Visited: <strong>${data.total_visited} places</strong> | Complexity: <code style="color: #38bdf8;">${data.complexity}</code>
          </p>
        </div>
        <div style="display: flex; gap: 0.5rem;">
          <button id="stepPrevBtn" class="btn-primary" style="padding: 0.4rem 0.8rem; font-size: 0.8rem; width: auto;">⏮ Prev</button>
          <button id="stepPlayBtn" class="btn-primary" style="padding: 0.4rem 0.8rem; font-size: 0.8rem; width: auto; background: #10b981;">▶ Play</button>
          <button id="stepNextBtn" class="btn-primary" style="padding: 0.4rem 0.8rem; font-size: 0.8rem; width: auto;">Next ⏭</button>
        </div>
      </div>

      <!-- Step Visualizer Card -->
      <div id="stepDetailBox" style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1.25rem; margin-bottom: 1.5rem;">
        <!-- Injected dynamically -->
      </div>

      <!-- Complete Traversal Order -->
      <div style="margin-bottom: 1rem;">
        <span class="form-label">Full Traversal Sequence:</span>
        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
          ${(data.traversal_order || Object.keys(data.discovery_times || {})).map((name, i) => `
            <span class="badge-tag" style="background: rgba(2, 132, 199, 0.2); color: #38bdf8; font-size: 0.85rem; padding: 0.35rem 0.7rem;">
              ${i + 1}. ${escapeHtml(name)}
            </span>
          `).join('')}
        </div>
      </div>
    `;

    document.getElementById('stepPrevBtn').addEventListener('click', () => {
      clearInterval(playInterval);
      if (currentStepIdx > 0) {
        currentStepIdx--;
        showStep(currentStepIdx, queueLabel);
      }
    });

    document.getElementById('stepNextBtn').addEventListener('click', () => {
      clearInterval(playInterval);
      if (currentStepIdx < currentSteps.length - 1) {
        currentStepIdx++;
        showStep(currentStepIdx, queueLabel);
      }
    });

    const playBtn = document.getElementById('stepPlayBtn');
    playBtn.addEventListener('click', () => {
      if (playInterval) {
        clearInterval(playInterval);
        playInterval = null;
        playBtn.innerText = '▶ Play';
      } else {
        playBtn.innerText = '⏸ Pause';
        playInterval = setInterval(() => {
          if (currentStepIdx < currentSteps.length - 1) {
            currentStepIdx++;
            showStep(currentStepIdx, queueLabel);
          } else {
            clearInterval(playInterval);
            playInterval = null;
            playBtn.innerText = '▶ Replay';
            currentStepIdx = 0;
          }
        }, 1200);
      }
    });

    if (currentSteps.length > 0) {
      showStep(0, queueLabel);
    }
  }

  function showStep(idx, queueLabel) {
    const box = document.getElementById('stepDetailBox');
    if (!box || !currentSteps[idx]) return;

    const s = currentSteps[idx];
    const items = s.queue || s.stack || [];

    box.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
        <span class="badge-tag ${s.action.includes('POP') ? 'pop' : 'push'}" style="font-size: 0.8rem; padding: 0.3rem 0.6rem;">
          Step ${s.step} / ${currentSteps.length}: ${escapeHtml(s.action)}
        </span>
        <span style="font-size: 0.85rem; color: #a78bfa; font-weight: 600;">
          ${s.timestamp ? escapeHtml(s.timestamp) : ''}
        </span>
      </div>

      <div style="font-size: 0.95rem; margin-bottom: 1rem; color: #f8fafc;">
        ${escapeHtml(s.description)}
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
        <div style="background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: var(--radius-sm);">
          <span style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">
            ${queueLabel} State:
          </span>
          <div style="display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.4rem;">
            ${items.length === 0 ? '<span style="color: var(--text-dim); font-size: 0.8rem;">Empty</span>' : items.map(item => `
              <span class="badge-tag" style="background: rgba(56, 189, 248, 0.2); color: #38bdf8;">${escapeHtml(item)}</span>
            `).join('')}
          </div>
        </div>

        <div style="background: rgba(0,0,0,0.3); padding: 0.75rem; border-radius: var(--radius-sm);">
          <span style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">
            Visited Set:
          </span>
          <div style="display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.4rem;">
            ${(s.visited || []).map(item => `
              <span class="badge-tag" style="background: rgba(16, 185, 129, 0.2); color: #34d399;">${escapeHtml(item)}</span>
            `).join('')}
          </div>
        </div>
      </div>
    `;
  }

  // =========================================================================
  // 2. DIJKSTRA'S SHORTEST PATH ALGORITHM
  // =========================================================================
  const dijkstraForm = document.getElementById('dijkstraForm');
  const dijkstraResult = document.getElementById('dijkstraResult');

  if (dijkstraForm) {
    dijkstraForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const startId = document.getElementById('dijkstraStart').value;
      const endId = document.getElementById('dijkstraEnd').value;

      try {
        const res = await fetch('/api/algorithms/dijkstra', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ start_id: startId, end_id: endId })
        });
        const data = await res.json();
        renderDijkstraResults(data);
      } catch (err) {
        alert('Failed to execute Dijkstra: ' + err.message);
      }
    });
  }

  function renderDijkstraResults(data) {
    if (!dijkstraResult) return;

    if (!data.found) {
      dijkstraResult.innerHTML = `
        <div style="padding: 2rem; text-align: center; color: #f87171;">
          ⚠️ ${escapeHtml(data.message || 'No route found.')}
        </div>
      `;
      return;
    }

    const routeLegs = (data.path_details || []).map((leg, idx) => `
      <div style="display: flex; align-items: center; gap: 0.75rem;">
        <div style="width: 28px; height: 28px; border-radius: 50%; background: #0284c7; color: #fff; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: 700;">
          ${idx + 1}
        </div>
        <div>
          <div style="font-weight: 600; color: #fff;">${escapeHtml(leg.name)}</div>
          <div style="font-size: 0.78rem; color: var(--text-muted);">${escapeHtml(leg.category || '')} (${escapeHtml(leg.area || '')})</div>
          ${leg.travel_from_prev ? `<div style="font-size: 0.75rem; color: #38bdf8;">↳ ${escapeHtml(leg.travel_from_prev)}</div>` : ''}
        </div>
      </div>
    `).join('<div style="margin: 0.35rem 0 0.35rem 13px; border-left: 2px dashed rgba(255,255,255,0.2); height: 18px;"></div>');

    const relaxationRows = (data.relaxation_steps || []).map(step => `
      <tr>
        <td><strong>#${step.step}</strong></td>
        <td>${escapeHtml(step.current_node)}</td>
        <td>${escapeHtml(step.neighbor)}</td>
        <td>${step.weight_km} km</td>
        <td>${step.old_distance} km</td>
        <td>${step.tentative_distance} km</td>
        <td>
          <span class="badge-tag ${step.relaxed ? 'relaxed' : 'kept'}">
            ${step.relaxed ? '✓ RELAXED' : 'KEPT'}
          </span>
        </td>
      </tr>
    `).join('');

    dijkstraResult.innerHTML = `
      <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1.25rem; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <div>
            <h4 style="font-family: var(--font-heading); font-size: 1.15rem; color: #34d399; font-weight: 700;">
              ✨ Optimal Shortest Path Found: ${data.total_distance_km} km
            </h4>
            <div style="font-size: 0.85rem; color: var(--text-muted);">
              From <strong>${escapeHtml(data.start_node)}</strong> to <strong>${escapeHtml(data.end_node)}</strong>
            </div>
          </div>
          <span class="hero-pill" style="margin: 0; background: rgba(16, 185, 129, 0.15); color: #34d399; border-color: rgba(16, 185, 129, 0.3);">
            ${data.complexity}
          </span>
        </div>

        <div style="padding: 1rem; background: rgba(0,0,0,0.3); border-radius: var(--radius-sm); margin-bottom: 1rem;">
          ${routeLegs}
        </div>
      </div>

      <h4 style="font-family: var(--font-heading); font-size: 1rem; margin-bottom: 0.75rem; color: #fff;">
        🔬 Step-by-Step Edge Relaxation Table (d[v] = min(d[v], d[u] + w(u,v)))
      </h4>
      <div class="trace-table-container">
        <table class="trace-table">
          <thead>
            <tr>
              <th>Step</th>
              <th>Current Node (u)</th>
              <th>Neighbor (v)</th>
              <th>Weight w(u,v)</th>
              <th>Old d[v]</th>
              <th>d[u] + w(u,v)</th>
              <th>Decision</th>
            </tr>
          </thead>
          <tbody>
            ${relaxationRows}
          </tbody>
        </table>
      </div>
    `;
  }

  // =========================================================================
  // 3. SET THEORY OPERATIONS
  // =========================================================================
  const setForm = document.getElementById('setForm');
  const setResultCard = document.getElementById('setResultCard');

  if (setForm) {
    setForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const setACat = document.getElementById('setACategory').value;
      const setACity = document.getElementById('setACity').value;
      const setBCat = document.getElementById('setBCategory').value;
      const setBCity = document.getElementById('setBCity').value;
      const op = document.getElementById('setOperation').value;

      const setA = {
        category: setACat || undefined,
        city: setACity || undefined,
        label: `${setACat || 'All Categories'} in ${setACity || 'Both Cities'}`
      };
      const setB = {
        category: setBCat || undefined,
        city: setBCity || undefined,
        label: `${setBCat || 'All Categories'} in ${setBCity || 'Both Cities'}`
      };

      try {
        const res = await fetch('/api/sets/operate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ set_a: setA, set_b: setB, operation: op })
        });
        const data = await res.json();
        renderSetResults(data);
      } catch (err) {
        alert('Failed to execute set operation: ' + err.message);
      }
    });
  }

  function renderSetResults(data) {
    if (!setResultCard) return;

    setResultCard.innerHTML = `
      <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1.25rem; margin-bottom: 1.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
          <h3 style="font-family: var(--font-heading); font-size: 1.25rem; color: #fff;">
            ${escapeHtml(data.symbol)} — Result: ${data.cardinality_Result} Elements
          </h3>
          <span style="font-family: var(--font-mono); font-size: 0.85rem; color: #38bdf8;">
            ${escapeHtml(data.mathematical_definition)}
          </span>
        </div>

        <div style="background: rgba(139, 92, 246, 0.1); border-left: 3px solid #8b5cf6; padding: 0.75rem 1rem; border-radius: 0 8px 8px 0; font-size: 0.85rem; margin-bottom: 1rem;">
          <strong>Principle of Inclusion-Exclusion (PIE):</strong><br>
          Formula: <code>${data.inclusion_exclusion_principle.formula}</code><br>
          Calculation: <code>${data.inclusion_exclusion_principle.calculation}</code> 
          (Holds: <span style="color: #34d399; font-weight: 700;">${data.inclusion_exclusion_principle.holds ? 'TRUE ✓' : 'FALSE'}</span>)
        </div>

        <!-- Cardinality Badges -->
        <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
          <span class="badge-tag" style="background: rgba(2, 132, 199, 0.2); color: #38bdf8;">|A| = ${data.cardinality_A}</span>
          <span class="badge-tag" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24;">|B| = ${data.cardinality_B}</span>
          <span class="badge-tag" style="background: rgba(139, 92, 246, 0.2); color: #c084fc;">|A ∩ B| = ${data.cardinality_Intersection}</span>
          <span class="badge-tag" style="background: rgba(16, 185, 129, 0.2); color: #34d399;">|A ∪ B| = ${data.cardinality_Union}</span>
        </div>
      </div>

      <!-- Venn Partition Cards -->
      <div class="venn-card-container">
        <div class="venn-box">
          <div class="venn-box-title" style="color: #38bdf8;">Set A Only (A \\ B) [${data.set_A_only.length}]</div>
          <div style="font-size: 0.82rem; color: var(--text-muted); max-height: 180px; overflow-y: auto;">
            ${data.set_A_only.map(x => `<div>• ${escapeHtml(x.name)} (${x.city})</div>`).join('') || '<div style="color: var(--text-dim);">Empty set ∅</div>'}
          </div>
        </div>

        <div class="venn-box intersection">
          <div class="venn-box-title" style="color: #c084fc;">Intersection (A ∩ B) [${data.intersection_items.length}]</div>
          <div style="font-size: 0.82rem; color: var(--text-muted); max-height: 180px; overflow-y: auto;">
            ${data.intersection_items.map(x => `<div>• <strong>${escapeHtml(x.name)}</strong> (${x.city})</div>`).join('') || '<div style="color: var(--text-dim);">Disjoint sets (A ∩ B = ∅)</div>'}
          </div>
        </div>

        <div class="venn-box">
          <div class="venn-box-title" style="color: #fbbf24;">Set B Only (B \\ A) [${data.set_B_only.length}]</div>
          <div style="font-size: 0.82rem; color: var(--text-muted); max-height: 180px; overflow-y: auto;">
            ${data.set_B_only.map(x => `<div>• ${escapeHtml(x.name)} (${x.city})</div>`).join('') || '<div style="color: var(--text-dim);">Empty set ∅</div>'}
          </div>
        </div>
      </div>
    `;
  }

  // =========================================================================
  // 4. BINARY RELATIONS & MATRIX
  // =========================================================================
  const relSelect = document.getElementById('relTypeSelect');
  const relCitySelect = document.getElementById('relCitySelect');
  const relResult = document.getElementById('relResultCard');
  const matrixContainer = document.getElementById('matrixContainer');

  if (relSelect && relCitySelect) {
    const updateRelationAnalysis = async () => {
      const rel = relSelect.value;
      const city = relCitySelect.value;
      try {
        const [relRes, matRes] = await Promise.all([
          fetch(`/api/relations/properties?relation=${encodeURIComponent(rel)}&city=${encodeURIComponent(city)}`),
          fetch(`/api/matrix?city=${encodeURIComponent(city)}&limit=10`)
        ]);
        const relData = await relRes.json();
        const matData = await matRes.json();
        renderRelationResults(relData);
        renderMatrix(matData);
      } catch (err) {
        console.error('Relation analysis error:', err);
      }
    };

    relSelect.addEventListener('change', updateRelationAnalysis);
    relCitySelect.addEventListener('change', updateRelationAnalysis);
    updateRelationAnalysis();
  }

  function renderRelationResults(data) {
    if (!relResult) return;

    relResult.innerHTML = `
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.25rem; margin-bottom: 1.5rem;">
        <!-- Reflexivity -->
        <div class="venn-box">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <strong style="color: #fff;">1. Reflexivity</strong>
            <span class="badge-tag ${data.is_reflexive ? 'relaxed' : 'pop'}">${data.is_reflexive ? 'REFLEXIVE' : 'NOT REFLEXIVE'}</span>
          </div>
          <p style="font-size: 0.82rem; color: var(--text-muted);">${escapeHtml(data.reflexive_explanation)}</p>
        </div>

        <!-- Symmetry -->
        <div class="venn-box">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <strong style="color: #fff;">2. Symmetry</strong>
            <span class="badge-tag ${data.is_symmetric ? 'relaxed' : 'pop'}">${data.is_symmetric ? 'SYMMETRIC' : 'NOT SYMMETRIC'}</span>
          </div>
          <p style="font-size: 0.82rem; color: var(--text-muted);">${escapeHtml(data.symmetric_explanation)}</p>
        </div>

        <!-- Transitivity -->
        <div class="venn-box">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <strong style="color: #fff;">3. Transitivity</strong>
            <span class="badge-tag ${data.is_transitive ? 'relaxed' : 'pop'}">${data.is_transitive ? 'TRANSITIVE' : 'NOT TRANSITIVE'}</span>
          </div>
          <p style="font-size: 0.82rem; color: var(--text-muted);">${escapeHtml(data.transitive_explanation)}</p>
        </div>
      </div>

      <div style="background: rgba(0,0,0,0.3); padding: 1rem; border-radius: var(--radius-sm); font-size: 0.85rem;">
        <strong>Equivalence Relation Verdict:</strong> ${data.is_equivalence ? '✅ Is an Equivalence Relation (Reflexive, Symmetric, and Transitive).' : '❌ Not an Equivalence Relation.'}
        <br><span style="color: var(--text-dim);">Relation Cardinality: |R| = ${data.relation_cardinality} pairs over set |V| = ${data.set_cardinality} places.</span>
      </div>
    `;
  }

  function renderMatrix(data) {
    if (!matrixContainer) return;
    const n = data.size;
    const names = data.node_names;
    const mat = data.matrix;

    let headerCols = names.map((name, i) => `<th style="writing-mode: vertical-rl; transform: rotate(180deg); padding: 0.5rem 0.2rem; font-size: 0.72rem; min-width: 32px;">${escapeHtml(name.substring(0, 14))}</th>`).join('');

    let rowsHtml = mat.map((row, i) => {
      const cells = row.map(val => `
        <td style="text-align: center; padding: 0.4rem; font-family: var(--font-mono); font-weight: 700; color: ${val === 1 ? '#38bdf8' : 'var(--text-dim)'}; background: ${val === 1 ? 'rgba(2, 132, 199, 0.15)' : 'transparent'};">
          ${val}
        </td>
      `).join('');
      return `
        <tr>
          <td style="font-weight: 600; font-size: 0.78rem; white-space: nowrap; padding-right: 0.75rem;">${i + 1}. ${escapeHtml(names[i])}</td>
          ${cells}
        </tr>
      `;
    }).join('');

    matrixContainer.innerHTML = `
      <div class="trace-table-container">
        <table class="trace-table" style="border: 1px solid var(--border-color);">
          <thead>
            <tr>
              <th>Node</th>
              ${headerCols}
            </tr>
          </thead>
          <tbody>
            ${rowsHtml}
          </tbody>
        </table>
      </div>
    `;
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
});
