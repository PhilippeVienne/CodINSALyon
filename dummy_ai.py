#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from base_ai import BaseAI
from model import Plane
from build_plane_managment import BuildPlaneManagement
from expansion_management import ExpansionManagement
from metier import ship_fuel, building_strategy
from supply_management import SupplyManagement


class DummyAI(BaseAI):
    def __init__(self, ip, port):
        super(BaseAI, self).__init__(ip, port)
        self.managers = [SupplyManagement(self), BuildPlaneManagement(self), ExpansionManagement(self)]

    def think(self):
        turn = 0
        while True:
            turn += 1
            # print self.game
            self.game.updateSimFrame()
            self.save_snapshot()
            print "# TURN %d : Update received" % turn

            for manager in self.managers:
                manager.think()

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
