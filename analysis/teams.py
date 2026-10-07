"""
================================================================================
IPL Team Analysis & Performance Module
================================================================================
Computes overall team records, win rates, highest/lowest totals,
season-by-season performance, and head-to-head records.
================================================================================
"""

import pandas as pd
from analysis.data_loader import get_data, get_team_metadata

# Real IPL Historical Trophy Count
IPL_TITLES = {
    "MI": 5,
    "CSK": 5,
    "KKR": 3,
    "SRH": 1,
    "RR": 1,
    "GT": 1,
    "RCB": 0,
    "DC": 0,
    "PBKS": 0,
    "LSG": 0
}

def get_all_teams():
    """
    Returns all teams with matches played, won, lost, win %,
    average score, highest score, titles, and brand colors.
    """
    matches_df, _, _ = get_data()
    team_meta = get_team_metadata()

    # Identify all teams
    all_teams = sorted(list(set(matches_df["team1"].unique()).union(set(matches_df["team2"].unique()))))
    teams_stats = []

    for team in all_teams:
        t_matches = matches_df[(matches_df["team1"] == team) | (matches_df["team2"] == team)]
        total_played = len(t_matches)
        wins = len(matches_df[matches_df["winner"] == team])
        losses = total_played - wins
        win_pct = round((wins / total_played) * 100, 1) if total_played > 0 else 0

        # Calculate scores when batting as team1 or team2
        scores_as_t1 = matches_df[matches_df["team1"] == team]["team1_score"].tolist()
        scores_as_t2 = matches_df[matches_df["team2"] == team]["team2_score"].tolist()
        all_scores = scores_as_t1 + scores_as_t2

        total_runs = sum(all_scores)
        avg_score = round(total_runs / len(all_scores), 1) if all_scores else 0
        highest_score = max(all_scores) if all_scores else 0
        lowest_score = min(all_scores) if all_scores else 0

        teams_stats.append({
            "team": team,
            "name": team_meta.get(team, {}).get("name", team),
            "color": team_meta.get(team, {}).get("color", "#00e5ff"),
            "matches_played": total_played,
            "wins": wins,
            "losses": losses,
            "win_pct": win_pct,
            "titles": IPL_TITLES.get(team, 0),
            "total_runs": total_runs,
            "avg_score": avg_score,
            "highest_score": highest_score,
            "lowest_score": lowest_score
        })

    # Sort primarily by wins and win percentage
    teams_stats.sort(key=lambda x: (x["wins"], x["win_pct"]), reverse=True)
    return teams_stats

def get_team_details(team_name: str):
    """
    Returns comprehensive metrics for a single team:
    - Overall record
    - Season-by-season win/loss record and average scores
    - Head-to-head record against all other opponents
    - Recent matches
    """
    matches_df, _, _ = get_data()
    team = team_name.strip().upper()
    team_meta = get_team_metadata()

    # Verify team exists
    all_teams = set(matches_df["team1"].unique()).union(set(matches_df["team2"].unique()))
    if team not in all_teams:
        return None

    t_matches = matches_df[(matches_df["team1"] == team) | (matches_df["team2"] == team)].sort_values(by="match_id", ascending=False)
    total_played = len(t_matches)
    wins = len(matches_df[matches_df["winner"] == team])
    losses = total_played - wins
    win_pct = round((wins / total_played) * 100, 1) if total_played > 0 else 0

    scores_as_t1 = matches_df[matches_df["team1"] == team]["team1_score"].tolist()
    scores_as_t2 = matches_df[matches_df["team2"] == team]["team2_score"].tolist()
    all_scores = scores_as_t1 + scores_as_t2
    avg_score = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0
    highest_score = max(all_scores) if all_scores else 0
    lowest_score = min(all_scores) if all_scores else 0

    # Season-by-season breakdown
    seasons = sorted(t_matches["season"].unique().tolist())
    season_performance = []
    for s in seasons:
        s_m = t_matches[t_matches["season"] == s]
        s_wins = len(s_m[s_m["winner"] == team])
        s_total = len(s_m)
        s_losses = s_total - s_wins
        s_win_pct = round((s_wins / s_total) * 100, 1) if s_total > 0 else 0

        season_performance.append({
            "season": int(s),
            "matches": s_total,
            "wins": s_wins,
            "losses": s_losses,
            "win_pct": s_win_pct
        })

    # Opponent records
    opponent_stats = {}
    for _, m in t_matches.iterrows():
        opp = m["team2"] if m["team1"] == team else m["team1"]
        if opp not in opponent_stats:
            opponent_stats[opp] = {"opponent": opp, "played": 0, "wins": 0, "losses": 0}
        opponent_stats[opp]["played"] += 1
        if m["winner"] == team:
            opponent_stats[opp]["wins"] += 1
        else:
            opponent_stats[opp]["losses"] += 1

    for opp, stats in opponent_stats.items():
        stats["win_pct"] = round((stats["wins"] / stats["played"]) * 100, 1)

    opponents_list = list(opponent_stats.values())
    opponents_list.sort(key=lambda x: x["played"], reverse=True)

    # Recent 10 matches
    recent = []
    for _, m in t_matches.head(10).iterrows():
        opp = m["team2"] if m["team1"] == team else m["team1"]
        result = "WON" if m["winner"] == team else "LOST"
        team_score = m["team1_score"] if m["team1"] == team else m["team2_score"]
        opp_score = m["team2_score"] if m["team1"] == team else m["team1_score"]
        recent.append({
            "match_id": int(m["match_id"]),
            "season": int(m["season"]),
            "opponent": opp,
            "venue": m["venue"],
            "team_score": int(team_score),
            "opp_score": int(opp_score),
            "result": result,
            "winner": m["winner"]
        })

    return {
        "team": team,
        "name": team_meta.get(team, {}).get("name", team),
        "color": team_meta.get(team, {}).get("color", "#00e5ff"),
        "titles": IPL_TITLES.get(team, 0),
        "matches_played": total_played,
        "wins": wins,
        "losses": losses,
        "win_pct": win_pct,
        "avg_score": avg_score,
        "highest_score": highest_score,
        "lowest_score": lowest_score,
        "season_performance": season_performance,
        "opponents": opponents_list,
        "recent_matches": recent
    }

