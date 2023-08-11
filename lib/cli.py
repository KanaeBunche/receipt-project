from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Region, Recipe, Ingredient, Base, FoodAssociation
import click

new_recipe = {
    "name": '',
    "description": '',
    "ingredients": '',
    "region": ''
}
@click.command()   
def cli():

    click.echo("To start you off, first select what it is you would like to do here:")
    click.echo("1. Add a new Recipe")
    click.echo("2. Grab an existing Recipe.")
    click.echo("3. Grab a list of available Recipes in the database based on region.")
    click.echo("4. Grab a list of available Recipes in the database based on your ingredients")
    choice = click.prompt("Enter the number of the command you want to execute!")

    if choice == "1":
        add_recipe_start()
    elif choice == "2":
        grab_recipe()
    elif choice == "3":
        grab_recipe_by_region()
    elif choice == "4":
        grab_recipe_by_ingredients()
    else:
        click.echo("Invalid choice. Exiting")
        cli()

@click.command()
def add_recipe_start():
    click.echo("_______________________________________")
    click.echo("Enter the name of your new Recipe")
    new_name = click.prompt("Name ")
    click.echo("")
    click.echo(f"Wow sounds interesting, want to go with this name?")
    confirm = click.prompt("Yes or No ")
    if confirm == "yes":
        new_recipe["name"] = new_name
        add_recipe_region()
    elif confirm == "no":
        add_recipe_start()
    else:
        click.echo("")
        click.echo("Invalid command prompt")
        add_recipe_start()

@click.command()
def add_recipe_region():
    click.echo("")
    click.echo("_______________________________________")
    click.echo("Enter the name of the Region your food is from, ex: Italy, Morocco, Korea, etc.")
    new_region = click.prompt("Region ")
    click.echo(f"Are you sure this is the region you want?")
    confirm = click.prompt("Yes or No ")
    if confirm == "yes":
        new_recipe["region"] = new_region
        add_recipe_ingredients()
    elif confirm == "no":
        add_recipe_region()
    else:
        click.echo("")
        click.echo("Invalid command prompt")
        add_recipe_region()

@click.command()
def add_recipe_ingredients():
    click.echo("")
    click.echo("_______________________________________")
    click.echo("Alright! Now lets add some ingredients to this bad boy!")
    new_ingredients = click.prompt("Add Ingredients ")
    click.echo(f"Are you good with these ingredients?")
    confirm = click.prompt("Yes or No ")
    if confirm == 'yes':
        new_recipe['ingredients'] = new_ingredients
        add_recipe_description()
    elif confirm == 'no':
        add_recipe_ingredients()
    else:
        click.echo("")
        click.echo("Invalid command prompt")
        add_recipe_ingredients()

@click.command()
def add_recipe_description():
    click.echo("")
    click.echo("_______________________________________")
    click.echo("Very nice! Now that you've got that taken care of, why not add a short description? Include the ingredients if you want!")
    new_description= click.prompt("Describe the Recipe ")
    click.echo(f" Are you good with this description?")
    confirm = click.prompt("Yes or No ")
    if confirm == 'yes':
        new_recipe['description'] = new_description
        confirm_recipe()
    elif confirm == 'no':
        add_recipe_description()
    else:
        click.echo("")
        click.echo("Invalid command prompt")
        add_recipe_description()

click.command()
def confirm_recipe():
    click.echo("")
    click.echo("_______________________________________")
    click.echo("Wow look at you go! You just completed an entire recipe! Have you made this before? Gordon????")
    click.echo("Well This is what your recipe looks like:")
    click.echo("")
    click.echo(f"Name: {new_recipe['name']}")
    click.echo("")
    click.echo(f"Region: {new_recipe['region']}")
    click.echo("")
    click.echo(f"Ingredients: {new_recipe['ingredients']}")
    click.echo("")
    click.echo(f"Description: {new_recipe['description']}")
    click.echo("")
    click.echo("Are you good with this? We can always restart if you like.")
    confirm = click.prompt("Save or Restart ")
    if confirm == 'save':
        save_recipe()
    elif confirm == 'restart':
        add_recipe_start()
    else:
        click.echo("")
        click.echo("Invalid command prompt")
        confirm_recipe()

