import folium

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
        self.render(m, data)
        print(m)

    def render(self, map, data):
        for row in data:
            if len(row[parser.REPEATER_CALL]) < 1:
                continue

            folium.Marker(
                [row[parser.REPEATER_LATITUDE], row[parser.REPEATER_LONGITUDE]],
                popup=(
                    '%s\nIn: %sOut: %s' % (
                        row[parser.REPEATER_CALL],
                        row[parser.REPEATER_INPUT],
                        row[parser.REPEATER_OUTPUT],
                    ))
            ).add_to(map)

        return map
