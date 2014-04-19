import sys
from base_ai import BaseAI

from command import MoveCommand
from model import Base
from model import Coord
from random import choice
from path import get_path, distance

class MoveAI(BaseAI):
    destinations = {}
    def think(self):
        while True:
            self.game.updateSimFrame()
            self.save_snapshot()
            self.move()
    def move(self):
        for p in self.my_planes.values():
            res = get_path(p, self.all_bases.values())
            if res:
                self.game.sendCommand(MoveCommand(p, res[0].position()))

if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    ai = MoveAI(sys.argv[1], int(sys.argv[2]))
    ai.think()
