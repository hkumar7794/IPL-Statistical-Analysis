/**
 * ==============================================================================
 * IPL Statistical Analysis - Team Deep Analysis Controller
 * ==============================================================================
 * Dynamic franchise selector, season-by-season grouped bars, and opponent tables.
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const initialTeam = urlParams.get('team') || 'CSK';

    const select = document.getElementById('teamSelectDropdown');
    if (select) {
        select.value = initialTeam;
        select.addEventListener('change', () => loadTeamDetails(select.value));
    }

    loadTeamDetails(initialTeam);
});

async function loadTeamDetails(teamCode) {
    const loading = document.getElementById('loadingIndicator');
    const content = document.getElementById('teamDetailsContent');

    if (loading) loading.style.display = 'flex';
    if (content) content.style.display = 'none';

    try {
        const res = await fetch(`/api/team/${encodeURIComponent(teamCode)}`);
        const json = await res.json();
        if (!json.success) throw new Error(json.error);

        const data = json.data;

        // 1. Header Information
        document.getElementById('teamFullName').textContent = data.name;
        const codeBadge = document.getElementById('teamCodeBadge');
        codeBadge.textContent = data.team;
        codeBadge.style.backgroundColor = data.color;
        codeBadge.style.color = '#000';
        codeBadge.style.fontWeight = '800';

        const trophyContainer = document.getElementById('teamTrophyBadge');
        if (data.titles > 0) {
            let stars = '';
            for (let i = 0; i < data.titles; i++) stars += '<i class="bi bi-star-fill text-warning me-1"></i>';
            trophyContainer.innerHTML = `
                <div class="px-3 py-2 rounded bg-warning bg-opacity-10 border border-warning border-opacity-25 text-warning fw-bold">
                    <i class="bi bi-trophy-fill me-1"></i> ${data.titles} Titles &nbsp; ${stars}
                </div>
            `;
        } else {
            trophyContainer.innerHTML = '';
        }

        // 2. KPIs
        document.getElementById('statMatches').textContent = data.matches_played;
        document.getElementById('statWins').textContent = data.wins;
        document.getElementById('statLosses').textContent = data.losses;
        document.getElementById('statWinPct').textContent = `${data.win_pct}%`;
        document.getElementById('statAvgScore').textContent = data.avg_score;
        document.getElementById('statHighest').textContent = data.highest_score;

        // 3. Season Performance Grouped Bar Chart
        const seasons = data.season_performance.map(s => `Season ${s.season}`);
        const seasonWins = data.season_performance.map(s => s.wins);
        const seasonLosses = data.season_performance.map(s => s.losses);

        renderGroupedBarChart('teamSeasonPerfChart', seasons, [
            { label: 'Wins', data: seasonWins, backgroundColor: '#10b981', borderRadius: 6 },
            { label: 'Losses', data: seasonLosses, backgroundColor: '#ef4444', borderRadius: 6 }
        ]);

        // 4. Win Rate Progression Line Chart
        const seasonWinRates = data.season_performance.map(s => s.win_pct);
        renderLineChart('teamWinRateChart', seasons, seasonWinRates, 'Win Rate %', data.color || '#00e5ff');

        // 5. Opponents Table
        const oppBody = document.getElementById('opponentsTableBody');
        oppBody.innerHTML = '';
        data.opponents.forEach(o => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong class="text-white">${o.opponent}</strong></td>
                <td class="text-center">${o.played}</td>
                <td class="text-center text-success fw-semibold">${o.wins}</td>
                <td class="text-center text-danger">${o.losses}</td>
                <td class="text-end fw-bold text-info">${o.win_pct}%</td>
            `;
            oppBody.appendChild(tr);
        });

        // 6. Recent Matches List
        const recentList = document.getElementById('recentMatchesList');
        recentList.innerHTML = '';
        data.recent_matches.forEach(m => {
            const isWon = m.result === 'WON';
            const item = document.createElement('div');
            item.className = 'p-2 rounded bg-dark bg-opacity-40 border border-secondary border-opacity-10 d-flex justify-content-between align-items-center';
            item.innerHTML = `
                <div>
                    <span class="badge ${isWon ? 'badge-win' : 'badge-loss'} me-2">${m.result}</span>
                    <span class="text-white small">vs <strong>${m.opponent}</strong> (${m.venue})</span>
                </div>
                <div class="text-end small">
                    <span class="text-muted">${m.team_score} - ${m.opp_score}</span>
                    <span class="text-secondary ms-1">(${m.season})</span>
                </div>
            `;
            recentList.appendChild(item);
        });

        if (loading) loading.style.display = 'none';
        if (content) content.style.display = 'block';

    } catch (err) {
        console.error('Error fetching team details:', err);
        if (loading) {
            loading.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
        }
    }
}
