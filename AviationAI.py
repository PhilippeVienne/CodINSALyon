import sys
from model import Plane
from model.Plane import Type

from base_ai import BaseAI
from command import BuildPlaneCommand


class AviationAI(BaseAI):
    destinations = {}
    def think(self):
        while True:
            self.game.updateSimFrame()
            self.save_snapshot()
            self.create_planes()
    def create_planes(self):
        if len(self.my_production_line.values())==0:
            self.toggle ^= 1
            # what type of plane to build?
            my_type = [Type.COMMERCIAL, Type.MILITARY][self.toggle]
            command = BuildPlaneCommand(my_type)
            self.game.sendCommand(command)
        else:
            print self.my_production_line.values()[0]

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
