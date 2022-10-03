import json
import asyncio
from phue import Bridge
from hue_light import HueLight
from hue_light_sensor import HueLightSensor
from modulator.brightness import HueBrightnessModulator
from modulator.temperature import HueTemperatureModulator


with open("config.json", "r") as c:
    config = json.load(c)


bridge = Bridge(config["bridge_ip"])
bridge.connect()

sensor = HueLightSensor(bridge, "Hue ambient light sensor 1")
sensor.setPower(True)

light = HueLight(bridge, "Hue ambiance panel 1")
light.setPower(True)

temperature = HueTemperatureModulator(light)
temperature_task = temperature.run()

brightness = HueBrightnessModulator(sensor, light)
brightness_task = brightness.run()

asyncio.run(asyncio.wait([ brightness_task, temperature_task ]))
