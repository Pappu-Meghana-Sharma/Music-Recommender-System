import pandas as pd
from .similarity import get_similarity_cached
from .get_poster_link import get_poster
import streamlit as st
from .redis_helper import cache_get,cache_set

  # Cache for 1 hour this is only for current streamlit session..if the app restarts(relaoded page) caching is lost
@st.cache_data(ttl=3600)
def get_poster_redis(track_id):
    cached = cache_get(f"poster:{track_id}")
    if cached is not None:
        return cached

    poster_url = get_poster(track_id)
    cache_set(f"poster:{track_id}", poster_url)
    return poster_url

def recommend_tfidf_v2(df, df_num, vectors, track_name, artist=None, num_weight=0.6, tfidf_weight=0.4):
    if artist:
        track_id = df[(df.track_name == track_name) & (df.artists.str.contains(artist, case=False, na=False))].index[0]
    else:
        track_id = df[df.track_name == track_name].index[0]

    sim = get_similarity_cached(track_id, df_num, vectors, num_weight, tfidf_weight)
    
    top_5 = sorted(list(enumerate(sim.tolist())), reverse=True, key=lambda x: x[1])[:10]
    ids = [id[0] for id in top_5]
    results = df.loc[ids, ['track_id','track_name','artists','album_name']]
    results = results[results['track_name'] != track_name]
    results = results.drop_duplicates(subset=['track_name'])[:6]
    results["poster_url"] = results["track_id"].apply(get_poster_redis)
    
    return results
