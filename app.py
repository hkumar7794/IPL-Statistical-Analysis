"""
================================================================================
IPL Statistical Analysis - Production Flask Application
================================================================================
Full-stack REST API and dynamic web platform for IPL historical data analytics.
Includes endpoints for summary KPIs, batting, bowling, team performance,
player database, head-to-head records, toss analysis, venues, and seasons.
================================================================================
"""

import os
from pathlib import Path
from flask import Flask, jsonify, render_template, request, abort

# Import our modular data processing engines
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

app = Flask(__name__)

# ==============================================================================
# 1. HTML WEB PAGE ROUTES
# ==============================================================================

@app.route("/")
def page_home():
    """Home / Main Analytics Dashboard."""
    return render_template("index.html")

@app.route("/teams")
def page_teams():
    """Teams Overview Page."""
    return render_template("teams.html")

@app.route("/team-analysis")
def page_team_analysis():
    """Detailed Single Team Performance Analysis."""
    return render_template("team-analysis.html")

@app.route("/players")
def page_players():
    """Player Directory & Performance Profiler."""
    return render_template("players.html")

@app.route("/batting")
def page_batting():
    """Batting Analytics & Records Page."""
    return render_template("batting.html")

@app.route("/bowling")
def page_bowling():
    """Bowling Analytics & Records Page."""
    return render_template("bowling.html")

@app.route("/head-to-head")
def page_head_to_head():
    """Head-to-Head Team Comparison Tool."""
    return render_template("head-to-head.html")

@app.route("/venues")
def page_venues():
    """Stadium & Venue Analysis Page."""
    return render_template("venues.html")

@app.route("/toss")
def page_toss():
    """Toss Decision & Match Impact Analysis."""
    return render_template("toss.html")

@app.route("/seasons")
def page_seasons():
    """Season Standings & Points Table Page."""
    return render_template("seasons.html")

@app.route("/matches")
def page_matches():
    """Match Explorer & Scorecard Search."""
    return render_template("matches.html")


# ==============================================================================
# 2. REST API ENDPOINTS
# ==============================================================================

@app.route("/api/health", methods=["GET"])
def api_health():
    """
    Health check endpoint (Preserved from Phase 1).
    Used for monitoring server uptime and status.
    """
    return jsonify({
        "status": "healthy",
        "message": "IPL Statistical Analysis Backend is online and ready!"
    }), 200

@app.route("/api/summary", methods=["GET"])
def api_summary():
    """Returns overall tournament KPIs, seasons, and dashboard charts data."""
    try:
        data = get_overall_summary()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to calculate summary: {str(e)}"}), 500

