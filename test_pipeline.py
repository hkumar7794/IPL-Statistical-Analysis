"""
Test Script for Phase 2 Data Pipeline and Analysis Modules
"""
import sys
from analysis.data_loader import get_data, get_team_metadata
from analysis.summary import get_overall_summary
from analysis.batting import get_top_batsmen, get_batting_charts_data
from analysis.bowling import get_top_bowlers, get_bowling_charts_data
from analysis.teams import get_all_teams, get_team_details, get_head_to_head
from analysis.players import get_players_directory, get_player_profile
from analysis.seasons import get_all_seasons_summary, get_season_details
from analysis.venues import get_all_venues, get_venue_details
from analysis.toss import get_toss_analysis
from analysis.matches import get_matches_list, get_match_details

def run_tests():
    print(">>> Testing Data Loader...")
    matches_df, deliveries_df, players_df = get_data()
    assert len(matches_df) > 0, "Matches DataFrame is empty"
    assert len(deliveries_df) > 0, "Deliveries DataFrame is empty"
    assert len(players_df) > 0, "Players DataFrame is empty"
    print(f"    Loaded {len(matches_df)} matches, {len(deliveries_df)} deliveries, {len(players_df)} players.")

    print(">>> Testing Overall Summary...")
    summary = get_overall_summary()
    assert summary["kpis"]["total_matches"] == 150
    assert summary["kpis"]["total_runs"] > 0
    print(f"    KPIs: {summary['kpis']['total_matches']} matches, {summary['kpis']['total_runs']} runs.")

    print(">>> Testing Batting Module...")
    batters = get_top_batsmen(limit=5)
    assert len(batters["leaderboard"]) == 5
    bat_charts = get_batting_charts_data()
    assert len(bat_charts["top_scorers"]["labels"]) == 10
    print(f"    Top run scorer: {batters['leaderboard'][0]['player']} with {batters['leaderboard'][0]['runs']} runs.")

    print(">>> Testing Bowling Module...")
    bowlers = get_top_bowlers(limit=5)
    assert len(bowlers["leaderboard"]) > 0
    bowl_charts = get_bowling_charts_data()
    assert len(bowl_charts["top_wickets"]["labels"]) > 0
    print(f"    Top wicket taker: {bowlers['leaderboard'][0]['player']} with {bowlers['leaderboard'][0]['wickets']} wickets.")

    print(">>> Testing Teams Module...")
    teams = get_all_teams()
    assert len(teams) == 10
    csk_details = get_team_details("CSK")
    assert csk_details is not None
    h2h = get_head_to_head("MI", "CSK")
    assert h2h["total_matches"] > 0
    print(f"    Teams tested: {len(teams)} teams. MI vs CSK matches: {h2h['total_matches']}.")

    print(">>> Testing Players Module...")
    p_dir = get_players_directory(query="Kohli")
    assert p_dir["count"] >= 1
    p_prof = get_player_profile("Virat Kohli")
    assert p_prof is not None
    print(f"    Player Profile: {p_prof['player']} ({p_prof['team']}), Average: {p_prof['average']}")

    print(">>> Testing Seasons Module...")
    seasons = get_all_seasons_summary()
    assert len(seasons) == 5
    s_detail = get_season_details(2023)
    assert s_detail is not None
    print(f"    Season 2023: Champion = {s_detail['champion_name']}, Matches = {s_detail['total_matches']}.")

    print(">>> Testing Venues Module...")
    venues = get_all_venues()
    assert len(venues) == 10
    v_detail = get_venue_details("Mumbai")
    assert v_detail is not None
    print(f"    Venues tested: {len(venues)}. Top venue: {venues[0]['venue']} ({venues[0]['matches_played']} matches).")

    print(">>> Testing Toss Module...")
    toss = get_toss_analysis()
    assert toss["total_matches"] == 150
    print(f"    Toss Analysis: {toss['decisions']['field_pct']}% opted to field. Win rate: {toss['match_outcomes']['toss_win_match_win_pct']}%.")

    print(">>> Testing Matches Module...")
    matches_res = get_matches_list(limit=10)
    assert len(matches_res["matches"]) == 10
    m_detail = get_match_details(1)
    assert m_detail is not None
    print(f"    Match 1: {m_detail['team1']} vs {m_detail['team2']}, Winner: {m_detail['winner']}.")

    print("\n[SUCCESS] ALL PHASE 2 PIPELINE & ANALYSIS TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
