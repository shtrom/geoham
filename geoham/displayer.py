import folium
import folium.plugins

import math

from . import parser
from .loggable_trait import LoggableTrait

class Displayer:
    def display(self, data):
        for line in self.render(data):
            print(line)

    def render(self, data):
        yield('callsign input   output  latitude    longitude')
        for row in data:
            if len(row[parser.REPEATER_CALL]) < 1:
                continue
            yield('%s   %s  %s  %s  %s' % (
                  row[parser.REPEATER_CALL],
                  row[parser.REPEATER_INPUT],
                  row[parser.REPEATER_OUTPUT],
                  row[parser.REPEATER_LATITUDE],
                  row[parser.REPEATER_LONGITUDE],
                  ))

class LeafletDisplayer(Displayer,LoggableTrait):
    def __init__(self):
        Displayer.__init__(self)
        self.init_logger(__name__)

    def display(self, data):
        m = folium.Map()
        g = folium.FeatureGroup(name='Repeaters')
        c = folium.plugins.MarkerCluster()
        self.render(c, data)
        g.add_child(c)
        m.add_child(g)
        return m

    def render(self, map, data):
        for row in data:
            if len(row[parser.REPEATER_CALL]) < 1:
                continue

            html = ''

            if isdefined(row[parser.REPEATER_MNEMONIC]):
                html = '''<b>{mNemonic} ({Call})</b>'''.format(**row)
            else:
                html = '''<b>{Call}</b>'''.format(**row)

            if isdefined(row[parser.REPEATER_LOCATION]):
                if isdefined(row[parser.REPEATER_SERVICE_AREA]):
                    html += '''<br>Location: {Location} ({Service Area})'''.format(**row)
                else:
                html += '''<br>Location: {Location}'''.format(**row)

            html+='''<br>Out: {Output} MHz / In: {Input} MHz'''.format(**row)

            if isdefined(row[parser.REPEATER_TONE]):
                html += '''<br>Tone: {Tone} kHz'''.format(**row)

            # TODO: need html encoding

            folium.Marker(
                [row[parser.REPEATER_LATITUDE], row[parser.REPEATER_LONGITUDE]],
                popup=html
            ).add_to(map)

        return map

def isdefined(value):
  return value is not None and \
         not (isinstance(value, float) and math.isnan(value))
