import sys
from base_ai import BaseAI

from command import MoveCommand
from command import LandCommand
from command import ExchangeResourcesCommand
from command import DropMilitarsCommand
from command import ExchangeResourcesCommand
from model import Base
from model import Coord
from model import Plane
from random import choice
from path import get_path
from path import distance
from path import is_near
from metier import loadUnit

class MoveAI(BaseAI):
    destinations = {}
    def think(self):
        while True:
            self.game.updateSimFrame()
            self.save_snapshot()
            self.try_build_plane()
            self.detect_attack()
            self.move()
    def move(self):
        all_bases = filter(lambda l: not l.isFriend(self.country),
                self.all_bases.values())
        for p in self.my_planes.values():
            if p.militaryInHold() < p.type.holdCapacity / 2.0:
                loadUnit(self.game, p, self.country)
            else:
                res = get_path(p, all_bases, None, 1)
                if res:
                    if distance(p.position(), res[0].position()) >= 0.5:
                        print 'move'
                        self.game.sendCommand(
                                DropMilitarsCommand(p, res[0], 6))
                    else:
                        print 'drop', distance(p.position(), res[0].position())
                        self.game.sendCommand(
                                DropMilitarsCommand(p, res[0], 6))
            print len(all_bases)

    def detect_attack(self):
        for neigh_base in self.not_owned_and_visible_bases.values():
            for axe in neigh_base.axes():
                if axe.next() in self.my_bases.values():
                    print "DANGER!!!"
                    print axe.next

if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    ai = MoveAI(sys.argv[1], int(sys.argv[2]))
    ai.think()
