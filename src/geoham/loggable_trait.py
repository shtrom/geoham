import logging

class LoggableTrait:
    _logger = None

    def init_logger(self, name=None):
        self._logger = logging.getLogger(name)

