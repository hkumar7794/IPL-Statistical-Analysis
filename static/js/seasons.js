/**
 * ==============================================================================
 * IPL Statistical Analysis - Seasons Controller
 * ==============================================================================
 * Renders Points Table, Orange/Purple Caps, and seasonal records from /api/season/<id>.
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    const select = document.getElementById('seasonSelectDropdown');
    if (select) {
        select.addEventListener('change', () => loadSeasonDetails(select.value));
        loadSeasonDetails(select.value);
    }
});

async function loadSeasonDetails(season) {
    const loading = document.getElementById('loadingIndicator');
    const content = document.getElementById('seasonDetailsContent');

    if (loading) loading.style.display = 'flex';
    if (content) content.style.display = 'none';

    try {
        const res = await fetch(`/api/season/${encodeURIComponent(season)}`);
        const json = await res.json();
        if (!json.success) throw new Error(json.error);

        const data = json.data;

        // Champion
        document.getElementById('champTeamName').textContent = data.champion_name;
        const cBadge = document.getElementById('champBadge');
        cBadge.textContent = data.champion;
        cBadge.className = 'badge bg-warning text-dark fw-bold fs-6 my-2';
        document.getElementById('runnerUpName').textContent = `${data.runner_up_name} (${data.runner_up})`;

        // Orange & Purple Caps
        document.getElementById('orangeCapPlayer').textContent = data.orange_cap.player;
        document.getElementById('orangeCapRuns').textContent = `${data.orange_cap.runs} runs`;

        document.getElementById('purpleCapPlayer').textContent = data.purple_cap.player;
        document.getElementById('purpleCapWickets').textContent = `${data.purple_cap.wickets} wickets`;

        // KPIs
        document.getElementById('sMatches').textContent = data.total_matches;
        document.getElementById('sRuns').textContent = data.total_runs.toLocaleString();
        document.getElementById('sAvgRuns').textContent = data.avg_match_runs;
        document.getElementById('sHighestScore').textContent = `${data.highest_score.score} (${data.highest_score.team})`;

        // Points Table
        const ptBody = document.getElementById('pointsTableBody');
        ptBody.innerHTML = '';
        data.points_table.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="text-center fw-bold text-muted">${row.rank}</td>
                <td>
                    <span class="badge me-1" style="background-color: ${row.color}; color: #000; font-weight: 700;">${row.team}</span>
                    <strong class="text-white">${row.name}</strong>
                </td>
                <td class="text-center">${row.played}</td>
                <td class="text-center text-success fw-semibold">${row.won}</td>
                <td class="text-center text-danger">${row.lost}</td>
                <td class="text-center fw-bold text-info fs-6">${row.points}</td>
                <td class="text-end fw-semibold text-light">${row.win_pct}%</td>
            `;
            ptBody.appendChild(tr);
        });

        // Matches Fixtures
        const mBody = document.getElementById('seasonMatchesBody');
        mBody.innerHTML = '';
        data.matches.forEach(m => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="small text-muted">${m.date}</td>
                <td><strong class="text-white">${m.team1}</strong> vs <strong class="text-white">${m.team2}</strong></td>
                <td><span class="small text-secondary">${m.venue}</span></td>
                <td class="text-center"><span class="badge bg-dark border border-secondary">${m.team1_score} - ${m.team2_score}</span></td>
                <td><span class="badge badge-win">${m.winner}</span></td>
                <td class="small text-info">${m.player_of_match}</td>
            `;
            mBody.appendChild(tr);
        });

        if (loading) loading.style.display = 'none';
        if (content) content.style.display = 'block';

    } catch (err) {
        console.error('Error loading season details:', err);
        if (loading) {
            loading.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
        }
    }
}
