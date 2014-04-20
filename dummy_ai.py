#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from base_ai import BaseAI
from model.Plane import State

from command import MoveCommand, ExchangeResourcesCommand, LandCommand, WaitCommand

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

            # print self.my_planes
            # print [p.state() for _, p in self.my_planes.iteritems()]
            for p_id, plane in self.my_planes.iteritems():
                # If the plane is in the country's airport
                if plane.curBase() is None:
                    print '@@@@ WAITING 1 !', plane.curBase()
                    pass
                    # wait_cmd = WaitCommand(plane)
                    # self.game.sendCommand(wait_cmd)
                elif plane.curBase().position() == self.country.position() and plane.state() == State.AT_AIRPORT:

                    if plane.fuelInHold() == 0:
                        print '@@@@ EXCHANGING !'
                        fuel = plane.type.tankCapacity
                        exchange_cmd = ExchangeResourcesCommand(plane, 0, fuel, False)
                        self.game.sendCommand(exchange_cmd)
                    else:
                        print '@@@@ GOING ELSEWHERE !'
                        valid_bases = [b for b in self.all_bases.values() if b.position() != plane.position()]
                        closest_base = min(valid_bases, key=lambda b : b.position().distanceTo(plane.position()))
                        move_cmd = LandCommand(plane, closest_base)
                        self.game.sendCommand(move_cmd)

                # If the plane is over the country (but not in its airport) and without fuel,
                elif plane.curBase().position() == self.country.position() and plane.state() != State.AT_AIRPORT and plane.fuelInHold() == 0:
                    print '@@@@ LANDING !'
                    land_cmd = LandCommand(plane, self.country)
                    self.game.sendCommand(land_cmd)

                # If above another base, and have fuel to ship
                elif plane.curBase().position() != self.country.position():
                    if plane.fuelInHold() != 0:
                        exchange_cmd = ExchangeResourcesCommand(plane, 0, -plane.fuelInHold(), False)
                        self.game.sendCommand(exchange_cmd)
                    # If above another base, but without fuel
                    else:
                        move_cmd = LandCommand(plane, self.country)
                        self.game.sendCommand(move_cmd)
                else:
                    pass
                    #print '@@@@ WAITING 2 !'
                    # wait_cmd = WaitCommand(plane)
                    # self.game.sendCommand(wait_cmd)

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
