import click
import json
import logging

from geoham.displayer import Displayer, LeafletDisplayer
from geoham.downloader import Downloader
from geoham.parser import Parser

@click.group()
@click.option('--log_level', '-l', default='info',
              help='Set the log level [critical, error, warning, info, debug]')
def main(log_level):
    logging.basicConfig(level=log_level.upper())

@main.command(help='Download the data')
def download():
    downloader = Downloader()
    downloader.download()

@main.command(help='Parse the data')
@click.argument('file', type=click.File('r'))
def parse(file):
    parser = Parser()
    data = parser.parse(file)
    print(json.dumps(data))

@main.command(help='Display the data')
@click.argument('file', type=click.File('r'))
def display(file):
    parser = Parser()
    data = parser.parse(file)
    displayer = Displayer()
    displayer.display(data)

@main.command(help='Display the data on a map')
@click.argument('file', type=click.File('r'))
@click.argument('out', type=click.File('wb'))
def map(file, out):
    parser = Parser()
    data = parser.parse(file)
    click.echo('Rendering map...', err=True)
    displayer = LeafletDisplayer()
    map = displayer.display(data)
    map.save(out)

