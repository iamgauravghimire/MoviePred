from tmdbv3api import TMDb, Search
from tmdbv3api import Movie as TMDBMovie

import django
import os





if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE","core.settings")
    django.setup()


import dotenv
dotenv.load_dotenv()

from MoviePred.models import Movie,Review
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
def fetch_movie_posters():
    tmdb = TMDb()
    tmdb.api_key = TMDB_API_KEY
    tmdb_movie = TMDBMovie()
    tmdb.language = 'en'
    tmdb.debug = True
    movies = Movie.objects.all()
    # print(movies)
    for movie in movies:
        
        response = tmdb_movie.search(movie.title)
        print(response)
        if response and len(response) > 0:
            movie_info = response[0]
            movie_id = movie_info.id
            movie_images = tmdb_movie.images(movie_id=movie_id)

            if movie_images and 'posters' in movie_images:
                posters = movie_images['posters']
                medium_poster_path = None
                extra_small_poster_path = None

                for poster in posters:
                    if not medium_poster_path and poster['width'] >= 500:
                        medium_poster_path = poster['file_path']

                    if not extra_small_poster_path and poster['width'] >= 200:
                        extra_small_poster_path = poster['file_path']
                    if medium_poster_path and extra_small_poster_path:
                        break


                if medium_poster_path:
                    movie.medium_poster_url = f"https://image.tmdb.org/t/p/w500{medium_poster_path}"
                if extra_small_poster_path:
                    movie.extra_small_poster_url = f"https://image.tmdb.org/t/p/w200{extra_small_poster_path}"    
                movie.save()

fetch_movie_posters()