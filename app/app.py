import os
import pickle
import streamlit as st
import yt_dlp

from recommender import get_recommendations
from poster import fetch_posters

# 🔥 Page config
st.set_page_config(
    page_title="Movie Recommendation System",
    layout="wide"
)

# 🔥 CSS
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

.movie-title {
    font-size: 16px;
    margin-top: 8px;
    margin-bottom: 10px;
    color: #e2e8f0;
    text-align: center;
    font-weight: bold;
}

.section-title {
    font-size: 28px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 20px;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# 🔹 Load titles
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

titles = pickle.load(
    open(
        os.path.join(BASE_DIR, "../models/movie_titles.pkl"),
        "rb"
    )
)

# ======================================================
# 🔥 TRAILER FUNCTION
# ======================================================

def get_trailer(movie_name):

    try:

        query = f"ytsearch1:{movie_name} official trailer"

        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "no_warnings": True,
            "extract_flat": True,
            "force_generic_extractor": False
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(query, download=False)

            if "entries" in info and len(info["entries"]) > 0:

                video = info["entries"][0]

                video_id = video["id"]

                youtube_embed_url = (
                    f"https://www.youtube.com/embed/"
                    f"{video_id}?autoplay=0&mute=1"
                )

                return youtube_embed_url

    except:
        return None

# 🔹 Title
st.markdown(
    '<h1 class="title">🎬 Movie Recommendation System</h1>',
    unsafe_allow_html=True
)

# 🔹 Dropdown
selected = st.selectbox(
    "Select Movie",
    titles
)

# 🔹 Recommend Button
if st.button("Recommend"):

    try:

        # ======================================================
        # 🔥 SELECTED MOVIE
        # ======================================================

        st.markdown(
            '<div class="section-title">🎯 Selected Movie</div>',
            unsafe_allow_html=True
        )

        selected_poster = fetch_posters([selected])[0]

        selected_slug = selected.replace(" ", "-").lower()

        selected_watch_link = (
            f"https://www.justwatch.com/in/search?q={selected_slug}"
        )

        c1, c2, c3 = st.columns([1,2,1])

        with c2:

            # 🔥 Poster
            st.image(selected_poster)

            # 🔥 Movie Title
            st.markdown(f"""
            <div class="movie-title">
                {selected}
            </div>
            """, unsafe_allow_html=True)

            # 🔥 Trailer
            trailer_url = get_trailer(selected)

            if trailer_url:

                st.markdown("### 🎬 Trailer")

                st.iframe(
                    trailer_url,
                    height=400,
                )

            else:
                st.info("Trailer not found")

            # 🔥 Watch Movie
            st.link_button(
                "▶ Watch Movie",
                selected_watch_link,
                use_container_width=True
            )

        # ======================================================
        # 🔥 RECOMMENDED MOVIES
        # ======================================================

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">🔥 Recommended Movies</div>',
            unsafe_allow_html=True
        )

        movies = get_recommendations(selected)

        posters = fetch_posters(movies)

        cols = st.columns(len(movies))

        for i in range(len(movies)):

            with cols[i]:

                movie_slug = (
                    movies[i]
                    .replace(" ", "-")
                    .lower()
                )

                movie_watch_link = (
                    f"https://www.justwatch.com/in/search?q={movie_slug}"
                )

                # 🔥 Poster
                st.image(posters[i])

                # 🔥 Movie Title
                st.markdown(f"""
                <div class="movie-title">
                    {movies[i]}
                </div>
                """, unsafe_allow_html=True)

                # 🔥 Trailer
                trailer_url = get_trailer(movies[i])

                if trailer_url:

                    st.iframe(
                        trailer_url,
                        height=220
                    )

                else:
                    st.info("Trailer not found")

                # 🔥 Watch Button
                st.link_button(
                    "▶ Watch",
                    movie_watch_link,
                    use_container_width=True
                )

    except Exception as e:

        st.error(e)