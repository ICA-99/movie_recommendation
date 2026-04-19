import streamlit as st
import pickle
from recommender import get_recommendations
from poster import fetch_posters

# 🔥 Page config
st.set_page_config(page_title="Movie Recommendation System", layout="wide")

# 🔥 CSS (same style)
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #f8fafc;
}

.movie-card {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 10px;
    text-align: center;
    transition: 0.3s;
}

.movie-card:hover {
    transform: scale(1.05);
}

.movie-title {
    font-size: 14px;
    margin-top: 8px;
    color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# 🔹 Load titles
titles = pickle.load(open("../models/movie_titles.pkl", "rb"))

# 🔹 Title
st.markdown('<h1 class="title">🎬 Movie Recommender (by Anjan)</h1>', unsafe_allow_html=True)

# 🔹 Dropdown
selected = st.selectbox("Select Movie", titles)

# 🔹 Button
if st.button("Recommend"):

    try:
        movies = get_recommendations(selected)
        posters = fetch_posters(movies)   # 👈 your function

        st.markdown("<br>", unsafe_allow_html=True)

        cols = st.columns(len(movies))

        for i in range(len(movies)):
            with cols[i]:
                st.markdown(f"""
                <div class="movie-card">
                    <img src="{posters[i]}" width="100%">
                    <div class="movie-title">{movies[i]}</div>
                </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(e)