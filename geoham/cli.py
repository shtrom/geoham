import click
import logging

from geoham.downloader import Downloader

@click.group()
@click.option('--log_level', '-l', default='info')
def main(log_level):
    click.echo('main')
    logging.basicConfig(level=log_level.upper())

@main.command()
def download():
    downloader = Downloader()
    downloader.download()
