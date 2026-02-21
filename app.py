import streamlit as st
import pandas as pd
from recommender import recommend

# -------------------------
# Page Config (MUST be first)
# -------------------------
st.set_page_config(
    page_title="Smart Place Recommender",
    page_icon="📍",
    layout="centered"
)

# -------------------------
# Load Dataset
# -------------------------
df = pd.read_csv("data/places.csv")

# -------------------------
# UI Header
# -------------------------
st.title("📍 Smart Place Recommender")

st.markdown(
    """
    ### 🔍 Personalized Place Recommendations  
    Find places based on **similarity, budget, and category**,  
    with **direct Google Maps navigation**.
    """
)

# -------------------------
# Place Selection
# -------------------------
place = st.selectbox(
    "Select a place you like:",
    df["place_name"]
)

# -------------------------
# Google Maps Link
# -------------------------
def google_maps_link(place_name, city="New Delhi"):
    query = place_name.replace(" ", "+") + "+" + city
    return f"https://www.google.com/maps/search/?api=1&query={query}"

# -------------------------
# Budget Filter
# -------------------------
max_budget = st.slider(
    "💰 Max budget for two (₹)",
    min_value=100,
    max_value=5000,
    value=1500,
    step=100
)

# -------------------------
# Category Filter
# -------------------------
categories = sorted(df["category"].unique())
selected_category = st.selectbox(
    "🍽️ Select category",
    ["All"] + categories
)

# -------------------------
# Recommendation Button
# -------------------------
if st.button("Recommend"):
    results = recommend(place)

    # Apply filters
    filtered = df[df["avg_cost"] <= max_budget]

    if selected_category != "All":
        filtered = filtered[filtered["category"] == selected_category]

    results = [r for r in results if r in filtered["place_name"].values]

    st.subheader("Recommended Places")

    if not results:
        st.info("No places match your filters. Try changing budget or category.")
    else:
        for r in results:
            st.markdown(
                f"""
                **📍 {r}**  
                👉 [Open in Google Maps]({google_maps_link(r)})
                ---
                """
            )