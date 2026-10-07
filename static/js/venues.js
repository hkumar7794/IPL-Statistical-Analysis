/**
 * ==============================================================================
 * IPL Statistical Analysis - Venues Controller
 * ==============================================================================
 * Fetches stadium performance metrics and charts from /api/venue/<name>.
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    const select = document.getElementById('venueSelectDropdown');
    if (select) {
        select.addEventListener('change', () => loadVenueDetails(select.value));
        loadVenueDetails(select.value);
    }
});

async function loadVenueDetails(venueName) {
    const loading = document.getElementById('loadingIndicator');
    const content = document.getElementById('venueContent');

    if (loading) loading.style.display = 'flex';
    if (content) content.style.display = 'none';

    try {
        const res = await fetch(`/api/venue/${encodeURIComponent(venueName)}`);
        const json = await res.json();
        if (!json.success) throw new Error(json.error);

        const data = json.data;

        // KPIs
        document.getElementById('vName').textContent = `${data.venue} Cricket Stadium`;
        document.getElementById('vMatches').textContent = data.total_matches;
        document.getElementById('vAvg1st').textContent = `${data.avg_1st_innings} runs`;
        document.getElementById('vAvg2nd').textContent = `${data.avg_2nd_innings} runs`;
        document.getElementById('vHighest').textContent = `${data.highest_score.score} (${data.highest_score.team})`;

        // Team wins chart
        const teams = data.team_wins.map(t => t.team);
        const wins = data.team_wins.map(t => t.wins);
        renderBarChart('venueTeamWinsChart', teams, wins, 'Victories at Ground', '#00e5ff');

        // Toss decisions chart
        const tossDec = data.toss_decisions;
        renderDoughnutChart(
            'venueTossChart',
            ['Field First', 'Bat First'],
            [tossDec.field || 0, tossDec.bat || 0],
            ['#10b981', '#f59e0b']
        );

        // Recent matches table
        const tbody = document.getElementById('venueMatchesBody');
        tbody.innerHTML = '';
        data.recent_matches.forEach(m => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><span class="badge bg-secondary">Season ${m.season}</span></td>
                <td><strong class="text-white">${m.team1}</strong> vs <strong class="text-white">${m.team2}</strong></td>
                <td class="text-center"><span class="badge bg-dark border border-secondary">${m.team1_score} - ${m.team2_score}</span></td>
                <td><span class="badge badge-win">${m.winner}</span></td>
                <td class="text-info">${m.player_of_match}</td>
            `;
            tbody.appendChild(tr);
        });

        if (loading) loading.style.display = 'none';
        if (content) content.style.display = 'block';

    } catch (err) {
        console.error('Error loading venue details:', err);
        if (loading) {
            loading.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
        }
    }
}
