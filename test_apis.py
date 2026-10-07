"""
Automated API Test Suite for IPL Statistical Analysis
Tests all endpoints using Flask's test_client.
"""

from app import app

def run_api_tests():
    client = app.test_client()
    endpoints = [
        ("/api/health", 200),
        ("/api/summary", 200),
        ("/api/teams", 200),
        ("/api/team/CSK", 200),
        ("/api/team-comparison?team1=MI&team2=CSK", 200),
        ("/api/players?query=Virat", 200),
        ("/api/player/Virat Kohli", 200),
        ("/api/top-batsmen?limit=10", 200),
        ("/api/batting/charts", 200),
        ("/api/top-bowlers?limit=10", 200),
        ("/api/bowling/charts", 200),
        ("/api/seasons", 200),
        ("/api/season/2023", 200),
        ("/api/venues", 200),
        ("/api/venue/Mumbai", 200),
        ("/api/toss-analysis", 200),
        ("/api/matches?limit=10", 200),
        ("/api/match/1", 200),
        ("/api/team/UNKNOWN_TEAM", 404),
        ("/api/player/UNKNOWN_PLAYER", 404),
        ("/api/season/1990", 404),
        ("/api/team-comparison?team1=MI&team2=MI", 400),
    ]

    print(">>> Testing all Flask REST API Endpoints...")
    for path, expected_status in endpoints:
        res = client.get(path)
        assert res.status_code == expected_status, f"Failed {path}: expected {expected_status}, got {res.status_code}"
        assert res.is_json, f"Failed {path}: response is not JSON"
        json_data = res.get_json()
        if expected_status == 200:
            assert json_data.get("success") is True or "status" in json_data
        print(f"    [OK] {res.status_code} - {path}")

    print("\n[SUCCESS] ALL REST API ENDPOINTS TESTED AND WORKING PERFECTLY!")

if __name__ == "__main__":
    run_api_tests()
