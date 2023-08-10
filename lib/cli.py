from db.seed import Session
from db.models import Region, Recipe, Ingredient
import click


session=Session()

@click.group()   
def cli():
    pass

@click.command()
@click.option("--name", prompt="Enter your name: ", help ="The name of the user")
def hello(name):
    click.echo(f"Hello {name}!")

@cli.command()
@click.option("--region-name", prompt="Enter region name: ", help="The name of the region")
def add_region(region_name):
    session = Session()

    new_region = Region(name=region_name)
    session.add(new_region)
    session.commit()

    click.echo(f"Added region: {region_name}")

@cli.command()
@click.option("--title", prompt="Enter recipe title: ", help="The title of the recipe")
@click.option("--ingredients", prompt="Enter ingredients: ", help="List of ingredients")
def add_recipe(title, ingredients,region_id):
    session = Session()


    new_recipe = Recipe(title=title, ingredients=ingredients, region_id=region_id)
    session.add(new_recipe)
    session.commit()

    click.echo(f"Added recipe: {title}")

@cli.command()
@click.option("--name", prompt="Enter ingredient name: ", help="The name of the ingredient")
def add_ingredient(name):
    session = Session()

    new_ingredient = Ingredient(name=name)
    session.add(new_ingredient)
    session.commit()

    click.echo(f"Added ingredient: {name}")

    
if __name__ == "__main__":
    cli()