from metier import building_strategy


class BuildPlaneManagement:
    def __init__(self, base_ai):
        self.base_ai=base_ai

    def think(self):
        builder = self.base_ai.manager_building
        print(self.base_ai.my_planes.values()[-1:0])
        builder.create_new()
        #building_strategy(self.base_ai.game, self.base_ai.my_production_line)