import click
import json
import logging

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
@click.argument('file', type=click.File('rb'))
def parse(file):
    parser = Parser()
    data = parser.parse(file)
    print(json.dumps(data))
