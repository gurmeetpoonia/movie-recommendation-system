import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# load dataset 
ratings = pd.read_csv("ratings.csv")
movies = pd.read_csv("movies.csv")
tags = pd.read_csv("tags.csv")
tags=tags[["movieId","tag"]]
tags["tag"]=tags["tag"].fillna("")




# Merge datasets
df = ratings.merge(movies, on="movieId")
popular_movies = (df.groupby("title").size().sort_values(ascending=False))
top_rated_movies = (df.groupby("title")["rating"].mean().sort_values(ascending=False))

# User-Movie Matrix
user_movie_matrix = ratings.pivot_table(
    index="userId",
    columns="movieId",
    values="rating"
).fillna(0)

# User Similarity
user_similarity = cosine_similarity(user_movie_matrix)

user_similarity_df = pd.DataFrame(
    user_similarity,
    index=user_movie_matrix.index,
    columns=user_movie_matrix.index
)
tags=(tags.groupby("movieId")["tag"].apply(lambda x:" ".join(x.astype(str)))).reset_index()
movies=movies.merge(tags,on="movieId",how="left")
movies["tag"]=movies["tag"].fillna("")
movies["genres"]=movies["genres"].str.replace("|"," ",regex=False)
movies["content"]=(movies["title"]+" "+ movies["genres"]+ " " + movies["tag"])


# TF-IDF Vectorizer
tfidf = TfidfVectorizer(stop_words="english",ngram_range=(1, 2), min_df=2)
tfidf_matrix = tfidf.fit_transform(movies["content"])


# Cosine Similarity
cosine_sim = cosine_similarity(tfidf_matrix)


# Movie Title -> Index Mapping
indices = pd.Series(movies.index,index=movies["title"]).drop_duplicates()



CONTENT_WEIGHT = 0.6
COLLAB_WEIGHT = 0.4


def hybrid_recommend(movie_name, user_id, top_n=5):

    if movie_name not in indices:
        return []

    movie_index = indices[movie_name]

    similarity_scores = list(enumerate(cosine_sim[movie_index]))

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )[1:50]

    watched_movies = set(
        ratings[
            ratings["userId"] == user_id
        ]["movieId"]
    )

    recommendations = []

    for idx, similarity in similarity_scores:

        movie = movies.iloc[idx]

        movie_id = movie["movieId"]

        content_score = similarity * 100

        # ---------- Collaborative Score ----------

        weighted_sum = 0
        similarity_sum = 0

        movie_ratings = ratings[
            ratings["movieId"] == movie_id
        ]

        for _, row in movie_ratings.iterrows():

            other_user = row["userId"]

            if other_user == user_id:
                continue

            sim = user_similarity_df.loc[
                user_id,
                other_user
            ]

            weighted_sum += sim * row["rating"]
            similarity_sum += abs(sim)

        if similarity_sum > 0:
            predicted_rating = weighted_sum / similarity_sum
        else:
            predicted_rating = 0

        collaborative_score = predicted_rating * 20

        hybrid_score = (
            CONTENT_WEIGHT * content_score +
            COLLAB_WEIGHT * collaborative_score
        )

        recommendations.append({

            "title": movie["title"],

            "genres": movie["genres"],

            "content_score": round(content_score,2),

            "predicted_rating": round(predicted_rating,2),

            "score": round(hybrid_score,2)

        })

    recommendations = sorted(
        recommendations,
        key=lambda x:x["score"],
        reverse=True
    )

    return recommendations[:top_n]