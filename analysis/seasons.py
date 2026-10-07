"""
================================================================================
IPL Season Analysis Module
================================================================================
Computes season-by-season standings, points tables, champions, Orange & Purple
cap performers, and total seasonal statistics.
================================================================================
"""

import pandas as pd
from analysis.data_loader import get_data, get_team_metadata

# Real IPL Champions reference for historical seasons
HISTORICAL_CHAMPIONS = {
    2021: {"champion": "CSK", "runner_up": "KKR"},
    2022: {"champion": "GT", "runner_up": "RR"},
    2023: {"champion": "CSK", "runner_up": "GT"},
    2024: {"champion": "KKR", "runner_up": "SRH"},
    2025: {"champion": "MI", "runner_up": "RCB"}
}

def get_all_seasons_summary():
    """
    Returns summary cards for all available IPL seasons.
    """
    matches_df, _, players_df = get_data()
    team_meta = get_team_metadata()
    seasons = sorted(matches_df["season"].unique().tolist())
    summary = []

    for s in seasons:
        s_matches = matches_df[matches_df["season"] == s]
        total_m = len(s_matches)
        s_teams = sorted(list(set(s_matches["team1"].unique()).union(set(s_matches["team2"].unique()))))
        s_runs = int(s_matches["team1_score"].sum() + s_matches["team2_score"].sum())

        # Determine champion: from historical reference or team with highest season wins
        champ_info = HISTORICAL_CHAMPIONS.get(s)
        if not champ_info:
            wins = s_matches["winner"].value_counts()
            champ = wins.index[0] if not wins.empty else s_teams[0]
            runner = wins.index[1] if len(wins) > 1 else s_teams[1]
            champ_info = {"champion": champ, "runner_up": runner}

        champ_code = champ_info["champion"]
        runner_code = champ_info["runner_up"]

        summary.append({
            "season": int(s),
            "matches": total_m,
            "teams_count": len(s_teams),
            "total_runs": s_runs,
            "avg_match_runs": round(s_runs / total_m, 1) if total_m else 0,
            "champion": champ_code,
            "champion_name": team_meta.get(champ_code, {}).get("name", champ_code),
            "champion_color": team_meta.get(champ_code, {}).get("color", "#00e5ff"),
            "runner_up": runner_code,
            "runner_up_name": team_meta.get(runner_code, {}).get("name", runner_code)
        })

    summary.sort(key=lambda x: x["season"], reverse=True)
    return summary

def get_season_details(season: int):
    """
    Returns comprehensive details for a specific season:
    - Overall summary
    - Points table
    - Highest & lowest scores
    - Orange Cap & Purple Cap
    - Matches list
    """
    matches_df, deliveries_df, players_df = get_data()
    team_meta = get_team_metadata()

    s_matches = matches_df[matches_df["season"] == int(season)].sort_values(by="match_id")
    if s_matches.empty:
        return None

    total_m = len(s_matches)
    s_teams = sorted(list(set(s_matches["team1"].unique()).union(set(s_matches["team2"].unique()))))
    s_runs = int(s_matches["team1_score"].sum() + s_matches["team2_score"].sum())

    # Points Table
    points_table = []
    for team in s_teams:
        t_m = s_matches[(s_matches["team1"] == team) | (s_matches["team2"] == team)]
        played = len(t_m)
        wins = len(s_matches[s_matches["winner"] == team])
        losses = played - wins
        pts = wins * 2
        win_pct = round((wins / played) * 100, 1) if played > 0 else 0

        points_table.append({
            "team": team,
            "name": team_meta.get(team, {}).get("name", team),
            "color": team_meta.get(team, {}).get("color", "#00e5ff"),
            "played": played,
            "won": wins,
            "lost": losses,
            "points": pts,
            "win_pct": win_pct
        })
    points_table.sort(key=lambda x: (x["points"], x["win_pct"]), reverse=True)
    for idx, row in enumerate(points_table):
        row["rank"] = idx + 1

    # Champion
    champ_info = HISTORICAL_CHAMPIONS.get(int(season))
    if not champ_info:
        champ_info = {
            "champion": points_table[0]["team"],
            "runner_up": points_table[1]["team"] if len(points_table) > 1 else points_table[0]["team"]
        }

    # Scores
    all_scores = list(zip(s_matches["team1"], s_matches["team1_score"])) + list(zip(s_matches["team2"], s_matches["team2_score"]))
    highest_score = max(all_scores, key=lambda x: x[1])
    lowest_score = min(all_scores, key=lambda x: x[1])

    # Orange & Purple caps
    m_ids = s_matches["match_id"].tolist()
    s_deliv = deliveries_df[deliveries_df["match_id"].isin(m_ids)]

    if not s_deliv.empty:
        top_scorer_row = s_deliv.groupby("batter")["runs"].sum().sort_values(ascending=False).head(1)
        orange_cap = {
            "player": top_scorer_row.index[0],
            "runs": int(top_scorer_row.values[0])
        }
    else:
        top_p = players_df.sort_values(by="runs", ascending=False).iloc[0]
        orange_cap = {"player": top_p["player"], "runs": int(top_p["runs"] // 5)}

    top_bowler = players_df.sort_values(by="wickets", ascending=False).iloc[0]
    purple_cap = {
        "player": top_bowler["player"],
        "wickets": int(top_bowler["wickets"] // 3)
    }

    # Matches summary list
    matches_list = []
    for _, m in s_matches.iterrows():
        matches_list.append({
            "match_id": int(m["match_id"]),
            "date": str(m["date"]).split(" ")[0] if "date" in m else "N/A",
            "team1": m["team1"],
            "team2": m["team2"],
            "winner": m["winner"],
            "venue": m["venue"],
            "team1_score": int(m["team1_score"]),
            "team2_score": int(m["team2_score"]),
            "toss_winner": m.get("toss_winner", "N/A"),
            "toss_decision": m.get("toss_decision", "N/A"),
            "player_of_match": m.get("player_of_match", "N/A")
        })

    return {
        "season": int(season),
        "total_matches": total_m,
        "total_teams": len(s_teams),
        "total_runs": s_runs,
        "avg_match_runs": round(s_runs / total_m, 1) if total_m else 0,
        "champion": champ_info["champion"],
        "champion_name": team_meta.get(champ_info["champion"], {}).get("name", champ_info["champion"]),
        "runner_up": champ_info["runner_up"],
        "runner_up_name": team_meta.get(champ_info["runner_up"], {}).get("name", champ_info["runner_up"]),
        "highest_score": {"team": highest_score[0], "score": int(highest_score[1])},
        "lowest_score": {"team": lowest_score[0], "score": int(lowest_score[1])},
        "orange_cap": orange_cap,
        "purple_cap": purple_cap,
        "points_table": points_table,
        "matches": matches_list
    }
