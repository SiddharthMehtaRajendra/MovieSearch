import re
import pymysql
import services.database as db
from datetime import datetime
from sqlalchemy.sql import text

class Rating:

    def __init__(self, ratings):
        super().__init__()
        self.ratings = ratings
        self.connection = db.get_connection() 

    def process_row(self, rating):
        if rating:
            user_id = int(rating[0])
            movie_id = int(rating[1])
            rating_val = rating[2]
            unix_time = int(rating[3])
            timestamp = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
        return (user_id, movie_id, rating_val, timestamp)
    
    def load_into_db(self):
        self.create_table()
        self.insert()

    def create_table(self):
        sqlQuery = text('''\
                CREATE TABLE IF NOT EXISTS ratings ( \
                    id INT NOT NULL AUTO_INCREMENT, \
                    user_id INT NOT NULL, \
                    movie_id INT NOT NULL, \
                    rating VARCHAR(5), \
                    timestamp TIMESTAMP, \
                    PRIMARY KEY (id), \
                    FOREIGN KEY (movie_id) REFERENCES movies(id), \
                    UNIQUE (id, timestamp) \
                )''')
        self.connection.execute(sqlQuery)

    def insert(self):
        try:
            if self.ratings:
                line_count = 0
                for rating in self.ratings:
                    user_id, movie_id, rating_val, timestamp = self.process_row(rating)
                    insert_statement = text('''INSERT INTO ratings \
                                    (user_id, movie_id, rating, timestamp) \
                                    VALUES (:user_id,:movie_id,:rating,:timestamp)''')
                    record = {"user_id": user_id, "movie_id": movie_id, "rating": rating_val, "timestamp": timestamp}
                    self.connection.execute(insert_statement, **record)
                    line_count += 1
                print(f'Successfully Inserted {line_count} into ratings table')
        except Exception as e:
            print("Exception occured:{}".format(e))
        finally:
            db.close_connection()
                


        

            
