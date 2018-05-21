import csv
import logging

from .loggable_trait import LoggableTrait

REPEATER_OUTPUT       = 'Output'
REPEATER_INPUT        = 'Input'
REPEATER_CALL         = 'Call'
REPEATER_MNEMONIC     = 'mNemonic'
REPEATER_LOCATION     = 'Location'
REPEATER_SERVICE_AREA = 'Service Area'
REPEATER_LATITUDE     = 'Latitude'
REPEATER_LONGITUDE    = 'Longitude'
REPEATER_S            = 'S'
REPEATER_ERP          = 'ERP'
REPEATER_HASL         = 'HASL'
REPEATER_TO           = 'T/O'
REPEATER_SP           = 'Sp'
REPEATER_TONE         = 'Tone'
REPEATER_NOTES        = 'Notes'

NUM_FIELDS = [
    REPEATER_OUTPUT,
    REPEATER_INPUT,
    REPEATER_LATITUDE,
    REPEATER_LONGITUDE,
    REPEATER_S,
    REPEATER_ERP,
    REPEATER_HASL,
    REPEATER_TO,
    REPEATER_TONE,
]

class Parser(LoggableTrait):
    def __init__(self):
        self.init_logger(__name__)

    def parse(self, file):
        reader = csv.DictReader(file)

        return list(self._fix_types(reader))

    def _fix_types(self, data):
        for row in data:
            try:
                for field in NUM_FIELDS:
                    row[field] = float(row[field])
            except ValueError:
                self._logger.warning('Cannot convert field `%s` value `%s` to float in `%s`' % (
                    field,
                    row[field],
                    row,
                ))
                continue
            yield row
