import sys
from base_ai import BaseAI

from command import MoveCommand
from command import LandCommand
from command import BuildPlaneCommand
from command import ExchangeResourcesCommand
from command import DropMilitarsCommand
from command import ExchangeResourcesCommand
from model import Base
from model import Coord
from model import Plane
from model.Base import FullView
from random import choice
from build_plane_managment import BuildPlaneManagement
from expansion_management import ExpansionManagement
from path import get_path
from path import distance
from path import is_near
from metier import load_unit
from supply_management import SupplyManagement


class MoveAI(BaseAI):
    destinations = {}
    initialized = False

    def __init__(self, ip, port):
        super(BaseAI, self).__init__(ip, port)
        self.managers = [SupplyManagement(self), BuildPlaneManagement(self), ExpansionManagement(self)]
        self.manager_building = self.managers[0]
        self.my_production_line = []

    def think(self):
        while True:
            self.game.updateSimFrame()
            self.save_snapshot()
            if not self.initialized:
                self.init()
            self.move()
            for manager in self.managers:
                manager.think()
            self.try_build_plane()
    def init(self):
        """
        Initialize the AI.
        """
        self.visited = dict([(b, False) for b in self.all_bases])


    def try_build_plane(self, plane_type=None):
        if len(self.my_production_line) < 1:
            self.toggle ^= 1
            # what type of plane to build?
            if not plane_type:
                plane_type = [Plane.Type.COMMERCIAL, Plane.Type.MILITARY][self.toggle]
            self.game.sendCommand(BuildPlaneCommand(plane_type))


    def move(self):
        for b in self.visible_bases:
            self.visited[b] = True

        potential_bases = {}
        for k, l in self.visible_bases.items():
            print '#############', l.id(), l.ownerId(), self.country.ownerId()
            # if l.ownerId() != self.country.ownerId():
            # if not isinstance(self.all_bases[l.id()], FullView):
            if not l.id() in self.my_bases:
                potential_bases[k] = self.all_bases[k]
        for k, l in self.all_bases.items():
            if not self.visited[k] and not k in potential_bases:
                potential_bases[k] = l

        for k in potential_bases:
            print k,
        print

        # print potential_bases

        ls_bases = potential_bases.values()
        for p in self.my_planes.values():
            if is_near(p.position(), self.country.position(), 0.8) and \
                            p.militaryInHold() < p.type.holdCapacity / 2.0:
                load_unit(self.game, p, self.country)
            else:
                res = get_path(p, ls_bases, None, 1)
                if res:
                    if not is_near(p.position(), res[0].position(), 0.3):
                        print 'move', p.id(), res[0].id()
                        self.game.sendCommand(
                            DropMilitarsCommand(p, res[0], 1))
                    else:
                        print 'drop', p.id(), res[0].id()
                        self.game.sendCommand(
                            DropMilitarsCommand(p, res[0], 1))
            print len(potential_bases)

if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    ai = MoveAI(sys.argv[1], int(sys.argv[2]))
    ai.think()
