#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model import Plane
from path import is_near

from model.Plane import State, Type
from command import ExchangeResourcesCommand, LandCommand, FillFuelTankCommand
from model.Base import FullView
from command import BuildPlaneCommand

def load_unit(game, plane, base):
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

def resource_potential(base, plane, game):
    risk = 15
    if isinstance(base, FullView):
        risk = base.fuelInStock()

    planes_on_base = [p for p in game.my_planes.itervalues() if p.position() == base.position()]
    crowdedness = 1.0
    if planes_on_base:
        crowdedness += len(planes_on_base) ** 2

    return base.position().distanceTo(plane.position()) * risk

def valid_position(plane, position):
    max_distance = float(plane.fuelInTank()) / plane.type.fuelConsumptionPerDistanceUnit
    return plane.position() != position and plane.position().distanceTo(position) < max_distance / 2.

def ship_fuel(game, plane, fuel_percent=0.9):
    # If the plane is in the country's airport
    if plane.curBase() is None:
        return

    valid_bases = [b for b in game.all_bases.values() if valid_position(plane, b.position()) if b != plane.curBase()]

    if plane.curBase().position() == game.country.position() and plane.state() == State.AT_AIRPORT:
        if plane.fuelInHold() + plane.militaryInHold() == 0:
            fuel = plane.type.holdCapacity * fuel_percent
            military = plane.type.holdCapacity - fuel
            exchange_cmd = ExchangeResourcesCommand(plane, military, fuel, False)
            game.game.sendCommand(exchange_cmd)
        else:
            closest_base = min(valid_bases, key=lambda b : resource_potential(b, plane, game))
            move_cmd = LandCommand(plane, closest_base)
            game.game.sendCommand(move_cmd)
    # If the plane is over the country (but not in its airport) and without fuel
    elif plane.curBase().position() == game.country.position() and plane.state() != State.AT_AIRPORT\
     and plane.fuelInHold() + plane.militaryInHold() == 0:
        land_cmd = LandCommand(plane, game.country)
        game.game.sendCommand(land_cmd)

    # If above another base
    elif plane.curBase().position() != game.country.position():
        # If you have fuel (and maybe military) to ship
        if plane.fuelInHold() != 0:
            exchange_cmd = ExchangeResourcesCommand(plane, -plane.militaryInHold(), -plane.fuelInHold(), False)
            game.game.sendCommand(exchange_cmd)
        # If you don't have fuel
        else:
            best_base = game.country
            if valid_bases:
                best_base = max(valid_bases, key=lambda b : resource_potential(b, plane, game))

            max_distance = float(plane.fuelInTank()) / plane.type.fuelConsumptionPerDistanceUnit
            if plane.position().distanceTo(best_base.position()) > max_distance:
                fill_cmd = FillFuelTankCommand(plane, plane.curBase().fuelInStock())
                game.game.sendCommand(fill_cmd)
            else:
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
