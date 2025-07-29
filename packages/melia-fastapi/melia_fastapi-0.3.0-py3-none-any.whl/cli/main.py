import click
from engine.main import MeliaTemplate

@click.group()
def cli():
    pass
    
@cli.command()
@click.option('--name', prompt='Name of the project', help='Name of the fastapi application')
@click.option('--author', prompt='Author of the project', help='Author of the project')
@click.option('--email', prompt='Email of the author', help='Email of the author')
@click.option('--description', prompt='Project description', help='Project description')
def new(name, author, email, description):
    template = MeliaTemplate()
    template.make_starter_from_tree(name, author, email, description)
    click.echo(f"Project {name} Initialized")
        
if __name__=='__main__':
    cli()