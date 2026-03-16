import psycopg2
from app.config import settings

def get_db_connection():
    try:
        conn = psycopg2.connect(settings.database_url)
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None