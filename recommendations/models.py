from django.db import models
from django.contrib.auth.models import User
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from django.utils import timezone
import csv
import decimal



class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    genres = models.CharField(max_length=255, default='')
    year = models.CharField(max_length=50)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default = 0.0)
    image_url = models.CharField(max_length=200,default = '', null=True)
    
    
    def get_average_rating(self):
    	reader = open('dataset/u.data','r')

    	cumsum = 0
    	count = 1
    	for line in reader:
    		line = line.split('\t')
    		if self.id == int(line[1]):
    			cumsum += decimal.Decimal(int(line[2]))
    			# print(line[2], count, cumsum)
    			count += 1
    	self.avg_rating = cumsum/count
    	self.avg_rating = round(self.avg_rating, 1)
    	reader.close()
    	self.save()
    	print(self.avg_rating)
    	
    	return self.avg_rating



    def __str__(self):
        return self.title




#RATING_CHOICES = (1.0, 2.0, 3.0, 4.0, 5.0)

class Rating(models.Model):
	user = models.ForeignKey('CriticUser')
	movie = models.ForeignKey('Movie')

	rating = models.DecimalField(max_digits=3, 
            decimal_places=1, default = 0.0)

	# index = models.IntegerField()
	def __str__(self):
		return '(%s %s)' %(self.user.user.username, self.movie.title)




class CriticUser(models.Model):
	# id = models.CharField(primary_key=True, max_length = 25)
	user = models.OneToOneField(User)
	# userRating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)	
	def __str__(self):
		return self.user.username



class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=30)
    def __str__(self):
        return self.category


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    movie = models.ForeignKey('Movie')
    genre = models.ForeignKey('Category')
    def __str__(self):
        return '(%s %s)' %(self.movie.title, self.genre.category)

