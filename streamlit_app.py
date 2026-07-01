import streamlit as st
import requests
import urllib.parse
from streamlit_searchbox import st_searchbox
import re
import pandas as pd 
import os
from urllib.parse import quote
from dotenv import load_dotenv
from recommendation import movies, hybrid_recommend

ratings = pd.read_csv("ratings.csv")

# LOAD ENVIRONMENT & CONFIG
load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")
YOUTUBE_API_KEY=os.getenv("YOUTUBE_API_KEY")
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)
#st.write(YOUTUBE_API_KEY)
# LOAD CSS
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        st.warning("style.css file not found.")

load_css()


# HELPER FUNCTION: CLEAN MOVIE TITLE
def clean_title(title):

    return re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()


def extract_year(title):
    """
    Extracts year from MovieLens title, e.g. 'Toy Story (1995)' -> '1995'
    Returns None if not found.
    """
    match = re.search(r"\((\d{4})\)\s*$", title)
    return match.group(1) if match else None
@st.cache_data(show_spinner=False)
def get_trailer_url(movie_title):
    try:
        url = (
            "https://www.googleapis.com/youtube/v3/search"
        )

        params = {
            "part": "snippet",
            "q": f"{movie_title} Official Trailer",
            "key": YOUTUBE_API_KEY,
            "maxResults": 1,
            "type": "video"
        }

        response = requests.get(url, params=params)
        data = response.json()

        items = data.get("items", [])

        if items:
            return items[0]["id"]["videoId"]
           

    except Exception as e :
        print ("error:",e)

    return None
PLACEHOLDER_IMG = "https://via.placeholder.com/180x260/1a2238/ffffff?text=%F0%9F%8E%AC"
@st.cache_data(show_spinner=False)
def get_movie_poster(movie_title, year=None):
    if not API_KEY:
        return PLACEHOLDER_IMG
    try:
        movie_title = clean_title(movie_title)
        # Exact title search
        params = {"t": movie_title,"apikey": API_KEY}
        if year:
            params["y"] = year

        response = requests.get("https://www.omdbapi.com/",params=params,timeout=5)
        data = response.json()

        if data.get("Response") == "True":
            poster = data.get("Poster")
            if poster and poster != "N/A":
                # Check if image actually exists
                check = requests.get(poster, timeout=5)

                if check.status_code == 200:
                    return poster

        # Search fallback
        search = requests.get("https://www.omdbapi.com/",params={"s": movie_title,"apikey": API_KEY},timeout=5)
        search_data = search.json()

        if search_data.get("Response") == "True":
            for movie in search_data["Search"]:
                poster = movie.get("Poster")
                if poster and poster != "N/A":
                    try:
                        check = requests.get(poster, timeout=5)
                        if check.status_code == 200:
                            return poster
                    except:
                        continue
    except Exception:
        pass
    return PLACEHOLDER_IMG



# HERO SECTION
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <h1>🎬 Movie Recommendation System</h1>
        <p>Discover movies similar to your favorites</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")



# SEARCH SECTION
st.subheader("🔍 Search Movie")

movie_list = movies["title"].tolist()

def search_movies(searchterm: str):
    if not searchterm:
        return []

    return [movie for movie in movie_list if movie.lower().startswith(searchterm.lower())][:100]  # Maximum 10 results

user_options = ["Select User ID"] + sorted(ratings["userId"].unique())

col1, col2, col3 = st.columns([4, 1, 1])

with col1:
    selected_movie = st_searchbox(
        search_movies,
        placeholder="🔍 Search a movie...",
        key="movie_search"
    )

with col2:
    user_id = st.selectbox("👤 User",user_options,index=0,label_visibility="collapsed",placeholder="Please select userId", key="user_id")

with col3:
    recommend_btn = st.button(
        "🎬 Recommend",
        use_container_width=True
    )
# RECOMMEND BUTTON & POSTER CARDS
if recommend_btn:
    if not selected_movie:
        st.warning("⚠️ Please search and select a movie.")
        st.stop()

    elif  user_id == "Select User ID":
        
        st.warning("⚠️ Please select a User ID.")
        st.stop()

    else:
        with st.spinner("Finding similar movies..."):
            recommendations = hybrid_recommend(selected_movie,user_id )

            if not recommendations:
                st.error("No recommendations found for this movie.")
            else:
                st.write("")
                st.subheader("🍿 Recommended Movies")
                st.write("")

                cols = st.columns(5, gap="medium")

                for i, movie in enumerate(recommendations[:5]):
                    with cols[i]:
                        m_title = movie.get("title", "Unknown Title")
                        m_score = movie.get("score", "0")
                        m_pred = movie.get("predicted_rating",0)
                        m_content = movie.get("content_score",0)

                        clean_name = clean_title(m_title)
                        movie_year = extract_year(m_title)

                        video_id = get_trailer_url(clean_name)
                        poster_url = get_movie_poster(clean_name, movie_year)
                       
                        trailer_html = ""
                        if video_id:
                            trailer_html = f'<a href="https://www.youtube.com/watch?v={video_id}" target="_blank" class="trailer-btn">🎥 Watch Trailer</a>'
                        else:
                            search_link = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(f"{clean_name} Official Trailer")
                            trailer_html = f'<a href="{search_link}" target="_blank" class="trailer-btn">🔍 Search Trailer</a>'


                        card_html = f"""
                        <div class="movie-card">
                            <img src="{poster_url}" class="movie-poster-img"
                                onerror="this.onerror=null; this.src='{PLACEHOLDER_IMG}';"
                                    alt="{m_title}">
                                <div class="movie-info">
                                <div class="movie-title">{m_title}</div>
                                <div class="score">⭐ Hybrid Score : {m_score}%</div>
                                <div class="genre">🎯 Content : {m_content:.1f}%</div>
                                <div class="genre">👤 Predicted Rating : {m_pred}/5</div>
                                {trailer_html}
                            </div>
                        </div>
                        """
                        if video_id:
                            embed_html = f'''<iframe width="100%" height="200"
                            src="https://www.youtube.com/embed/{video_id}?autoplay=1"
                            frameborder="0" allow="autoplay;
                            encrypted-media" allowfullscreen>
                            </iframe>'''
                        else:
                            st.warning("Trailor not found")

                        st.markdown(card_html, unsafe_allow_html=True)

                
# FOOTER
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | TF-IDF | Cosine Similarity | OMDB API")