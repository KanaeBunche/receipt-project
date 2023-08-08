
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Region, Recipe, Ingredients, UserList

def seed_database():
    regions_data = [
        {"name": "Italy"},
        {"name": "Paris"},
        {"name": "United States of America"}
        
    ]

    for region_data in regions_data:
        region = Region(name=region_data['name'])
        session.add(region)
        session.commit()

        recipes_data = [
        {"name" : "Italy", "description": "You Put the noodels in the water","ingredients" :"Noodles, GroundBeef,Tomatoe Sauce"},
        {"name": "Paris", "description": "You Put the Fish in the fryer","ingredients" :"GroundBeef, Bread"},
        {"name": "United States of America", "description": "You Put the ground eef in the hot pan", "ingredients": "GroundBeef, Bread"}
        # Add more recipes
    ]
        


    for recipe_data in recipes_data:
        recipe = Recipe(recipe_data)
        session.add(recipe)
        session.commit()
    
    
if __name__ == '__main__':
    engine = create_engine('sqlite:///sql_food.db')
    Session = sessionmaker(bind=engine)
    session = Session

