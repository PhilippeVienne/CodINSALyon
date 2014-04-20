from command import MoveCommand
from command import ExchangeResourcesCommand


class FuelDelivery:
    def __init__(self, base_ai, plane):
        self.plane = plane
        self.base_ai = base_ai

    def fulfill(self, base, fuel):
        basePosition = base.get_position()
        self.base_ai.game.send_command(MoveCommand(self.plane, basePosition))
        self.base_ai.game.send_command(ExchangeResourcesCommand(self.plane, 0, -fuel, False))

    def minimal_fuel_to_go(self, base):
        return ( 1 )*base.get_position().distanceTo(self.plane.get_position())

    def seliver_max_fuel(self, base):
        return fulfill(base,)