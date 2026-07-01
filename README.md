# 🎬 Movie Recommendation System

A modern **Hybrid Movie Recommendation System** built with **Python, Streamlit, TF-IDF, Cosine Similarity, OMDb API, YouTube API, and Docker**. It recommends movies based on content similarity and enriched movie metadata, while also providing posters and official trailers.

---

## ✨ Features

- 🔍 Smart Movie Search
- 🎬 Content-Based Recommendation Engine
- 🏷️ Genre + Tags Based Similarity
- 🖼️ Movie Posters (OMDb API)
- 🎥 Official Trailer (YouTube Data API)
- ⭐ Similarity Match Score
- 🎨 Modern Dark UI
- ⚡ Fast Search with Autocomplete
- 🐳 Docker Support
- 📱 Responsive Streamlit Interface

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- Scikit-learn
- TF-IDF Vectorizer
- Cosine Similarity
- OMDb API
- YouTube Data API v3
- Docker
- Git & GitHub

---

## 📂 Dataset

This project uses the **MovieLens Latest Small Dataset**.

Files used:

- movies.csv
- ratings.csv
- tags.csv

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/gurmeetpoonia/movie-recommendation-system.git
cd movie-recommendation-system
```

### Create Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 API Keys

Create a **.env** file in the project root.

```env
OMDB_API_KEY=YOUR_OMDB_API_KEY
YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY
```

---

## ▶️ Run Project

```bash
streamlit run streamlit_app.py
```

---

# 🐳 Docker

Build Image

```bash
docker build -t movie-recommender .
```

Run Container

```bash
docker run -p 8501:8501 movie-recommender
```

Open

```
http://localhost:8501
```

---

## 📸 Screenshots

### Home Page

> Add screenshot here

### Recommendation Results

> Add screenshot here

---

## 📁 Project Structure

```
movie-recommendation-system
│
├── streamlit_app.py
├── recommendation.py
├── style.css
├── Dockerfile
├── requirements.txt
├── movies.csv
├── ratings.csv
├── tags.csv
├── .dockerignore
├── .gitignore
└── README.md
```

---

## 🔮 Future Improvements

- Collaborative Filtering
- Hybrid Recommendation Model
- User Login System
- Movie Details Page
- IMDb Rating
- Cast & Director
- Favorites / Watchlist
- Deployment on Streamlit Cloud
- TMDB Integration

---

## 👨‍💻 Author

**Gurmeet Punia**

GitHub:
https://github.com/gurmeetpoonia

---

## ⭐ Support

If you like this project, don't forget to ⭐ star the repository.