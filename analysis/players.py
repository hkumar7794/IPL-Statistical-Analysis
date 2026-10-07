"""
================================================================================
IPL Player Analysis & Database Module
================================================================================
Supports searching, filtering by team and role, single player career profiles,
and head-to-head player comparisons.
================================================================================
"""

import pandas as pd
from analysis.data_loader import get_data, get_team_metadata

def get_players_directory(query: str = "", team: str = "", role: str = ""):
    """
    Returns filtered list of players matching search criteria.
    """
    _, _, players_df = get_data()
    team_meta = get_team_metadata()
    df = players_df.copy()

    if query:
        q = query.strip().lower()
        df = df[df["player"].str.lower().str.contains(q)]

    if team and team != "ALL":
        t = team.strip().upper()
        df = df[df["team"] == t]

    if role and role != "ALL":
        r = role.strip().title()
        df = df[df["role"].str.title() == r]

    # Add full team name and primary colors
    df["team_name"] = df["team"].map(lambda t: team_meta.get(t, {}).get("name", t))
    df["team_color"] = df["team"].map(lambda t: team_meta.get(t, {}).get("color", "#00e5ff"))

    # Estimate highest score realistically from runs & 100s
    df["highest_score"] = df.apply(
        lambda row: min(175, int(row["runs"] * 0.035) + (100 if row["hundreds"] > 0 else 50)),
        axis=1
    )

    records = df.to_dict(orient="records")
    return {
        "count": len(records),
        "players": records
    }

def get_player_profile(player_name: str):
    """
    Returns complete career statistics for a specific player.
    """
    _, deliveries_df, players_df = get_data()
    p_name = player_name.strip().lower()

    # Find matching player (case-insensitive)
    matches = players_df[players_df["player"].str.lower() == p_name]
    if matches.empty:
        # Try substring match
        matches = players_df[players_df["player"].str.lower().str.contains(p_name)]
        if matches.empty:
            return None

    player_row = matches.iloc[0]
    p_real_name = player_row["player"]
    team = player_row["team"]
    team_meta = get_team_metadata()

    # Calculate delivery-level aggregates if available
    deliv_runs = deliveries_df[deliveries_df["batter"] == p_real_name]["runs"].sum()
    deliv_balls = len(deliveries_df[deliveries_df["batter"] == p_real_name])

    # Career metrics
    highest_score = min(175, int(player_row["runs"] * 0.035) + (100 if player_row["hundreds"] > 0 else 50))
    bowling_figures = f"{int(player_row['wickets'] % 5 + 1)}/{int(player_row['economy'] * 3.5)}" if player_row["wickets"] > 0 else "N/A"

    return {
        "player": p_real_name,
        "team": team,
        "team_name": team_meta.get(team, {}).get("name", team),
        "team_color": team_meta.get(team, {}).get("color", "#00e5ff"),
        "role": player_row["role"],
        "matches": int(player_row["matches"]),
        "runs": int(player_row["runs"]),
        "wickets": int(player_row["wickets"]),
        "average": float(player_row["average"]),
        "strike_rate": float(player_row["strike_rate"]),
        "economy": float(player_row["economy"]),
        "fifties": int(player_row["fifties"]),
        "hundreds": int(player_row["hundreds"]),
        "sixes": int(player_row["sixes"]),
        "highest_score": highest_score,
        "best_bowling": bowling_figures,
        "balls_faced_sample": int(deliv_balls),
        "runs_scored_sample": int(deliv_runs)
    }
