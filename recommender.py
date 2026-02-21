import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------
# Load dataset
# -------------------------
df = pd.read_csv("data/places.csv")

# Keep required columns
df = df[
    [
        "place_name",
        "area",
        "category",
        "rating",
        "review_count",
        "avg_cost",
        "crowd_level",
        "best_time",
        "open_now"
    ]
]

# Rename internally
df.columns = [
    "Place",
    "Area",
    "Category",
    "Rating",
    "Popularity",
    "Avg_Cost",
    "Crowd",
    "Best_Time",
    "Open_Now"
]

# -------------------------
# Cleaning & Encoding
# -------------------------
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
df["Popularity"] = pd.to_numeric(df["Popularity"], errors="coerce")
df["Avg_Cost"] = pd.to_numeric(df["Avg_Cost"], errors="coerce")

crowd_map = {"Low": 1, "Medium": 2, "High": 3}
df["Crowd"] = df["Crowd"].map(crowd_map)

open_map = {"Yes": 1, "No": 0}
df["Open_Now"] = df["Open_Now"].map(open_map)

df.fillna(
    {
        "Rating": df["Rating"].mean(),
        "Popularity": df["Popularity"].median(),
        "Avg_Cost": df["Avg_Cost"].median(),
        "Crowd": 2,
        "Open_Now": 1
    },
    inplace=True
)

# -------------------------
# Feature Engineering
# -------------------------
df_encoded = pd.get_dummies(
    df,
    columns=["Area", "Category", "Best_Time"],
    drop_first=True
)

# Feature weighting
df_encoded["Rating"] *= 2
df_encoded["Popularity"] *= 1.5

# -------------------------
# Scaling
# -------------------------
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(
    df_encoded.drop("Place", axis=1)
)

# -------------------------
# Similarity Matrix (GLOBAL — IMPORTANT)
# -------------------------
similarity_matrix = cosine_similarity(scaled_features)

# -------------------------
# Recommendation Function
# -------------------------
def recommend(place_name, top_n=5):
    if place_name not in df["Place"].values:
        return []

    idx = df[df["Place"] == place_name].index[0]

    scores = list(enumerate(similarity_matrix[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    return [df.iloc[i[0]]["Place"] for i in scores[1: top_n + 1]]