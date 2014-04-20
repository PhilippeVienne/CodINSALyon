#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model import Plane
from path import is_near

from model.Plane import State, Type
from command import ExchangeResourcesCommand, LandCommand
from model.Base import FullView
from command import BuildPlaneCommand

def loadUnit(game, plane, base):
    """
    Ask to load units in *plane* from *base*.

    Arguments:
    plane -- Plane to load
    base  -- Base where unit are taken
    """
    print plane, "Getting", base.position()
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

def resource_potential(base, plane):
    risk = 20
    if isinstance(base, FullView):
        risk = base.fuelInStock()

    return base.position().distanceTo(plane.position()) * risk

def valid_position(plane, position):
    max_distance = float(plane.fuelInTank()) / plane.type.fuelConsumptionPerDistanceUnit
    return plane.position() != position and plane.position().distanceTo(position) < max_distance / 2.

def ship_fuel(game, plane, fuel_percent=0.9):
    # If the plane is in the country's airport
    if plane.curBase() is None:
        return

    valid_bases = [b for b in game.all_bases.values() if valid_position(plane, b.position())]

    if plane.curBase().position() == game.country.position() and plane.state() == State.AT_AIRPORT:
        if plane.fuelInHold() == 0:
            fuel = plane.type.tankCapacity * fuel_percent
            military = plane.type.tankCapacity - fuel
            exchange_cmd = ExchangeResourcesCommand(plane, military, fuel, False)
            game.game.sendCommand(exchange_cmd)
        else:
            closest_base = min(valid_bases, key=lambda b : resource_potential(b, plane))
            move_cmd = LandCommand(plane, closest_base)
            game.game.sendCommand(move_cmd)
    # If the plane is over the country (but not in its airport) and without fuel
    elif plane.curBase().position() == game.country.position() and plane.state() != State.AT_AIRPORT\
     and plane.fuelInHold() + plane.militaryInHold() == 0:
        land_cmd = LandCommand(plane, game.country)
        game.game.sendCommand(land_cmd)

    # If above another base, and have fuel to ship
    elif plane.curBase().position() != game.country.position():
        if plane.fuelInHold() + plane.militaryInHold() != 0:
            exchange_cmd = ExchangeResourcesCommand(plane, -plane.militaryInHold(), -plane.fuelInHold(), False)
            game.game.sendCommand(exchange_cmd)
        # If above another base, but without fuel
        else:
            best_base = game.country
            if valid_bases:
                best_base = max(valid_bases, key=lambda b : resource_potential(b, plane))
            move_cmd = LandCommand(plane, best_base)
            game.game.sendCommand(move_cmd)
    else:
        return

toggle = 1
def building_strategy(game, production_line):
    global toggle
    if len(production_line.values())==0:
        toggle ^= 1
        # what type of plane to build?
        my_type = [Type.COMMERCIAL, Type.MILITARY][toggle]
        command = BuildPlaneCommand(my_type)
        game.sendCommand(command)
    else:
        print production_line.values()[0]