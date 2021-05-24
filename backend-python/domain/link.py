import re
import pymysql
import services.database as db
from datetime import datetime
from sqlalchemy.sql import text

class Link:

    def __init__(self, links):
        super().__init__()
        self.links = links
        self.connection = db.get_connection()

    def process_row(self, link):
        if link:
            movie_id = int(link[0])
            imdbId = None
            if(link[1]):
                imdbId = int(link[1])
            tmdbId = None
            if(link[2]):
                tmdbId = int(link[2])
        return (movie_id, imdbId, tmdbId)
    
    def load_into_db(self):
        self.create_table()
        self.insert()

    def create_table(self):
        sqlQuery = text('''\
                CREATE TABLE IF NOT EXISTS links ( \
                    id INT NOT NULL AUTO_INCREMENT, \
                    movie_id INT NOT NULL, \
                    imdb_id INT, \
                    tmdb_id INT, \
                    PRIMARY KEY (id), \
                    FOREIGN KEY (movie_id) REFERENCES movies(id) \
                )''')
        self.connection.execute(sqlQuery)

    def insert(self):
        try:
            if self.links:
                line_count = 0
                for link in self.links:
                    movie_id, imdbId, tmdbId = self.process_row(link)
                    insert_statement = text('''INSERT INTO links \
                                    (movie_id, imdb_id, tmdb_id) \
                                    VALUES (:movie_id,:imdb_id,:tmdb_id)''')
                    record = {"movie_id": movie_id, "imdb_id": imdbId, "tmdb_id": tmdbId}
                    self.connection.execute(insert_statement, **record)
                    line_count += 1
                print(f'Successfully Inserted {line_count} into links table')
        except Exception as e:
            print("Exception occured:{}".format(e))
        finally:
            db.close_connection()
                


        

            
