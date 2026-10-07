/**
 * ==============================================================================
 * IPL Statistical Analysis - Batting Controller
 * ==============================================================================
 * Fetches batting leaderboards and Chart.js datasets with live filters.
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    loadBattingData();

    document.getElementById('seasonFilter').addEventListener('change', loadBattingData);
    document.getElementById('sortFilter').addEventListener('change', loadBattingData);
    document.getElementById('limitFilter').addEventListener('change', loadBattingData);
});

async function loadBattingData() {
    const season = document.getElementById('seasonFilter').value;
    const sort = document.getElementById('sortFilter').value;
    const limit = document.getElementById('limitFilter').value;

    try {
        // 1. Fetch leaderboard
        const res = await fetch(`/api/top-batsmen?season=${encodeURIComponent(season)}&sort=${encodeURIComponent(sort)}&limit=${encodeURIComponent(limit)}`);
        const json = await res.json();
        if (!json.success) throw new Error(json.error);

        renderBattingTable(json.data.leaderboard);
        document.getElementById('leaderboardCountBadge').textContent = `${json.data.leaderboard.length} Players`;

        // 2. Fetch charts data
        const cRes = await fetch('/api/batting/charts');
        const cJson = await cRes.json();
        if (cJson.success) {
            const cData = cJson.data;
            renderBarChart('topScorersChart', cData.top_scorers.labels, cData.top_scorers.runs, 'Runs Scored', '#ef4444');
            renderBarChart('strikeRateChart', cData.top_strike_rates.labels, cData.top_strike_rates.strike_rates, 'Strike Rate', '#f59e0b');
        }

    } catch (err) {
        console.error('Error loading batting data:', err);
    }
}

function renderBattingTable(players) {
    const tbody = document.getElementById('battingTableBody');
    tbody.innerHTML = '';

    players.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="text-center fw-bold text-muted">${p.rank}</td>
            <td><strong class="text-white">${p.player}</strong></td>
            <td><span class="badge bg-secondary bg-opacity-75">${p.team}</span></td>
            <td class="text-center">${p.matches}</td>
            <td class="text-end fw-bold text-success">${p.runs.toLocaleString()}</td>
            <td class="text-end text-warning">${p.average}</td>
            <td class="text-end fw-bold text-info">${p.strike_rate}</td>
            <td class="text-center">${p.fifties}</td>
            <td class="text-center text-success">${p.hundreds}</td>
            <td class="text-center text-warning fw-semibold">${p.sixes}</td>
        `;
        tbody.appendChild(tr);
    });
}
