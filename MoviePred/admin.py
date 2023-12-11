from django.contrib import admin
from .models import Movie,Review,Genre
from django.contrib.auth.models import Group
# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description',)
    list_filter = ('genre',)

# admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Genre)

admin.site.unregister(Group)
admin.site.site_header = "MoviePred Admin"
