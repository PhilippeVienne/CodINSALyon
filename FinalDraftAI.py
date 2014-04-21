import sys
from base_ai import BaseAI
from RandomBomb import RandomBomb
import logging

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


class AttackManager(object):
    def __init__(self, base_ai):
        self.base_ai = base_ai
        self.plane_ids = set()
    def assign(self, plane):
        self.plane_ids.add(plane.id)

    def release(self, plane):
        self.plane_ids.remove(plane.id)

class FinalDraftAI(BaseAI):
    destinations = {}
    initialized = False

    def __init__(self, ip, port):
        super(BaseAI, self).__init__(ip, port)
        self.expansion_manager = ExpansionManagement(self)
        self.supply_manager = SupplyManagement(self)
        self.build_plane_manager = BuildPlaneManagement(self)
        self.attack_manager = AttackManager(self)
        self.random_bomb = RandomBomb(self)
        self.managers = [self.supply_manager, self.build_plane_manager, self.expansion_manager, self.random_bomb]
        self.my_production_line = []
        self.my_planes = {}
        self.toggle = 1

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

    def try_build_plane(self):
        if self.my_production_line:
            self.game.sendCommand(BuildPlaneCommand(self.my_production_line.pop()))
        else:
            self.toggle = 1
            if self.toggle:
                self.build_plane_manager.create(Plane.Type.COMMERCIAL, self.expansion_manager)
            else:
                self.build_plane_manager.create(Plane.Type.MILITARY, self.attack_manager)

    def move(self):
        pass

if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    ai = FinalDraftAI(sys.argv[1], int(sys.argv[2]))
    while True:
        try:
            ai.think()
        except Exception as e:
            logging.exception(e)
            raise e
