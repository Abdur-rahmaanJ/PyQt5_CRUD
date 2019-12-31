import sys
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils import app_path

engine = create_engine('sqlite:///{}'.format(app_path('db/items.db')))
Session = sessionmaker(bind=engine)

Base = declarative_base()