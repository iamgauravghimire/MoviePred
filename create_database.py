import pandas as pd
import os
import django
import numpy as np

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE","core.settings")
    django.setup()


from MoviePred.models import Movie, Review


movie_df = pd.read_csv('rotten_tomatoes_movies.csv', usecols=['rotten_tomatoes_link','movie_title', 'movie_info', 'original_release_date', 'genres'])
# print(movie_df.head())

reviews_df = pd.read_csv('rotten_tomatoes_critic_reviews.csv', usecols=['rotten_tomatoes_link','critic_name','review_type', 'review_date', 'review_content'])
# print(reviews_df.head())

all_movies = []

movie_df.rename(columns= {'rotten_tomatoes_link': 'movie_link',
                           'movie_title': 'title', 
                           'movie_info': 'description', 
                           'original_release_date': 'date_released' }, inplace=True)
print(movie_df.head())

movie_df.dropna(
    axis=0,
    how='any',
    inplace=True
)


reviews_df.rename(columns= {'rotten_tomatoes_link': 'movie_link',
                            'review_content': 'content',
                            }, inplace=True)

reviews_df.dropna(
    axis=0,
    how='any',
    inplace=True
)

print(reviews_df.head())


# for movie in reviews_df['movie_link']:
#     if movie not in all_movies:
#         all_movies.append(movie)



print(len(movie_df.index))

movie_df = movie_df.sample(n=1000, random_state=42)
print(len(movie_df.index))

# for index, row in movie_df.iterrows():
#     print(row['title'], row['movie_link'])

# for review_index,review_row in reviews_df.iterrows():
#     for movie_index, movie_row in movie_df.iterrows():
#         if movie_row['movie_link'] == review_row['movie_link']:
print(len(reviews_df.index))
reviews_df = reviews_df[reviews_df['movie_link'].isin(movie_df['movie_link'])]

print(len(reviews_df.index))
print(reviews_df.head())
print(len(reviews_df[reviews_df.movie_link == 'm/0814255']))

grouped = reviews_df.groupby('movie_link')

selected_rows = grouped.apply(lambda x: x.sample(n=20, random_state=5) if len(x) >= 20 else x)
reviews_df = selected_rows.reset_index(drop=True)

print(len(reviews_df[reviews_df.movie_link == 'm/1000013-12_angry_men']))
print(len(reviews_df.index))

movie_df.to_csv('movies_set.csv')
reviews_df.to_csv('reviews_set.csv')