import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from .redis_helper import cache_get,cache_set
def load_data(path="data/dataset.csv"):
    df = pd.read_csv(path)
    df.dropna(axis=0, inplace=True)
    df = df.drop_duplicates(subset="track_id").reset_index(drop=True)
    return df

def preprocess_numerical_cached(df):
    cached=cache_get("numerical_data")
    if cached is not None:
         return cached
    numerical_cols = ['danceability', 'energy', 'loudness', 'speechiness', 
                      'acousticness', 'instrumentalness', 'liveness', 
                      'valence', 'tempo', 'popularity']
    scaler = MinMaxScaler()
    df_num = scaler.fit_transform(df[numerical_cols])
    cache_set("numerical_data",df_num)
    return df_num

def string_info(row):
    artists = row['artists'].strip().split(";")
    artists = [a.replace(" ", "") for a in artists]
    genre = row['track_genre'].replace(" ", "")
    exp_tag = "explicit" if row["explicit"] else "clean"
    return " ".join(artists + [genre, exp_tag]).lower()

def preprocess_tfidf_cached(df, max_features=2000):
    cached=cache_get("tfidif_vectors")
    if cached is not None:
        return cached
    df['info'] = df.apply(string_info, axis=1)
    tfidf = TfidfVectorizer(max_features=max_features, stop_words="english")
    vectors = tfidf.fit_transform(df['info'])
    cache_set("tfidf_vectors",vectors)
    return vectors
