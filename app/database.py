from psycopg_pool import AsyncConnectionPool
from app.config import get_settings

conninfo = f'''
dbname={get_settings().POSTGRES_DB}
user={get_settings().POSTGRES_USER}
password={get_settings().POSTGRES_PASSWORD}
host={get_settings().POSTGRES_HOST}
port={get_settings().POSTGRES_PORT}
'''

pool = AsyncConnectionPool(conninfo, max_size=10, open=False)

def get_db():
    return pool.connection()