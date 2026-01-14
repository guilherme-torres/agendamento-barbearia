from psycopg_pool import ConnectionPool, AsyncConnectionPool
from app.config import config

conninfo = f'''
dbname={config.POSTGRES_DB}
user={config.POSTGRES_USER}
password={config.POSTGRES_PASSWORD}
host={config.POSTGRES_HOST}
port={config.POSTGRES_PORT}
'''

pool = AsyncConnectionPool(conninfo, max_size=10, open=False)

def get_db():
    return pool.connection()