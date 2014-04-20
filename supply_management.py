from command import BuildPlaneCommand
from model import Plane
from metier import ship_fuel


class SupplyManagement:
    def __init__(self, base_ai):
        self.planes_id = set()
        self.base_ai = base_ai

    def assign(self, plane):
        self.planes_id.add(plane.id())

    def release(self, plane):
        return self.planes_id.remove(plane.id())

    def think(self):
        for key in self.planes_id:
            if not key in self.base_ai.my_planes:
                self.release(key)
            ship_fuel(self.base_ai, self.base_ai.my_planes[key])