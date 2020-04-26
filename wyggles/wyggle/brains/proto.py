from wyggles.wyggle.brain import WyggleBrain
from botsley.run import *

class See(Sensor):
    async def main(self, msg):
        while True:
            beacons = sprite_engine.query(self.x, self.y, self.sensor_range)

class SeesFood(Condition):
    async def main(self, msg):
        while True:
            beacons = sprite_engine.query(self.x, self.y, self.sensor_range)

class ProtoBrain(WyggleBrain):
    def __init__(self, model):
        super().__init__(model)
        with root() as root:
            with sensor(See):
            with selector():
                with condition(SeesFood) as sees:
                    with sequence():
                        with action(MoveTo, sees.position):
                with action() as a:
                    async def fn(task, msg):
                        print('b count: ', q.count)
                    a.use(fn)

        self.tree = root
