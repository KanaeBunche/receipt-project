from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Region(Base):
    __tablename__ = "Regions"
    
    id = Column(Integer, primary_key=True)
    region = Column(String, unique=True)
    recipes = Column(String, unique=False)
    
db_url = 'sqlite:///sql_food.db'
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

new_region = Region(region='Italy', recipes='Spaghetti')
session.add(new_region)
session.commit()

region_query = session.query(Region).filter_by(region='Italy').first()
print(region_query)