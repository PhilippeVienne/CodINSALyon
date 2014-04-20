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
from metier import need_democracy
from metier import bring_democracy
from metier import conquer
import context

class LoLAI(BaseAI):
    def think(self):
        while True:
            self.game.updateSimFrame()
            self.save_snapshot()
            self.move()

    def move(self):
        ls_bases = self.all_bases.values()
        fuel_rate = 0.31
        for p in self.my_planes.values():
            if is_near(p.position(), self.country.position(), 0.8) and \
                    need_democracy(p, fuel_rate):
                load_unit(self.game, p, self.country, fuel_rate)
            else:
                bring_democracy(self.game, p, ls_bases, fuel_rate)
                # conquer(self.game, p, ls_bases, fuel_rate)

if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    ai = LoLAI(sys.argv[1], int(sys.argv[2]))
    ai.think()

