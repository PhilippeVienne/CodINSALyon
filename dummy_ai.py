import sys
from base_ai import BaseAI
from pprint import pprint


class DummyAI(BaseAI):
    def __init__(self, ip, port):
        super(BaseAI, self).__init__(ip, port)

    def think(self):
        turn = 0
        while True:
            turn += 1
            # print self.game
            self.game.updateSimFrame()
            self.save_snapshot()
            print "# TURN %d : Update received" % turn

            pprint(dir(self.my_planes.values()[0]))
            pprint(dir(self.all_bases.values()[0]))
            print('-' * 80)


    def end(self):
        pass


if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    ai = DummyAI(sys.argv[1], int(sys.argv[2]))
    ai.think()
