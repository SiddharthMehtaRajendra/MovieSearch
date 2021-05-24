import re
import json
import pymysql
import services.database as db
from sqlalchemy.sql import text
from services.search_client import SearchClient

class Movie:

    def __init__(self, movies=None):
        super().__init__()
        self.movies = movies
        self.connection = db.get_connection()
        self.search_client = SearchClient()

    def process_row(self, movie):
        if movie:
            id = movie[0]
            title = " ".join(re.findall("[a-zA-Z]+", movie[1]))
            regex_year = re.search("\d{4}", movie[1])
            year = None
            if regex_year:
                year = regex_year.group(0)
            if movie[2]:
                genres = ','.join(movie[2].split('|'))
        return (id, title, year, genres)
    
    def load_into_db(self):
        self.create_table()
        self.bulk_insert_and_index()

    def create_table(self):
        sqlQuery = text('''\
                CREATE TABLE IF NOT EXISTS movies ( \
                    id int NOT NULL, \
                    title VARCHAR(255) NOT NULL, \
                    year INT(4), \
                    genres VARCHAR(255), \
                    PRIMARY KEY (id)\
                )''')
        self.connection.execute(sqlQuery)

    def search_movies(self, query):
        body = {
                "query": 
                    {
                        "multi_match": {
                            "query": query,
                            "type": "most_fields",
                            "fields": ["title", "year", "genres"]
                        }
                    }
                }
        response = self.search_client.search("movies", body)
        result = []
        for record in response:
            result.append(record['_source'])
        return result

    def search_movie_by_rating(self, rating):
        body = {
                "query": {
                    "match_phrase": {
                        "average_rating": rating
                    }
                },
                "sort" : [{
                    "average_rating" : {
                        "order" : "desc"
                        }
                    }
                ]
            }
        response = self.search_client.search("movie_ratings", body)
        result = []
        for record in response:
            result.append(record['_source'])
        return result

    def list_top_rated_movies(self):
        body = {
                 "_source": [
                    "title",
                    "year",
                    "genres",
                    "average_rating",
                    ],
                "sort": [
                    {
                    "average_rating": {
                        "order": "desc"
                        }
                    }
                ]
            }
        response = self.search_client.search("movie_ratings", body)
        result = []
        for record in response:
            result.append(record['_source'])
        return result

    def bulk_insert_and_index(self):
        try:
            if self.movies:
                line_count = 0
                for movie in self.movies:
                    id, title, year, genres = self.process_row(movie)
                    insert_statement = text('''INSERT INTO movies \
                                    (id, title, year, genres) \
                                    VALUES (:id,:title,:year,:genres)''')
                    record = {"id": id, "title": title, "year": year, "genres": genres}
                    self.connection.execute(insert_statement, **record)
                    self.search_client.index(id, "movies", record)
                    line_count += 1
                print(f'Successfully Inserted and Indexed {line_count} into movies table and ES')
        except Exception as e:
            print("Exception occured:{}".format(e))
        finally:
            db.close_connection()

    def index_movie_ratings(self):
        try:
            line_count = 0
            select_statement = text('''SELECT m.id, m.title, m.year, m.genres, AVG(r.rating) as average_rating from movies m \
                                INNER JOIN ratings r\
                                ON m.id = r.movie_id
                                GROUP BY m.id
                                ORDER BY average_rating DESC''') 
            result = self.connection.execute(select_statement)
            for record in result:
                self.search_client.index(record['id'], "movie_ratings", dict(record))
                line_count += 1
            print(f'Successfully Inserted and Indexed {line_count} from movie_ratings to ES')
        except Exception as e:
            print("Exception occured:{}".format(e))
        finally:
            db.close_connection()

                


        

            
