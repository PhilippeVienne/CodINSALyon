import sys
from base_ai import BaseAI
from pprint import pprint
from model.Plane import State

from command import MoveCommand

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

            print self.my_planes
            print [p.state() for _, p in self.my_planes.iteritems()]
            for p_id, plane in self.my_planes.iteritems():
                if plane.state() == State.AT_AIRPORT:
                    try:
                        valid_bases = [b for b in self.all_bases.values() if b.position() != plane.position()]
                        closest_base = min(valid_bases, key=lambda b : b.position().distanceTo(plane.position()))
                        move_cmd = MoveCommand(plane, closest_base.position())
                        self.game.sendCommand(move_cmd)
                    except ValueError:
                        continue
                print 'lol', plane
                #if plane.fuelInHold

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
