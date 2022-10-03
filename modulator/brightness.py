import json
import asyncio
from hue_light import HueLight
from hue_light_sensor import HueLightSensor


with open("config.json", "r") as c:
    config = json.load(c)

TARGET_BRIGHTNESS = config["brightness"]["target_brightness"]
BRIGHTNESS_TOLERANCE = config["brightness"]["brightness_tolerance"]
TIMESTEP = config["brightness"]["timestep"]
TIMESTEP_IDLE = config["brightness"]["timestep_idle"]
MIN_BRIGHTNESS = config["brightness"]["min_brightness"]
MAX_BRIGHTNESS = config["brightness"]["max_brightness"]
INITIAL_BRIGHTNESS = config["brightness"]["initial_brightness"]
BATTERY_WARN_THRESHOLD = config["battery_warn_threshold"]


class HueBrightnessModulator:
    def __init__(self, sensor: HueLightSensor, light: HueLight) -> None:
        self.sensor = sensor
        self.light = light

        self.last_light_level = None
        self.should_run = True

    def getNextBrightness(self):
        light_level = self.sensor.getLightLevel()

        if light_level == self.last_light_level:
            return False, None
        self.last_light_level = light_level

        brightness_difference = TARGET_BRIGHTNESS - light_level

        if abs(brightness_difference) < BRIGHTNESS_TOLERANCE:
            return True, None

        if brightness_difference > 0:
            return False, max(MIN_BRIGHTNESS, min(self.light.getBrightness() + 10, MAX_BRIGHTNESS))
        elif brightness_difference < 0:
            return False, max(MIN_BRIGHTNESS, min(self.light.getBrightness() - 10, MAX_BRIGHTNESS))

        return True, None

    async def run(self):
        try:
            # Setup
            print("starting brightness control")

            self.sensor.setLED(True)

            await asyncio.sleep(TIMESTEP * 2)

            # Core loop
            self.light.setBrightness(INITIAL_BRIGHTNESS)

            while self.should_run:
                battery = self.sensor.getBattery()
                idle, brightness = self.getNextBrightness()
                # print("self.getNextBrightness()", idle, brightness)


                if battery < BATTERY_WARN_THRESHOLD:
                    print("ALARM!111!11! Baterie is bei " + str(battery) + "%")

                if brightness:
                    # if self.sensor.getLightLevel() < TARGET_BRIGHTNESS * 2:
                    #     if self.light.getPower():
                    #         self.light.setBrightness(0)
                    #         self.light.setPower(False)
                    # else:
                    print("sensor:", self.sensor.getLightLevel(), "next_brightness:", brightness, "last_brightness:", self.light.getBrightness(), "target:", TARGET_BRIGHTNESS, "battery:", str(battery))

                    self.light.setBrightness(brightness)
                    if not self.light.getPower():
                        self.light.setPower(True)

                    # print("1 waiting for", TIMESTEP)
                    await asyncio.sleep(TIMESTEP)

                elif not idle:
                    # print("2 waiting for", TIMESTEP)
                    await asyncio.sleep(TIMESTEP)

                else:
                    # print("3 waiting for", TIMESTEP_IDLE)
                    await asyncio.sleep(TIMESTEP_IDLE)

        except KeyboardInterrupt:
            pass
        finally:
            self.sensor.setPower(False)
            self.sensor.setLED(False)
            print("stopping brightness control")
