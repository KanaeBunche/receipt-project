from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, PrimaryKeyConstraint, Table
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Region(Base):
    __tablename__ = "regions"
    __table_args__ = (PrimaryKeyConstraint('id'),)

    id = Column(Integer())
    name = Column(String())
    recipe_association = relationship('Recipe', back_populates='region_association')

class Recipe(Base):
    __tablename__ = "recipes"
    __table_args__ = (PrimaryKeyConstraint('id'),)

    id = Column(Integer())
    name = Column(String())
    description = Column(String())
    region_id = Column(Integer, ForeignKey('regions.id'))
    region_association = relationship('Region', back_populates='recipe_association')

class Ingredient(Base):
    __tablename__ = "ingredients"
    __table_args__ = (PrimaryKeyConstraint('id'),)
    id = Column(Integer())
    name = Column(String())
<<<<<<< HEAD
=======
    recipes = relationship('Recipe', secondary=association_table, backref='ingredients')
    user_list_id = Column(Integer, ForeignKey('userlist.id'))
    


>>>>>>> main

class FoodAssociation(Base):
    __tablename__ = "recipes_association"
    __table_args__ = (PrimaryKeyConstraint('id'),)
    id = Column(Integer())
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    ingredient = relationship("Ingredient", backref=backref('ingredients'))
    recipe = relationship("Recipe", backref=backref('recipes'))


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
