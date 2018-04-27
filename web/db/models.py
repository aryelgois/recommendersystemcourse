from sqlalchemy import Column, Integer, Text, Numeric
from db.database import Base


class Users(Base):

    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(Text)

    def __init__(self, id, name=None):
        self.id = id
        self.name = name

class MoviesIMDb(Base):

    __tablename__ = "MoviesIMDb"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    title = Column(Text)
    year = Column(Integer)
    image_url = Column(Text)
    summarie = Column(Text)

    def __init__(self, id, title=None, year=None, image_url=None, summarie=None):
        self.id = id
        self.title = title
        self.year = year
        self.image_url = image_url
        self.summarie = summarie



class Movies(Base):

    __tablename__= "Movies"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    id_imdb = Column(Integer)
    title = Column(Text)

    def __init__(self, id, id_imdb=None, title=None):

        self.id = id
        self.id_imdb = id_imdb
        self.title = title

class Ratings(Base):

    __tablename__ = "Ratings"

    user_id = Column(Integer, primary_key=True, nullable=False)
    movie_id = Column(Integer, primary_key=True, nullable=False)
    rating = Column(Numeric)

    def __init__(self, user_id, movie_id, rating=None):

        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating


class UserSimilarity(Base):

    __tablename__ = "UserSimilarity"

    id_user_x = Column(Integer, primary_key=True, nullable=False)
    id_user_y = Column(Integer, primary_key=True, nullable=False)
    similarity = Column(Numeric)

    def __init__(self, id_user_x, id_user_y, similarity=None):

        self.id_user_x = id_user_x
        self.id_user_y = id_user_y
        self.similarity = similarity


