"""
================================================================================
IPL Match Analysis & Explorer Module
================================================================================
Provides search, filtering, and deep-dive match breakdown with scores,
toss information, player of the match, and delivery-level innings summaries.
================================================================================
"""

import pandas as pd
from analysis.data_loader import get_data, get_team_metadata

def get_matches_list(season: int = None, team: str = "", venue: str = "", limit: int = 50, page: int = 1):
    """
    Returns filtered match records.
    """
    matches_df, _, _ = get_data()
    team_meta = get_team_metadata()
    df = matches_df.sort_values(by="match_id", ascending=False).copy()

    if season is not None:
        df = df[df["season"] == int(season)]

    if team and team != "ALL":
        t = team.strip().upper()
        df = df[(df["team1"] == t) | (df["team2"] == t)]

    if venue and venue != "ALL":
        v = venue.strip().lower()
        df = df[df["venue"].str.lower() == v]

    total_count = len(df)
    start_idx = (page - 1) * limit
    paginated = df.iloc[start_idx:start_idx + limit]

    matches_list = []
    for _, m in paginated.iterrows():
        matches_list.append({
            "match_id": int(m["match_id"]),
            "season": int(m["season"]),
            "date": str(m["date"]).split(" ")[0] if "date" in m else "N/A",
            "team1": m["team1"],
            "team1_name": team_meta.get(m["team1"], {}).get("name", m["team1"]),
            "team2": m["team2"],
            "team2_name": team_meta.get(m["team2"], {}).get("name", m["team2"]),
            "venue": m["venue"],
            "team1_score": int(m["team1_score"]),
            "team2_score": int(m["team2_score"]),
            "winner": m["winner"],
            "winner_name": team_meta.get(m["winner"], {}).get("name", m["winner"]),
            "win_margin": int(m.get("win_margin", 0)),
            "win_margin_type": m.get("win_margin_type", "runs"),
            "toss_winner": m.get("toss_winner", "N/A"),
            "toss_decision": m.get("toss_decision", "N/A"),
            "player_of_match": m.get("player_of_match", "N/A")
        })

    return {
        "total": total_count,
        "page": page,
        "limit": limit,
        "matches": matches_list
    }

def get_match_details(match_id: int):
    """
    Returns full details for an individual match, including innings overview.
    """
    matches_df, deliveries_df, _ = get_data()
    team_meta = get_team_metadata()

    m_row = matches_df[matches_df["match_id"] == int(match_id)]
    if m_row.empty:
        return None

    m = m_row.iloc[0]
    m_deliv = deliveries_df[deliveries_df["match_id"] == int(match_id)]

    # Top batters in this match from deliveries if recorded
    innings1_batsmen = []
    innings2_batsmen = []
    if not m_deliv.empty:
        inn1 = m_deliv[m_deliv["inning"] == 1]
        inn2 = m_deliv[m_deliv["inning"] == 2]

        top_inn1 = inn1.groupby("batter")["runs"].sum().sort_values(ascending=False).head(5)
        innings1_batsmen = [{"batter": b, "runs": int(r)} for b, r in top_inn1.items()]

        top_inn2 = inn2.groupby("batter")["runs"].sum().sort_values(ascending=False).head(5)
        innings2_batsmen = [{"batter": b, "runs": int(r)} for b, r in top_inn2.items()]

    return {
        "match_id": int(m["match_id"]),
        "season": int(m["season"]),
        "date": str(m["date"]).split(" ")[0] if "date" in m else "N/A",
        "team1": m["team1"],
        "team1_name": team_meta.get(m["team1"], {}).get("name", m["team1"]),
        "team2": m["team2"],
        "team2_name": team_meta.get(m["team2"], {}).get("name", m["team2"]),
        "venue": m["venue"],
        "team1_score": int(m["team1_score"]),
        "team2_score": int(m["team2_score"]),
        "winner": m["winner"],
        "winner_name": team_meta.get(m["winner"], {}).get("name", m["winner"]),
        "win_margin": int(m.get("win_margin", 0)),
        "win_margin_type": m.get("win_margin_type", "runs"),
        "toss_winner": m.get("toss_winner", "N/A"),
        "toss_decision": m.get("toss_decision", "N/A"),
        "player_of_match": m.get("player_of_match", "N/A"),
        "innings1_top_scorers": innings1_batsmen,
        "innings2_top_scorers": innings2_batsmen
    }
