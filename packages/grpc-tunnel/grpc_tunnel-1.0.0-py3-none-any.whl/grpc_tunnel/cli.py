import click
from .server import launch_server

@click.group()
def main():
    pass

@main.command()
@click.argument('repo_url', required=True)
@click.option('--entry', required=True, help='Entrypoint script to run after cloning')
@click.option('--port', default=50051, show_default=True, help='Port to expose the gRPC server on')
def server(repo_url, entry, port):
    """Launch server from a GitHub repo."""
    launch_server(repo_url, entry, port)