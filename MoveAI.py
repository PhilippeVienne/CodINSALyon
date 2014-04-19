import sys
from base_ai import BaseAI

from command import MoveCommand
from model import Base
from model import Coord
from random import choice

class MoveAI(BaseAI):
    def think(self):
        while True:
            self.game.updateSimFrame()
            self.save_snapshot()
            self.move()
    def move(self):
        b = choice(self.all_bases.values())
        planes = self.game.getMyPlanes()
        for p in planes.valuesView():
            self.game.sendCommand(MoveCommand(p, b.position()))

if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    ai = MoveAI(sys.argv[1], int(sys.argv[2]))
    ai.think()
