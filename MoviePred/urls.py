from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from MoviePred import views

urlpatterns = [
    path("movies/", views.MovieList.as_view()),
    path("movies/<int:pk>/", views.MovieDetail.as_view()),
    path("movies/<int:pk>/reviews/", views.MovieReviewListCreate.as_view()),
    # path('movies/<int:pk>/reviews/', views.MovieReviewList.as_view(), name='movie-review-list'),
    path("reviews/", views.ReviewList.as_view()),
    path("reviews/<int:pk>/", views.ReviewDetail.as_view()),
    path("recommendations/", views.MovieRecommendationView.as_view()),
    path("genres/", views.GenreList.as_view())
    
]

urlpatterns = format_suffix_patterns(urlpatterns)