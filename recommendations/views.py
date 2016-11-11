from django.shortcuts import render
from .models import Movie, CriticUser, Rating, Category, Genre
# from .test import *
from .new import cosine_similarity, get_top_k
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from recommendations.forms import UserForm, loginForm, RatingForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import requests
import json
import decimal

# configuration to use the tmdb API
CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
KEY = '70110d69244c193c6d54a4b76f8553c5'




def movie_list(request):
	# render the movies correctly, with proper image url
	items = sorted(Movie.objects.all(), key = lambda movie: movie.avg_rating, 
					reverse = True)[:100]
	paginator = Paginator(items, 12)

	page = request.GET.get('page')

	try:
		movies = paginator.page(page)

	except PageNotAnInteger:
		# if page is not an integer, deliver first page
		movies = paginator.page(1)

	except EmptyPage:
		# if page is out of range (eg 9999), deliver the last page of results
		movies = paginator.page(paginator.num_pages)
	# count = 0
	# for movie in movies:
	# 	if movie.image_url == '':
	# 		movie.image_url = get_image(movie.id)
	# 		movie.save()
	# 		print(movie.image_url)
	# 		print(count,"\n")
	# 		count = count + 1

	return render(request, 'recommendations/movie_list.html', {'movies':movies})


def categories(request, id):
	category = Category.objects.get(id = id)
	gen = category.genre_set.all()
	mov = [i.movie.title for i in gen]
	movies = Movie.objects.filter(title__in = mov)
	movies = sorted(movies, key = lambda movie: movie.avg_rating, reverse = True)
	paginator = Paginator(movies, 12)

	page = request.GET.get('page')

	try:
		movies = paginator.page(page)

	except PageNotAnInteger:
		# if page is not an integer, deliver first page
		movies = paginator.page(1)

	except EmptyPage:
		# if page is out of range (eg 9999), deliver the last page of results
		movies = paginator.page(paginator.num_pages)
	# count = 0
	# for movie in movies:
	# 	if movie.image_url == '':
	# 		movie.image_url = get_image(movie.id)
	# 		movie.save()
	# 		print(movie.image_url)
	# 		print(count,"\n")
	# 		count = count + 1

	return render(request, 'recommendations/categories.html', {'category':category, 'movies':movies})



def movie_detail(request, id):
	try:
		item = Movie.objects.get(id = id)
		gen = item.genre_set.all()
		cat = [i.genre.category for i in gen]
		catList = Category.objects.filter(category__in = cat)

		if request.method == 'POST':
			if request.user.is_authenticated():
				form = RatingForm(data = request.POST)
				ratingVal = request.POST['rating']

				if form.is_valid():
					rate(request.user, item, ratingVal)
					messages.success(request, "You have successfully rated this movie.")
					return HttpResponseRedirect('/refined_similarities')


			else:
				return HttpResponseRedirect('/login')

		else:
			form = RatingForm()

	except Movie.DoesNotExist:
		raise Http404("Movie does not exist")		

	prediction = np.load('recommendations/prediction_matrix.npy')
	print(prediction)
	sims = cosine_similarity(prediction)
	top_k = get_top_k(sims, id, 200)

	movies = []
	for i in top_k:
		movie = Movie.objects.get(id = i)
		movies.append(movie)

		movies = movies[0:8]
	
	return render(request, 'recommendations/movie_detail.html', 
						{'item':item, 'movies':movies, 'catList':catList, 'form':form })



