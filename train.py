import pandas as pd
import ast
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

# Load data
movies = pd.read_csv("data/tmdb_5000_movies.csv")
credits = pd.read_csv("data/tmdb_5000_credits.csv")

movies = movies.merge(credits, on="title")
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
movies.dropna(inplace=True)

# -------- preprocessing --------
def convert(obj):
    return [i["name"] for i in ast.literal_eval(obj)]

def convert_cast(obj):
    L = []
    for i, item in enumerate(ast.literal_eval(obj)):
        if i == 3:
            break
        L.append(item["name"])
    return L

def fetch_director(obj):
    for i in ast.literal_eval(obj):
        if i["job"] == "Director":
            return [i["name"]]
    return []

movies["genres"] = movies["genres"].apply(convert)
movies["keywords"] = movies["keywords"].apply(convert)
movies["cast"] = movies["cast"].apply(convert_cast)
movies["crew"] = movies["crew"].apply(fetch_director)

movies["overview"] = movies["overview"].apply(lambda x: x.split())

for col in ["genres","keywords","cast","crew"]:
    movies[col] = movies[col].apply(lambda x: [i.replace(" ","") for i in x])

movies["tags"] = movies["overview"] + movies["genres"] + movies["keywords"] + movies["cast"] + movies["crew"]

new_df = movies[["movie_id","title","tags"]]
new_df["tags"] = new_df["tags"].apply(lambda x: " ".join(x).lower())

# -------- stemming --------
ps = PorterStemmer()
def stem(text):
    return " ".join([ps.stem(word) for word in text.split()])

new_df["tags"] = new_df["tags"].apply(stem)

# -------- vectorization --------
tfidf = TfidfVectorizer(max_features=3000, stop_words="english")
vectors = tfidf.fit_transform(new_df["tags"])

# -------- save --------
pickle.dump(new_df["title"].tolist(), open("models/movie_titles.pkl", "wb"))
pickle.dump(vectors, open("models/vectors.pkl", "wb"))

print("Training done ✅")