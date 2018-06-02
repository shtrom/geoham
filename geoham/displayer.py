import folium
import folium.plugins

import html
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
    colors = [
            'red',
            'blue',
            'gray',
            'darkred',
            'lightred',
            'orange',
            'beige',
            'green',
            'darkgreen',
            'lightgreen',
            'darkblue',
            'lightblue',
            'purple',
            'darkpurple',
            'pink',
            'cadetblue',
            'lightgray',
            'black'
    ]

    def __init__(self):
        Displayer.__init__(self)
        self.init_logger(__name__)

    def display(self, data):
        m = folium.Map()

        band_group = data.groupby(parser.REPEATER_BAND)
        c = folium.plugins.MarkerCluster(control=False)
        groups = band_group.apply(self.render_group, m, c)

        m.add_child(c)
        for sg in groups:
            m.add_child(sg)

        m.fit_bounds([
            [ min(data[parser.REPEATER_LATITUDE]), min(data[parser.REPEATER_LONGITUDE])],
            [ max(data[parser.REPEATER_LATITUDE]), max(data[parser.REPEATER_LONGITUDE])]
        ])

        folium.LayerControl().add_to(m)

        return m

    def render_group(self, data, m, g):
        sg = folium.plugins.FeatureGroupSubGroup(g,
                                                 name=data[parser.REPEATER_BAND].unique()[0])
        self.render(sg, data)

        return sg

    def render(self, m, data):
        for row in data.iterrows():
            row = row[1]
            if len(row[parser.REPEATER_CALL]) < 1:
                continue

            popup_html = ''

            if isdefined(row[parser.REPEATER_MNEMONIC]):
                contents = '''{mNemonic} ({Call})'''.format(**row)
            else:
                contents = '''{Call}'''.format(**row)
            popup_html = '''<b>%s</b>''' % html.escape(contents)

            if isdefined(row[parser.REPEATER_LOCATION]):
                if isdefined(row[parser.REPEATER_SERVICE_AREA]):
                    contents = '''Location: {Location} ({Service Area})'''.format(**row)
                else:
                    contents = '''Location: {Location}'''.format(**row)
                popup_html += '''<br>%s''' % html.escape(contents)

            contents ='''Out: {Output} MHz / In: {Input} MHz ({Offset} MHz)'''.format(**row)
            popup_html += '''<br>%s''' % html.escape(contents)

            if isdefined(row[parser.REPEATER_TONE]):
                contents = '''Tone: {Tone} kHz'''.format(**row)
                popup_html += '''<br>%s''' % html.escape(contents)

            folium.Marker(
                [row[parser.REPEATER_LATITUDE], row[parser.REPEATER_LONGITUDE]],
                popup=popup_html,
                icon=folium.Icon(
                    # color=self.colors[6],
                    # prefix='fa',
                    icon='wifi-alt'
                )
            ).add_to(m)

        return m

def isdefined(value):
  return value is not None and \
         not (isinstance(value, float) and math.isnan(value))
