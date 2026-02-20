import streamlit as st
from recommender import recommend
import pandas as pd

df = pd.read_csv("data/places.csv")

st.title("📍 Smart Place Recommender")
st.set_page_config(
    page_title="Smart Place Recommender",
    page_icon="📍",
    layout="centered"
)

st.markdown(
    """
    ### 🔍 Personalized Place Recommendations  
    Find the best places based on **similarity, budget, and category**,  
    with **direct Google Maps navigation**.
    """
)

place = st.selectbox("Select a place you like:", df['name'])

def google_maps_link(place_name, city="Bangalore"):
    query = place_name.replace(" ", "+") + "+" + city
    return f"https://www.google.com/maps/search/?api=1&query={query}"

# Budget filter
max_budget = st.slider(
    "💰 Max budget for two (₹)",
    min_value=100,
    max_value=2000,
    value=600,
    step=100
)

# Category filter
categories = sorted(df['listed_in(type)'].unique())
selected_category = st.selectbox(
    "🍽️ Select category",
    ["All"] + categories
)

if st.button("Recommend"):
    results = recommend(place)
    filtered = df[df['approx_cost(for two people)'] <= max_budget]
    if selected_category != "All":
      filtered = filtered[filtered['listed_in(type)'] == selected_category]

    results = [r for r in results if r in filtered['name'].values]
    st.subheader("Recommended Places:")
    for r in results:
      link = google_maps_link(r)
      st.markdown(f"➡️ **{r}**  \n[📍 Open in Google Maps]({link})")