
import sys
import os
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.protocol.models import ExportImportDevice, AuthenticationMechanism, SymmetricKey

iothub_connection_str = "HostName=MTreeIOTHub-01.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=hGoPyQiFID7w1ZorfXZdzLiTf/UOc5qpgRDowg+adUk="


def registerDeviceOnIotHub(deviceId):

    try:
        print("kjansnkjdnkn")
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

