from django.db import models
from django.contrib.auth.models import User
from MoviePred.models import Genre, Review
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    genre_preferences = models.ManyToManyField(Genre, related_name='users')

    def __str__(self):
        return self.user.username
    
