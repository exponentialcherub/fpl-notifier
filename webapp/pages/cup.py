import streamlit as st
import sys
import os
import pandas as pd
import requests

# Add root to path so we can import from config and cup
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config.cup_config import CupConfig
from config.config import Config
from config.manager_config import ManagerConfig
from cup.league_table_calculator import calculate_league_table
from cup.results_calculator import calculate_results
from api.fpl_api import FplAPI

st.title("🏅 FPL Draft Cup")

# Load configs
cup = CupConfig()
config = Config()
manager_config = ManagerConfig()
fpl_api = FplAPI(config.fpl_domain)

st.header(cup.competition_name)
st.markdown(f"**Format:** {cup.format} | **Scoring:** {cup.scoring}")
st.markdown("---")

# Get current gameweek
current_gw = fpl_api.get_current_gameweek()
st.info(f"📅 Current Gameweek: **{current_gw}**")

# Helper to build league table dataframe
def build_table_df(sorted_table):
    return pd.DataFrame([
        {
            "Pos": idx + 1,
            "Team": team,
            "P": stats['played'],
            "W": stats['won'],
            "D": stats['drawn'],
            "L": stats['lost'],
            "PF": stats['points_for'],
            "PA": stats['points_against'],
            "PD": stats['points_diff'],
            "Pts": stats['match_points']
        }
        for idx, (team, stats) in enumerate(sorted_table)
    ])

# Calculate results and league tables for each group
st.subheader("📊 Group Tables")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Group A")
    group_a = cup.groups.get("A")
    if group_a:
        fixtures_a = cup.fixtures.group_A
        results_a = calculate_results(config.league_id, fpl_api, fixtures_a, manager_config, current_gw)
        table_a = calculate_league_table(results_a, group_a.teams)
        df_a = build_table_df(table_a)
        st.dataframe(df_a, use_container_width=True, hide_index=True)

with col2:
    st.markdown("### Group B")
    group_b = cup.groups.get("B")
    if group_b:
        fixtures_b = cup.fixtures.group_B
        results_b = calculate_results(config.league_id, fpl_api, fixtures_b, manager_config, current_gw)
        table_b = calculate_league_table(results_b, group_b.teams)
        df_b = build_table_df(table_b)
        st.dataframe(df_b, use_container_width=True, hide_index=True)

# Next Fixtures
st.markdown("---")
st.subheader("⏭️ Next Fixtures")

all_fixtures = cup.fixtures.group_A + cup.fixtures.group_B
next_fixtures = [f for f in all_fixtures if f.gameweek > current_gw]

if next_fixtures:
    next_gw = min(f.gameweek for f in next_fixtures)
    upcoming = [f for f in next_fixtures if f.gameweek == next_gw]
    
    st.markdown(f"**Gameweek {next_gw}**")
    
    next_df = pd.DataFrame([
        {"Home": f.home, "vs": "vs", "Away": f.away}
        for f in upcoming
    ])
    st.dataframe(next_df, use_container_width=True, hide_index=True)
else:
    st.info("No upcoming fixtures - group stage complete!")

# Full Fixture List
st.markdown("---")
st.subheader("📋 Full Fixture List")

tab1, tab2 = st.tabs(["Group A", "Group B"])

with tab1:
    fixtures_a_df = pd.DataFrame([
        {
            "GW": f.gameweek,
            "Home": f.home,
            "vs": "vs",
            "Away": f.away,
            "Status": "✅ Played" if f.gameweek <= current_gw else "⏳ Upcoming"
        }
        for f in cup.fixtures.group_A
    ])
    st.dataframe(fixtures_a_df, use_container_width=True, hide_index=True)

with tab2:
    fixtures_b_df = pd.DataFrame([
        {
            "GW": f.gameweek,
            "Home": f.home,
            "vs": "vs",
            "Away": f.away,
            "Status": "✅ Played" if f.gameweek <= current_gw else "⏳ Upcoming"
        }
        for f in cup.fixtures.group_B
    ])
    st.dataframe(fixtures_b_df, use_container_width=True, hide_index=True)