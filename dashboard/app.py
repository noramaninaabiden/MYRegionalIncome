import streamlit as st
import pandas as pd
from google.cloud import bigquery
import plotly.express as px
from google.oauth2 import service_account

PROJECT_ID = "my-regional-income-504816"
DATASET = "gold"

st.set_page_config(page_title="MYRegionalIncome", layout="wide")

@st.cache_data(ttl=3600)
def load_data():
    if "gcp_service_account" in st.secrets:
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        client = bigquery.Client(project=PROJECT_ID, credentials=credentials)
    else:
        client = bigquery.Client(project=PROJECT_ID)

    query = f"""
        select *
        from `{PROJECT_ID}.{DATASET}.fct_state_socioeconomic`
        order by state, year
    """
    return client.query(query).to_dataframe()


df = load_data()

st.title("Malaysia Regional Income Index")
st.caption("Inflation-adjusted household income by state (OpenDOSM)")

# --- Sidebar filters ---
st.sidebar.header("Filters")

all_states = sorted(df["state"].unique())
selected_states = st.sidebar.multiselect("State(s)", all_states, default=all_states)

all_years = sorted(df["year"].unique())
selected_year = st.sidebar.selectbox("Year (for state comparison)", all_years, index=len(all_years) - 1)

filtered_df = df[df["state"].isin(selected_states)]

# --- Trend chart: nominal vs real income over time ---
st.subheader("Income Trend Over Time")

trend_df = filtered_df.melt(
    id_vars=["state", "year"],
    value_vars=["income_mean", "real_income_mean"],
    var_name="metric",
    value_name="value",
)

trend_df["year"] = trend_df["year"].astype(str)

fig_trend = px.line(
    trend_df, x="year", y="value", color="state", line_dash="metric", markers=True,
    labels={"value": "Income (MYR)", "year": "Year"},
    category_orders={"year": sorted(trend_df["year"].unique())},
)

st.plotly_chart(fig_trend, use_container_width=True)

# --- State comparison for selected year ---
st.subheader(f"State Comparison — {selected_year}")

year_df = filtered_df[filtered_df["year"] == selected_year].sort_values("real_income_mean", ascending=False)

fig_bar = px.bar(
    year_df, x="state", y="real_income_mean", color="region",
    labels={"real_income_mean": "Real Income (MYR, 2010 base)", "state": "State"},
)
st.plotly_chart(fig_bar, use_container_width=True)

# --- Underlying data ---
st.subheader("Underlying Data")
st.dataframe(filtered_df, use_container_width=True)