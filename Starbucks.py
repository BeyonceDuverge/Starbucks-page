"""
Name: Beyonce Duverge
CS23: Section 8
Data: USA Starbucks
URL: Link to the web application on Streamlit Cloud

Description: Hello, and welcome to my Streamlit project on Starbucks.
This project explores Starbucks store locations across the United States using line charts, horizontal and stacked bar charts, and a geographic scatter map.
"""
#Disclaimer: This code was created with the help of Copilot

# python -m streamlit run starbucks.py

import pandas as pd
import streamlit as st
import pydeck as pdk

# [ST4] Page Design
st.set_page_config(
    page_title="Starbucks U.S. Analytics",
    layout="wide"
)

# [ST4] Custom Page Design
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F8EFEA;
    }
    h1, h2, h3 {
        color: #006241;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# [ST4] Layout & image
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("starbucks_logo.png", width=150)

st.title("Starbucks U.S. Store Analysis")

st.markdown(
    """
    Hello, and welcome to my Streamlit project on Starbucks. 
    This project explores Starbucks store locations across the United States 
    using Streamlit charts and an interactive geographic map.
    The design is inspired by the iconic Pink Drink.
    """
)

# [PY3] Safe file loading
df = pd.read_excel("usa_starbucks.xlsx", engine="openpyxl")

# [DA1] Data cleaning
df.columns = df.columns.str.lower().str.replace(" ", "_")
df = df[df["brand"] == "Starbucks"]

df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

df = df.dropna(subset=["latitude", "longitude", "state/province"])
df = df.drop_duplicates(subset="store_number")

# [DA2] Aggregate and sort
state_counts = (
    df.groupby("state/province")
    .size()
    .reset_index(name="store_count")
    .sort_values(by="store_count", ascending=False)
)

# [DA3] Largest value
top_state = state_counts.iloc[0]

# [DA9] Calculations
total_stores = len(df)
average_stores = round(state_counts["store_count"].mean(), 1)

# [DA7] New column
df["density_category"] = "Low"

# [DA8] iterrows()
for _, row in state_counts.iterrows():
    if row["store_count"] > 500:
        df.loc[df["state/province"] == row["state/province"], "density_category"] = "High"
    elif row["store_count"] > 200:
        df.loc[df["state/province"] == row["state/province"], "density_category"] = "Medium"

# [ST4] Sidebar and navigation
st.sidebar.header("Dashboard Controls")

page = st.sidebar.radio(
    "Choose a page",
    ["Summary", "State Comparison", "Geographic Map", "Ownership Analysis"]
)

# [ST3] Multi-select
selected_states = st.sidebar.multiselect(
    "Select state(s)",
    options=sorted(df["state/province"].unique()),
    default=["CA"]
)

# [ST1] Slider
min_stores = st.sidebar.slider(
    "Minimum stores per state",
    min_value=1,
    max_value=int(state_counts["store_count"].max()),
    value=1
)

# [DA4] One-condition filter
filtered_df = df[df["state/province"].isin(selected_states)]

# [DA5] Two-condition filter
filtered_state_counts = state_counts[
    (state_counts["state/province"].isin(selected_states)) &
    (state_counts["store_count"] >= min_stores)
]

if page == "Summary":
    st.subheader("📊 Summary")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Starbucks Stores", f"{total_stores:,}")
    c2.metric("Average Stores per State", average_stores)
    c3.metric("Top State", top_state["state/province"], top_state["store_count"])

    # [VIZ1] Line chart
    top10 = state_counts.head(10).set_index("state/province")
    st.line_chart(top10["store_count"])

elif page == "State Comparison":
    st.subheader("🏷️ Stores by State")

    # [VIZ2] Bar chart
    sorted_data = (
        filtered_state_counts
        .sort_values(by="store_count", ascending=False)
        .set_index("state/province")
    )

    st.bar_chart(sorted_data["store_count"])

