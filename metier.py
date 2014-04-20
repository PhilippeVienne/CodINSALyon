#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model import Plane
from path import is_near
from path import get_path

import context
from model.Plane import State, Type

from model.Base import FullView

from command import LandCommand
from command import ExchangeResourcesCommand
from command import DropMilitarsCommand
from command import BuildPlaneCommand
from command import FillFuelTankCommand

from model.GameSettings import MINIMUM_BASE_GARRISON
from model.GameSettings import MINIMUM_CAPTURE_GARRISON

def conquer(game, plane, bases, min_fuel,
        nb_drop=MINIMUM_BASE_GARRISON + MINIMUM_CAPTURE_GARRISON + 0.042):
    """
    Description of conquer. Pop element from *bases*. Give a copy if you want
    to prevent modification.

    Arguments:
    game        -- Game to use
    plane       -- Plane used to conquer
    bases       -- Conquerable bases
    min_fuel    -- Amount of minimum fuel to release
    nb_drop     -- Number of militar units to drop
    """
    res = get_path(plane, bases, None, 1)
    if res:
        b = res[0]
        if b.id() in context.my_bases:
            b = context.my_bases[b.id()]
            deliver_petrol(game, plane, b, nb_drop,
                    b.fuelInStock() - min_fuel)
        else:
            max_mili = plane.militaryInHold()
            mili = min(nb_drop, max_mili)
            if not is_near(plane.position(), b.position(), 0.42):
                game.sendCommand(
                        DropMilitarsCommand(plane, b, mili))
            else:
                game.sendCommand(
                        DropMilitarsCommand(plane, b, mili))

def deliver_petrol(game, plane, base, nb_mili, min_fuel):
    if min_fuel < 0:
        min_fuel = 0
    if plane.state() == Plane.State.AT_AIRPORT and \
            is_near(plane.position(), base.position()):
        max_fuel = plane.fuelInHold()
        max_mili = plane.militaryInHold()
        fuel = max(min_fuel, max_fuel)
        mili = min(nb_mili, max_mili)
        print plane.id(), ': Deposit', fuel, 'fuel and', mili, 'mili'
        game.sendCommand(
                ExchangeResourcesCommand(plane, -mili, -fuel, False))
    else:
        game.sendCommand(LandCommand(plane, base))

def bring_democracy(game, plane, bases, fuel_rate):
    conquer(game, plane, bases, 4.2 * fuel_rate)

def load_unit(game, plane, base, fuel_rate=0.0):
    """
    Ask to load units in *plane* from *base*.

    Arguments:
    game       -- Game to use
    plane      -- Plane to load
    base       -- Base where unit are taken
    fuel_rate  -- Rate of fuel to take
    """
    print plane, "Getting", base.position()
    if plane.state() == Plane.State.AT_AIRPORT and \
            is_near(plane.position(), base.position()):
        try:
            min_fuel = base.fuelInStock()
        except AttributeError:
            min_fuel = 421337
        try:
            min_military = base.militaryGarrison()
        except AttributeError:
            min_military = 421337
        fuel = min(min_fuel, plane.type.tankCapacity * fuel_rate)
        military = min(min_military, plane.type.holdCapacity - fuel)
        game.sendCommand(
                ExchangeResourcesCommand(plane, military, fuel, False))
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

def need_democracy(plane, fuel_rate):
    return plane.fuelInHold() + plane.militaryInHold() == 0

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
