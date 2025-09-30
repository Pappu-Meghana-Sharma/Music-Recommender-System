import streamlit as st
import pandas as pd
from recommender.preprocessing import load_data, preprocess_numerical_cached, preprocess_tfidf_cached
from recommender.recommend_songs import recommend_tfidf_v2

st.set_page_config(page_title="Music Recommender 🎶", layout="wide")
st.title("🎵 Music Recommendation System")

# Load data
   #this one gets recomputed again everytime the user refreshes the page so used redis to cache at preprocessing level
@st.cache_resource
def setup():
    df = load_data("data/dataset.csv")
    df_num = preprocess_numerical_cached(df)
    vectors = preprocess_tfidf_cached(df)
    return df, df_num, vectors

df, df_num, vectors = setup()
col1, col2 = st.columns([2, 2])

with col1:
    all_tracks = df["track_name"].unique().tolist()
    track = st.selectbox("🎶 Select a song and Press Enter:", options=all_tracks)

with col2:
    possible_artists = df[df["track_name"] == track]["artists"].unique().tolist()
    artist = None
    if len(possible_artists) >= 1:
        artist = st.selectbox("🎤 Select artist (optional):", options=["(Any)"] + possible_artists)
        if artist == "(Any)":
            artist= None
            
            
method = st.radio(
    "Choose recommendation method:",
    ["Hybrid (TF-IDF + Numerical)","TF-IDF only"]
)
    
if st.button("✨ Get Recommendations"):
    if method == "TF-IDF only":
        recs = recommend_tfidf_v2(df, df_num, vectors, track, artist, num_weight=0, tfidf_weight=1)
    else:
        recs = recommend_tfidf_v2(df, df_num, vectors, track, artist)

    cols = st.columns(2)
    for i, (_, row) in enumerate(recs.iterrows()):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div style="background-color:#181818; padding:15px; border-radius:15px; margin-bottom:20px; text-align:center;">
                    <img src="{row['poster_url']}" width="200" style="border-radius:15px;"/>
                    <h4 style="color:white; margin-top:10px;">{row['track_name']}</h4>
                    <p style="color:#B3B3B3;">{row['artists']}<br><i>{row['album_name']}</i></p>
                </div>
                """,
                unsafe_allow_html=True
            )

            