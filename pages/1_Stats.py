import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Page setup
st.set_page_config(page_title="Spotify Stats Dashboard", page_icon="🎶", layout="wide")
st.title("🎶 Spotify Stats Dashboard")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/dataset.csv")
    return df

df = load_data()
df = df.drop(columns=["Unnamed: 0"], errors="ignore")

# --- GLOBAL KPIs ---
total_tracks = len(df)
unique_artists = df["artists"].nunique()
avg_popularity = int(df["popularity"].mean())

col1, col2, col3 = st.columns(3)
col1.metric("🎵 Total Tracks", f"{total_tracks:,}")
col2.metric("👩‍🎤 Unique Artists", f"{unique_artists:,}")
col3.metric("🔥 Avg Popularity", f"{avg_popularity}")

st.markdown("---")

# --- SELECT ARTIST ---
st.subheader("👤 Explore Artist")
artist_list = df["artists"].sort_values().unique().tolist()
selected_artist = st.selectbox("Select an artist:", ["(All)"] + list(artist_list))

if selected_artist != "(All)":
    artist_df = df[df["artists"] == selected_artist].sort_values(by="popularity", ascending=False)
    st.write(f"Top songs by **{selected_artist}**:")
    st.dataframe(artist_df[["track_name", "album_name", "popularity", "track_genre"]])

    # KPI for artist
    total_artist_tracks = len(artist_df)
    avg_artist_pop = int(artist_df["popularity"].mean())
    col1, col2 = st.columns(2)
    col1.metric("🎵 Total Tracks", f"{total_artist_tracks}")
    col2.metric("🔥 Avg Popularity", f"{avg_artist_pop}")

st.markdown("---")

col1, col2 = st.columns(2)
# --- TOP ARTISTS BY SONG COUNT ---
with col1:
    st.subheader("👑 Top 20 Artists by Song Count")
    top_artists = df['artists'].value_counts().head(20)

    fig, ax = plt.subplots(figsize=(9,7))
    sns.barplot(
        x=top_artists.values,
        y=top_artists.index,
        hue=top_artists.index,
        dodge=False,
        palette="viridis",
        legend=False
    )
    ax.set_xlabel("Number of Songs")
    ax.set_ylabel("Artist")
    plt.tight_layout()
    st.pyplot(fig)

# --- POPULARITY-TOP 10---
with col2:
    st.subheader("🔥 Top 10 Artists by Avg Popularity")
    top_artists_popularity=df.groupby('artists')['popularity'].mean().sort_values(ascending=False).head(10)
    
    fig2, ax2 = plt.subplots(figsize=(9,6))
    sns.barplot(
        x=top_artists_popularity.values,
        y=top_artists_popularity.index,
        hue=top_artists_popularity.index,
        dodge=False,
        palette="magma",
        legend=False
    )
    ax2.set_xlabel("Popularity")
    ax2.set_ylabel("Artists")
    ax2.tick_params(axis='x', labelsize=16)
    ax2.tick_params(axis='y', labelsize=16)
    plt.tight_layout()
    st.pyplot(fig2)
    


col3,col4=st.columns(2)

#-- POPULARITY DISTRIBUTIOn
with col3:
    st.subheader("🎼 Popularity Distribution")
    fig3, ax3 = plt.subplots(figsize=(9,7))
    sns.histplot(df['popularity'], bins=30, kde=True, color="skyblue", line_kws={'color':'blue'}, ax=ax3)
    ax3.set_xlabel("Popularity")
    ax3.set_ylabel("Count")
    plt.tight_layout()
    st.pyplot(fig3)

    

# --- AUDIO FEATURE CORRELATION ---
with col4:
    st.subheader("🎵 Correlation Between Audio Features")
    corr_file = "data/corr_matrix.csv"
    if os.path.exists(corr_file):
        corr_matrix = pd.read_csv(corr_file, index_col=0)
    else:
        features = [
            'danceability', 'energy', 'speechiness', 'acousticness',
            'instrumentalness', 'liveness', 'valence', 'tempo'
        ]
        corr_matrix = df[features].corr()
        corr_matrix.to_csv(corr_file)
    fig4, ax4 = plt.subplots(figsize=(9,7))
    sns.heatmap(corr_matrix, annot=True, cmap="Blues", center=0, ax=ax4)
    ax4.tick_params(axis='x', labelsize=16)
    ax4.tick_params(axis='y', labelsize=16)
    plt.tight_layout()
    st.pyplot(fig4)

# --- RAW DATA ---
with st.expander("📂 View Raw Spotify Data"):
    st.dataframe(df.head(50))