def get_head_to_head(team1: str, team2: str):
    """
    Direct head-to-head comparison between two teams.
    """
    matches_df, _, _ = get_data()
    team1 = team1.strip().upper()
    team2 = team2.strip().upper()
    team_meta = get_team_metadata()

    # Filter matches where both teams played against each other
    h2h_matches = matches_df[
        ((matches_df["team1"] == team1) & (matches_df["team2"] == team2)) |
        ((matches_df["team1"] == team2) & (matches_df["team2"] == team1))
    ].sort_values(by="match_id", ascending=False)

    total_played = len(h2h_matches)
    team1_wins = len(h2h_matches[h2h_matches["winner"] == team1])
    team2_wins = len(h2h_matches[h2h_matches["winner"] == team2])
    ties_no_result = total_played - (team1_wins + team2_wins)

    # Average scores in head-to-head encounters
    t1_scores = []
    t2_scores = []
    for _, m in h2h_matches.iterrows():
        if m["team1"] == team1:
            t1_scores.append(m["team1_score"])
            t2_scores.append(m["team2_score"])
        else:
            t1_scores.append(m["team2_score"])
            t2_scores.append(m["team1_score"])

    t1_avg = round(sum(t1_scores) / len(t1_scores), 1) if t1_scores else 0
    t2_avg = round(sum(t2_scores) / len(t2_scores), 1) if t2_scores else 0

    # Recent encounters
    encounters = []
    for _, m in h2h_matches.head(10).iterrows():
        encounters.append({
            "match_id": int(m["match_id"]),
            "season": int(m["season"]),
            "venue": m["venue"],
            "team1": m["team1"],
            "team2": m["team2"],
            "team1_score": int(m["team1_score"]),
            "team2_score": int(m["team2_score"]),
            "winner": m["winner"]
        })

    return {
        "team1": {
            "code": team1,
            "name": team_meta.get(team1, {}).get("name", team1),
            "wins": team1_wins,
            "win_pct": round((team1_wins / total_played) * 100, 1) if total_played else 0,
            "avg_score": t1_avg,
            "color": team_meta.get(team1, {}).get("color", "#00e5ff")
        },
        "team2": {
            "code": team2,
            "name": team_meta.get(team2, {}).get("name", team2),
            "wins": team2_wins,
            "win_pct": round((team2_wins / total_played) * 100, 1) if total_played else 0,
            "avg_score": t2_avg,
            "color": team_meta.get(team2, {}).get("color", "#ff007f")
        },
        "total_matches": total_played,
        "recent_matches": encounters
    }
