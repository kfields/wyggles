from botsley.run.behavior import *

from wyggles.engine import *

class See(Sensor):
    async def main(self, msg):
        while True:
            beacons = sprite_engine.query(self.x, self.y, self.sensor_range)