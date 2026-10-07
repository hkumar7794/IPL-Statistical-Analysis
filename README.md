# 🏏 IPL Statistical Analysis & Analytics Dashboard

A modern, responsive, full-stack cricket analytics web application built with **Python Flask**, **Pandas**, **Bootstrap 5**, and **Chart.js**.

Designed as a premier academic and hackathon project for exploring and analyzing Indian Premier League (IPL) historical data.

---

## 🌟 Key Highlights & Features

* **Interactive Home Dashboard**: 6 Key Performance Indicator (KPI) metric cards and 4 responsive visual charts.
* **10 IPL Franchises Overview**: Win percentages, titles count, total runs scored, and average scores per team.
* **Deep Franchise Performance**: Season-by-season win/loss trends, opponent head-to-head records, and recent fixture outcomes.
* **Head-to-Head Comparison Tool**: Compare any two franchises side-by-side with head-to-head win shares and scoring comparisons.
* **Player Directory & Profiler**: Searchable and filterable database by name, franchise, and role with interactive career modal dialogs.
* **Batting Leaderboard**: Top run-scorers, batting averages, boundary counts (50s, 100s, 6s), and destructive strike rates.
* **Bowling Leaderboard**: Leading wicket-takers, economy rate masters, and bowling averages with season filters.
* **Season Standings & Honors**: Tournament champions, Orange Cap, Purple Cap, official points table, and match archives.
* **Toss Decision & Match Impact**: Empirical analysis of bat first vs field first decisions and coin toss-to-match victory correlation.
* **Stadium & Venue Analytics**: Pitch scoring averages, 1st vs 2nd innings totals, and franchise fortress win records.
* **Match Explorer**: Filterable match results archive with interactive match scorecard dialogs.
* **100% Data-Driven REST APIs**: Built using Flask with clean JSON payloads and structured error handling.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Bootstrap Icons, Chart.js 4.4 |
| **Backend API** | Python 3, Flask 3.1, Jinja2 Templates |
| **Data Processing** | Pandas 2.x, NumPy 1.26+ |
| **Data Storage** | Structured CSV Datasets (`matches_clean.csv`, `deliveries_clean.csv`, `players_clean.csv`) |
| **Deployment Ready** | Gunicorn WSGI Server |

---

## 📁 Project Architecture & Directory Structure

```text
IPL-Statistical-Analysis/
│
├── app.py                     # Flask web server and REST API routing hub
├── requirements.txt           # Python package dependencies
├── .gitignore                 # Files excluded from Git version control
├── README.md                  # Complete project documentation
├── test_pipeline.py           # Test suite for Phase 2 data calculations
├── test_apis.py               # Test suite for Phase 3 REST API endpoints
├── test_full_suite.py         # End-to-end page and API test runner
│
├── data/
│   ├── raw/                   # Original dataset archives
│   │   ├── matches.csv
│   │   ├── deliveries.csv
│   │   └── players.csv
│   └── processed/             # Cleaned, standardized, and enriched data
│       ├── matches_clean.csv
│       ├── deliveries_clean.csv
│       └── players_clean.csv
│
├── analysis/                  # Modular data analytics calculations
│   ├── __init__.py
│   ├── cleaner.py             # Data cleansing, validation, and type coercion
│   ├── data_loader.py         # In-memory DataFrame cache manager
│   ├── summary.py             # Tournament KPIs and dashboard aggregations
│   ├── batting.py             # Batting leaderboards, boundaries, strike rates
│   ├── bowling.py             # Bowling records, economy rates, wicket charts
│   ├── teams.py               # Franchise records, win %, head-to-head logic
│   ├── players.py             # Player search directory and career profiles
│   ├── seasons.py             # Points table, champions, Orange/Purple caps
│   ├── venues.py              # Stadium averages, ground toss records
│   ├── toss.py                # Toss decisions & match victory correlations
│   └── matches.py             # Match queries and delivery-level scorecards
│
├── templates/                 # Jinja2 HTML web templates
│   ├── base.html              # Shared layout, navbar, footer, scripts
│   ├── index.html             # Main analytics dashboard
│   ├── teams.html             # Franchises directory
│   ├── team-analysis.html     # Deep franchise performance
│   ├── head-to-head.html      # Two-team comparative tool
│   ├── players.html           # Player search and career modals
│   ├── batting.html           # Batting leaderboards & charts
│   ├── bowling.html           # Bowling leaderboards & charts
│   ├── seasons.html           # Season points table & standings
│   ├── toss.html              # Toss decision analytics
│   ├── venues.html            # Stadiums analysis
│   └── matches.html           # Match results explorer
│
├── static/                    # Frontend styling and client-side logic
│   ├── css/
│   │   └── style.css          # Modern dark cricket theme styling
│   ├── js/
│   │   ├── charts.js          # Reusable Chart.js factory
│   │   ├── dashboard.js       # Dashboard KPI and graph controller
│   │   ├── teams.js           # Teams view controller
│   │   ├── team-analysis.js   # Team deep-dive controller
│   │   ├── head-to-head.js    # Comparative matchup controller
│   │   ├── players.js         # Player search and modal controller
│   │   ├── batting.js         # Batting leaderboard controller
│   │   ├── bowling.js         # Bowling leaderboard controller
│   │   ├── seasons.js         # Season standings controller
│   │   ├── toss.js            # Toss impact controller
│   │   ├── venues.js          # Stadium analytics controller
│   │   └── matches.js         # Match scorecard controller
│   └── images/                # Brand graphics and assets
│
└── screenshots/               # Application preview images for showcase
```

