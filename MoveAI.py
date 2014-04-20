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
from metier import load_unit

class MoveAI(BaseAI):
    destinations = {}
    initialized = False
    help_needed = []

    def think(self):
        while True:
            self.game.updateSimFrame()
            self.save_snapshot()
            if not self.initialized:
                self.init()
            self.detect_attack()
            self.move()


    def init(self):
        """
        Initialize the AI.
        """
        self.visited = dict([(b, False) for b in self.all_bases])

    def move(self):
        potential_bases = dict(filter(lambda (_, l): not l.isFriend(self.country),
                self.visible_bases.items()))
        potential_bases.update(dict(filter(lambda (i, _): not self.visited[i],
            self.all_bases.items())))
        print filter(lambda (i, _): not self.visited[i],
            self.all_bases.items())

        for b in self.visible_bases.keys():
            self.visited[b] = True

        for p in self.my_planes.values():
            if is_near(p.position(), self.country.position(), 0.8) and \
                    p.militaryInHold() < p.type.holdCapacity / 2.0:
                load_unit(self.game, p, self.country)
            else:
                res = get_path(p, potential_bases.values(), None, 1)
                if res:
                    if not is_near(p.position(), res[0].position(), 0.3):
                        print 'move'
                        self.game.sendCommand(
                                DropMilitarsCommand(p, res[0], 6))
                    else:
                        print 'drop', distance(p.position(), res[0].position())
                        self.game.sendCommand(
                                DropMilitarsCommand(p, res[0], 6))
            print len(potential_bases)

    def detect_attack(self):
        for neigh_base in self.not_owned_and_visible_bases.values():
            for axe in neigh_base.axes():
                if axe.next() in self.my_bases.values():
                    print "DANGER!!!"
                    help_needed.append(axe.next().id)

if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    ai = MoveAI(sys.argv[1], int(sys.argv[2]))
    ai.think()
