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

from ai import AbstractAI

class BaseAI(AbstractAI):
    def __init__(self, ip, port):
        AbstractAI.__init__(self, ip, port)

    def think(self):
        while True:
            # print self.game
            self.game.updateSimFrame()
            print "Update received"

    def end(self):
        pass


if __name__ == "__main__":
    # Usage
    if len(sys.argv) != 3:
        print "Usage : ./AI.py ip port"
        sys.exit()

    ai = BaseAI(sys.argv[1], int(sys.argv[2]))
    ai.think()
