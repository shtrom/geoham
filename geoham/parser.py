import csv

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

class Parser:
    def parse(self, file):
        reader = csv.DictReader(file)

        return list(reader)
