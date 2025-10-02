# 🎶 Music Recommendation System

> A journey of building a music recommender from scratch - complete with all the failed experiments and lessons learned along the way.

**[Live Demo]([your-app-link-here](https://music-recommender-system-wwdytwieulwfrxkdpmgy2d.streamlit.app/))**

## 📖 What This Project Really Is

This project documents the steps I followed while building a music recommender system. It highlights the different approaches I experimented with, what worked well, what didn’t, and how I refined the system into a working solution with a simple UI.

I'm sharing this because I think the messy middle part of building something is just as valuable as the final product.

---

## 🎯 The Problem I Wanted to Solve

I set out to build a music recommender that could:

- Suggest similar tracks when you give it one input song
- Use both the audio features (danceability, energy, loudness) and text metadata (artist names, genres, explicit tags)
- Have an interactive interface with album posters and even Spotify embeds

The real challenge? Balancing speed, accuracy, and user experience without compromising too much on any of them.

---

## 🔄 The Journey (aka Trial and Error)

### ⏱️ First Attempt: Just the Numbers

I started simple with cosine similarity using only numerical audio features.

**What worked:** The recommendations actually had some musical coherence, which was encouraging.

**What didn't:** It was painfully slow when computing on-the-fly, and sometimes suggested completely unrelated artists.

**Key insight:** Raw features alone aren't enough, and if it's slow, nobody's going to use it.

### 📝 Second Attempt: Text-Based with TF-IDF

Next, I pivoted to TF-IDF vectorization on metadata like artists, genres, and explicit flags.

**What worked:** Super fast! Sparse vectorization with cosine similarity is really efficient.

**What didn't:** The results were often musically unrelated. Two songs would be "similar" just because they shared a few words in the artist or genre fields.

**Key insight:** Text alone can't capture the actual "feel" of music. You can't just match keywords and expect good recommendations.

### ⚡ The Breakthrough: Hybrid Approach

After those two failures, I finally landed on something that worked - a hybrid recommender:

1. Calculate similarity using numerical audio features (cosine)
2. Calculate similarity using textual features (TF-IDF)
3. Combine them with weights: **0.6 × numeric + 0.4 × text**

This gave me the best of both worlds:

- Recommendations felt musically related
- Still fast enough for interactive use
- Easy to tune by adjusting the weights

This was the sweet spot between quality and efficiency.

---

## 🛠️ How I Structured the Code

To keep everything modular and maintainable:

```
Music-Recommender-System/
│
├── data/
│   └── dataset.csv              # The music dataset
│
├── recommender/
│   ├── preprocessing.py         # Data preprocessing & caching logic
│   ├── recommend_songs.py       # Main hybrid recommender
│   ├── similarity.py            # Similarity calculation functions
│   ├── redis_helper.py          # Redis caching + fallback
│   └── get_poster_link.py       # Spotify API wrapper
│
├── pages/
│   ├── Recommendations.py       # Main recommender UI
│   ├── Spotify_Embed.py         # Embed Spotify tracks
│   └── Stats.py                 # Feature exploration page
│
├── app.py                       # Streamlit entry point
├── config.py                    # Local config (gitignored)
├── .env                         # API secrets (gitignored)
└── requirements.txt
```

---

## 🔗 Integrating Spotify API

To make the recommendations feel real and polished, I integrated the Spotify Web API:

- Registered a developer app on Spotify
- Implemented the Client Credentials OAuth flow
- Wrote a helper function `get_poster(track_id)` to fetch album artwork
- Added placeholder images when Spotify doesn't have a poster

This made the UI go from "cool project" to "actually looks professional."

---

## 💾 Caching Strategy (Because API Calls Are Expensive)

Fetching posters repeatedly is slow and risks hitting API rate limits. So I implemented a two-layer caching system:

**Redis (preferred for production):**
- Stores posters and auth tokens with automatic expiry
- Works even when multiple users access the app simultaneously
- Scales well

**In-memory dictionary (fallback for development):**
- No extra setup required
- Quick for local development
- But resets when the app restarts

The code automatically falls back to in-memory if Redis isn't available. Best of both worlds.

---

## 🎨 Building the UI with Streamlit

I chose Streamlit because:

- Super quick to prototype with
- Great for displaying images in a grid layout
- Multi-page support is built-in
- The learning curve is basically flat

**User flow:**
1. Select a song from the dropdown
2. Hybrid recommender fetches the top 6 similar tracks
3. Album posters and metadata display in a nice grid
4. Optionally embed and play tracks directly via Spotify

---

## ⚡ Challenges I Ran Into (And How I Fixed Them)

| Challenge | Solution |
|-----------|----------|
| Slow similarity calculations | Switched to vectorized cosine + precomputed matrices |
| Poor text-only results | Added hybrid weighting to balance audio and metadata |
| Spotify token expiration | Handled expiry logic in SpotifyAuthorization class |
| Poster fetch failures | Added try/except blocks with placeholder images |
| Too many API calls | Implemented Redis + in-memory caching |

---

## 🚀 Deployment

- Added `.gitignore` to keep `config.py` and `.env` out of version control
- Created `requirements.txt` for clean dependency management
- Deployed on Streamlit Community Cloud (free tier)
- Stored API keys securely using Streamlit Secrets

---

## 📌 What's Next?

Some ideas I'm considering for future iterations:

- **Playlist-level recommendations** instead of just track-to-track
- **User history personalization** to learn from listening patterns
- **Deep audio embeddings** using neural networks for better feature extraction
- Deploy on **HuggingFace Spaces** as an alternative to Streamlit Cloud

---

## ⚙️ Running This Locally

**1. Clone the repo**
```bash
git clone <repo_url>
cd Music-Recommender-System
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. (Optional) Start Redis**
```bash
redis-server
```
*Note: The app will work without Redis using in-memory caching, but Redis is recommended for production.*

**4. Get Spotify API Credentials**

You'll need to register an app on Spotify's developer portal:

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account (or create one if needed)
3. Click **"Create app"**
4. Fill in the details:
   - **App name:** Music Recommender (or whatever you want)
   - **App description:** A music recommendation system
   - **Redirect URI:** `http://localhost:8501` (required but not used for this project)
5. Check the terms and click **"Save"**
6. On your app's dashboard, click **"Settings"**
7. You'll see your **Client ID** and **Client Secret** (click "View client secret")

**5. Add your credentials to .env file**

Create a `.env` file in the project root:

```bash
CLIENT_ID=your_spotify_client_id_here
CLIENT_SECRET=your_spotify_client_secret_here
```

**Example `.env` format:**
```plaintext
CLIENT_ID=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
CLIENT_SECRET=z9y8x7w6v5u4t3s2r1q0p9o8n7m6l5k4
```

**6. Run the app**
```bash
streamlit run app.py
```

The app should open automatically in your browser at `http://localhost:8501`

---

## 🏁 Final Thoughts

This project was never about building the next Spotify. It was about learning by doing:

- Tried naive approaches → TF-IDF → finally landed on hybrid
- Learned to balance accuracy with performance
- Figured out how to integrate external APIs and implement smart caching
- Built a complete product from dataset to deployment

Now I actually understand the entire pipeline: **dataset → recommender → API integration → UI → deployment**.

And honestly? The failed experiments taught me more than the parts that worked on the first try.

---

## 📄 License

MIT License - feel free to use this however you want.

## 🤝 Contributing

Found a bug? Have an idea? Open an issue or submit a PR. I'm always learning!

---

Made with ☕ and a lot of trial and error.
