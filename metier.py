#!/usr/bin/env python
# -*- coding: utf-8 -*-

from model import Plane
from path import is_near
from command import ExchangeResourcesCommand
from command import LandCommand

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
