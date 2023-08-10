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
