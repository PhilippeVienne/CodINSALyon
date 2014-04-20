import sys
from base_ai import BaseAI
import random

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
from path import evaluation
from metier import load_unit
from metier import need_democracy
from metier import bring_democracy
from metier import conquer
import context

class ExpansionManagement:
    def __init__(self, base_ai):
        self.planes_id = set()
        self.base_ai = base_ai

    def assign(self, plane):
        self.planes_id.add(plane.id())

    def release(self, plane):
        return self.planes_id.remove(plane.id())

    def think(self):
        self.move()

    def move(self):
        ls_bases = self.base_ai.all_bases.values()
        fuel_rate = 0.31
        fuel_rate = 0.0
        next_order = []
        planes = filter(lambda k: k in self.base_ai.my_planes, self.planes_id)
        planes = map(lambda id: self.base_ai.my_planes[id], planes)
        for p in planes:
            if is_near(p.position(), self.base_ai.country.position(), 0.8) and \
                    need_democracy(p, fuel_rate):
                load_unit(self.base_ai.game, p, self.base_ai.country, fuel_rate)
            else:
                next_order += [p]

        mili_plane = filter(lambda p: p.militaryInHold() > 0, next_order)
        rand_plane = filter(lambda p: p.militaryInHold() == 0, next_order)
        rank = {}
        bs = ls_bases[:]
        # random.shuffle(mili_plane)
        # random.shuffle(rand_plane)
        for p in mili_plane:
            bring_democracy(self.base_ai.game, p, ls_bases, fuel_rate)
        for p in rand_plane:
            bring_democracy(self.base_ai.game, p, bs[:], fuel_rate)
