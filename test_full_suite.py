"""
Full Application Test Suite for IPL Statistical Analysis
Verifies all HTML pages and REST APIs render without errors.
"""

from app import app

def test_full_application():
    client = app.test_client()

    pages = [
        ("/", 200, "Indian Premier League Analytics"),
        ("/teams", 200, "IPL Franchises & Team Records"),
        ("/team-analysis", 200, "Franchise Performance Deep Dive"),
        ("/head-to-head", 200, "Head-to-Head Franchise Comparison"),
        ("/players", 200, "IPL Player Analytics & Career Records"),
        ("/batting", 200, "IPL Batting Records & Leaderboards"),
        ("/bowling", 200, "IPL Bowling Records & Leaderboards"),
        ("/seasons", 200, "IPL Season Standings & Honors"),
        ("/toss", 200, "IPL Toss Impact & Tactical Decision Analysis"),
        ("/venues", 200, "IPL Venues & Stadium Analytics"),
        ("/matches", 200, "IPL Match Explorer & Scorecards")
    ]

    print(">>> Testing all HTML Web Pages...")
    for path, expected_code, title_snippet in pages:
        res = client.get(path)
        assert res.status_code == expected_code, f"Failed page {path}: expected {expected_code}, got {res.status_code}"
        assert title_snippet in res.get_data(as_text=True), f"Snippet '{title_snippet}' not found in {path}"
        print(f"    [PAGE OK] {res.status_code} - {path}")

    apis = [
        ("/api/health", 200),
        ("/api/summary", 200),
        ("/api/teams", 200),
        ("/api/team/MI", 200),
        ("/api/team-comparison?team1=RCB&team2=CSK", 200),
        ("/api/players?query=dhoni", 200),
        ("/api/player/MS Dhoni", 200),
        ("/api/top-batsmen?limit=5", 200),
        ("/api/batting/charts", 200),
        ("/api/top-bowlers?limit=5", 200),
        ("/api/bowling/charts", 200),
        ("/api/seasons", 200),
        ("/api/season/2024", 200),
        ("/api/venues", 200),
        ("/api/venue/Kolkata", 200),
        ("/api/toss-analysis", 200),
        ("/api/matches?limit=5", 200),
        ("/api/match/5", 200)
    ]

    print("\n>>> Testing all REST API Endpoints...")
    for path, expected_code in apis:
        res = client.get(path)
        assert res.status_code == expected_code, f"Failed API {path}: expected {expected_code}, got {res.status_code}"
        assert res.is_json, f"Response at {path} is not valid JSON"
        print(f"    [API OK]  {res.status_code} - {path}")

    print("\n[SUCCESS] 100% OF PAGES AND ENDPOINTS VERIFIED AND WORKING SMOOTHLY!")

if __name__ == "__main__":
    test_full_application()
