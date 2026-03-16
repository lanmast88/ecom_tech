import psycopg2
from app.config import settings

def get_db_connection():
    return psycopg2.connect(settings.database_url)