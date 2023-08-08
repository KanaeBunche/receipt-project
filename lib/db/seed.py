
from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Region, Recipe, UserList

if __name__ == '__main__':
    engine = create_engine('sqlite:///sql_food.db')
    Session = sessionmaker(bind=engine)
    session = Session



