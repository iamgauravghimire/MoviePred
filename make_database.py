import django
import os
import csv
import pickle
from datetime import datetime
import re
import random

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE","core.settings")
    django.setup()

from MoviePred.models import Movie,Review,Genre
from django.contrib.auth.models import User

def generate_random_rating(is_rotten):
    if is_rotten == "rotten":
        rating = random.uniform(1.0,2.9)
    elif is_rotten == "fresh":
        rating = random.uniform(3.0,5.0)
    else:
        rating = None
    
    return round(rating, 1) if rating else None


def regex_time(text):
    review = re.sub("(@[A-Za-z0-9]+)", ' ', text)
    review = re.sub("(https?://[A-Za-z0-9./]+)", ' ', review)
    review = re.sub("(http\S+)", ' ', review)
    review = re.sub("([^a-zA-Z.!?])", ' ',review)
    review = re.sub("( +)", ' ', review)
    return review

def convert_date_format(date_string):
    try:
        date_object = datetime.strptime(date_string, "%m/%d/%Y")
        converted_date = date_object.strftime("%Y-%m-%d")
        return converted_date
    except ValueError:
        return date_string

print(convert_date_format('3/26/1993'))

def check_date_format(date_string):
    try:
        # Attempt to parse the date string in "yyyy-mm-dd" format
        datetime.strptime(date_string, "%Y-%m-%d")
        return False  # The date format is "yyyy-mm-dd"
    except ValueError:
        return True 

def create_genre():
    with open('movies_set.csv') as file:
        reader = csv.reader(file)
        next(reader)

        Genre.objects.all().delete()
        genres = []
        for row in reader:
            res = re.findall(r"\w+", row[4])
            genres.extend(res)

        genres = list(set(genres))
        
        for genre in genres:
            genre = Genre(
                name = genre
            )
            genre.save()

create_genre()

def run():
    with open('movies_set.csv') as file:
        reader = csv.reader(file)
        next(reader)
        user = User.objects.get(username = 'admin')
        Movie.objects.all().delete()

        for row in reader:
            print(row)
            if check_date_format(row[4]):
                row[5] = convert_date_format(row[5])
            if row[5] == "":
                row[5] = None
           


            movie = Movie(
            title = row[2],
            description = row[3],
            date_released = row[5],
            movie_id = row[1],
            movie_owner = user 
            )

            movie.save()
            res = re.findall(r"\w+", row[4])
            for gn in res:
                g1 = Genre.objects.get(name = gn)
                movie.genre.add(g1)

        

run()




with open('lg_tv.pickle', 'rb') as f:
    tfidf_vzer, lg_clf = pickle.load(f)



# pred = lg_clf.predict(tfidf_vzer.transform([regex_time("IT was a really bad  movie i really hated it.")]))
# print(pred)

def sentiment_predictor(review):
    pred = lg_clf.predict(tfidf_vzer.transform([regex_time(review)]))
    
    if pred == [1]:
        return 'Positive'
    else:
        return 'Negative'
    
def get_probabilities(review):
    probas = lg_clf.predict_proba(tfidf_vzer.transform([regex_time(review)]))

    return probas

def create_review():

    with open('reviews_set.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        Review.objects.all().delete()
        user = User.objects.get(username = 'admin')
        for row in reader:
            print(row)
            if check_date_format(row[4]):
                row[4] = convert_date_format(row[4])
            if row[4] == "":
                row[4] = None
            movie = Movie.objects.get(movie_id = row[1])
            sentiment_prediction = sentiment_predictor(row[5])
            probas = get_probabilities(row[5])
            prob_pos = probas[0][1]
            prob_neg = probas[0][0]
            rating = generate_random_rating(row[3].lower())
            review = Review(
                critic_name = row[2],
                rating = rating,
                content = row[5],
                review_date = row[4],
                movie = movie,
                sentiment_pred = sentiment_prediction,
                movie_link = row[1],
                user = user,
                prob_pos = prob_pos,
                prob_neg = prob_neg
            )

            review.save()

    
    # with open('reviews_set.csv') as file:
    #     reader = csv.reader(file)
    #     next(reader)

create_review()

# m = Review.objects.all()
# print(m.values())

