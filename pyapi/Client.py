#!/usr/bin/env python

import sys, glob
sys.path.append('gen-py')

from genbridge import Bridge
from genbridge.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

import threading

# Disclaimer : Je suis mauvais en python, prière de ne pas se moquer trop fort de mon code !

# Usage
if len(sys.argv) != 3:
    print "Usage : ./Client.py ip port"
    sys.exit()

try:
    # Make socket
    transport = TSocket.TSocket(sys.argv[1], sys.argv[2])

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    # Create a client to use the protocol encoder
    bridge = Bridge.Client(protocol)
    # Connect!
    transport.open()
    
    #BLA BLA BLA IA
    # threading.Thread(target=your_function).start()

    # Close!
    transport.close()

except Thrift.TException, tx:
  print '%s' % (tx.message)

