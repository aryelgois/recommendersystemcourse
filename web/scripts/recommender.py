import utils
import operator
import numpy as np

from db.models import Users, Movies, Ratings, MoviesIMDb, UserSimilarity
from db.database import db_session

def get_top_neighbors_rated_item(id_user, id_movie, N):

    users_movie = db_session.query(Ratings).filter(
        Ratings.movie_id==id_movie,
        Ratings.user_id!=id_user).all()

    if not users_movie:
        return []

    similar = []

    for item in users_movie:

        user_ = item.user_id

        similarity_register = db_session.query(UserSimilarity.similarity).filter(
            UserSimilarity.id_user_x==id_user,
            UserSimilarity.id_user_y==user_).first()

        if not similarity_register:
            similarity_value = 0.0
        else:
            similarity_value = float(similarity_register[0])

        similar.append((user_, similarity_value))

    sorted_ = sorted(similar, key=operator.itemgetter(1), reverse=True)

    return sorted_[:N]

def predict_rating(id_user, id_movie):

    N = 20

    items_rated_by_user = utils.get_movies_by_user(id_user)

    items_rated_by_user_values = [items_rated_by_user[x] for x in items_rated_by_user]
    mean_user = np.mean(items_rated_by_user_values)

    topN_users = get_top_neighbors_rated_item(id_user, id_movie, N)

    sum_ = 0
    sum_K = 0

    for top_user in topN_users:

        user_u = top_user[0]
        similarity = top_user[1]

        rating_user_u = utils.get_rating_by_user_movie(user_u, id_movie)

        items_rated_by_user_u = utils.get_movies_by_user(user_u)
        items_rated_by_user_u_values = [items_rated_by_user_u[x] for x in items_rated_by_user_u]

        mean_user_u = np.mean(items_rated_by_user_u_values)

        sum_ += similarity * (rating_user_u - mean_user_u)
        sum_K += abs(similarity)

    if sum_K == 0:
        k = 0
    else:
        k = 1 / sum_K

    final_rating = mean_user + k * sum_

    return final_rating

if __name__ == '__main__':

    result_ = predict_rating(1, 1)
    print(result_)
