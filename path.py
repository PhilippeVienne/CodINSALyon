#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('api/java/lib/proxy.jar')

import math
from model import Plane
from model import Base
import context

def distance(p1, p2):
    """
    Euclidian distance

    Arguments:
    p1 -- Coord.View : First point
    p2 -- Coord.View : Second point

    Returns:
    Return the euclidian distance between *p1* and *p2*
    """
    return math.sqrt((p1.x() - p2.x()) ** 2 + (p1.y() - p2.y()) ** 2)

def is_near(p1, p2, threashold=0.1):
    """
    Indicate if *p1* and *p2* are close one of each other.

    Arguments:
    p1         -- Coord.View : First point
    p2         -- Coord.View : First point
    threashold -- Real : Distance threashold (default 0.1)

    Returns:
    Bool : True if they are close
    """
    return distance(p1, p2) < threashold


def evaluation(plane, base):
    """
    Calculate the evaluation for the plane *plane* to go into the position of
    *base*.

    Arguments:
    plane -- Plane
    base  -- BasicView

    Returns:
    Real : Represent the rank to go to the position *base*.
    """
    d = distance(plane.position(), base.position())
    fuel_ratio = plane.fuelInTank() / plane.type.tankCapacity
    if plane.ownerId() == base.ownerId(): # My base
        if fuel_ratio >= 0.23:
            return d + 1000
        fuel = context.my_bases[base.id()].fuelInStock()
        if fuel <= 0:
            return (d + 1.0) * (fuel_ratio + 0.42)
        return d * fuel_ratio
    return d

def get_path(plane, bases, fuel=None, max_iteration=5):
    """
    Construct a new path for the plane *plane* inside the set of node *bases*.
    Do only a maximum of *max_iteration* iteration. The arguments *plane* and
    *bases* may be modified by the function. Give a copy to prevent
    modification.

    Arguments:
    plane         -- Plane : Construct the path from this plane
    bases         -- [BasicView] : Set of nodes
    fuel          -- Maybe double : Current fuel or None if the current fuel
    (default None)
    max_iteration -- Int : Max iteration (default 5)

    Returns:
    [BasicView] : Path
    """
    if max_iteration is 0:
        return []
    if not bases:
        return []
    if fuel is None:
        fuel = plane.fuelInTank()
    i, nearest = sorted(enumerate(bases),
            key=lambda (_, b): evaluation(plane, b))[0]
    bases.pop(i)
    d = distance(plane.position(), nearest.position())
    fuel -= d * plane.type.fuelConsumptionPerDistanceUnit
    if fuel < 0:
        fuel = 0
        return []
    return [nearest] + get_path(plane, bases, fuel, max_iteration - 1)
