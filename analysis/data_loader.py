"""
================================================================================
IPL Data Loader & Cache Manager
================================================================================
Loads the processed IPL datasets into memory once and caches them for fast,
low-latency responses across all API endpoints and calculations.
================================================================================
"""

from pathlib import Path
import pandas as pd
from analysis.cleaner import clean_and_prepare_datasets, TEAM_META

# Global in-memory cache for DataFrames
_CACHE = {
    "matches": None,
    "deliveries": None,
    "players": None
}

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

def get_data(force_reload: bool = False):
    """
    Returns (matches_df, deliveries_df, players_df).
    Caches the DataFrames in memory so API requests don't reload CSV files.
    """
    global _CACHE

    if not force_reload and _CACHE["matches"] is not None:
        return _CACHE["matches"], _CACHE["deliveries"], _CACHE["players"]

    matches_file = PROCESSED_DIR / "matches_clean.csv"
    deliveries_file = PROCESSED_DIR / "deliveries_clean.csv"
    players_file = PROCESSED_DIR / "players_clean.csv"

    # If processed files don't exist yet, run the cleaner
    if not (matches_file.exists() and deliveries_file.exists() and players_file.exists()):
        matches_df, deliveries_df, players_df = clean_and_prepare_datasets(DATA_DIR)
    else:
        matches_df = pd.read_csv(matches_file)
        deliveries_df = pd.read_csv(deliveries_file)
        players_df = pd.read_csv(players_file)

    # Date parsing
    if "date" in matches_df.columns:
        matches_df["date"] = pd.to_datetime(matches_df["date"])

    _CACHE["matches"] = matches_df
    _CACHE["deliveries"] = deliveries_df
    _CACHE["players"] = players_df

    return _CACHE["matches"], _CACHE["deliveries"], _CACHE["players"]

def get_team_metadata():
    """Returns team full names, primary and secondary brand colors."""
    return TEAM_META
