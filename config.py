# config.py
import psycopg2.extras

DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': '123456',
    'dbname': 'ecommerce',
    'cursor_factory': psycopg2.extras.RealDictCursor
}
