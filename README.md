```html
<p>movieRecommendations is a simple django based movie recommendation engine. It uses the dataset from movielens, link: http://grouplens.org/datasets/movielens/100k/</p>

<p>The approach used is MatrixFactorization using Stochastic Gradient Descent. First, the given movielens dataset is used to create a movie-movie similarity matrix (using Collaborative Filtering). Then this data is used to display the top similar movies to a movie when the user browses to the particular movie.</p>

<p>It also trains the users on the go, i.e. when the users rate movies, these data are used to refine the recommendations. For this, the users are again trained separately.</p>

<p>Reference Links:</p>
<ul>
    <li>http://blog.ethanrosenthal.com/2016/01/09/explicit-matrix-factorization-sgd-als/</li>
    <li>https://www.youtube.com/watch?v=UfNU3Vhv5CA</li>
</ul>


Usage:
<ul>
    <li> Get the necessary packages: 
        numpy, pandas, matplotlib
    </li>
    
    <li> Migrate the database: 
        ./manage.py makemigrations
        ./manage.py migrate
    </li>
    
    <li> Populate the database with movie details , takes a few hours, if you have a better way, please suggest
        cd recommendations/
        from populate import *
        AllMovies.get_all_movies()
        AllCritics.get_all_critics()
        AllUsers.get_all_users()
        AllRatings.get_all_ratings() 
        AllGenres.get_all_genres()
    </li>

    <li> check the website
        ./manage.py runserver
    </li>
</ul>    
```
