"""
================================================================================
IPL Toss Analysis Module
================================================================================
Analyzes toss trends, decisions (bat first vs field first), correlation
between winning the toss and winning the match, and season-wise toss shifts.
================================================================================
"""

import pandas as pd
from analysis.data_loader import get_data, get_team_metadata

def get_toss_analysis():
    """
    Computes overall toss metrics, decision breakdown, and match outcome
    correlations.
    """
    matches_df, _, _ = get_data()
    total_matches = len(matches_df)

    # 1. Toss decisions count
    decisions = matches_df["toss_decision"].value_counts().to_dict()
    field_count = int(decisions.get("field", 0))
    bat_count = int(decisions.get("bat", 0))
    field_pct = round((field_count / total_matches) * 100, 1) if total_matches else 0
    bat_pct = round((bat_count / total_matches) * 100, 1) if total_matches else 0

    # 2. Toss Winner won Match
    toss_and_match = matches_df[matches_df["toss_winner"] == matches_df["winner"]]
    toss_win_match_win_count = len(toss_and_match)
    toss_win_match_loss_count = total_matches - toss_win_match_win_count
    toss_win_match_win_pct = round((toss_win_match_win_count / total_matches) * 100, 1) if total_matches else 0

    # 3. Decision Success Rates
    field_matches = matches_df[matches_df["toss_decision"] == "field"]
    field_and_win = len(field_matches[field_matches["toss_winner"] == field_matches["winner"]])
    field_win_rate = round((field_and_win / len(field_matches)) * 100, 1) if len(field_matches) else 0

    bat_matches = matches_df[matches_df["toss_decision"] == "bat"]
    bat_and_win = len(bat_matches[bat_matches["toss_winner"] == bat_matches["winner"]])
    bat_win_rate = round((bat_and_win / len(bat_matches)) * 100, 1) if len(bat_matches) else 0

    # 4. Toss Winners Leaderboard
    team_meta = get_team_metadata()
    toss_winners = matches_df["toss_winner"].value_counts().to_dict()
    toss_winners_list = []
    for team, count in toss_winners.items():
        toss_winners_list.append({
            "team": team,
            "name": team_meta.get(team, {}).get("name", team),
            "toss_wins": int(count),
            "color": team_meta.get(team, {}).get("color", "#00e5ff")
        })

    # 5. Season-by-Season Toss Decisions
    seasons = sorted(matches_df["season"].unique().tolist())
    season_trends = []
    for s in seasons:
        s_m = matches_df[matches_df["season"] == s]
        s_field = int(len(s_m[s_m["toss_decision"] == "field"]))
        s_bat = int(len(s_m[s_m["toss_decision"] == "bat"]))
        season_trends.append({
            "season": int(s),
            "field": s_field,
            "bat": s_bat
        })

    return {
        "total_matches": total_matches,
        "decisions": {
            "field_count": field_count,
            "bat_count": bat_count,
            "field_pct": field_pct,
            "bat_pct": bat_pct
        },
        "match_outcomes": {
            "toss_winner_won_match": toss_win_match_win_count,
            "toss_winner_lost_match": toss_win_match_loss_count,
            "toss_win_match_win_pct": toss_win_match_win_pct
        },
        "decision_success": {
            "field_win_rate": field_win_rate,
            "bat_win_rate": bat_win_rate
        },
        "toss_winners": toss_winners_list,
        "season_trends": season_trends
    }
