#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('api/java/lib/proxy.jar')

import math
from model import Plane

def distance(p1, p2):
    """
    Euclidian distance

    Arguments:
    p1 -- (x, y) : Tuple containing the x, y, of the first point.
    p2 -- (x, y) : Tuple containing the x, y, of the second point.

    Returns:
    Return the euclidian distance between *p1* and *p2*
    """
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[0] - p2[0]) ** 2)

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
    p1 = plane.position().x(), plane.position().y()
    p2 = base.position().x(), base.position().y()
    return distance(p1, p2)

def get_path(plane, bases, fuel=None, max_iteration=5):
    """
    Construct a new path for the plane *plane* inside the set of node *bases*.
    Do only a maximum of *max_iteration* iteration. The arguments *plane* and
    *bases* may be modified by the function. Give a copy to prevent
    modification.

    Arguments:
    plane -- Plane : Construct the path from this plane
    bases -- [BasicView] : Set of nodes
    fuel -- Maybe double : Current fuel or None if the current fuel (default
    None)
    max_iteration -- Int : Max iteration (default 5)

    Returns:
    [(x, y)] : Path
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
    p1 = plane.position().x(), plane.position().y()
    p2 = nearest.position().x(), nearest.position().y()
    d = distance(p1, p2)
    fuel -= d * plane.type.fuelConsumptionPerDistanceUnit
    if fuel < 0:
        fuel = 0
        return []
    return [nearest] + get_path(plane, bases, fuel, max_iteration - 1)
