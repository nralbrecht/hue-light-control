from phue import Bridge


class HueLight:
    def __init__(self, bridge: Bridge, name: str) -> None:
        self.bridge = bridge
        self.light_id = int(bridge.get_light_id_by_name(name))
        self.light = bridge.get_light_objects("id")[self.light_id]


    def getPower(self):
        return self.light.on
    def setPower(self, enable: bool):
        self.light.on = enable


    def getBrightness(self):
        return self.light.brightness

    def setBrightness(self, value: int):
        self.light.brightness = value


    def getColor(self):
        return self.light.colortemp_k

    def setColor(self, value: int):
        self.light.colortemp_k = value
