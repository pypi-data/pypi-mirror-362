import click
from engine.main import MeliaTemplate

@click.group()
def cli():
    pass
    
@cli.command()
@click.option('--name', prompt='Name of the project', help='Name of the fastapi apploication')
def init(name):
    template = MeliaTemplate()
    template.make_starter_from_tree(name)
    click.echo(f"Project {name} Initialized")
        

if __name__=='__main__':
    cli()