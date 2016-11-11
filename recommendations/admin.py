from django.contrib import admin
from .models import Movie, CriticUser, Rating, Genre, Category


admin.site.register(Movie)
admin.site.register(CriticUser)
admin.site.register(Rating)
admin.site.register(Category)
admin.site.register(Genre)