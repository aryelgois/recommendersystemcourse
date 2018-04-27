import utils
import numpy as np

from db.models import Users, Movies, Ratings, MoviesIMDb, UserSimilarity
from db.database import db_session


def intersect_items(id_user_x, id_user_y, local_movie_users=[]):

    """

    :param id_user_x: id of user x
    :param id_user_y: id of user y
    :param local_movie_users: a list of movies rated by all users. If passed, get the information locally.
    If not, get the information of the database.
    :return: a list of items rated by two users
    """

    if len(local_movie_users) == 0:
        dict_x = utils.get_movies_by_user(id_user_x)
        dict_y = utils.get_movies_by_user(id_user_y)
    else:
        dict_x = local_movie_users[id_user_x]
        dict_y = local_movie_users[id_user_y]

    intersect_keys = [k for k in dict_x.keys() if k in dict_y.keys()]

    return_dict_x = [(k, dict_x[k]) for k in dict_x.keys() if k in intersect_keys]
    return_dict_y = [(k, dict_y[k]) for k in dict_y.keys() if k in intersect_keys]

    return return_dict_x, return_dict_y


def similarity_value(id_user_x, id_user_y, local_movie_user=[]):

    """

    :param id_user_x: id of user x
    :param id_user_y: id of user y
    :param local_movie_user: a list of movies rated by all users. If passed, get the information locally.
    If not, get the information of the database.
    :return: similarity value by two users (in this case, similarity value is pearson correlation)
    """

    ratings_x, ratings_y = intersect_items(id_user_x, id_user_y, local_movie_user)

    if len(ratings_x) == 0:
        return 0.0

    list_ratings_user_x = np.array([float(value[1]) for value in ratings_x])
    list_ratings_user_y = np.array([float(value[1]) for value in ratings_y])

    mean_rating_x = np.mean(list_ratings_user_x)
    mean_rating_y = np.mean(list_ratings_user_y)

    numerator = (list_ratings_user_x - mean_rating_x) * (list_ratings_user_y - mean_rating_y)

    numerator = np.sum(numerator)

    if numerator == 0:
        return 0.0

    den_x = np.sum(np.power((list_ratings_user_x - mean_rating_x), 2))
    den_y = np.sum(np.power((list_ratings_user_y - mean_rating_y), 2))

    similarity_value = numerator / np.sqrt((den_x * den_y))

    return similarity_value


def users_similarity_local():

    """

    :return: a map with all similarities of database calculated
    """

    local_ = utils.pre_get_movies_by_user()

    all_users = utils.get_all_users()

    map_similarity = {}

    for i in all_users:
        for j in all_users:

            if i < j:
                map_similarity[(i, j)] = similarity_value(i, j, local_)

    return map_similarity


def user_similarity_db():

    """

    :return: calculate all users similarity and insert this information in dabase
    """

    deleted_rows = db_session.query(UserSimilarity).delete()
    db_session.commit()
    print("Deleted %i rows" % deleted_rows)

    local_ = utils.pre_get_movies_by_user()

    all_users = utils.get_all_users()

    for i in all_users:
        print("Calculating similarity of user %i" % i)

        for j in all_users:

            if i < j:
                value = similarity_value(i, j, local_)
                similarity_instance = UserSimilarity(i, j, value)
                db_session.add(similarity_instance)


    db_session.commit()


if __name__ == "__main__":

    print("Calculate all similarities")
    user_similarity_db()