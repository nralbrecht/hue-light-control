import json
import asyncio
from hue_light import HueLight
from monitor_color import MonitorColorHelper


with open("config.json", "r") as c:
    config = json.load(c)

TIMESTEP_COLOR = config["color"]["timestep"]
TIMESTEP_INITIAL_COLOR = config["color"]["timestep_initial"]
INITIAL_COLOR = config["color"]["initial_color"]
MIN_COLOR = config["color"]["min_color"]
MAX_COLOR = config["color"]["max_color"]
BATTERY_WARN_THRESHOLD = config["battery_warn_threshold"]


class HueTemperatureModulator:
    def __init__(self, light: HueLight) -> None:
        self.light = light
        self.monitor_color_helper = MonitorColorHelper()

        self.should_run = True

    def getNextColor(self):
        temperature = self.monitor_color_helper.get_temperature()

        return int(min(MAX_COLOR, max(MIN_COLOR, temperature))), temperature


    async def run(self):
        try:
            # Setup
            print("starting color control")

            await asyncio.sleep(TIMESTEP_INITIAL_COLOR)

            # Core loop
            self.light.setColor(INITIAL_COLOR)

            while self.should_run:
                await asyncio.sleep(TIMESTEP_COLOR)

                color, colorOriginal = self.getNextColor()

                print("color:", self.light.getColor(), "->", color, colorOriginal)

                if self.light.getPower():
                    if color:
                        self.light.setColor(color)
                    else:
                        print("color not defined")
                else:
                    print("cant change color! the lamp is off")

        except KeyboardInterrupt:
            pass
        finally:
            print("stopping color control")

