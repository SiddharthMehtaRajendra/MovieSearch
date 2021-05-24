import click
import flask
from flask import request
import os
from pathlib import Path
from services.csv_preprocessor import CSVReader
from domain.movie import Movie
from domain.tag import Tag
from domain.link import Link
from domain.rating import Rating
from services.search_client import SearchClient
import services.database as database
from pprint import pprint

app = flask.Flask(__name__)
movielens_path = './ml-latest-small'
db = database.get_connection()

@app.route("/test-es")
def test_es():
    result = SearchClient().run_es()
    return flask.jsonify(dict(result=result))

@app.route("/test")
def test():
    result = "Success"
    return flask.jsonify(dict(result=result))

@app.route("/search_movies")
def search_movies():
    query = request.args.get('query')
    movie = Movie()
    result = movie.search_movies(query)
    return flask.jsonify(dict(result=result))

@app.route("/search_by_rating")
def search_movie_by_rating():
    query = request.args.get('rating')
    movie = Movie()
    result = movie.search_movie_by_rating(query)
    return flask.jsonify(dict(result=result))

@app.route("/list_top_rated")
def list_top_rated_movies():
    movie = Movie()
    result = movie.list_top_rated_movies()
    return flask.jsonify(dict(result=result))


@app.route("/load-data", methods=["POST"])
def load_movielens():
    csv_reader = CSVReader(movielens_path)
    
    movies = csv_reader.file_reader('movies')
    if movies:
        movie = Movie(movies)
        result = movie.load_into_db()
    
    ratings = csv_reader.file_reader('ratings')
    if ratings:
        rating = Rating(ratings)
        result = rating.load_into_db()
    
    tags = csv_reader.file_reader('tags')
    if tags:
        tag = Tag(tags)
        result = tag.load_into_db()
    
    links = csv_reader.file_reader('links')
    if links:
        link = Link(links)
        result = link.load_into_db()
    
    movie = Movie()
    movie.index_movie_ratings()
    result = "Successfully Loaded and Indexed All Data!"
    return flask.jsonify(dict(result=result, backend="python"))
