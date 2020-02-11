import pandas as pd

# Columns from Chirp's CSV output
IDX	        = 'Location'
NAME	        = 'Name'
FREQ	        = 'Frequency'
DUPLEX	        = 'Duplex'
OFFSET	        = 'Offset'
TONE	        = 'Tone'
R_TONE_FREQ	= 'rToneFreq'
C_TONE_FREQ	= 'cToneFreq'
DTCS_CODE	= 'DtcsCode'
DTCS_POL	= 'DtcsPolarity'
MODE	        = 'Mode'
TSTEP	        = 'TStep'
SKIP	        = 'Skip'
COMMENT	        = 'Comment'
URCALL	        = 'URCALL'
RPT1CALL	= 'RPT1CALL'
RPT2CALL	= 'RPT2CALL'
DVCODE	        = 'DVCODE'

DUPLEX_MINUS	= '-'
DUPLEX_NONE	= ''
DUPLEX_PLUS	= '+'
DUPLEX_SPLIT	= 'split'
DUPLEX_OFF	= 'off'

TONE_CROSS      = 'Cross'
TONE_DISABLE	= ''
TONE_DTCS	= 'DTCS'
TONE_ENABLE	= 'Tone'
TONE_TSQL	= 'TSQL'

DTCS_POL_NN	= 'NN'
DTCS_POL_NR	= 'NR'
DTCS_POL_RN	= 'RN'
DTCS_POL_RR	= 'RR'

MODE_AM	        = 'AM'
MODE_DV	        = 'DV'
MODE_FM	        = 'FM'
MODE_NFM	= 'NFM'
MODE_WFM	= 'WFM'

SKIP_PRIO       = "P"
SKIP_SKIP       = "S"

class Mapping:
    CHIRP_FIELDS = [
        IDX,
        NAME,
        FREQ,
        DUPLEX,
        OFFSET,
        TONE,
        R_TONE_FREQ,
        C_TONE_FREQ,
        DTCS_CODE,
        DTCS_POL,
        MODE,
        TSTEP,
        SKIP,
        COMMENT,
        URCALL,
        RPT1CALL,
        RPT2CALL,
        DVCODE,
    ]

    def __init__(self, mapping):
        '''
        Initialise a mapping of input data field to Chirp-formatted output data.

        Args:
            mapping ({str: str, ...}): a dictionary keyed to input data fields with Chirp-data values.
        '''
        self.mapping = mapping

    def remap(self, df):
        '''
        Remap the colums of input data to Chirp-formatted output data.

        If multiple columns map to the same Chirp-column, they will be concatenated into that column.

        Args:
            df (pd.DataFrame)

        Returns:
            pd.DataFrame
        '''
        return df.rename(self.mapping, inplace=True)

        out_columns = {}
        for k in df.keys():
            if k in self.mapping.keys:
                chirp_field = self.mapping[k]
                if chirp_field is not None:
                    out_columns[chirp_field] = self._array_new_append(k,
                                                                  out_columns[chirp_field])
        out = pd.dataframe()
        for k in out_columns.keys():
            for k2 in out_columns[k]:
                out[k]

        return out

        def _array_new_append(self, v, a):
            ''' Add value v to array a, or create a new array '''
            if a is None:
                return [v]
            else:
                a.append(v)
                return v
