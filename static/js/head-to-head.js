/**
 * ==============================================================================
 * IPL Statistical Analysis - Head-to-Head Controller
 * ==============================================================================
 * Fetches matchup data between Team A and Team B from /api/team-comparison.
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    const compareBtn = document.getElementById('compareBtn');
    if (compareBtn) {
        compareBtn.addEventListener('click', runComparison);
    }
    runComparison();
});

async function runComparison() {
    const t1 = document.getElementById('teamASelect').value;
    const t2 = document.getElementById('teamBSelect').value;

    if (t1 === t2) {
        alert('Please choose two different franchises to compare!');
        return;
    }

    const loading = document.getElementById('loadingIndicator');
    const results = document.getElementById('comparisonResults');

    if (loading) loading.style.display = 'flex';
    if (results) results.style.display = 'none';

    try {
        const res = await fetch(`/api/team-comparison?team1=${encodeURIComponent(t1)}&team2=${encodeURIComponent(t2)}`);
        const json = await res.json();
        if (!json.success) throw new Error(json.error);

        const data = json.data;
        const a = data.team1;
        const b = data.team2;

        // Card A
        document.getElementById('nameTeamA').textContent = a.name;
        const badgeA = document.getElementById('badgeTeamA');
        badgeA.textContent = a.code;
        badgeA.style.backgroundColor = a.color;
        badgeA.style.color = '#000';
        document.getElementById('cardTeamA').style.borderTopColor = a.color;
        document.getElementById('winsTeamA').textContent = a.wins;
        document.getElementById('pctTeamA').textContent = `${a.win_pct}%`;
        document.getElementById('avgTeamA').textContent = a.avg_score;

        // Total
        document.getElementById('totalClashes').textContent = data.total_matches;

        // Card B
        document.getElementById('nameTeamB').textContent = b.name;
        const badgeB = document.getElementById('badgeTeamB');
        badgeB.textContent = b.code;
        badgeB.style.backgroundColor = b.color;
        badgeB.style.color = '#000';
        document.getElementById('cardTeamB').style.borderTopColor = b.color;
        document.getElementById('winsTeamB').textContent = b.wins;
        document.getElementById('pctTeamB').textContent = `${b.win_pct}%`;
        document.getElementById('avgTeamB').textContent = b.avg_score;

        // Render Comparison Bar Chart
        renderBarChart(
            'h2hChart',
            [`${a.code} Wins`, `${b.code} Wins`, `${a.code} Avg Score`, `${b.code} Avg Score`],
            [a.wins, b.wins, a.avg_score, b.avg_score],
            'Comparison Metrics',
            [a.color || '#00e5ff', b.color || '#f59e0b', a.color || '#00e5ff', b.color || '#f59e0b']
        );

        // Render Matches History
        const list = document.getElementById('h2hMatchesList');
        list.innerHTML = '';

        if (!data.recent_matches || data.recent_matches.length === 0) {
            list.innerHTML = '<div class="text-muted p-3">No matches recorded between these two teams.</div>';
        } else {
            data.recent_matches.forEach(m => {
                const item = document.createElement('div');
                item.className = 'p-3 rounded bg-dark bg-opacity-40 border border-secondary border-opacity-15 d-flex justify-content-between align-items-center';
                item.innerHTML = `
                    <div>
                        <div class="fw-semibold text-white">
                            ${m.team1} (${m.team1_score}) vs ${m.team2} (${m.team2_score})
                        </div>
                        <div class="small text-muted">${m.venue} &bull; Season ${m.season}</div>
                    </div>
                    <div>
                        <span class="badge badge-win">Winner: ${m.winner}</span>
                    </div>
                `;
                list.appendChild(item);
            });
        }

        if (loading) loading.style.display = 'none';
        if (results) results.style.display = 'block';

    } catch (err) {
        console.error('Error during comparison:', err);
        if (loading) {
            loading.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
        }
    }
}
