# To populate the fields of all tables,
# either from the csv files or the database itself.
from django.db import models
from django.contrib.auth.models import User
from .models import Movie, CriticUser, Rating, Genre, Category



class AllMovies(models.Model):
	
	def get_all_movies():
		reader = open('dataset/u.item', mode = 'r', encoding = 'ISO-8859-1')
		
		for line in reader:
			line = line.split('|')
			movie = Movie()
			movie.id = int(line[0])
			movie.title = line[1]
			movie.year = line[2]
			print(movie.id, movie.title, movie.year)
			# movie.genres = line[2]
			movie.save()
		reader.close()
         



class AllCritics(models.Model):
	
	def get_all_critics():
		users = User.objects.all()
		for i in users:
			criticUser = CriticUser()
			if not CriticUser.objects.filter(user=i).exists():
				criticUser.user = i
				criticUser.id = i.id
				print(criticUser.id)
				criticUser.save()



class AllUsers(models.Model):

	def get_all_users():
		reader = open('dataset/u.data','r')
		count = 0
		for line in reader:
			line = line.split('\t')
			user = User()
			user.id = int(line[0])
			user.username = line[0]
			if not User.objects.filter(id=int(line[0])).exists():
				user.save()
				print(count)
				count += 1

		reader.close()




class AllRatings(models.Model):		
	def get_all_ratings():
		reader = open('dataset/u.data','r')
		# userId,movieId,rating,timestamp

		# movieReader = open('dataset/movies.csv','r')

		for line in reader:
			line = line.split('\t')
			
			# create an instance of Rating model
			ratingUser = Rating()
			
			user = User.objects.get(username=line[0])

			criticUser = CriticUser.objects.get(user = user)

			ratingUser.user = criticUser

			# get the movie model and assign to Rating.movie
			movie = Movie.objects.get(id=int(line[1]))
			ratingUser.movie = movie

			# finally, get the rating
			ratingUser.rating = line[2]


			ratingUser.save()
			print(ratingUser)
		reader.close()




class AllGenres(models.Model):
	def get_all_genres():
		reader = open('dataset/u.item', mode = 'r', encoding = 'ISO-8859-1')
		for line in reader:
			line = line.split('|')

			for i in range(19):
				if int(line[i+5])==1:
					allgen = Genre()
					movie = Movie.objects.get(id=int(line[0]))
					allgen.movie = movie
					genre = Category.objects.get(id=i)
					allgen.genre = genre
					print(allgen)
					allgen.save()
	
		reader.close()

