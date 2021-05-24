import re
import pymysql
import services.database as db
from datetime import datetime
from sqlalchemy.sql import text

class Tag:

    def __init__(self, tags):
        super().__init__()
        self.tags = tags
        self.connection = db.get_connection()

    def process_row(self, tag):
        if tag:
            user_id = int(tag[0])
            movie_id = int(tag[1])
            tag_val = tag[2]
            unix_time = int(tag[3])
            timestamp = datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
        return (user_id, movie_id, tag_val, timestamp)
    
    def load_into_db(self):
        self.create_table()
        self.insert()

    def create_table(self):
        sqlQuery = text('''\
                CREATE TABLE IF NOT EXISTS tags ( \
                    id INT NOT NULL AUTO_INCREMENT, \
                    user_id INT NOT NULL, \
                    movie_id INT NOT NULL, \
                    tag VARCHAR(255), \
                    timestamp TIMESTAMP, \
                    PRIMARY KEY (id), \
                    FOREIGN KEY (movie_id) REFERENCES movies(id), \
                    UNIQUE (id, timestamp) \
                )''')
        self.connection.execute(sqlQuery)

    def insert(self):
        try:
            if self.tags:
                line_count = 0
                for tag in self.tags:
                    user_id, movie_id, tag_val, timestamp = self.process_row(tag)
                    insert_statement = text('''INSERT INTO tags \
                                    (user_id, movie_id, tag, timestamp) \
                                    VALUES (:user_id,:movie_id,:tag, :timestamp)''')
                    record = {"user_id": user_id, "movie_id": movie_id, "tag": tag_val, "timestamp": timestamp}
                    self.connection.execute(insert_statement, **record)
                    line_count += 1
                print(f'Successfully Inserted {line_count} into tags table')
        except Exception as e:
            print("Exception occured:{}".format(e))
        finally:
            db.close_connection()
                


        

            
