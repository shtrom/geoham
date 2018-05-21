import click
import logging

from geoham.downloader import Downloader

@click.group()
@click.option('--log_level', '-l', default='info',
              help='Set the log level [critical, error, warning, info, debug]')
def main(log_level):
    logging.basicConfig(level=log_level.upper())

@main.command(help='Download the data')
def download():
    downloader = Downloader()
    downloader.download()
