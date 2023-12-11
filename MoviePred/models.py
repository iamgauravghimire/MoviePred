from django.db import models
import datetime
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
# Create your models here.



class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Movie(models.Model):
    movie_id = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    genre = models.ManyToManyField(Genre, related_name="movies",default=None)
    date_released = models.DateField(null=True,default=datetime.date.today)
    movie_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies')
    medium_poster_url = models.URLField(null=True)
    extra_small_poster_url = models.URLField(null=True)
    def __str__(self):
        return  self.title



class Review(models.Model):
    
    options = (
        ('positive', 'Positive'),
        ('negative', 'Negative')
    )
    
    critic_name = models.CharField(max_length=100)
    # review_type = models.CharField(max_length=10, choices=type_options)
    content = models.TextField(max_length=10000)
    review_date = models.DateField(auto_now_add=True)
    movie = models.ForeignKey(Movie, related_name='reviews', on_delete=models.CASCADE, related_query_name='review')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', related_query_name='review')
    movie_link = models.CharField(max_length=100, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(Decimal('0.0')), MaxValueValidator(Decimal('5.0'))])
    sentiment_pred = models.CharField(max_length=20, choices=options, default='positive')
    prob_pos = models.DecimalField(max_digits=4, decimal_places=3, null=True)
    prob_neg = models.DecimalField(max_digits=4, decimal_places=3, null=True)
    def __str__(self):
        return self.content
    


