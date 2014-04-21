from model import Plane
from command import ExchangeResourcesCommand, DropMilitarsCommand
from model.Base import FullView
from random import random

class RandomBomb:
    WAITING = 1
    LOADING = 3
    ATTACKING = 2

    def __init__(self, base_ai):
        self.planes_id = set()
        self.base_ai = base_ai
        self.states = {}
        self.targets = []

    def assign(self, plane):
        self.planes_id.add(plane.id())

    def release(self, plane):
        return self.planes_id.remove(plane.id())

    def think(self):
        self.register_targets()
        self.bomb()
        remove = set()
        for key in self.planes_id:
            if key not in self.base_ai.my_planes:
                remove.add(key)
            else:
                self.manage(self.base_ai.my_planes[key])
        self.planes_id -= remove

    def bomb(self):
        if (random() * 10 % 10) > 5:
            print "\n\n===========================\n\nBombing!"
            self.base_ai.build_plane_manager.create(Plane.Type.COMMERCIAL, self)

    def manage(self, plane):
        if self.states[plane.id()] == self.WAITING and self.targets:
            self.load(plane)
            self.launch(plane)

    def load(self, plane):
        self.base_ai.game.sendCommand(ExchangeResourcesCommand(plane, 99.7, 0.0, False))
        self.states[plane.id()] = self.LOADING

    def launch(self, plane):
        self.base_ai.game.sendCommand(DropMilitarsCommand(self.targets.pop(), plane, 99.0))
        self.states[plane.id()] = self.ATTACKING

    def register_targets(self):
        for b in filter(self.base_ai.all_bases, lambda i: i.ownerId() == self.country.ownerId()):
            if isinstance(FullView, b) and b.militaryGarrison <= 100:
                self.targets.append(b)