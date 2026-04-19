import pickle
from sklearn.metrics.pairwise import cosine_similarity

titles = pickle.load(open("../models/movie_titles.pkl", "rb"))
vectors = pickle.load(open("../models/vectors.pkl", "rb"))

def get_recommendations(movie_name):
    idx = titles.index(movie_name)
    scores = cosine_similarity(vectors[idx], vectors).flatten()

    similar = sorted(
        list(enumerate(scores)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    return [titles[i[0]] for i in similar]