@click.command()
def save_recipe():
    save_region = None
    save_recipe = None
    save_ingredients = []
    save_foodassociations = []
    
    for region in regions:
        if new_recipe['region'].lower() == region.name.lower():
            save_region = region
            break
    else:
        save_region = Region(name = new_recipe['region'])
        session.add(save_region)
        session.commit()
            
            
    ingredient_list = [ingredient.strip() for ingredient in new_recipe['ingredients'].split(',')]
    for new_ingredient in ingredient_list:
        existing_ingredient = next((ingredient for ingredient in ingredients if ingredient.name.lower() == new_ingredient.lower()), None)
        if existing_ingredient:
            save_ingredients.append(existing_ingredient)
        else:
            create_ingredient = Ingredient(name = new_ingredient)
            session.add(create_ingredient)
            session.commit()
            save_ingredients.append(create_ingredient)
    for recipe in recipes:
        if new_recipe['name']  == recipe.name:
            click.echo(f'Recipe already Exists, sorry :(')
            add_recipe_start()
    else:
        recipe_data = {
            'name': new_recipe['name'],
            'description': new_recipe['description'],
            'region_id': save_region.id
        }
        save_recipe = Recipe(name = recipe_data['name'], description = recipe_data['description'], region_id = recipe_data['region_id'])
        session.add(save_recipe)
        session.commit()
    for ingredient in save_ingredients:
        food_association = FoodAssociation(ingredient_id  = ingredient.id, recipe_id = save_recipe.id)
        session.add(food_association)
        save_foodassociations.append(food_association)
        for recipe in recipes:
            if ingredient.name.lower() in recipe.description.lower():
                food_association2 = FoodAssociation(ingredient_id=ingredient.id, recipe_id=recipe.id)
                session.add(food_association2)
                save_foodassociations.append(food_association2)
    session.commit()
    click.echo("")
    click.echo("Congratulations! You've successfully added a Recipe to our database. I'll go ahead a bring you back up to the start of the program, unless you'd like to exit?")
    confirm = click.prompt("Reset or Exit ")
    if confirm == "reset":
        click.echo("")
        click.echo("")
        click.echo("_______________________________________")
        cli()
    else:
        pass

@click.command()
def grab_recipe():
    session = Session()
    while True:
            
        recipe_name = click.prompt("Enter the recipe name (or type back to main menu)")
        
        if recipe_name.lower() == 'main menu':
            click.echo("Going back to the main menu.")
            cli()  
            break

       
        found_recipe = None
        for recipe in recipes:
            if recipe.name.lower() == recipe_name.lower():
                found_recipe = recipe

        if found_recipe:
            click.echo("")
            click.echo("")
            click.echo("_______________________________________")
            click.echo(f"- {found_recipe.name}")
            click.echo(f"- {found_recipe.description}")
            click.echo("")
        else:
            click.echo(f"No recipe found for the name: '{recipe_name}'.")
        

            
      


@click.command()
def grab_recipe_by_region():

    while True:
        region_name = click.prompt("Enter the region name (or type back to main menu)")
        
        if region_name.lower() == 'main menu':
            click.echo("Going back to the main menu.")
            cli()  
            break
        
        region = session.query(Region).filter_by(name=region_name).first()

        if region:
            recipes = region.recipe_association
            if recipes:
                click.echo("")
                click.echo("")
                click.echo("_______________________________________")
                click.echo(f"Recipes in region '{region_name}':")
                click.echo("")
                for recipe in recipes:
                    click.echo(f"- {recipe.name}")
                    click.echo(f"- {recipe.description}")
                    click.echo("")
            else:
                click.echo(f"No recipes found in region '{region_name}'.")
        else:
            click.echo(f"Region '{region_name}' not found.")

@click.command()
def grab_recipe_by_ingredients():
    click.echo("")
    click.echo("")
    click.echo("_______________________________________")
    click.echo("Go ahead and give me a list of ingredients you would like to search for. If an ingredient you list does not exist in our database, don't worry--we'll just ignore it!")
    prompt = click.prompt("Ingredients ")
    ingredient_prompt_list = [ingredient.strip() for ingredient in prompt.split(',')]
    ingredient_exists_list = []
    recipe_id_list = []
    recipe_list = []
    
    for ingredient_prompt in ingredient_prompt_list:
        existing_ingredient = next((ingredient for ingredient in ingredients if ingredient.name.lower() == ingredient_prompt.lower()), None)
        if existing_ingredient:
            ingredient_exists_list.append(existing_ingredient)
            
    for ingredient in ingredient_exists_list:
        ingredient_relationship = next((relationship for relationship in foodassociations if ingredient.id == relationship.ingredient_id), None)
        if ingredient_relationship:
            recipe_id_list.append(ingredient_relationship)
    
    for recipe_id in recipe_id_list:
        recipe_relationship = next((recipe for recipe in recipes if recipe.id == recipe_id.recipe_id), None)
        if recipe_relationship:
            if recipe_relationship not in recipe_list:
                recipe_list.append(recipe_relationship)
            
    for recipe in recipe_list:
        click.echo("")
        click.echo("_______________________________________")
        click.echo("")
        click.echo(f'Recipe: {recipe.name}')
        click.echo("")
        click.echo(f'Description: {recipe.description}')
        click.echo("")
        recipe_region = next((region for region in regions if region.id == recipe.region_id), None)
        click.echo(f'Region: {recipe_region.name}')
        click.echo("")
    click.echo("Cool, that's a good few recipes. So? Whaddaya wanna do? Check new ingredients out or go back to the start?")
    confirm = click.prompt("Reset or go back to the main menu ")
    if confirm == "reset":
        click.echo("")
        click.echo("")
        click.echo("_______________________________________")
        grab_recipe_by_ingredients()
    else:
        cli()


if __name__ == "__main__":
    engine = create_engine('sqlite:///lib/db/sql_food.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    recipes = session.query(Recipe).all()
    regions = session.query(Region).all()
    ingredients = session.query(Ingredient).all()
    foodassociations = session.query(FoodAssociation).all()
    print("Hello and welcome to our little project on generating Recipes!")
    cli()

