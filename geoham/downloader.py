import logging

from .loggable_trait import LoggableTrait

try:
    # Python 3
    from urllib.request import urlretrieve
except ModuleNotFoundError:
    # Python 2
    from urllib import urlretrieve

class Downloader(LoggableTrait): # not awesome...

    _url='http://www.wia.org.au/members/repeaters/data/documents/Repeater%20Directory%20180318.csv'

    def __init__(self):
        self.init_logger(__name__)

    def download(self):
        outfile = self._url.split('/')
        if len(outfile) > 1:
            outfile = outfile[-1]
        else:
            outfile = None

        self._logger.info('Downloading %s...' % self._url)
        filename, httpmessage  = urlretrieve(self._url, outfile)
        self._logger.info('Saved as %s' % filename)
        return filename
