from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Region(Base):
    __tablename__ = "regions"
    
    id = Column(Integer, primary_key=True)
    region = Column(String, unique=True)
    recipes = Column(String, unique = False)


class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    instructions = Column(String)
    ingredients = Column(String)

    region_id = Column(Integer, ForeignKey('regions.id'))
    
    
    
db_url = 'sqlite:///sql_food.db'
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

new_region = Region(region='Italy', recipes='Spaghetti')
session.add(new_region)
session.commit()

new_recipe = Recipe(title='Spaghetti', instructions='Cook pasta', ingredients='Spaghetti', region_id=new_region.id)
session.add(new_recipe)
session.commit()


region_query = session.query(Region).filter_by(region='Italy').first()
print(region_query)

