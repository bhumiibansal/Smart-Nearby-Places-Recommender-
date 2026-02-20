import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_csv("data/places.csv")

# Select required columns
df = df[['name', 'listed_in(type)', 'rate', 'votes', 'approx_cost(for two people)']]

# Rename columns
df.columns = ['Place', 'Category', 'Rating', 'Popularity', 'Avg_Cost']

# Clean Rating (e.g., '4.1/5' -> 4.1)
df['Rating'] = df['Rating'].astype(str).str.replace('/5', '', regex=False)
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

# Clean Cost
df['Avg_Cost'] = pd.to_numeric(df['Avg_Cost'], errors='coerce')

# Fill missing values
df.fillna({
    'Rating': df['Rating'].mean(),
    'Avg_Cost': df['Avg_Cost'].median(),
    'Popularity': 0
}, inplace=True)

# One-hot encode category
df_encoded = pd.get_dummies(df, columns=['Category'])

# Scale features
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(
    df_encoded.drop('Place', axis=1)
)

# Compute similarity
# Weight features
df_encoded['Rating'] *= 2
df_encoded['Popularity'] *= 1.5

def recommend(place_name, top_n=5):
    if place_name not in df['Place'].values:
        return []

    idx = df[df['Place'] == place_name].index[0]
    scores = list(enumerate(similarity_matrix[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    return [df.iloc[i[0]]['Place'] for i in scores[1:top_n+1]]