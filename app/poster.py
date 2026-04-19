import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")


def fetch_posters(movies):
    posters = []
    for movie in movies:
        try:
            url = f"http://www.omdbapi.com/?t={movie}&apikey={API_KEY}"
            res = requests.get(url).json()
            if res.get("Response") == "True":
                posters.append(res.get("Poster"))
            else:
                posters.append(None)
        except:
            posters.append(None)
    return posters