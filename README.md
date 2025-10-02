🎶 Music Recommendation System

📖 A Journey of Building My Recommender

This project is not just about the final code. It’s a documentary of my thought process, the experiments I tried, what failed, and how I finally got a working recommendation engine with a UI.

1. 🎯 Problem Definition

I wanted to build a music recommender system that could:

Suggest similar tracks given one input song.

Use both audio/numerical features (like danceability, energy, loudness) and text metadata (like artist, genre, explicit flag).

Provide an interactive interface with posters and even Spotify embeds.

The challenge: balancing speed, accuracy, and user experience.

2. ⏱️ First Attempt: Numerical Similarity

I began with a naive cosine similarity using numerical audio features.

✅ Pros: Recommendations had some musical coherence.

❌ Cons: Slow when computed on-the-fly, and sometimes suggested unrelated artists.

This was my first insight:
👉 Raw features alone are not enough, and efficiency matters.

3. 📝 Second Attempt: TF-IDF on Metadata

Next, I tried a TF-IDF vectorizer on metadata like artists, genres, explicit.

✅ Pros: Very fast, thanks to sparse vectorization + cosine similarity.

❌ Cons: Results were often unrelated musically (two “similar” songs just because they shared words in artist/genre fields).

This showed me:
👉 Text alone cannot capture the real “feel” of music.

4. ⚡ Breakthrough: Hybrid Approach

Finally, I designed a hybrid recommender:

Numerical audio features similarity (cosine).

Textual features (TF-IDF) similarity.

Weighted combination: 0.6 * numeric + 0.4 * text.

This balance gave the best results:

Recommendations felt musically related.

Still fast enough for interactive use.

Easy to tune with weights.

👉 The sweet spot between quality and efficiency.

5. 🛠️ Code Structure

To keep things modular, I structured the repo like this:

Music-Recommender-System/
│
├── data/                     # datasets
│   └── dataset.csv
│
├── recommender/              # core logic
│   ├── preprocessing.py      # preprocessing & caching
│   ├── recommend_songs.py    # main hybrid recommender
│   ├── similarity.py         # similarity functions
│   ├── redis_helper.py       # caching helper (Redis + fallback)
│   └── get_poster_link.py    # Spotify API wrapper
│
├── pages/                    # Streamlit multi-page app
│   ├── Recommendations.py    # main recommender UI
│   ├── Spotify_Embed.py      # embed tracks directly
│   └── Stats.py              # feature exploration
│
├── app.py                    # Streamlit entry point
├── config.py                 # local config (ignored in git)
├── .env                      # secrets (CLIENT_ID, CLIENT_SECRET)
└── requirements.txt

6. 🔗 Spotify API Integration

To make recommendations realistic, I integrated the Spotify Web API:

Registered a developer app.

Implemented Client Credentials flow for tokens.

Wrote a helper get_poster(track_id) to fetch album posters.

Added a placeholder image if Spotify had no poster.

7. 💾 Caching (Redis + Fallback)

Fetching posters repeatedly = slow + risk of hitting API limits.

So I implemented two layers of caching:

Redis (preferred in production)

Stores posters + tokens with expiry.

Works even if multiple users access at once.

In-memory dictionary (fallback)

Used during development.

No extra setup, but resets when app restarts.

👉 Redis = scalable, in-memory = quick dev.

8. 🎨 Streamlit UI

Built an interactive UI with Streamlit because it’s:

Quick to prototype.

Great for displaying posters in a grid.

Supports multiple pages easily.

Flow in the app:

User selects a song.

Hybrid recommender fetches top 6 similar tracks.

Posters + metadata displayed beautifully.

Optionally embed Spotify tracks directly.

9. ⚡ Challenges & Fixes

Slow similarity checks → switched to vectorized cosine + precomputed matrices.

Poor text-only results → added hybrid weighting.

Token expiration → handled expiry in SpotifyAuthorization.

Poster failures → added try/except with placeholders.

Repetitive API calls → Redis + in-memory caching.

10. 🚀 Deployment

Added .gitignore to hide config.py + .env.

Created requirements.txt for dependencies.

Used Streamlit Community Cloud for free hosting.

API keys stored securely in Streamlit Secrets.

11. 📌 Next Steps

Playlist-level recommendations (not just track-to-track).

User-history personalization.

Deep audio embeddings (e.g., neural nets).

Deploy also on HuggingFace Spaces (alternative to Streamlit).

⚙️ How to Run Locally
# Clone repo
git clone <repo_url>
cd Music-Recommender-System

# Install dependencies
pip install -r requirements.txt

# (Optional) Start Redis
redis-server

# Add credentials
echo "CLIENT_ID=your_id" >> .env
echo "CLIENT_SECRET=your_secret" >> .env

# Run app
streamlit run app.py

🏁 Conclusion

This project wasn’t about replicating Spotify. It was about learning by building:

Tried naive → TF-IDF → hybrid.

Balanced accuracy vs. performance.

Integrated APIs + caching.

Built a full working product with a UI.

👉 Now I truly understand the end-to-end journey:
dataset → recommender → API/UI → deployment.
