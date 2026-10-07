"""
================================================================================
IPL General Summary & Dashboard Statistics
================================================================================
Calculates overall key performance indicators (KPIs) and summary chart data
for the dashboard.
================================================================================
"""

import pandas as pd
from analysis.data_loader import get_data, get_team_metadata

def get_overall_summary():
    """
    Computes overall IPL summary metrics across all seasons.
    """
    matches_df, deliveries_df, players_df = get_data()

    total_matches = int(len(matches_df))
    seasons = sorted([int(s) for s in matches_df["season"].unique()])
    total_seasons = len(seasons)

    teams = sorted(list(set(matches_df["team1"].unique()).union(set(matches_df["team2"].unique()))))
    total_teams = len(teams)

    total_players = int(len(players_df))
    venues = sorted(matches_df["venue"].unique().tolist())
    total_venues = len(venues)

    total_runs = int(matches_df["team1_score"].sum() + matches_df["team2_score"].sum())
    total_wickets = int(players_df["wickets"].sum())

    avg_runs_per_match = round(total_runs / total_matches, 1) if total_matches > 0 else 0

    # Highest and lowest scores recorded
    all_scores = list(zip(matches_df["team1"], matches_df["team1_score"])) + list(zip(matches_df["team2"], matches_df["team2_score"]))
    highest_score_item = max(all_scores, key=lambda x: x[1]) if all_scores else ("N/A", 0)
    lowest_score_item = min(all_scores, key=lambda x: x[1]) if all_scores else ("N/A", 0)

    # Season breakdown
    season_summary = []
    for s in seasons:
        s_matches = matches_df[matches_df["season"] == s]
        s_runs = int(s_matches["team1_score"].sum() + s_matches["team2_score"].sum())
        season_summary.append({
            "season": s,
            "matches": int(len(s_matches)),
            "runs": s_runs,
            "avg_score": round(s_runs / (len(s_matches) * 2), 1) if len(s_matches) > 0 else 0
        })

    # Team wins distribution
    team_wins = matches_df["winner"].value_counts().to_dict()
    team_meta = get_team_metadata()
    team_wins_list = []
    for team in teams:
        team_wins_list.append({
            "team": team,
            "name": team_meta.get(team, {}).get("name", team),
            "wins": int(team_wins.get(team, 0)),
            "color": team_meta.get(team, {}).get("color", "#00e5ff")
        })
    team_wins_list.sort(key=lambda x: x["wins"], reverse=True)

    # Toss decision breakdown
    toss_decisions = matches_df["toss_decision"].value_counts().to_dict()

    # Toss winner winning match
    toss_and_match_win = int(matches_df["toss_match_winner"].sum())
    toss_win_match_lost = total_matches - toss_and_match_win

    return {
        "kpis": {
            "total_matches": total_matches,
            "total_seasons": total_seasons,
            "total_teams": total_teams,
            "total_players": total_players,
            "total_venues": total_venues,
            "total_runs": total_runs,
            "total_wickets": total_wickets,
            "avg_runs_per_match": avg_runs_per_match,
            "highest_score": {
                "team": highest_score_item[0],
                "score": int(highest_score_item[1])
            },
            "lowest_score": {
                "team": lowest_score_item[0],
                "score": int(lowest_score_item[1])
            }
        },
        "seasons_list": seasons,
        "season_summary": season_summary,
        "team_wins": team_wins_list,
        "toss_stats": {
            "decisions": toss_decisions,
            "toss_winner_won_match": toss_and_match_win,
            "toss_winner_lost_match": toss_win_match_lost,
            "toss_win_match_win_pct": round((toss_and_match_win / total_matches) * 100, 1) if total_matches else 0
        }
    }
