"""
================================================================================
IPL Venue & Stadium Analysis Module
================================================================================
Computes stadium statistics, average first and second innings totals,
highest team totals, team fortress records, and toss trends per venue.
================================================================================
"""

import pandas as pd
from analysis.data_loader import get_data, get_team_metadata

def get_all_venues():
    """
    Returns summary statistics for all IPL stadiums.
    """
    matches_df, _, _ = get_data()
    venues = sorted(matches_df["venue"].unique().tolist())
    team_meta = get_team_metadata()
    venue_stats = []

    for venue in venues:
        v_matches = matches_df[matches_df["venue"] == venue]
        total_m = len(v_matches)

        # Average innings score
        t1_scores = v_matches["team1_score"].tolist()
        t2_scores = v_matches["team2_score"].tolist()
        avg_1st_innings = round(sum(t1_scores) / len(t1_scores), 1) if t1_scores else 0
        avg_2nd_innings = round(sum(t2_scores) / len(t2_scores), 1) if t2_scores else 0

        # Highest score
        all_v_scores = list(zip(v_matches["team1"], t1_scores)) + list(zip(v_matches["team2"], t2_scores))
        high_score_entry = max(all_v_scores, key=lambda x: x[1]) if all_v_scores else ("N/A", 0)

        # Most successful team at venue
        wins = v_matches["winner"].value_counts()
        top_team = wins.index[0] if not wins.empty else "N/A"
        top_team_wins = int(wins.iloc[0]) if not wins.empty else 0

        # Bat first vs Field first wins
        bat_first_wins = len(v_matches[v_matches["winner"] == v_matches["team1"]])
        field_first_wins = len(v_matches[v_matches["winner"] == v_matches["team2"]])

        venue_stats.append({
            "venue": venue,
            "matches_played": total_m,
            "avg_1st_innings": avg_1st_innings,
            "avg_2nd_innings": avg_2nd_innings,
            "highest_score": {
                "team": high_score_entry[0],
                "score": int(high_score_entry[1])
            },
            "most_successful_team": {
                "team": top_team,
                "name": team_meta.get(top_team, {}).get("name", top_team),
                "wins": top_team_wins
            },
            "bat_first_wins": bat_first_wins,
            "field_first_wins": field_first_wins
        })

    venue_stats.sort(key=lambda x: x["matches_played"], reverse=True)
    return venue_stats

def get_venue_details(venue_name: str):
    """
    Returns deep-dive statistics and match list for a specific venue.
    """
    matches_df, _, _ = get_data()
    v_name = venue_name.strip()

    v_matches = matches_df[matches_df["venue"].str.lower() == v_name.lower()].sort_values(by="match_id", ascending=False)
    if v_matches.empty:
        return None

    total_m = len(v_matches)
    t1_scores = v_matches["team1_score"].tolist()
    t2_scores = v_matches["team2_score"].tolist()
    avg_1st = round(sum(t1_scores) / total_m, 1) if total_m else 0
    avg_2nd = round(sum(t2_scores) / total_m, 1) if total_m else 0

    all_scores = list(zip(v_matches["team1"], t1_scores)) + list(zip(v_matches["team2"], t2_scores))
    high_score = max(all_scores, key=lambda x: x[1])

    # Wins distribution
    team_wins = v_matches["winner"].value_counts().to_dict()

    # Toss decision breakdown
    toss_decisions = v_matches["toss_decision"].value_counts().to_dict()

    # Matches
    recent = []
    for _, m in v_matches.head(10).iterrows():
        recent.append({
            "match_id": int(m["match_id"]),
            "season": int(m["season"]),
            "team1": m["team1"],
            "team2": m["team2"],
            "team1_score": int(m["team1_score"]),
            "team2_score": int(m["team2_score"]),
            "winner": m["winner"],
            "player_of_match": m.get("player_of_match", "N/A")
        })

    return {
        "venue": venue_name,
        "total_matches": total_m,
        "avg_1st_innings": avg_1st,
        "avg_2nd_innings": avg_2nd,
        "highest_score": {"team": high_score[0], "score": int(high_score[1])},
        "team_wins": [{"team": t, "wins": int(w)} for t, w in team_wins.items()],
        "toss_decisions": toss_decisions,
        "recent_matches": recent
    }
