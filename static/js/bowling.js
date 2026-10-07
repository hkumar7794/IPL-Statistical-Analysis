/**
 * ==============================================================================
 * IPL Statistical Analysis - Bowling Controller
 * ==============================================================================
 * Fetches bowling leaderboards and Chart.js datasets with dynamic filters.
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    loadBowlingData();

    document.getElementById('seasonFilter').addEventListener('change', loadBowlingData);
    document.getElementById('sortFilter').addEventListener('change', loadBowlingData);
    document.getElementById('limitFilter').addEventListener('change', loadBowlingData);
});

async function loadBowlingData() {
    const season = document.getElementById('seasonFilter').value;
    const sort = document.getElementById('sortFilter').value;
    const limit = document.getElementById('limitFilter').value;

    try {
        // 1. Fetch leaderboard
        const res = await fetch(`/api/top-bowlers?season=${encodeURIComponent(season)}&sort=${encodeURIComponent(sort)}&limit=${encodeURIComponent(limit)}`);
        const json = await res.json();
        if (!json.success) throw new Error(json.error);

        renderBowlingTable(json.data.leaderboard);
        document.getElementById('bowlerCountBadge').textContent = `${json.data.leaderboard.length} Bowlers`;

        // 2. Fetch charts
        const cRes = await fetch('/api/bowling/charts');
        const cJson = await cRes.json();
        if (cJson.success) {
            const cData = cJson.data;
            renderBarChart('topWicketsChart', cData.top_wickets.labels, cData.top_wickets.wickets, 'Wickets Taken', '#ef4444');
            renderBarChart('economyChart', cData.best_economy.labels, cData.best_economy.economy, 'Economy (Runs/Over)', '#00e5ff');
        }

    } catch (err) {
        console.error('Error loading bowling data:', err);
    }
}

function renderBowlingTable(bowlers) {
    const tbody = document.getElementById('bowlingTableBody');
    tbody.innerHTML = '';

    bowlers.forEach(b => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="text-center fw-bold text-muted">${b.rank}</td>
            <td><strong class="text-white">${b.player}</strong></td>
            <td><span class="badge bg-secondary bg-opacity-75">${b.team}</span></td>
            <td class="text-center">${b.matches}</td>
            <td class="text-end fw-bold text-danger fs-6">${b.wickets}</td>
            <td class="text-end fw-bold text-info">${b.economy > 0 ? b.economy : 'N/A'}</td>
            <td class="text-end text-warning">${b.average > 0 ? b.average : 'N/A'}</td>
        `;
        tbody.appendChild(tr);
    });
}
