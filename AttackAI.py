import sys
from base_ai import BaseAI
import random

from command import MoveCommand
from command import LandCommand
from command import ExchangeResourcesCommand
from command import DropMilitarsCommand
from model import Base
from model import Coord
from model import Plane
from random import choice
from path import get_path
from path import distance
from path import is_near
from metier import load_unit, conquer
from model.Plane import Type as PlaneType
from model.Plane import State

class AttackAI(BaseAI):
    initialized = False

    def think(self):
        while True:
            self.game.updateSimFrame()
            self.save_snapshot()
            if not self.initialized:
                self.init()
            self.detect_attack()
            if self.need_help_queue:
                self.reject_attack()
            else:
                self.try_build_plane(PlaneType.COMMERCIAL)
                if self.all_bases:
                    for plane in self.my_planes.values():
                        if plane.state() == State.AT_AIRPORT:
                            random_base = random.choice(self.all_bases.values())
                            self.game.sendCommand(
                                ExchangeResourcesCommand(plane, plane.type.holdCapacity, plane.type.tankCapacity, False))
                            self.game.sendCommand(
                                MoveCommand(plane, random_base.position()))
                            self.game.sendCommand(
                                LandCommand(plane, random_base))
                            self.game.sendCommand(
                                ExchangeResourcesCommand(plane, -plane.type.holdCapacity, 0, False))


    def init(self):
        """
        Initialize the AI.
        """
        self.need_help_queue = []
        self.initialized = True



    def detect_attack(self):
        for my_base in self.my_bases.values():
            for axe in my_base.axes():
                if axe.next().ownerId() != 0 and axe.next().ownerId() != self.country.ownerId():
                    his_base = self.all_bases[axe.next().id()]
                    print "DANGER!!!"
                    for axxe in his_base.axes():
                        if axxe.next().ownerId() == 0 or axxe.next().ownerId() == self.country.ownerId():
                            attack_id = axxe.next().id()
                            if attack_id not in self.need_help_queue:
                                self.need_help_queue.append(attack_id)
                                self.try_build_plane(PlaneType.MILITARY)


    def reject_attack(self):
        for plane in self.my_planes.values():
            if plane.state() == State.AT_AIRPORT:
                if plane.curBase().position() == self.country.position():
                    if self.need_help_queue:
                        # the plane is ready to be sent for help
                        node_id = self.need_help_queue.pop(0)
                        distance = plane.position().distanceTo(self.all_bases[node_id].position())
                        fuel = plane.type.fuelConsumptionPerDistanceUnit * distance
                        fuel *= 1.1
                        if fuel < plane.type.tankCapacity:
                            fq = plane.type.tankCapacity
                            mq = plane.type.holdCapacity

                            self.game.sendCommand(
                                ExchangeResourcesCommand(plane, mq, fq, False))
                            self.game.sendCommand(
                                MoveCommand(plane, self.all_bases[node_id].position()))
                            self.game.sendCommand(
                                LandCommand(plane, self.all_bases[node_id]))
                            self.game.sendCommand(
                                ExchangeResourcesCommand(plane, -mq, 0, False))
                        else:
                            self.try_build_plane(PlaneType.COMMERCIAL)
                else:
                    self.game.sendCommand(
                        MoveCommand(plane, self.country.position()))
                    self.game.sendCommand(
                        LandCommand(plane, self.country))



if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    ai = AttackAI(sys.argv[1], int(sys.argv[2]))
    ai.think()