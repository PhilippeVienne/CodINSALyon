from command import BuildPlaneCommand
from model import Plane
from metier import ship_fuel


class SupplyManagement:
    def __init__(self, base_ai):
        '''

        :param proxy:
        :return:
        '''
        self.planes_id = []
        self.base_ai = base_ai

    def create_new_supplier(self):
        self.base_ai.try_build_plane(Plane.Type.COMMERCIAL)

    def push(self, plane):
        self.planes_id.append(plane.get_id())

    def pop(self, plane):
        return self.planes_id.remove(plane.get_id())

    def think(self):
        for key in self.planes_id:
            ship_fuel(self.base_ai,self.base_ai.my_planes[key])
