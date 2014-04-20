import sys
from base_ai import BaseAI
from GraphUtils import GraphUtils

from command import MoveCommand, DropMilitarsCommand
from model import Base
from model import Coord
from random import choice
from path import get_path, distance
from model import Plane

class IntelligentStarterAI(BaseAI):
    def think(self):
        while True:
            self.game.updateSimFrame()
            self.save_snapshot()
            self.move()
    def move(self):
        print "------------------------------------------\n" * 3
        bases_scores = sorted([(i, GraphUtils.interconnection_score_from_country(b, self.country, 2)) for i, b in self.all_bases.items()], reverse=True, key=lambda e: e[1])
        print bases_scores

if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    ai = IntelligentStarterAI(sys.argv[1], int(sys.argv[2]))
    ai.think()
