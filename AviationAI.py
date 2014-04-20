import sys

from model.Plane import Type
import random
from base_ai import BaseAI
from command import BuildPlaneCommand, MoveCommand, LandCommand


class AviationAI(BaseAI):
    destinations = {}

    def think(self):
        while True:
            self.game.updateSimFrame()
            self.save_snapshot()
            self.create_planes()
            self.save_planes()

    def create_planes(self):
        if len(self.my_production_line.values()) == 0:
            self.toggle ^= 1
            # what type of plane to build?
            my_type = [Type.COMMERCIAL, Type.MILITARY][self.toggle]
            command = BuildPlaneCommand(my_type)
            self.game.sendCommand(command)

    def nearest_base(self, plane):
        safe_base = random.choice(self.all_bases.values())
        for base in self.all_bases.values():
            if plane.position().squareDistanceTo(base.position()) < safe_base.position().squareDistanceTo(plane.position()):
                safe_base = base
        return safe_base

    def save_planes(self):
        for plane in self.my_planes.values():
            print(plane)
            print(plane.fuelInTank() < 0.5 * plane.type.tankCapacity)
            if plane.fuelInTank() < 0.5 * plane.type.tankCapacity:
                safe_base = self.nearest_base(plane)
                print(safe_base)
                self.game.sendCommand(MoveCommand(plane,safe_base.position()))
                self.game.sendCommand(LandCommand(plane,safe_base))


if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    from org.apache.log4j import PropertyConfigurator

    PropertyConfigurator.configure('log4j.properties')
    print 'Hello'
    ai = AviationAI(sys.argv[1], int(sys.argv[2]))
    print 'Toto'
    ai.think()
