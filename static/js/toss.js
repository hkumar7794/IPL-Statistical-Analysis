/**
 * ==============================================================================
 * IPL Statistical Analysis - Toss Analysis Controller
 * ==============================================================================
 * Fetches toss impact data from /api/toss-analysis and renders Doughnut & Bar charts.
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    loadTossData();
});

async function loadTossData() {
    const loading = document.getElementById('loadingIndicator');
    const content = document.getElementById('tossContent');

    try {
        const res = await fetch('/api/toss-analysis');
        const json = await res.json();
        if (!json.success) throw new Error(json.error);

        const data = json.data;

        // 1. KPIs
        document.getElementById('tossTotal').textContent = data.total_matches;
        document.getElementById('tossFieldPct').textContent = `${data.decisions.field_pct}%`;
        document.getElementById('tossFieldCount').textContent = `${data.decisions.field_count} decisions`;
        document.getElementById('tossBatPct').textContent = `${data.decisions.bat_pct}%`;
        document.getElementById('tossBatCount').textContent = `${data.decisions.bat_count} decisions`;
        document.getElementById('tossMatchWinPct').textContent = `${data.match_outcomes.toss_win_match_win_pct}%`;
        document.getElementById('tossMatchWinCount').textContent = `${data.match_outcomes.toss_winner_won_match} victories`;

        // 2. Render Toss Decisions Doughnut
        renderDoughnutChart(
            'tossDecisionDoughnut',
            ['Field First (Chasing)', 'Bat First (Defending)'],
            [data.decisions.field_count, data.decisions.bat_count],
            ['#00e5ff', '#f59e0b']
        );

        // 3. Render Decision Win Rates Bar Chart
        renderBarChart(
            'decisionSuccessChart',
            ['When Opting to Field', 'When Opting to Bat', 'Overall Toss-to-Match Win Rate'],
            [data.decision_success.field_win_rate, data.decision_success.bat_win_rate, data.match_outcomes.toss_win_match_win_pct],
            'Win Rate %',
            ['#10b981', '#f59e0b', '#3b82f6']
        );

        // 4. Toss Winners Table
        const wBody = document.getElementById('tossWinnersBody');
        wBody.innerHTML = '';
        data.toss_winners.forEach(tw => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>
                    <span class="badge me-1" style="background-color: ${tw.color}; color: #000; font-weight: 700;">${tw.team}</span>
                    <strong class="text-white">${tw.name}</strong>
                </td>
                <td class="text-end fw-bold text-info">${tw.toss_wins}</td>
            `;
            wBody.appendChild(tr);
        });

        // 5. Season Trends Table
        const tBody = document.getElementById('tossTrendsBody');
        tBody.innerHTML = '';
        data.season_trends.forEach(st => {
            const total = st.field + st.bat;
            const fieldPct = total > 0 ? ((st.field / total) * 100).toFixed(1) : 0;
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong class="text-white">Season ${st.season}</strong></td>
                <td class="text-center text-info fw-semibold">${st.field}</td>
                <td class="text-center text-warning">${st.bat}</td>
                <td class="text-end fw-bold text-success">${fieldPct}%</td>
            `;
            tBody.appendChild(tr);
        });

        if (loading) loading.style.display = 'none';
        if (content) content.style.display = 'block';

    } catch (err) {
        console.error('Error loading toss data:', err);
        if (loading) {
            loading.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
        }
    }
}
