from phue import Bridge


class HueLightSensor:
    def __init__(self, bridge: Bridge, name: str) -> None:
        self.bridge = bridge
        self.sensor_id = int(bridge.get_sensor_id_by_name(name))
        self.sensor = bridge.get_sensor_objects("id")[self.sensor_id]


    def setPower(self, enable: bool):
        self.bridge.set_sensor_config(self.sensor_id, "on", enable)

    def setLED(self, enable: bool):
        self.bridge.set_sensor_config(self.sensor_id, "ledindication", enable)


    def getLightLevel(self):
        return self.sensor.state["lightlevel"]

    def getBattery(self):
        return self.sensor.config["battery"]
