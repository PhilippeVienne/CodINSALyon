import sys

sys.path.append('api/java/lib/commons-codec-1.6.jar')
sys.path.append('api/java/lib/commons-lang3-3.1.jar')
sys.path.append('api/java/lib/commons-logging-1.1.1.jar')
sys.path.append('api/java/lib/httpclient-4.2.5.jar')
sys.path.append('api/java/lib/httpcore-4.2.4.jar')
sys.path.append('api/java/lib/java_websocket.jar')
sys.path.append('api/java/lib/junit-4.4.jar')
sys.path.append('api/java/lib/libthrift-0.9.1.jar')
sys.path.append('api/java/lib/libthrift-0.9.1-javadoc.jar')
sys.path.append('api/java/lib/log4j-1.2.14.jar')
sys.path.append('api/java/lib/proxy.jar')
sys.path.append('api/java/lib/servlet-api-2.5.jar')
sys.path.append('api/java/lib/slf4j-api-1.5.8.jar')
sys.path.append('api/java/lib/slf4j-log4j12-1.5.8.jar')
sys.path.append('api/java/lib/utils.json.jar')
# sys.path.append("proxy.jar")

from ai import AbstractAI
from proxy import Proxy
import model.AbstractBase
import model.Base
import model.Coord
import model.Plane
import model.Plane.BasicView
from path import get_path
from command import BuildPlaneCommand
import context

class BaseAI(AbstractAI):
    def __init__(self, ip, port):
        AbstractAI.__init__(self, ip, port)
        self.toggle = 0
        self.my_planes = {}
        self.my_production_line = []

    def think(self):
        while True:
            # print self.game
            self.game.updateSimFrame()
            self.save_snapshot()

            # self.try_build_plane()
            # for p in self.my_planes.values():
            #     print p, ":", get_path(p, self.all_bases.values())
            # print "Update received"
            # print self.all_bases

    def save_snapshot(self):
        """
        Save the current game snapshot. *self.game* have to be initiated before
        by calling *updateSimFrame*.
        """
        self.all_bases = self.game.getAllBases()
        self.country = self.game.getCountry()
        self.ennemy_planes = self.game.getEnnemyPlanes()
        self.killed_planes = self.game.getKilledPlanes()
        self.map_height = self.game.getMapHeight()
        self.map_width = self.game.getMapWidth()
        self.my_bases = self.game.getMyBases()
        self.my_planes_before = self.my_planes
        self.my_planes = self.game.getMyPlanes()
        self.not_o_and_not_v_bases = self.game.getNotOwnedAndNotVisibleBases()
        self.not_o_and_v_bases = self.game.getNotOwnedAndVisibleBases()
        self.num_frame = self.game.getNumFrame()
        self.visible_bases = self.game.getVisibleBase()

        self.all_bases = dict((k, self.all_bases[k])
                              for k in self.all_bases)
        self.ennemy_planes = dict((k, self.ennemy_planes[k])
                                  for k in self.ennemy_planes)
        self.killed_planes = dict((k, self.killed_planes[k])
                                  for k in self.killed_planes)
        self.my_bases = dict((k, self.my_bases[k])
                             for k in self.my_bases)
        self.my_planes = dict((k, self.my_planes[k])
                              for k in self.my_planes)
        self.not_owned_and_not_visible_bases = dict((k,
            self.not_o_and_not_v_bases[k]) for k in self.not_o_and_not_v_bases)
        self.not_owned_and_visible_bases = dict((k,
            self.not_o_and_v_bases[k]) for k in self.not_o_and_v_bases)
        self.visible_bases = dict((k, self.visible_bases[k])
                                  for k in self.visible_bases)

        context.all_bases = self.all_bases
        context.ennemy_planes = self.ennemy_planes
        context.killed_planes = self.killed_planes
        context.my_bases = self.my_bases
        context.my_planes = self.my_planes
        context.not_owned_and_not_visible_bases =  \
                self.not_owned_and_not_visible_bases
        context.not_owned_and_visible_bases = self.not_owned_and_visible_bases
        context.visible_bases = self.visible_bases
        context.my_production_line = self.my_production_line

    def end(self):
        pass


if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    ai = BaseAI(sys.argv[1], int(sys.argv[2]))
    ai.think()
