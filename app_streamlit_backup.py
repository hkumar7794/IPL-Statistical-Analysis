
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="IPL Analytics", page_icon="🏏", layout="wide")

BASE = Path(__file__).parent
MATCHES = BASE / "data" / "matches.csv"
PLAYERS = BASE / "data" / "players.csv"
DELIVERIES = BASE / "data" / "deliveries.csv"

@st.cache_data
def load_data():
    matches = pd.read_csv(MATCHES)
    players = pd.read_csv(PLAYERS)
    deliveries = pd.read_csv(DELIVERIES)
    return matches, players, deliveries

matches, players, deliveries = load_data()

# ---------- Styling ----------
st.markdown("""
<style>
.main-title {font-size: 42px; font-weight: 800; margin-bottom: 0;}
.subtitle {font-size: 18px; opacity: .75; margin-bottom: 25px;}
.card {
    padding: 18px; border-radius: 14px; border: 1px solid rgba(128,128,128,.25);
    background: rgba(128,128,128,.06); text-align:center;
}
.small {font-size: 13px; opacity:.7;}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🏏 IPL Analytics")
page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "📊 Dashboard", "👥 Teams", "🏏 Players", "⚔️ Comparison", "🗓️ Matches", "ℹ️ About"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Demo dataset included. Replace CSV files in /data with your real IPL dataset.")

def metric_card(label, value):
    st.markdown(f'<div class="card"><div class="small">{label}</div><h2>{value}</h2></div>', unsafe_allow_html=True)

# ---------- HOME ----------
if page == "🏠 Home":
    st.markdown('<div class="main-title">🏏 IPL Statistical Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Interactive cricket analytics dashboard built with Python, Pandas, Plotly and Streamlit.</div>', unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    with c1: metric_card("Matches in demo dataset", f"{len(matches):,}")
    with c2: metric_card("Players", f"{len(players):,}")
    with c3: metric_card("Teams", f"{players.team.nunique():,}")

    st.markdown("### What this project does")
    st.write("""
    This dashboard converts IPL match and player data into useful statistics and visualizations.
    You can explore team wins, player batting/bowling performance, season trends, head-to-head
    comparisons and individual match information.
    """)

    st.markdown("### Project pipeline")
    st.code("""IPL CSV Data
     ↓
Data Cleaning with Pandas
     ↓
Statistical Analysis
     ↓
Interactive Plotly Charts
     ↓
Streamlit Dashboard
     ↓
Insights & Comparisons""")

# ---------- DASHBOARD ----------
elif page == "📊 Dashboard":
    st.title("📊 IPL Dashboard")
    seasons = sorted(matches.season.unique())
    selected_season = st.selectbox("Select Season", ["All"] + seasons)

    df = matches.copy() if selected_season == "All" else matches[matches.season == selected_season].copy()

    total_runs = int(df.team1_score.sum() + df.team2_score.sum())
    total_wins = df.winner.nunique()
    avg_score = round((df.team1_score.mean() + df.team2_score.mean()) / 2, 1)

    c1,c2,c3,c4 = st.columns(4)
    with c1: metric_card("Matches", f"{len(df):,}")
    with c2: metric_card("Total Runs", f"{total_runs:,}")
    with c3: metric_card("Teams with wins", f"{total_wins:,}")
    with c4: metric_card("Average innings score", avg_score)

    st.markdown("### Team Wins")
    wins = df.winner.value_counts().reset_index()
    wins.columns = ["Team","Wins"]
    fig = px.bar(wins, x="Team", y="Wins", text="Wins", title="Wins by Team")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Average Team Score")
    score_df = pd.concat([
        df[["team1","team1_score"]].rename(columns={"team1":"team","team1_score":"score"}),
        df[["team2","team2_score"]].rename(columns={"team2":"team","team2_score":"score"})
    ])
    avg = score_df.groupby("team", as_index=False)["score"].mean().sort_values("score", ascending=False)
    fig = px.bar(avg, x="team", y="score", text_auto=".1f", title="Average Innings Score by Team")
    st.plotly_chart(fig, use_container_width=True)

# ---------- TEAMS ----------
elif page == "👥 Teams":
    st.title("👥 Team Analysis")
    team = st.selectbox("Select Team", sorted(set(matches.team1) | set(matches.team2)))
    team_matches = matches[(matches.team1 == team) | (matches.team2 == team)].copy()
    wins = int((team_matches.winner == team).sum())
    losses = len(team_matches) - wins
    win_pct = round(wins / len(team_matches) * 100, 1) if len(team_matches) else 0

    c1,c2,c3 = st.columns(3)
    with c1: metric_card("Matches", len(team_matches))
    with c2: metric_card("Wins", wins)
    with c3: metric_card("Win %", f"{win_pct}%")

    st.markdown("### Season-wise performance")
    season_perf = team_matches.groupby("season").apply(lambda x: pd.Series({
        "Matches": len(x),
        "Wins": int((x.winner == team).sum())
    })).reset_index()
    season_perf["Losses"] = season_perf["Matches"] - season_perf["Wins"]
    fig = px.bar(season_perf, x="season", y=["Wins","Losses"], barmode="group", title=f"{team}: Wins vs Losses")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Recent matches")
    st.dataframe(team_matches.tail(15), use_container_width=True, hide_index=True)

# ---------- PLAYERS ----------
elif page == "🏏 Players":
    st.title("🏏 Player Analysis")
    player = st.selectbox("Select Player", sorted(players.player))
    p = players[players.player == player].iloc[0]

    c1,c2,c3,c4 = st.columns(4)
    with c1: metric_card("Team", p.team)
    with c2: metric_card("Matches", int(p.matches))
    with c3: metric_card("Runs", int(p.runs))
    with c4: metric_card("Strike Rate", p.strike_rate)

    c5,c6,c7,c8 = st.columns(4)
    with c5: metric_card("Wickets", int(p.wickets))
    with c6: metric_card("Average", p.average)
    with c7: metric_card("50s", int(p.fifties))
    with c8: metric_card("6s", int(p.sixes))

    st.markdown("### Player profile")
    st.write(f"**Role:** {p.role}  |  **Team:** {p.team}")

    comparison = pd.DataFrame({
        "Metric":["Runs","Wickets","Fifties","Hundreds","Sixes"],
        "Value":[p.runs,p.wickets,p.fifties,p.hundreds,p.sixes]
    })
    fig = px.bar(comparison, x="Metric", y="Value", text="Value", title=f"{player} — Career Statistics")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Top run scorers")
    top = players.sort_values("runs", ascending=False).head(10)
    fig = px.bar(top, x="runs", y="player", orientation="h", text="runs", title="Top 10 Run Scorers")
    fig.update_layout(yaxis={"categoryorder":"total ascending"})
    st.plotly_chart(fig, use_container_width=True)

# ---------- COMPARISON ----------
elif page == "⚔️ Comparison":
    st.title("⚔️ Team & Player Comparison")
    tab1, tab2 = st.tabs(["Teams", "Players"])

    with tab1:
        t1 = st.selectbox("Team 1", sorted(teams := sorted(set(matches.team1) | set(matches.team2))), key="t1")
        t2 = st.selectbox("Team 2", [t for t in teams if t != t1], key="t2")

        rows = []
        for t in [t1,t2]:
            tm = matches[(matches.team1 == t) | (matches.team2 == t)]
            w = int((tm.winner == t).sum())
            rows.append({"Team":t, "Matches":len(tm), "Wins":w, "Losses":len(tm)-w,
                         "Win %":round(w/len(tm)*100,1) if len(tm) else 0})
        comp = pd.DataFrame(rows)
        st.dataframe(comp, use_container_width=True, hide_index=True)

        fig = px.bar(comp, x="Team", y=["Wins","Losses"], barmode="group", title="Head-to-Head Team Metrics")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        p1 = st.selectbox("Player 1", sorted(players.player), key="p1")
        p2 = st.selectbox("Player 2", [p for p in sorted(players.player) if p != p1], key="p2")
        comp = players[players.player.isin([p1,p2])][["player","runs","wickets","average","strike_rate","sixes"]]
        st.dataframe(comp, use_container_width=True, hide_index=True)
        fig = px.bar(comp, x="player", y=["runs","wickets","sixes"], barmode="group", title="Player Comparison")
        st.plotly_chart(fig, use_container_width=True)

# ---------- MATCHES ----------
elif page == "🗓️ Matches":
    st.title("🗓️ Match Analysis")
    season = st.selectbox("Season", sorted(matches.season.unique()), key="matchseason")
    season_df = matches[matches.season == season]
    match_id = st.selectbox("Select Match", season_df.match_id.tolist())
    m = season_df[season_df.match_id == match_id].iloc[0]

    st.subheader(f"{m.team1} vs {m.team2}")
    c1,c2,c3,c4 = st.columns(4)
    with c1: metric_card("Winner", m.winner)
    with c2: metric_card("Venue", m.venue)
    with c3: metric_card(f"{m.team1} Score", int(m.team1_score))
    with c4: metric_card(f"{m.team2} Score", int(m.team2_score))

    match_data = pd.DataFrame({"Team":[m.team1,m.team2],"Runs":[m.team1_score,m.team2_score]})
    fig = px.bar(match_data, x="Team", y="Runs", text="Runs", title="Match Score Comparison")
    st.plotly_chart(fig, use_container_width=True)

    d = deliveries[deliveries.match_id == match_id]
    if len(d):
        rr = d.groupby(["inning","over"], as_index=False)["runs"].sum()
        rr["cumulative_runs"] = rr.groupby("inning")["runs"].cumsum()
        fig = px.line(rr, x="over", y="cumulative_runs", color="inning", markers=True,
                      title="Cumulative Runs by Over (Demo Delivery Data)")
        st.plotly_chart(fig, use_container_width=True)

# ---------- ABOUT ----------
else:
    st.title("ℹ️ About the Project")
    st.write("""
    **IPL Statistical Analysis and Performance Dashboard** is a B.Tech CSE/Data Science project
    demonstrating data cleaning, exploratory analysis, statistics and interactive visualization.
    """)
    st.markdown("### Technology")
    st.markdown("""
    - Python
    - Pandas
    - NumPy
    - Plotly
    - Streamlit
    - CSV data
    """)
    st.markdown("### Important")
    st.warning("The included CSV files are demo data for learning and UI demonstration. For a research/hackathon submission, replace them with a verified IPL dataset and document the data source and license.")
    st.markdown("### Future upgrades")
    st.markdown("""
    - Real IPL historical dataset
    - Match-winner prediction
    - Player performance prediction
    - Win probability
    - SQL database
    - User authentication
    - Deployment
    """)
