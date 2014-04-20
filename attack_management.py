import sys
from base_ai import BaseAI
import random

from command import MoveCommand
from command import LandCommand
from command import ExchangeResourcesCommand
from model.Plane import Type as PlaneType
from model.Plane import State



class AttackManager(object):

    def __init__(self, base_ai):
        self.base_ai = base_ai
        self.plane_ids = set()
        self.need_help_queue = []

    def assign(self, plane):
        self.plane_ids.add(plane.id)

    def release(self, plane):
        self.plane_ids.remove(plane.id)

    def think(self):
        self.detect_attack()
        if self.need_help_queue:
            self.reject_attack()


    def detect_attack(self):
        for my_base in self.base_ai.my_bases.values():
            for axe in my_base.axes():
                if axe.next().ownerId() != 0 and axe.next().ownerId() != self.base_ai.country.ownerId():
                    his_base = self.base_ai.all_bases[axe.next().id()]
                    for axxe in his_base.axes():
                        if axxe.next().ownerId() == 0 or axxe.next().ownerId() == self.base_ai.country.ownerId():
                            attack_id = axxe.next().id()
                            if attack_id not in self.need_help_queue:
                                self.need_help_queue.append(attack_id)
                                self.base_ai.try_build_plane(PlaneType.MILITARY)


    def reject_attack(self):
        for plane_id in self.plane_ids:
            plane = self.base_ai.my_planes[plane_id]

            if plane.state() == State.AT_AIRPORT:
                if plane.curBase().position() == self.base_ai.country.position():
                    if self.need_help_queue:
                        # the plane is ready to be sent for help
                        node_id = self.need_help_queue.pop(0)
                        distance = plane.position().distanceTo(self.base_ai.all_bases[node_id].position())
                        fuel = plane.type.fuelConsumptionPerDistanceUnit * distance
                        fuel *= 1.1
                        if fuel < plane.type.tankCapacity:
                            fq = plane.type.tankCapacity
                            mq = plane.type.holdCapacity

                            self.base_ai.game.sendCommand(
                                ExchangeResourcesCommand(plane, mq, fq, False))
                            self.base_ai.game.sendCommand(
                                MoveCommand(plane, self.base_ai.all_bases[node_id].position()))
                            self.base_ai.game.sendCommand(
                                LandCommand(plane, self.base_ai.all_bases[node_id]))
                            self.base_ai.game.sendCommand(
                                ExchangeResourcesCommand(plane, -mq, 0, False))
                        else:
                            self.base_ai.try_build_plane(PlaneType.COMMERCIAL)
                else:
                    self.base_ai.game.sendCommand(
                        MoveCommand(plane, self.base_ai.country.position()))
                    self.base_ai.game.sendCommand(
                        LandCommand(plane, self.base_ai.country))