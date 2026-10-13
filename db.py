import os
import sqlalchemy as sql
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()

url = URL.create(
    drivername='postgresql+psycopg2',
    username='postgres',
    password=os.getenv('DB_PASSWORD'),
    host='localhost',
    port='5432',
    database='crm'
)

engine = sql.create_engine(url, connect_args={'client_encoding': 'UTF8', 'options': '-c lc_messages=C'})