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

    click.echo("Welcome! To start you off, first select what it is you would like to do here:")
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
    new_name = click.prompt("Name: ")
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
    new_region = click.prompt("Region: ")
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
    new_ingredients = click.prompt("Add Ingredients:")
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
    new_description= click.prompt("Describe the Recipe:")
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

click.command()
def save_recipe():
    save_region = None
    save_recipe = None
    save_ingredients = []
    save_foodassociations = []
    
    for region in regions:
        if new_recipe['region'].lower() == region.name.lower():
            save_region = region
            click.echo(f'Region Exists: {save_region}')
            break
    else:
        save_region = Region(name = new_recipe['region'])
        click.echo(f'Region does not Exist: {save_region}')
        session.add(save_region)
        session.commit()
            
            
    ingredient_list = [ingredient.strip() for ingredient in new_recipe['ingredients'].split(',')]
    for new_ingredient in ingredient_list:
        existing_ingredient = next((ingredient for ingredient in ingredients if ingredient.name.lower() == new_ingredient.lower()), None)
        if existing_ingredient:
            save_ingredients.append(existing_ingredient)
            click.echo(f'Ingredient already exists: {existing_ingredient}')
        else:
            click.echo(f'Ingredient did not exist: {new_ingredient}')
            create_ingredient = Ingredient(name = new_ingredient)
            session.add(create_ingredient)
            session.commit()
            click.echo(f'New Ingredient Created with ID: {create_ingredient.id}')
            save_ingredients.append(create_ingredient)
    # for ingredient in ingredients:
    #     for new_ingredient in ingredient_list:
    #         if new_ingredient.lower() == ingredient.name.lower():
    #             save_ingredients.append(ingredient)
    #             click.echo(f'Ingredient already exists: {ingredient}')
    #             break
    #     else:
    #         click.echo(f'Ingredient does not exist: {new_ingredient}')
    #         create_ingredient = Ingredient(name = new_ingredient)
    #         session.add(create_ingredient)
    #         session.commit()
    #         save_ingredients.append(create_ingredient)
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
        click.echo(f'Created new Recipe: {save_recipe}, name: {save_recipe.name}, description: {save_recipe.description}, region_id: {save_recipe.region_id}')
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

@click.command()
def grab_recipe():
    click.echo(regions)

@click.command()
def grab_recipe_by_region():
    click.echo(ingredients)

@click.command()
def grab_recipe_by_ingredients():
    click.echo(foodassociations)

if __name__ == "__main__":
    engine = create_engine('sqlite:///lib/db/sql_food.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    recipes = session.query(Recipe).all()
    regions = session.query(Region).all()
    ingredients = session.query(Ingredient).all()
    foodassociations = session.query(FoodAssociation).all()
    cli()
    # @click.command()
    # @click.option("--name", prompt="Enter your name: ", help ="The name of the user")
    # def hello(name):
    #     click.echo(f"Hello {name}!")

    # @cli.command()
    # @click.option("--region-name", prompt="Enter region name: ", help="The name of the region")
    # def add_region(region_name):
    #     session = Session()

    #     new_region_name = region_name

    #     click.echo(f"Added region: {region_name}")
    #     click.pause()
    # @cli.command()
    # @click.option("--title", prompt="Enter recipe title: ", help="The title of the recipe")
    # @click.option("--ingredients", prompt="Enter ingredients: ", help="List of ingredients")
    # def add_recipe(title, ingredients, region_id):
    #     session = Session()

        
    #     new_recipe_title=title
    #     new_recipe_ingredients=ingredients
    #     new_recipe_region=region_id

    #     click.echo(f"Added recipe: {title}")
    #     click.pause()
        
    # @cli.command()
    # @click.option("--name", prompt="Enter ingredient name: ", help="The name of the ingredient")
    # def add_ingredient(name):
    #     session = Session()

    #     new_ingredient = name

    #     click.echo(f"Added ingredient: {name}")
    #     click.pause()
        