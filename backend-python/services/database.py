import pymysql
import sqlalchemy as db

_connection = None

def get_connection():
    # specify database configurations
    config = {
        'host': 'mysql',
        'port': 3306,
        'user': 'root',
        'password': 'testpass',
        'database': 'challenge'
    }
    global _connection
    if not _connection:
        db_user = config.get('user')
        db_pwd = config.get('password')
        db_host = config.get('host')
        db_port = config.get('port')
        db_name = config.get('database')

        connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
        engine = db.create_engine(connection_str)
        _connection = engine.connect()
    return _connection

def close_connection():
    global _connection
    if _connection:
        _connection.close()
        _connection = None
