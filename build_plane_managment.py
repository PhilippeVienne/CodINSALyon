from metier import building_strategy


class BuildPlaneManagement:
    def __init__(self, base_ai):
        self.base_ai=base_ai
        self.assignations = []

    def create(self, plane_type, assign_to):
        self.base_ai.my_production_line.append(plane_type)
        self.assignations.append(assign_to)

    def think(self):
        for p in self.base_ai.country.planes():
            if p.id not in self.base_ai.my_planes_before:
                if self.assignations:
                    manager = self.assignations.pop()
                    manager.assign(p)
                else:
                    self.base_ai.expansion_manager.assign(p)