/**
 * ==============================================================================
 * IPL Statistical Analysis - Teams Overview Controller
 * ==============================================================================
 * Renders all 10 IPL franchises with performance metrics and navigation links.
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    loadTeams();
});

async function loadTeams() {
    const loading = document.getElementById('loadingIndicator');
    const grid = document.getElementById('teamsGrid');

    try {
        const res = await fetch('/api/teams');
        const json = await res.json();
        if (!json.success) throw new Error(json.error);

        const teams = json.data;
        grid.innerHTML = '';

        teams.forEach(t => {
            const col = document.createElement('div');
            col.className = 'col-md-6 col-lg-4';

            // Generate trophy stars
            let trophiesHtml = '';
            for (let i = 0; i < t.titles; i++) {
                trophiesHtml += '<i class="bi bi-star-fill text-warning me-1"></i>';
            }

            col.innerHTML = `
                <div class="analytics-card h-100 d-flex flex-column justify-content-between">
                    <div>
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <div>
                                <h4 class="fw-bold mb-0 text-white">${t.team}</h4>
                                <span class="text-muted small">${t.name}</span>
                            </div>
                            <span class="badge" style="background-color: ${t.color}; color: #000; font-size: 0.9rem; font-weight: 800; padding: 0.4rem 0.8rem;">
                                ${t.team}
                            </span>
                        </div>

                        ${t.titles > 0 ? `
                        <div class="mb-3 py-1 px-2 rounded bg-warning bg-opacity-10 border border-warning border-opacity-25 d-flex align-items-center">
                            <i class="bi bi-trophy-fill text-warning me-2"></i>
                            <span class="small text-warning fw-semibold">${t.titles} IPL Trophy${t.titles > 1 ? 's' : ''}</span>
                            <span class="ms-auto">${trophiesHtml}</span>
                        </div>
                        ` : ''}

                        <div class="row g-2 text-center py-2 rounded bg-dark bg-opacity-50 my-2">
                            <div class="col-4">
                                <div class="small text-muted">Played</div>
                                <div class="fw-bold text-white fs-5">${t.matches_played}</div>
                            </div>
                            <div class="col-4">
                                <div class="small text-muted">Wins</div>
                                <div class="fw-bold text-success fs-5">${t.wins}</div>
                            </div>
                            <div class="col-4">
                                <div class="small text-muted">Win Rate</div>
                                <div class="fw-bold text-info fs-5">${t.win_pct}%</div>
                            </div>
                        </div>

                        <div class="row g-2 text-center py-2 rounded bg-dark bg-opacity-25 mb-3">
                            <div class="col-4">
                                <div class="small text-muted">Avg Score</div>
                                <div class="fw-semibold text-warning">${t.avg_score}</div>
                            </div>
                            <div class="col-4">
                                <div class="small text-muted">Highest</div>
                                <div class="fw-semibold text-white">${t.highest_score}</div>
                            </div>
                            <div class="col-4">
                                <div class="small text-muted">Total Runs</div>
                                <div class="fw-semibold text-light">${t.total_runs.toLocaleString()}</div>
                            </div>
                        </div>
                    </div>

                    <a href="/team-analysis?team=${t.team}" class="btn btn-outline-info w-100 mt-2">
                        <i class="bi bi-graph-up-arrow me-1"></i> Analyze Team Performance
                    </a>
                </div>
            `;
            grid.appendChild(col);
        });

        if (loading) loading.style.display = 'none';
        if (grid) grid.style.display = 'flex';

    } catch (err) {
        console.error('Error loading teams:', err);
        if (loading) {
            loading.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
        }
    }
}
