#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback
from tools import registerDeviceOnIotHub,startClient
from config import GatewayConfig



COORDINATOR_NAME = "Factory"


print("starting client")
startClient(COORDINATOR_NAME)
print("Client Started")

COORDINATOR_PORT = GatewayConfig[COORDINATOR_NAME]
print("Started Coordinator device "+COORDINATOR_NAME + " listening at port " , COORDINATOR_PORT)


s = socket.socket()
s.bind(('127.0.0.1', COORDINATOR_PORT))
s.listen(5)
while True:
    c, addr = s.accept()      
    deviceId = c.recv(1024).decode()
    if deviceId:
        print("deviceid received ", deviceId)
        registerDeviceOnIotHub(deviceId, COORDINATOR_NAME)
    c.close()