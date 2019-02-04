import csv
import pandas as pd
import numpy as np
import logging

from .loggable_trait import LoggableTrait

from . import chirp

REPEATER_OUTPUT = 'Output'
REPEATER_INPUT = 'Input'
REPEATER_CALL = 'Call'
REPEATER_MNEMONIC = 'mNemonic'
REPEATER_LOCATION = 'Location'
REPEATER_SERVICE_AREA = 'Service Area'
REPEATER_LATITUDE = 'Latitude'
REPEATER_LONGITUDE = 'Longitude'
REPEATER_STATUS = 'Status'
REPEATER_ERP = 'ERP'
REPEATER_HASL = 'HASL'
REPEATER_TO = 'T/O'
REPEATER_SPONSOR = 'Sponsor'
REPEATER_TONE = 'Tone'
REPEATER_NOTES = 'Notes'

# Calculated fields
REPEATER_BAND = 'Band'
REPEATER_DUPLEX = 'Duplex'
REPEATER_OFFSET = 'Offset'

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

FIELD_MAPPING = {
    REPEATER_OUTPUT: chirp.FREQ,
    REPEATER_INPUT: None,
    REPEATER_CALL: chirp.NAME,
    REPEATER_MNEMONIC: chirp.COMMENT,
    REPEATER_LOCATION: chirp.COMMENT,
    REPEATER_SERVICE_AREA: chirp.COMMENT,
    REPEATER_LATITUDE: chirp.COMMENT,
    REPEATER_LONGITUDE: chirp.COMMENT,
    REPEATER_STATUS: chirp.COMMENT,
    REPEATER_ERP: chirp.COMMENT,
    REPEATER_HASL: chirp.COMMENT,
    REPEATER_TO: chirp.COMMENT,
    REPEATER_SPONSOR: chirp.COMMENT,
    REPEATER_TONE: chirp.TONE,
    REPEATER_NOTES: chirp.COMMENT,

    # Calculated fields
    REPEATER_DUPLEX: chirp.OFFSET,
    REPEATER_OFFSET: chirp.OFFSET,
}

NA_FIELDS = ['-', 'Various', '?']

NUM_FIELDS = [k for k in FIELD_TYPES.keys() if FIELD_TYPES[k] == np.float64]


class Parser(LoggableTrait):
    band_service = None

    def __init__(self):
        self.init_logger(__name__)
        self.band_service = BandService()
        self.chirp_mapping = chirp.Mapping(FIELD_MAPPING)

    def parse(self, file):
        data = pd.read_csv(file,
                           names=FIELD_TYPES.keys(),
                           dtype=FIELD_TYPES,
                           na_values=NA_FIELDS,
                           header=0,
                           usecols=(list(range(len(FIELD_TYPES)))),
                           error_bad_lines=False,  # XXX: This will drop rows with too many notes
                           warn_bad_lines=self._logger.isEnabledFor(
                               logging.WARNING)
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

        data[REPEATER_BAND] = self.band_service.band_from_frequency_series(
            data[REPEATER_OUTPUT])

        offsets = round(data[REPEATER_INPUT] - data[REPEATER_OUTPUT], 3)
        # '-' if offsets < 0 else '+'
        data[REPEATER_DUPLEX] = abs(offsets)/offsets
        data[REPEATER_OFFSET] = abs(offsets)

        return self.chirp_mapping.remap(data), skipped_data


class BandService:
    # Band name to lower-ish frequency [MHz] mapping
    BANDS = {
        '160m': 1.8,
        '80m': 3.5,
        '40m': 7,
        '30m': 10,
        '20m': 14,
        '17m': 18,
        '15m': 21,
        '12m': 24,
        '10m': 28,
        '6m': 50,
        '2m': 144,
        '1.25m': 222,
        '70cm': 429,
        '33cm': 902,
        '23cm': 1240,
        '13cm': 2300,
    }

    def band_from_frequency_series(self, f):
        return f.apply(self.band_from_frequency)

    def band_from_frequency(self, f):
        '''
            >>> b = BandService()
            >>> b.band_from_frequency(145)
            '2m'
        '''
        for b in self.BANDS.keys():
            if (f // self.BANDS[b]) == 1.0:
                return b
        return "%fMHz" % f
