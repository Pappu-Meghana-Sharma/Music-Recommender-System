# import streamlit as st

# st.set_page_config(page_title="Music Recommender 🎶", layout="wide")
# st.title("🎧 Welcome to Music Recommender")

# st.markdown("""
# This app recommends songs based on similarity using:
# - **Posters & Cards** view  
# - **Spotify Embedded Player** view  

# 👉 Use the sidebar to navigate between pages.
# """)


import streamlit as st

# Page config
st.set_page_config(page_title="Music Recommender 🎶", layout="wide", page_icon="🎵")

# Dark theme styling (Spotify-like feel)
st.markdown(
    """
    <style>
    .main {
        background-color: #121212;
        color: #FFFFFF;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #1DB954;
        color: white;
        border-radius: 8px;
    }
    h1, h2, h3 {
        color: #1DB954;
    }
    .stMarkdown p {
        color: #B3B3B3;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def set_page_param(page_name: str):
    params = st.query_params
    params.update({"page": page_name})
    st.query_params = params 
    
    
# Title / Header
st.title("🎧 Welcome to Music Recommender")
st.markdown(
    """
    Explore and discover music in multiple ways:
    - **Poster View**: Get recommendations with album posters and info cards
    - **Spotify Player**: Play recommended tracks directly with embedded Spotify player
    - **Stats & Insights**: Analysis of trends in the dataset like top artists, genres, and track popularity
    """
)

# Navigation buttons (optional)
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🎵 Go to Recommendations"):
        st.switch_page("pages/2_Recommendations.py")
with col2:
    if st.button("🎧 Go to Spotify Player"):
        st.switch_page("pages/3_Spotify_Embed.py")
with col3:
    if st.button("📊 Go to Stats"):
        st.switch_page("pages/1_Stats.py")

# Optional footer
st.markdown(
    """
    ---
    Made by: Meghana Sharma  
    Data source: Spotify dataset
    """
)

