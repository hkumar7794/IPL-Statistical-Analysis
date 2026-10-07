/**
 * ==============================================================================
 * IPL Statistical Analysis - Dashboard Controller
 * ==============================================================================
 * Fetches tournament summary from /api/summary and populates KPIs and Chart.js graphs.
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    loadDashboardData();
});

async function loadDashboardData() {
    const loading = document.getElementById('loadingIndicator');
    const content = document.getElementById('dashboardContent');

    try {
        const response = await fetch('/api/summary');
        const json = await response.json();

        if (!json.success) {
            throw new Error(json.error || 'Failed to load dashboard data');
        }

        const data = json.data;
        const kpis = data.kpis;

        // 1. Populate KPI Cards
        document.getElementById('kpiMatches').textContent = kpis.total_matches.toLocaleString();
        document.getElementById('kpiSeasons').textContent = kpis.total_seasons.toLocaleString();
        document.getElementById('kpiTeams').textContent = kpis.total_teams.toLocaleString();
        document.getElementById('kpiPlayers').textContent = kpis.total_players.toLocaleString();
        document.getElementById('kpiRuns').textContent = kpis.total_runs.toLocaleString();
        document.getElementById('kpiWickets').textContent = kpis.total_wickets.toLocaleString();

        // 2. Tournament Benchmarks
        document.getElementById('statAvgRuns').textContent = `${kpis.avg_runs_per_match} runs`;
        document.getElementById('statHighestScore').textContent = `${kpis.highest_score.score} (${kpis.highest_score.team})`;
        document.getElementById('statLowestScore').textContent = `${kpis.lowest_score.score} (${kpis.lowest_score.team})`;
        document.getElementById('statTossWinPct').textContent = `${data.toss_stats.toss_win_match_win_pct}%`;

        // 3. Render Team Wins Bar Chart
        const teamLabels = data.team_wins.map(t => t.team);
        const teamWins = data.team_wins.map(t => t.wins);
        const teamColors = data.team_wins.map(t => t.color);
        renderBarChart('teamWinsChart', teamLabels, teamWins, 'Matches Won', teamColors);

        // 4. Render Toss Decisions Doughnut Chart
        const tossDecisions = data.toss_stats.decisions;
        renderDoughnutChart(
            'tossDecisionChart',
            ['Field First (Chase)', 'Bat First (Defend)'],
            [tossDecisions.field || 0, tossDecisions.bat || 0],
            ['#00e5ff', '#f59e0b']
        );

        // 5. Render Runs Per Season Line Chart
        const seasonLabels = data.season_summary.map(s => `Season ${s.season}`);
        const seasonRuns = data.season_summary.map(s => s.runs);
        renderLineChart('runsPerSeasonChart', seasonLabels, seasonRuns, 'Runs Scored', '#10b981');

        // 6. Render Matches Per Season Bar Chart
        const seasonMatches = data.season_summary.map(s => s.matches);
        renderBarChart('matchesPerSeasonChart', seasonLabels, seasonMatches, 'Matches Played', '#3b82f6');

        // Show content
        if (loading) loading.style.display = 'none';
        if (content) content.style.display = 'block';

    } catch (err) {
        console.error('Error loading dashboard:', err);
        if (loading) {
            loading.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    <h5 class="alert-heading"><i class="bi bi-exclamation-triangle-fill me-2"></i> Error Loading Dashboard</h5>
                    <p class="mb-0">${err.message}</p>
                </div>
            `;
        }
    }
}
