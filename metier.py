#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model import Plane
from path import is_near

from model.Plane import State
from command import ExchangeResourcesCommand, LandCommand

def loadUnit(game, plane, base):
    """
    Ask to load units in *plane* from *base*.

    Arguments:
    plane -- Plane to load
    base  -- Base where unit are taken
    """
    if plane.state() == Plane.State.AT_AIRPORT and \
            is_near(plane.position(), base.position()):
        try:
            nb = base.militaryGarrison()
        except AttributeError:
            nb = 421337
        game.sendCommand(ExchangeResourcesCommand(plane, min(
                plane.type.holdCapacity - plane.militaryInHold(),
                nb), 0, False))
    else:
        game.sendCommand(LandCommand(plane, base))

def ship_fuel(game, plane):
    # If the plane is in the country's airport
    if plane.curBase() is None:
        pass
    elif plane.curBase().position() == game.country.position() and plane.state() == State.AT_AIRPORT:

        if plane.fuelInHold() == 0:
            fuel = plane.type.tankCapacity
            exchange_cmd = ExchangeResourcesCommand(plane, 0, fuel, False)
            game.game.sendCommand(exchange_cmd)
        else:
            valid_bases = [b for b in game.all_bases.values() if b.position() != plane.position()]
            closest_base = min(valid_bases, key=lambda b : b.position().distanceTo(plane.position()))
            move_cmd = LandCommand(plane, closest_base)
            game.game.sendCommand(move_cmd)
    # If the plane is over the country (but not in its airport) and without fuel,
    elif plane.curBase().position() == game.country.position() and plane.state() != State.AT_AIRPORT and plane.fuelInHold() == 0:
        land_cmd = LandCommand(plane, game.country)
        game.game.sendCommand(land_cmd)

    # If above another base, and have fuel to ship
    elif plane.curBase().position() != game.country.position():
        if plane.fuelInHold() != 0:
            exchange_cmd = ExchangeResourcesCommand(plane, 0, -plane.fuelInHold(), False)
            game.game.sendCommand(exchange_cmd)
        # If above another base, but without fuel
        else:
            move_cmd = LandCommand(plane, game.country)
            game.game.sendCommand(move_cmd)
    else:
        pass
