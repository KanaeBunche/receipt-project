from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, PrimaryKeyConstraint, Table
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

association_table = Table('association', Base.metadata,
                    Column('ingredient_id', Integer, ForeignKey('ingredients.id')),
                    Column('recipe_id', Integer, ForeignKey('recipes.id')))

class Region(Base):
    __tablename__ = "regions"
    __table_args__ = (PrimaryKeyConstraint('id'),)
    
    id = Column(Integer())
    name = Column(String())
    recipes = relationship('Region', backref=backref('region'))

class Recipe(Base):
    __tablename__ = "recipes"
    __table_args__ = (PrimaryKeyConstraint('id'),)

    id = Column(Integer())
    name = Column(String())
    description = Column(String())
    region_id = Column(Integer, ForeignKey('regions.id'))
    ingredients = relationship('Ingredient', secondary=association_table, backref = 'recipes')
    
class Ingredients(Base):
    __tablename__ = "ingredients"
    __table_args__ = (PrimaryKeyConstraint('id'),)
    
    id = Column(Integer())
    name = Column(String())
    recipes = relationship('Recipe', secondary=association_table, backref='ingredients')
    

class UserList(Base):
    __tablename__ = "userlist"

    id= Column(Integer, primary_key=True)
    ingredients = Column(String)
    region_id = Column(Integer, ForeignKey('regions.id'))



db_url = 'sqlite:///sql_food.db'
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

# duplicate_regions = session.query(Region).filter_by(region='Italy').all()
# for region in duplicate_regions:
#     session.delete(region)
# session.commit()


# new_region = Region(region = 'Italy', recipes='Spaghetti')
# session.add(new_region)
# session.commit()

# #creating a new recepie associated with the region
# new_recipe = Recipe(name='Sandwhich', ingredients='meat', region_id=new_region.id)
# session.add(new_recipe)
# session.commit()

# new_userlist = UserList(region = 'South Africa', ingredients='Tomatoes, pasta',region_id=new_region.id)
# session.add(new_region)
# session.commit()


# region_query = session.query(Region).filter_by(region='Italy').first()
# print(region_query)
# print("Region:",region_query.region)
# print("Recipe:",region_query.recipes)

# recipe_query = session.query(Recipe).filter_by(title='Sandwhich').first()
# print(recipe_query)
# print("Recipe:", recipe_query.title)
# print("Ingredients:", recipe_query.ingredients)
# print("Region:", recipe_query.region.region)

# userlist_query = session.query(UserList).filter_by(ingredients='Tomatoes, pasta').first()
# print(userlist_query)
# print("User List Ingredients:", userlist_query.ingredients)
# print("User List Region:", userlist_query.region.region)
