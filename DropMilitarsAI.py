import sys
from base_ai import BaseAI

from command import MoveCommand, DropMilitarsCommand
from model import Base
from model import Coord
from random import choice
from path import get_path, distance
from model import Plane

class DropMilitarsAI(BaseAI):
    destinations = {}
    def think(self):
        while True:
            self.game.updateSimFrame()
            self.save_snapshot()
            self.move()
    def move(self):
        bases_to_go_to = filter(lambda b: b.ownerId is not self.country.ownerId, self.all_bases.values())
        print "bases_to_go_to:", bases_to_go_to
        for p in self.my_planes.values():
            print "Plane state:", p.state()
            if p.state() == Plane.State.IDLE or p.state() == Plane.State.AT_AIRPORT:
                print "This plane is idle!"
                res = get_path(p, bases_to_go_to)
                if res:
                    self.game.sendCommand(DropMilitarsCommand(p, res[0], 1))

if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    ai = DropMilitarsAI(sys.argv[1], int(sys.argv[2]))
    ai.think()
