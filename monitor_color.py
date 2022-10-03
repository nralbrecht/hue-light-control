import numpy
import colour
from PIL import ImageGrab


class MonitorColorHelper:
    def get_temperature(self):
        self._update_screen_shot()
        self._update_color_temperature()

        return self.color_temperature

    def _update_screen_shot(self):
        image = ImageGrab.grab()
        image = image.resize((1, 1))
        # image = image.crop((left, upper, right, lower))
        self.average_color = image.getpixel((0,0))

    def _update_color_temperature(self):
        # Assuming sRGB encoded colour values.

        # Conversion to tristimulus values.
        print(numpy.array(self.average_color) / 255)
        XYZ = colour.sRGB_to_XYZ(numpy.array(self.average_color) / 255)

        # Conversion to chromaticity coordinates.
        xy = colour.XYZ_to_xy(XYZ)

        # Conversion to correlated colour temperature in K.
        self.color_temperature = colour.xy_to_CCT(xy, 'hernandez1999')