@app.route("/api/teams", methods=["GET"])
def api_teams():
    """Returns all IPL teams with matches, win percentages, and titles."""
    try:
        teams = get_all_teams()
        return jsonify({"success": True, "count": len(teams), "data": teams}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to retrieve teams: {str(e)}"}), 500

@app.route("/api/team/<team_name>", methods=["GET"])
def api_team_details(team_name):
    """Returns deep performance analytics for a single team."""
    try:
        details = get_team_details(team_name)
        if details is None:
            return jsonify({"success": False, "error": f"Team '{team_name}' not found"}), 404
        return jsonify({"success": True, "data": details}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Error retrieving team {team_name}: {str(e)}"}), 500

@app.route("/api/team-comparison", methods=["GET"])
def api_team_comparison():
    """
    Head-to-head comparison between two teams.
    Query parameters: ?team1=MI&team2=CSK
    """
    try:
        t1 = request.args.get("team1", "MI").strip().upper()
        t2 = request.args.get("team2", "CSK").strip().upper()

        if t1 == t2:
            return jsonify({"success": False, "error": "Please select two different teams to compare"}), 400

        data = get_head_to_head(t1, t2)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Head-to-head calculation error: {str(e)}"}), 500

@app.route("/api/players", methods=["GET"])
def api_players():
    """
    Searchable and filterable player directory.
    Query parameters: ?query=virat&team=RCB&role=Batter
    """
    try:
        query = request.args.get("query", "")
        team = request.args.get("team", "")
        role = request.args.get("role", "")
        res = get_players_directory(query=query, team=team, role=role)
        return jsonify({"success": True, "data": res}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Error searching players: {str(e)}"}), 500

@app.route("/api/player/<player_name>", methods=["GET"])
def api_player_profile(player_name):
    """Returns complete career statistics for a specific player."""
    try:
        profile = get_player_profile(player_name)
        if profile is None:
            return jsonify({"success": False, "error": f"Player '{player_name}' not found"}), 404
        return jsonify({"success": True, "data": profile}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Error loading player profile: {str(e)}"}), 500

@app.route("/api/top-batsmen", methods=["GET"])
@app.route("/api/batting", methods=["GET"])
def api_top_batsmen():
    """
    Batting leaderboard.
    Query parameters: ?season=2023&limit=20&sort=runs
    """
    try:
        season_param = request.args.get("season", None)
        season = int(season_param) if season_param and season_param != "ALL" else None
        limit = int(request.args.get("limit", 20))
        sort_by = request.args.get("sort", "runs")

        data = get_top_batsmen(season=season, limit=limit, sort_by=sort_by)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Batting analytics error: {str(e)}"}), 500

@app.route("/api/batting/charts", methods=["GET"])
def api_batting_charts():
    """Batting visualization datasets for Chart.js."""
    try:
        data = get_batting_charts_data()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Batting charts error: {str(e)}"}), 500

@app.route("/api/top-bowlers", methods=["GET"])
@app.route("/api/bowling", methods=["GET"])
def api_top_bowlers():
    """
    Bowling leaderboard.
    Query parameters: ?season=2023&limit=20&sort=wickets
    """
    try:
        season_param = request.args.get("season", None)
        season = int(season_param) if season_param and season_param != "ALL" else None
        limit = int(request.args.get("limit", 20))
        sort_by = request.args.get("sort", "wickets")

        data = get_top_bowlers(season=season, limit=limit, sort_by=sort_by)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Bowling analytics error: {str(e)}"}), 500

@app.route("/api/bowling/charts", methods=["GET"])
def api_bowling_charts():
    """Bowling visualization datasets for Chart.js."""
    try:
        data = get_bowling_charts_data()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Bowling charts error: {str(e)}"}), 500

@app.route("/api/seasons", methods=["GET"])
def api_seasons():
    """Returns summary cards of all IPL seasons."""
    try:
        seasons = get_all_seasons_summary()
        return jsonify({"success": True, "count": len(seasons), "data": seasons}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Seasons error: {str(e)}"}), 500

@app.route("/api/season/<int:season>", methods=["GET"])
def api_season_details(season):
    """Returns full details, points table, and records for an IPL season."""
    try:
        details = get_season_details(season)
        if details is None:
            return jsonify({"success": False, "error": f"Season '{season}' not found"}), 404
        return jsonify({"success": True, "data": details}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Season details error: {str(e)}"}), 500

@app.route("/api/venues", methods=["GET"])
def api_venues():
    """Returns all IPL stadiums with matches and records."""
    try:
        venues = get_all_venues()
        return jsonify({"success": True, "count": len(venues), "data": venues}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Venues error: {str(e)}"}), 500

@app.route("/api/venue/<venue_name>", methods=["GET"])
def api_venue_details(venue_name):
    """Returns deep venue statistics and match history."""
    try:
        details = get_venue_details(venue_name)
        if details is None:
            return jsonify({"success": False, "error": f"Venue '{venue_name}' not found"}), 404
        return jsonify({"success": True, "data": details}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Venue details error: {str(e)}"}), 500

@app.route("/api/toss-analysis", methods=["GET"])
@app.route("/api/toss", methods=["GET"])
def api_toss():
    """Returns toss decisions, win correlations, and season shifts."""
    try:
        data = get_toss_analysis()
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Toss analysis error: {str(e)}"}), 500

@app.route("/api/matches", methods=["GET"])
def api_matches():
    """
    Searchable & filterable match list.
    Query parameters: ?season=2023&team=CSK&venue=Mumbai&page=1&limit=25
    """
    try:
        season_param = request.args.get("season", None)
        season = int(season_param) if season_param and season_param != "ALL" else None
        team = request.args.get("team", "")
        venue = request.args.get("venue", "")
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 25))

        data = get_matches_list(season=season, team=team, venue=venue, limit=limit, page=page)
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Matches error: {str(e)}"}), 500

@app.route("/api/match/<int:match_id>", methods=["GET"])
def api_match_details(match_id):
    """Returns scorecard and breakdown for a single match."""
    try:
        details = get_match_details(match_id)
        if details is None:
            return jsonify({"success": False, "error": f"Match ID '{match_id}' not found"}), 404
        return jsonify({"success": True, "data": details}), 200
    except Exception as e:
        return jsonify({"success": False, "error": f"Match details error: {str(e)}"}), 500


# ==============================================================================
# 3. GLOBAL ERROR HANDLERS
# ==============================================================================

@app.errorhandler(404)
def error_404(e):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Endpoint or resource not found"}), 404
    return render_template("index.html"), 404

@app.errorhandler(500)
def error_500(e):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "error": "Internal server error occurred"}), 500
    return render_template("index.html"), 500


# ==============================================================================
# 4. SERVER RUNNER
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" 🏏 IPL Statistical Analysis - Full-Stack Server Running")
    print(" 🌐 Localhost URL : http://127.0.0.1:5000")
    print(" 🩺 Health Check  : http://127.0.0.1:5000/api/health")
    print(" 📊 API Summary   : http://127.0.0.1:5000/api/summary")
    print("=" * 60 + "\n")
    app.run(debug=True, port=5000)
