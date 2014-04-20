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

    def think(self):
        while True:
            self.game.updateSimFrame()
            self.save_snapshot()
            if not self.initialized:
                self.init()
            self.detect_attack()
            self.reject_attack()
            self.move()

    def init(self):
        """
        Initialize the AI.
        """
        self.help_in_queue = []



    def detect_attack(self):
        for neigh_base in self.not_owned_and_visible_bases.values():
            for axe in neigh_base.axes():
                if axe.next() in self.my_bases.values():
                    print "DANGER!!!"
                    self.help_in_queue.append(axe.next().id)
                    self.try_build_plane(PlaneType.MILITARY)


    def reject_attack(self):
        for (p_key, p_value) in self.my_planes:
            if p_key in help_in_queue:
                # the plane is ready to be sent for help
                help_in_queue.remove(p_key)
                mq =
                self.game.sendCommand(
                    ExchangeResourcesCommand(p_value, mq, fq, False))