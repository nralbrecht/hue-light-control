import numpy
import colour
from PIL import ImageGrab


class MonitorColorHelper:
    def get_temperature(self):
        self._update_screen_shot()
        self._update_average_color()
        self._update_color_temperature()

        return self.color_temperature

    def _update_screen_shot(self):
        self.image = ImageGrab.grab()
        self.image = self.image.resize((10, 10))

    def _update_average_color(self):
        width, height = self.image.size

        r_total = 0
        g_total = 0
        b_total = 0

        count = 0
        for x in range(0, width):
            for y in range(0, height):
                r, g, b = self.image.getpixel((x,y))
                r_total += r
                g_total += g
                b_total += b
                count += 1

        self.average_color = (r_total/count, g_total/count, b_total/count)

    def _update_color_temperature(self):
        # Assuming sRGB encoded colour values.

        # Conversion to tristimulus values.
        print(numpy.array(self.average_color) / 255)
        XYZ = colour.sRGB_to_XYZ(numpy.array(self.average_color) / 255)

        # Conversion to chromaticity coordinates.
        xy = colour.XYZ_to_xy(XYZ)

        # Conversion to correlated colour temperature in K.
        self.color_temperature = colour.xy_to_CCT(xy, 'hernandez1999')
