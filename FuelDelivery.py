from command import MoveCommand
from command import ExchangeResourcesCommand


class FuelDelivery:
    def __init__(self, base_ai, plane):
        self.plane = plane
        self.base_ai = base_ai

    def fullfill(self, base):
        basePosition = base.get_position()
        base_ai.game.send_command(MoveCommand(self.plane, self.base_ai.))