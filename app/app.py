import streamlit as st
import os
from data_processor import parse_matchup_data, calculate_metrics

st.set_page_config(page_title="T20 Matchup Strategy Engine", layout="wide")

st.title("T20 Matchup Strategy Engine")
st.caption("Tactical Batter vs Bowler Head-to-Head Analytics")

# Load data
DATA_PATH = os.path.join(os.path.dirname(__file__), "sample_ipl.json")
df = parse_matchup_data(DATA_PATH)

batters = sorted(df["batter"].unique())
bowlers = sorted(df["bowler"].unique())
phases = ["All", "Powerplay", "Middle", "Death"]

# Filter controls
col1, col2, col3 = st.columns(3)

with col1:
    selected_batter = st.selectbox("Select Batter", batters, key="batter_select")

with col2:
    selected_bowler = st.selectbox("Select Bowler", bowlers, key="bowler_select")

with col3:
    selected_phase = st.selectbox("Match Phase", phases, key="phase_select")

# Analytics calculation
metrics = calculate_metrics(df, selected_batter, selected_bowler, selected_phase)

st.divider()

# Native Streamlit Metric Cards
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

with m_col1:
    st.metric(label="Runs Scored", value=metrics["runs"])

with m_col2:
    st.metric(label="Balls Faced", value=metrics["balls"])

with m_col3:
    st.metric(label="Strike Rate", value=metrics["strike_rate"])

with m_col4:
    st.metric(label="Dismissals", value=metrics["dismissals"])