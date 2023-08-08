
from faker import Faker
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Region, Recipe, Ingredients, UserList

def seed_database():
    
    regions_data = [
        {"name": "Italy"},
        {"name": "France"},
        {"name": "United States of America"}
    ]
    for region_data in regions_data:
        region = Region(name=region_data["name"])
        session.add(region)
        session.commit()

    # recipes_data = [
    #     {"name" : "Italy", "description": "You Put the noodels in the water","ingredients" :"Noodles, GroundBeef,Tomatoe Sauce"},
    #     {"name": "Paris", "description": "You Put the Fish in the fryer","ingredients" :"GroundBeef, Bread"},
    #     {"name": "United States of America", "description": "You Put the ground eef in the hot pan", "ingredients": "GroundBeef, Bread"}
    # ]
    recipes_data = [
        {"name" : "Spaghetti Bolognese", "description": "Classic Italian pasta dish. *instructions here*", "region_name": "Italy"},
        {"name": "Croissant", "description": "Delicious French pastry", "region_name": "France"},
        {"name": "Burger", "description": "All-American favorite", "region_name": "United States"},
    ]
    
    for recipe_data in recipes_data:
        region = session.query(Region).filter_by(name=recipe_data["region_name"]).first()
        if region:
            recipe = Recipe(
                name = recipe_data["name"],
                description=recipe_data["description"],
                region=region
            )
            session.add(recipe)
            session.commit()
            
            ingredients_data = recipe_data.get("ingredients", [])
            for ingredient_name in ingredients_data:
                ingredient = Ingredients(name=ingredient_name, recipe=recipe)
                session.add(ingredient)
                session.commit()

    for recipe_data in recipes_data:
        recipe = Recipe(recipe_data)
        session.add(recipe)
        session.commit()
    
    # engine = create_engine('sqlite:///sql_food.db')
    # Session = sessionmaker(bind=engine)
    # session = Session()

    # Add more sample data for recipes and user lists

if __name__ == '__main__':
    engine = create_engine('sqlite:///sql_food.db')
    Session = sessionmaker(bind=engine)
    session = Session
# if __name__ == "__main__":
#     seed_database()
