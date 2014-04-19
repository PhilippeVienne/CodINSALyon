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
#sys.path.append("proxy.jar")

from ai import AbstractAI
from proxy import Proxy
import model.AbstractBase;
import model.Base;
import model.Coord;
import model.Plane;
import model.Plane.BasicView;

class BaseIA(AbstractAI):
    def __init__(self, ip, port):
        AbstractAI.__init__(self, ip, port)

    def think(self):
        while True:
            # print self.game
            self.game.updateSimFrame();
            self.save_snapshot()
            print "Update received"

    def save_snapshot(self):
        """
        Save the current game snapshot. *self.game* have to be initiated before
        by calling *updateSimFrame*.
        """
        self.all_bases = getAllBases()
        self.country = getCountry()
        self.ennemy_planes = getEnnemyPlanes()
        self.killed_planes = getKilledPlanes()
        self.map_height = getMapHeight()
        self.map_width = getMapWidth()
        self.my_bases = getMyBases()
        self.my_planes = getMyPlanes()
        self.not_o_and_not_v_bases = getNotOwnedAndNotVisibleBases()
        self.not_o_and_v_bases = getNotOwnedAndVisibleBases()
        self.num_frame = getNumFrame()
        self.visible_bases = getVisibleBase()

        self.all_bases = {k: self.all_bases
                for k in self.all_bases}
        self.ennemy_planes = {k: self.ennemy_planes
                for k in self.ennemy_planes}
        self.killed_planes = {k: self.killed_planes
                for k in self.killed_planes}
        self.my_bases = {k: self.my_bases
                for k in self.my_bases}
        self.my_planes = {k: self.my_planes
                for k in self.my_planes}
        self.not_owned_and_not_visible_bases = {k: self.not_o_and_not_v_bases
                for k in self.not_o_and_not_v_bases}
        self.not_owned_and_visible_bases = {k: self.not_o_and_v_bases
                for k in self.not_o_and_v_bases}
        self.visible_bases = {k: self.visible_bases
                for k in self.visible_bases}

    def end(self):
        pass

if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    ai = BaseIA(sys.argv[1], int(sys.argv[2]))
    ai.think();
