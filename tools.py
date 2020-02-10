
import sys
import os
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from azure.iot.hub.protocol.models import ExportImportDevice, AuthenticationMechanism, SymmetricKey
import threading

iothub_connection_str = "HostName=MTreeIOTHub-01.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=hGoPyQiFID7w1ZorfXZdzLiTf/UOc5qpgRDowg+adUk="
CONNECTION_STRING_CLIENT = "HostName=MTreeIOTHub-01.azure-devices.net;DeviceId=TestSymkeys;SharedAccessKey=x/AdXWMkad4nIrOQa0y5oR5uv4Oga3A1am9clL7o+HA="

def registerDeviceOnIotHub(deviceId):

    try:
        # Create IoTHubRegistryManager
        iothub_registry_manager = IoTHubRegistryManager(iothub_connection_str)

        primary_key1 = "aaabbbcccdddeeefffggghhhiiijjjkkklllmmmnnnoo"
        secondary_key1 = "111222333444555666777888999000aaabbbcccdddee"
        symmetric_key1 = SymmetricKey(primary_key=primary_key1, secondary_key=secondary_key1)
        authentication1 = AuthenticationMechanism(type="sas", symmetric_key=symmetric_key1)
        device1 = ExportImportDevice(id=deviceId, status="enabled", authentication=authentication1)

        # Create devices
        device1.import_mode = "create"

        iothub_registry_manager.bulk_create_or_update_devices([device1])

        

    except Exception as ex:
        print("Unexpected error {0}".format(ex))
    except KeyboardInterrupt:
        print("iothub_registry_manager_sample stopped")

def startClient():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING_CLIENT)
    print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

    # Start a thread to listen 
    device_method_thread = threading.Thread(target=device_method_listener, args=(client,))
    device_method_thread.daemon = True
    device_method_thread.start()


def device_method_listener(device_client):
    while True:
        method_request = device_client.receive_method_request()
        print (
            "\nMethod callback called with:\nmethodName = {method_name}\npayload = {payload}".format(
                method_name=method_request.name,
                payload=method_request.payload
            )
        )
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