---

## 🚀 Quickstart Guide: Running Locally

### Step 1: Open VS Code
Open the project root directory in **Visual Studio Code**:
```powershell
File -> Open Folder -> IPL_Statistical_Analysis
```

### Step 2: Open Terminal
In VS Code, press <kbd>Ctrl</kbd> + <kbd>`</kbd> or navigate to **Terminal** &rarr; **New Terminal**.

### Step 3: Activate Virtual Environment
```powershell
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# On Windows (Command Prompt):
venv\Scripts\activate.bat

# On macOS/Linux:
source venv/bin/activate
```
*(You will see `(venv)` appear at the start of your terminal command prompt).*

### Step 4: Install Dependencies (if not already installed)
```powershell
pip install -r requirements.txt
```

### Step 5: Start the Flask Web Server
```powershell
python app.py
```

### Step 6: Access the Dashboard
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

### Step 7: Stopping the Server
To stop the local web server at any time, press <kbd>Ctrl</kbd> + <kbd>C</kbd> in your terminal.

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/health` | `GET` | Server health and uptime verification |
| `/api/summary` | `GET` | Overall tournament KPIs and dashboard charts data |
| `/api/teams` | `GET` | List of all 10 franchises with win %, titles, and runs |
| `/api/team/<team>` | `GET` | Deep performance records for a specific team |
| `/api/team-comparison` | `GET` | Head-to-head match stats (`?team1=MI&team2=CSK`) |
| `/api/players` | `GET` | Filterable player directory (`?query=virat&team=RCB`) |
| `/api/player/<name>` | `GET` | Complete career statistical profile of a player |
| `/api/top-batsmen` | `GET` | Batting leaderboard (`?season=2023&sort=runs&limit=20`) |
| `/api/batting/charts` | `GET` | Chart-ready dataset for batting analytics |
| `/api/top-bowlers` | `GET` | Bowling leaderboard (`?season=2023&sort=wickets`) |
| `/api/bowling/charts` | `GET` | Chart-ready dataset for bowling analytics |
| `/api/seasons` | `GET` | Summary of all historical IPL editions |
| `/api/season/<year>` | `GET` | Points table, awards, and fixtures for an edition |
| `/api/venues` | `GET` | Overview of all stadiums with scoring averages |
| `/api/venue/<name>` | `GET` | Deep dive into ground scoring records |
| `/api/toss-analysis` | `GET` | Bat vs field decisions and win correlations |
| `/api/matches` | `GET` | Filterable match archive (`?season=2024&team=CSK`) |
| `/api/match/<id>` | `GET` | Complete match scorecard and awards |

---

## 🧪 Automated Testing

Run the included automated test suites to verify data pipeline logic, API schemas, and page rendering:

```powershell
# Test Phase 2 Data Pipeline:
python test_pipeline.py

# Test Phase 3 REST APIs:
python test_apis.py

# Test Full End-to-End Application:
python test_full_suite.py
```

---

## 🌐 Free Cloud Deployment (e.g. Render / Railway)

1. Push your repository to **GitHub**.
2. Visit [Render.com](https://render.com) and create a **New Web Service**.
3. Connect your GitHub repository.
4. Set the following settings:
   * **Runtime**: `Python 3`
   * **Build Command**: `pip install -r requirements.txt`
   * **Start Command**: `gunicorn app:app`
5. Click **Deploy Web Service** &mdash; your public URL will be live in 2 minutes!

---

## 🎓 Academic Viva Questions & Answers

* **Q: Why use Flask instead of Django?**
  * *A: Flask is lightweight and unopinionated, making it ideal for microservices and data-centric applications where routing and Pandas integration require zero boilerplate.*
* **Q: How does the frontend communicate with the backend?**
  * *A: Using asynchronous `fetch()` API calls in JavaScript that receive JSON payloads from Flask REST routes without triggering full browser reloads.*
* **Q: How is Strike Rate calculated?**
  * *A: $\text{Strike Rate} = \left(\frac{\text{Runs Scored}}{\text{Balls Faced}}\right) \times 100$.*
* **Q: How is Bowling Economy Rate calculated?**
  * *A: $\text{Economy Rate} = \frac{\text{Runs Conceded}}{\text{Overs Bowled}}$.*
* **Q: How is data cached for high performance?**
  * *A: An in-memory cache manager in `analysis/data_loader.py` loads and parses cleaned CSVs into Pandas DataFrames once at server startup, delivering instant sub-millisecond API responses.*
