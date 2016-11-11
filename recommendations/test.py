import pandas as pd
import numpy as np



# df = pd.read_pickle('dataset/df.rating')

# n_users = df.user_id.unique().shape[0]
# n_movies = df.movie_id.unique().shape[0]

# ratings = np.zeros((n_users, n_movies))

# for row in df.itertuples():
#     ratings[row[4]-1, row[2]-1]] = row[3]


def train_test_split(ratings):
    test = np.zeros(ratings.shape)
    train = ratings.copy()

    for user in range(ratings.shape[0]):
        test_ratings = np.random.choice(ratings[user, :].nonzero()[0],
        size=10, replace=False)

        train[user, test_ratings] = 0
        test[user, test_ratings] = ratings[user, test_ratings]

    assert(np.all((train*test) == 0))

    return train, test

# train, test = train_test_split(ratings)



# from sklearn.metrics import mean_squared_error

# def get_mse(pred, actual):
#     pred = pred[actual.nonzero()].flatten()
#     actual = actual[actual.nonzero()].flatten()
#     return mean_squared_error(pred, actual)


def fast_similarity(ratings, kind='user', epsilon=1e-9):
    # epsilon -> small number for handling dived-by-zero errors
    if kind == 'user':
        sim = ratings.dot(ratings.T) + epsilon
    elif kind == 'item':
        sim = ratings.T.dot(ratings) + epsilon
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)


# user_similarity = fast_similarity(train, kind='user')
# item_similarity = fast_similarity(train, kind='item')
# print (item_similarity[:4, :4])



def predict_fast_simple(ratings, similarity, kind='user'):
    if kind == 'user':
        return similarity.dot(ratings) / np.array([np.abs(similarity).sum(axis=1)]).T
    elif kind == 'item':
        return ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])

# item_prediction = predict_fast_simple(train, item_similarity, kind='item')
# user_prediction = predict_fast_simple(train, user_similarity, kind='user')


# def get_all_movies():
#     movies = {}
#     al = Movie.objects.all()
#     for i in range(al.count()+1):
#         movies[i+1] = al[i].title

#     return movies

def top_k_movies(similarity, mapper, movie_idx, k = 10):
    # return [mapper[x] for x in np.argsort(similarity[movie_idx, :])[:-k-1:-1]]
    return [mapper[x] for x in np.argsort(similarity[movie_idx,:])[:-k-1:-1]]




