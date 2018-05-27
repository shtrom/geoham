import csv
import pandas as pd
import numpy as np
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
REPEATER_STATUS       = 'Status'
REPEATER_ERP          = 'ERP'
REPEATER_HASL         = 'HASL'
REPEATER_TO           = 'T/O'
REPEATER_SPONSOR      = 'Sponsor'
REPEATER_TONE         = 'Tone'
REPEATER_NOTES        = 'Notes'

FIELD_TYPES = {
    REPEATER_OUTPUT: np.float64,
    REPEATER_INPUT: np.float64,
    REPEATER_CALL: np.character,
    REPEATER_MNEMONIC: np.character,
    REPEATER_LOCATION: np.character,
    REPEATER_SERVICE_AREA: np.character,
    REPEATER_LATITUDE: np.float64,
    REPEATER_LONGITUDE: np.float64,
    REPEATER_STATUS: np.character,
    REPEATER_ERP: np.float64,
    REPEATER_HASL: np.float64,
    REPEATER_TO: np.float64,
    REPEATER_SPONSOR: np.character,
    REPEATER_TONE: np.float64,
    REPEATER_NOTES: np.character,
}

NA_FIELDS = [ '-', 'Various', '?' ]

NUM_FIELDS = [ k for k in FIELD_TYPES.keys() if FIELD_TYPES[k] == np.float64 ]


class Parser(LoggableTrait):
    def __init__(self):
        self.init_logger(__name__)

    def parse(self, file):
        data = pd.read_csv(file,
                             names=FIELD_TYPES.keys(),
                             dtype=FIELD_TYPES,
                             na_values = NA_FIELDS,
                             header=0,
                             error_bad_lines=False, # XXX: This will drop rows with too many notes
                             warn_bad_lines=self._logger.isEnabledFor(logging.WARNING)
                             )

        skipped_data = data[(
            data[REPEATER_CALL].isnull()
            | data[REPEATER_LATITUDE].isnull()
            | data[REPEATER_LONGITUDE].isnull()
        )]
        self._logger.debug('Skipping %s invalid rows: %s' % (
            len(skipped_data),
            skipped_data
        ))

        data = data[(
            data[REPEATER_CALL].notnull()
            & data[REPEATER_LATITUDE].notnull()
            & data[REPEATER_LONGITUDE].notnull()
        )]

        return (IterableDataFrame(data), IterableDataFrame(skipped_data))


class IterableDataFrame:
    """
        Decorator for a Pandas DataFrame making it more practically iterable
        (i.e., not using iterrows()).
    """
    data = None

    def __init__(self, pandasDataframe):
        self.data = pandasDataframe

    def __iter__(self):
        for row in self.data.iterrows():
            yield row[1]

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)

    def __str__(self):
        return str(self.data)
