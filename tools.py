
import sys
import os
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from azure.iot.hub.protocol.models import ExportImportDevice, AuthenticationMechanism, SymmetricKey,TwinProperties
import threading
import socket
import selectors
from datetime import datetime
import random
from config import DeviceConfig

deviceIdConnString=""
iothub_connection_str = "HostName=MTreeIOTHub-01.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=hGoPyQiFID7w1ZorfXZdzLiTf/UOc5qpgRDowg+adUk="
CONNECTION_STRING_CLIENT = "HostName=MTreeIOTHub-01.azure-devices.net;DeviceId="+deviceIdConnString+";SharedAccessKey=x/AdXWMkad4nIrOQa0y5oR5uv4Oga3A1am9clL7o+HA="
sel = selectors.DefaultSelector()
client = None

def registerDeviceOnIotHub(deviceId,coordinatorName):

    try:
        # Create IoTHubRegistryManager
        iothub_registry_manager = IoTHubRegistryManager(iothub_connection_str)

        primary_key1 = "aaabbbcccdddeeefffggghhhiiijjjkkklllmmmnnnoo"
        secondary_key1 = "111222333444555666777888999000aaabbbcccdddee"
        symmetric_key1 = SymmetricKey(primary_key=primary_key1, secondary_key=secondary_key1)
        authentication1 = AuthenticationMechanism(type="sas", symmetric_key=symmetric_key1)
        device1 = ExportImportDevice(id=deviceId, status="enabled",tags={'parent':coordinatorName}, authentication=authentication1)
        print("registering device {} with coordinator {}".format(deviceId,coordinatorName))
        # Create devices
        device1.import_mode = "create"

        iothub_registry_manager.bulk_create_or_update_devices([device1])

        

    except Exception as ex:
        print("Unexpected error {0}".format(ex))
    except KeyboardInterrupt:
        print("iothub_registry_manager_sample stopped")

def startClient(coordinatorName):
    global client
    CONNECTION_STRING_CLIENT = "HostName=MTreeIOTHub-01.azure-devices.net;DeviceId="+  str(coordinatorName)+";SharedAccessKey=aaabbbcccdddeeefffggghhhiiijjjkkklllmmmnnnoo"

    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING_CLIENT)
    # Start a thread to listen 
    device_method_thread = threading.Thread(target=device_method_listener, args=(client,))
    device_method_thread.daemon = True
    device_method_thread.start()



def sendMessageToDevice(deviceId):

    s = socket.socket()          
  
    # Define the port on which you want to connect 
    port = DeviceConfig[deviceId]                
    print("Connecting to server\n")

    # connect to the server on local computer 
    s.connect(('127.0.0.1', port)) 
    print("Connected to server\n")
    # close the connection 
    s.close()  
    print("Closing the server\n")

def sendMessageToCloud(deviceId):
    global client
    TEMPERATURE = 20.0
    HUMIDITY = 60

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    temperature = TEMPERATURE + (random.random() * 15)
    humidity = HUMIDITY + (random.random() * 20)

    msg_txt_formatted = dict(
        temperature=temperature,
        humidity=humidity,
        deviceId=deviceId,
        timestamp = current_time 
    )
    message = Message(str(msg_txt_formatted))
    client.send_message(message)
    print("Sending message to IOT-Cloud",msg_txt_formatted)
    

def device_method_listener(device_client):
    while True:
        method_request = device_client.receive_method_request()
        print (
            "\nMethod callback called with:\nmethodName = {method_name}\npayload = {payload}".format(
                method_name=method_request.name,
                payload=method_request.payload
            )
        )

        sendMessageToDevice(method_request.payload)

        sendMessageToCloud(method_request.payload)
        if method_request.name == "msg":
            try:
                MESSAGE = int(method_request.payload)
                print("MESSAGE RECEIVED PAYLOAD ",MESSAGE)
            except ValueError:
                response_payload = {"Response": "Invalid parameter"}
                response_status = 400
            else:
                response_payload = {"Response": "Executed direct method {}".format(method_request.name)}
                response_status = 200
        else:
            response_payload = {"Response": "Direct method {} not defined".format(method_request.name)}
            response_status = 404

        method_response = MethodResponse(method_request.request_id, response_status, payload=response_payload)
        device_client.send_method_response(method_response)