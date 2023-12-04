import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from contextlib import closing
pymysql.install_as_MySQLdb()


load_dotenv(verbose=True)

DATABASE_ID = os.getenv('DATABASE_ID')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')

engine = create_engine('mysql://'+DATABASE_ID+':'+DATABASE_PASSWORD+'@'+DATABASE_HOST+':'+DATABASE_PORT+'/'+DATABASE_NAME)

def get_db():
    db = Session(engine)
    return closing(db)