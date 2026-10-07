/**
 * ==============================================================================
 * IPL Statistical Analysis - Players Controller
 * ==============================================================================
 * Real-time search, multi-factor filtering, and career profile modal inspection.
 * ==============================================================================
 */

let allPlayersData = [];

document.addEventListener('DOMContentLoaded', () => {
    fetchPlayers();

    const searchInput = document.getElementById('playerSearchInput');
    const teamSelect = document.getElementById('teamFilterSelect');
    const roleSelect = document.getElementById('roleFilterSelect');
    const resetBtn = document.getElementById('resetFiltersBtn');

    if (searchInput) searchInput.addEventListener('input', debounce(fetchPlayers, 250));
    if (teamSelect) teamSelect.addEventListener('change', fetchPlayers);
    if (roleSelect) roleSelect.addEventListener('change', fetchPlayers);
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            searchInput.value = '';
            teamSelect.value = 'ALL';
            roleSelect.value = 'ALL';
            fetchPlayers();
        });
    }
});

function debounce(func, wait) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

async function fetchPlayers() {
    const searchVal = document.getElementById('playerSearchInput').value.trim();
    const teamVal = document.getElementById('teamFilterSelect').value;
    const roleVal = document.getElementById('roleFilterSelect').value;

    const loading = document.getElementById('loadingIndicator');
    const grid = document.getElementById('playersGrid');
    const emptyState = document.getElementById('emptyState');

    if (loading) loading.style.display = 'flex';
    if (grid) grid.style.display = 'none';
    if (emptyState) emptyState.style.display = 'none';

    try {
        const url = `/api/players?query=${encodeURIComponent(searchVal)}&team=${encodeURIComponent(teamVal)}&role=${encodeURIComponent(roleVal)}`;
        const res = await fetch(url);
        const json = await res.json();

        if (!json.success) throw new Error(json.error || 'Failed to fetch players');

        allPlayersData = json.data.players;
        renderPlayersGrid(allPlayersData);

        if (loading) loading.style.display = 'none';
    } catch (err) {
        console.error('Error fetching players:', err);
        if (loading) loading.style.display = 'none';
        if (emptyState) {
            emptyState.style.display = 'block';
            emptyState.querySelector('h4').textContent = err.message;
        }
    }
}

function renderPlayersGrid(players) {
    const grid = document.getElementById('playersGrid');
    const emptyState = document.getElementById('emptyState');

    if (!players || players.length === 0) {
        grid.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    grid.innerHTML = '';
    emptyState.style.display = 'none';
    grid.style.display = 'flex';

    players.forEach(p => {
        const col = document.createElement('div');
        col.className = 'col-md-6 col-lg-4';

        col.innerHTML = `
            <div class="analytics-card h-100 d-flex flex-column justify-content-between">
                <div>
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <div>
                            <h5 class="fw-bold mb-1 text-white">${p.player}</h5>
                            <span class="badge" style="background-color: ${p.team_color}; color: #000; font-weight: 700;">
                                ${p.team}
                            </span>
                            <span class="badge bg-secondary bg-opacity-50 text-light ms-1">${p.role}</span>
                        </div>
                        <i class="bi bi-person-circle fs-2 text-info opacity-50"></i>
                    </div>

                    <div class="row g-2 text-center my-3 py-2 rounded bg-dark bg-opacity-40">
                        <div class="col-4">
                            <div class="small text-muted">Runs</div>
                            <div class="fw-bold text-success">${p.runs.toLocaleString()}</div>
                        </div>
                        <div class="col-4">
                            <div class="small text-muted">Avg</div>
                            <div class="fw-bold text-warning">${p.average}</div>
                        </div>
                        <div class="col-4">
                            <div class="small text-muted">SR</div>
                            <div class="fw-bold text-primary">${p.strike_rate}</div>
                        </div>
                    </div>

                    <div class="row g-2 text-center py-2 rounded bg-dark bg-opacity-20 mb-3">
                        <div class="col-4">
                            <div class="small text-muted">Matches</div>
                            <div class="fw-semibold text-white">${p.matches}</div>
                        </div>
                        <div class="col-4">
                            <div class="small text-muted">Wickets</div>
                            <div class="fw-semibold text-danger">${p.wickets}</div>
                        </div>
                        <div class="col-4">
                            <div class="small text-muted">Sixes</div>
                            <div class="fw-semibold text-warning">${p.sixes}</div>
                        </div>
                    </div>
                </div>

                <button class="btn btn-outline-info btn-sm w-100 mt-2" onclick="openPlayerModal('${encodeURIComponent(p.player)}')">
                    <i class="bi bi-eye me-1"></i> View Full Career Stats
                </button>
            </div>
        `;
        grid.appendChild(col);
    });
}

async function openPlayerModal(playerNameEncoded) {
    const playerName = decodeURIComponent(playerNameEncoded);
    try {
        const res = await fetch(`/api/player/${encodeURIComponent(playerName)}`);
        const json = await res.json();
        if (!json.success) throw new Error(json.error);

        const p = json.data;
        document.getElementById('modalPlayerName').textContent = p.player;
        
        const teamBadge = document.getElementById('modalPlayerTeamBadge');
        teamBadge.textContent = p.team;
        teamBadge.style.backgroundColor = p.team_color;
        teamBadge.style.color = '#000';

        document.getElementById('modalPlayerRoleBadge').textContent = p.role;
        document.getElementById('modalMatches').textContent = p.matches;
        document.getElementById('modalRuns').textContent = p.runs.toLocaleString();
        document.getElementById('modalAverage').textContent = p.average;
        document.getElementById('modalStrikeRate').textContent = p.strike_rate;
        document.getElementById('modalWickets').textContent = p.wickets;
        document.getElementById('modalEconomy').textContent = p.economy > 0 ? p.economy : 'N/A';
        document.getElementById('modalHighestScore').textContent = p.highest_score;
        document.getElementById('modalHundreds').textContent = p.hundreds;
        document.getElementById('modalFifties').textContent = p.fifties;
        document.getElementById('modalSixes').textContent = p.sixes;
        document.getElementById('modalBestBowling').textContent = p.best_bowling;
        document.getElementById('modalBallsSample').textContent = `${p.balls_faced_sample} balls`;
        document.getElementById('modalRunsSample').textContent = `${p.runs_scored_sample} runs`;
        document.getElementById('modalFullFranchise').textContent = p.team_name;

        const modal = new bootstrap.Modal(document.getElementById('playerProfileModal'));
        modal.show();
    } catch (err) {
        alert('Could not load player profile: ' + err.message);
    }
}
