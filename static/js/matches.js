/**
 * ==============================================================================
 * IPL Statistical Analysis - Matches Controller
 * ==============================================================================
 * Fetches filtered matches archive and opens interactive match scorecard modal.
 * ==============================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
    loadMatches();

    document.getElementById('seasonFilter').addEventListener('change', loadMatches);
    document.getElementById('teamFilter').addEventListener('change', loadMatches);
    document.getElementById('venueFilter').addEventListener('change', loadMatches);
});

async function loadMatches() {
    const season = document.getElementById('seasonFilter').value;
    const team = document.getElementById('teamFilter').value;
    const venue = document.getElementById('venueFilter').value;

    const tbody = document.getElementById('matchesTableBody');
    tbody.innerHTML = '<tr><td colspan="9" class="text-center py-4 text-muted">Filtering matches...</td></tr>';

    try {
        const url = `/api/matches?season=${encodeURIComponent(season)}&team=${encodeURIComponent(team)}&venue=${encodeURIComponent(venue)}&limit=100`;
        const res = await fetch(url);
        const json = await res.json();
        if (!json.success) throw new Error(json.error);

        const matches = json.data.matches;
        document.getElementById('matchCountBadge').textContent = `${json.data.total} Matches`;

        if (!matches || matches.length === 0) {
            tbody.innerHTML = '<tr><td colspan="9" class="text-center py-4 text-muted">No matches match your filter criteria.</td></tr>';
            return;
        }

        tbody.innerHTML = '';
        matches.forEach(m => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="text-center text-muted fw-bold">${m.match_id}</td>
                <td class="small text-muted">${m.date}</td>
                <td><span class="badge bg-dark border border-secondary">${m.season}</span></td>
                <td><strong class="text-white">${m.team1}</strong> vs <strong class="text-white">${m.team2}</strong></td>
                <td class="small text-secondary">${m.venue}</td>
                <td class="text-center fw-semibold text-info">${m.team1_score} - ${m.team2_score}</td>
                <td><span class="badge badge-win">${m.winner}</span></td>
                <td class="small text-warning">${m.player_of_match}</td>
                <td class="text-end">
                    <button class="btn btn-outline-info btn-sm" onclick="openMatchModal(${m.match_id})">
                        <i class="bi bi-file-earmark-text"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(tr);
        });

    } catch (err) {
        console.error('Error loading matches:', err);
        tbody.innerHTML = `<tr><td colspan="9" class="text-center py-4 text-danger">${err.message}</td></tr>`;
    }
}

async function openMatchModal(matchId) {
    try {
        const res = await fetch(`/api/match/${matchId}`);
        const json = await res.json();
        if (!json.success) throw new Error(json.error);

        const m = json.data;
        document.getElementById('modalMatchTitle').textContent = `Match #${m.match_id}: ${m.team1_name} vs ${m.team2_name}`;
        document.getElementById('modalMatchSubtitle').textContent = `${m.venue} &bull; Season ${m.season} &bull; ${m.date}`;

        document.getElementById('modalTeam1Name').textContent = m.team1_name;
        document.getElementById('modalTeam1Score').textContent = `${m.team1_score} runs`;

        document.getElementById('modalTeam2Name').textContent = m.team2_name;
        document.getElementById('modalTeam2Score').textContent = `${m.team2_score} runs`;

        document.getElementById('modalTossWinner').textContent = m.toss_winner;
        document.getElementById('modalTossDecision').textContent = `Opted to ${m.toss_decision}`;

        document.getElementById('modalWinnerBadge').textContent = `${m.winner_name} won by ${m.win_margin} ${m.win_margin_type}`;
        document.getElementById('modalPotm').textContent = m.player_of_match;

        const modal = new bootstrap.Modal(document.getElementById('matchModal'));
        modal.show();
    } catch (err) {
        alert('Could not load match scorecard: ' + err.message);
    }
}
