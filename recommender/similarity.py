from sklearn.metrics.pairwise import cosine_similarity
from .redis_helper import cache_set,cache_get
def find_similarity(track_id, vectors):
    return cosine_similarity(vectors[track_id].reshape(1,-1), vectors)

def combine_similarity(track_id, df_num, vectors, num_weight=0.5, tfidf_weight=0.5):
    
    tfidf_sim = find_similarity(track_id, vectors)[0]
    num_sim = cosine_similarity(df_num[track_id].reshape(1, -1), df_num)[0]
    return num_weight * num_sim + tfidf_weight * tfidf_sim


def get_similarity_cached(track_id, df_num, vectors, num_weight=0.5, tfidf_weight=0.5):
    sim_key = f"sim:{track_id}:num{num_weight}:tfidf{tfidf_weight}"
    cached = cache_get(sim_key)
    if cached is not None:
        return cached
    
    sim = combine_similarity(track_id, df_num, vectors, num_weight, tfidf_weight)
    cache_set(sim_key, sim)
    return sim