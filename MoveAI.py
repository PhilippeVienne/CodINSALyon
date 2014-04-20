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
from model.Base import FullView
from random import choice
from path import get_path
from path import distance
from path import is_near
from metier import load_unit
from metier import conquer

class MoveAI(BaseAI):
    destinations = {}
    initialized = False

    def think(self):
        while True:
            self.game.updateSimFrame()
            self.save_snapshot()
            if not self.initialized:
                self.init()
            self.move()

    def init(self):
        """
        Initialize the AI.
        """
        self.visited = dict([(b, False) for b in self.all_bases])

    def move(self):
        for b in self.visible_bases:
            self.visited[b] = True

        potential_bases = {}
        for k, l in self.visible_bases.items():
            # if l.ownerId() != self.country.ownerId():
            if not l.id() in self.my_bases:
                potential_bases[k] = self.all_bases[k]
        for k, l in self.all_bases.items():
            if not self.visited[k] and not k in potential_bases:
                potential_bases[k] = l

        ls_bases = potential_bases.values()
        for p in self.my_planes.values():
            if is_near(p.position(), self.country.position(), 0.8) and \
                    p.militaryInHold() < p.type.holdCapacity / 2.0:
                load_unit(self.game, p, self.country)
            else:
                conquer(game, p, ls_bases, nb_drop=2)

if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    ai = MoveAI(sys.argv[1], int(sys.argv[2]))
    ai.think()