def train_user(request):
	user = request.user
	
	criticUser = CriticUser.objects.get(user = user)
	userRated = criticUser.rating_set.all()
	
	movieList = [i.movie for i in userRated]
	
	catList = []
	for i in movieList:
		gen = i.genre_set.all()
		cat = [i.genre.id for i in gen]
		catList += cat
	catList = set(catList)

	pred_matrix = np.load('recommendations/prediction_matrix.npy')
	user_vec = np.zeros(80)
	n_iters = 1000
	gamma = 0.001
	lmbda = 0.01
	qarray = []
	for i in range(len(userRated)):
		temp = pred_matrix[userRated[i].movie.id - 1]
		qarray.append(temp)
	
	qarray = np.array(qarray)
	actual = np.array([i.rating for i in userRated])		
	actual = actual.astype('float64')

	# apply GD for the user
	for n in range(n_iters):
		for i in range(len(actual)):
			e = actual[i] - user_vec.dot(qarray[i].T)
			user_vec += gamma * (e*qarray[i] - lmbda*user_vec)

	pred_ratings = user_vec.dot(pred_matrix.T)
	indices = pred_ratings.argsort()
	indices += 1
	index = indices[-1]
	sims = cosine_similarity(pred_matrix)
	top_k = get_top_k(sims, index, 9)

	print(pred_ratings)

	movies = []
	for i in top_k:
		movie = Movie.objects.get(id=i)
		movies.append(movie)
	# movies = sorted(movies, key = lambda movie:movie.avg_rating)

	# compList = {i.id:(set([j.genre.id for j in i.genre_set.all()])) for i in movies}
	
	# diffDict = {}
	# for idx in compList.keys():
	# 	diffDict[idx] = len(catList - compList[idx])

	# diffDict = sorted(diffDict.items(), key = lambda x: x[1])

	# finalIndices = [diffDict[i][0] for i in range(len(diffDict))]
	# # finalIndices = tuple(finalIndices)
	# movies = []
	# for i in finalIndices:
	# 	movies.append(Movie.objects.get(id=i))
		
	# movies = sorted(movies, key = lambda movie: movie.avg_rating, reverse = True)

	paginator = Paginator(movies, 12)

	page = request.GET.get('page')

	try:
		movies = paginator.page(page)

	except PageNotAnInteger:
		# if page is not an integer, deliver first page
		movies = paginator.page(1)

	except EmptyPage:
		# if page is out of range (eg 9999), deliver the last page of results
		movies = paginator.page(paginator.num_pages)

	return render(request, 'recommendations/refined_similarities.html', 
						{'movies':movies })



def rate(user, movie, rat):
	if not Rating.objects.filter(user__id=user.id, movie__id=movie.id).exists():
		criticUser = CriticUser()
		criticUser.user = user
		criticUser.id = user.id
		criticUser.save()
		rating = Rating()
		rating.user = criticUser
		rating.movie = movie
		rating.rating = rat
		rating.save()
	else:
		rating = Rating.objects.filter(user__id = user.id, movie__id= movie.id)
		rating = rating[0]
		rating.rating = rat
		rating.save()
		# messages.success(request, "You have successfully rated this movie.")
	print("{} has successfully rated {} with {} ratings".
		format(rating.user, rating.movie, rating.rating))



def search(request):
    query = request.POST.get('q','')
    exclude = [' ']
    if query:
        qset = (
            Q(title__icontains = query)
        )
        results = Movie.objects.filter(qset)
        results = sorted(results, key = lambda result: result.avg_rating, reverse = True)
        count = len(results)
    else:
        results = []

    return render(request, 'recommendations/search.html', {'results':results, 'count':count, 'query':query})



@login_required
def dashboard(request):
	user = request.user
	criticUser = CriticUser.objects.get(user=user)
	ratings = criticUser.rating_set.all()

	return render(request, 'recommendations/dashboard.html', {'ratings':ratings})



def get_image(movieID):
	# returns the url of the movie given the movieID
	url = CONFIG_PATTERN.format(key=KEY)
	r = requests.get(url)
	config = r.json()

	base_url = config['images']['base_url']
	sizes = config['images']['poster_sizes']

	max_size = 'w92'
	imdbid =  get_imdb_id(movieID)
	if imdbid[0] == 't':
		IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
		r = requests.get(IMG_PATTERN.format(key=KEY, imdbid = imdbid))
		
		if r.ok is False:
			return "Poster Not found.."

		
		api_response = r.json()


		if len(api_response['posters']) == 0:
			return "Poster Not found.."

		poster = api_response['posters'][0]

		url = base_url + max_size + poster['file_path']

		return url



def get_imdb_id(imdb_url):
	# returns the imdb id of the given imdburl	
	req = requests.get(imdb_url)
	return req.url.split('/')[-2]




def register(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data = request.POST)
        

		if user_form.is_valid():
		    user = user_form.save()

		    user.set_password(user.password)
		    user.save()
		    registered = True

		else:
		    print(user_form.errors)

	else:
		user_form = UserForm()

	return render(request, 'recommendations/register.html', {'user_form':user_form, 'registered':registered})



def user_login(request):
	if request.method == 'POST':
		login_form = loginForm(data = request.POST)
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username = username, password = password)

        # if not user.is_staff and not user.is_superuser:
		if user is None:
			return HttpResponse('Invalid login details supplied.')

		if user.is_active:
			login(request,user)
			return HttpResponseRedirect('/')
		
		else:
		    return HttpResponse('Your MovieEngine Account has been disabled.')

        # else:
        #     return HttpResponse("Invalid login details supplied.")

	else:
		login_form = loginForm()

	return render(request, 'recommendations/login.html', {'login_form': login_form})


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')