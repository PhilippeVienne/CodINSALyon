import model.Plane

class Command():
    SUCCESS = 0
    WARNING_COMMAND = -1
    ERROR_COMMAND = -2
    ERROR_TIME_OUT = -3
    ERROR_FORBIDDEN = -4
    ERROR_UNKNOWN = -5
    
    def __init__(self):
        pass
    
class AttackCommand(Command):
    
    def __init__(self, plane, target):
        Command.__init__(self)
        if p is None or target is None:
            raise Error("Attack Command :  null reference")
        self.planeSrc = plane
        self.planeTarget = target

    def __str__(self):
        return "attack " + self.planeSrc.get_id() + " -> " + self.planeTarget.get_id()
    
    def get_plane_src(self):
        return self.planeSrc
    
    def get_plane_target(self):
        return self.planeTarget
    
class BuildPlaneCommand(Command):

    def __init__(self, requestedType):
        Command.__init__(self)
        if requestedType is None:
            raise "BuildPlaneCommande : null reference"
        self.requestedType = requestedType

    def __str__(self):
        return "build " + ("military" if self.requestedType == Plane.Type.MILITARY else "commercial")
    
    def get_requested_type(self):
        return self.requestedType
    
class DropMilitarsCommand(Command):
    
    def __init__(self, plane, base, nb_drop):
        Command.__init__(self)
        if plane is None or base is None:
            raise "DropMilitarsCommand : Null reference"
        self.planeSrc = plane
        self.baseTarget = base
        self.quantity = nb_drop

    def __str__(self):
        return "drop " + self.planeSrc.get_id() + " --(" + self.quantity + ")--> " + self.baseTarget.get_id()
    
    def get_plane(self):
        return self.plane
    
    def get_base(self):
        return self.base
    
    def get_nbdrop(self):
        return self.nbdrop
    
class ExchangeResourcesCommand(Command):
    def __init__(self, plane, mil_qty, fuel_qty, delete):
        Command.__init__(self)
        if plane is None:
            raise "LoadRessourcesCommand : Null reference"
        self.planeSrc = plane
        self.militarQuantity = mil_qty
        self.fuelQuantity = fuel_qty
        self.delete_ressources = delete

    def __str__(self):
        return "loadResource " + self.planeSrc.get_id() + " : militar => " + self.militarQuantity + "; fuel => " + self.fuelQuantity

    def get_plane(self):
        return self.plane
    
    def get_fuel_qty(self):
        return self.fuelQuantity
    
    def get_mil_qty(self):
        return self.militarQuantity

    def get_delete_resources(self):
        return self.delete_ressources
    
class FillFuelTankCommand(Command):

    def __init__(self, plane, quantity_fuel):
        Command.__init__(self)
        if plane is None:
            raise "FillFuelTankCommand : Null reference"
        self.planeSrc = plane
        self.quantity = quantity_fuel

    def __str__(self):
        return "store " + self.planeSrc.get_id() + " :> " + self.quantity
    
    def get_plane(self):
        return self.plane
    
    def get_nbdrop(self):
        return self.nbdrop

class FollowCommand(Command):

    def __init__(self, plane, target):
        Command.__init__(self)
        if plane is None or target is None:
            raise "FollowCommand : null reference"
        self.planeSrc = plane
        self.planeTarget = target

    def __str__(self):
        return "follow " + self.planeSrc.get_id() + " -> " + self.planeTarget._id()

    def get_plane_src(self):
        return self.planeSrc
    
    def get_plane_target(self):
        return self.planeTarget
    
class LandCommand(Command):
    def __init__(self, plane, base):
        Command.__init__(self)
        if base is None or plane is None:
            raise "LandCommand : null reference"
        self.plane = plane
        self.base = base

    def get_plane(self):
        return self.plane
    
    def get_base(self):
        return self.base
    
    def __str__(self):
        return "land " + self.plane.get_id() + " -> " + self.base.get_id()

class MoveCommand(Command):

    def __init__(self, plane, coord):
        Command.__init__(self)
        if plane is None:
            raise "MoveCommand : null reference"
        self.plane = plane
        self.destination = coord

    def get_plane(self):
        return self.plane
    
    def get_destination(self):
        return self.destination

    def __str__(self):
        return "mv "+self.plane.get_id()+" -> "+str(coord)

class WaitCommand(Command):

    def __init__(self, plane):
        Command.__init__(self)
        if plane is None:
            raise "WaitCommand : null reference"
        self.plane = plane
        
    def get_plane(self):
        return self.plane   
    
    def __str__(self):
        return "wait " + str(self.plane)
    