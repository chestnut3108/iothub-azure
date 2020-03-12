from flask import Flask,request
from flask_table import Table, Col,ButtonCol,LinkCol
app = Flask(__name__)
import sys
import os
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.protocol.models import ExportImportDevice, AuthenticationMechanism, SymmetricKey,QuerySpecification
import util
import event
import threading
import redis


redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)

class ItemTable(Table):
    device_id = Col('device_id')
    coordinator = Col('coordinator')
    authentication = LinkCol('Poll Device','hey',url_kwargs=dict(device_id ='device_id',coordinator = 'coordinator')   )


iothub_connection_str = "HostName=MTreeIOTHub-01.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=hGoPyQiFID7w1ZorfXZdzLiTf/UOc5qpgRDowg+adUk="

def getDevices():
	iothub_registry_manager = IoTHubRegistryManager(iothub_connection_str)
	listOfDevices = iothub_registry_manager.get_devices(100)
	deviceInfoList = []
	for device in listOfDevices:
		deviceInfo = {}
		deviceId = device.as_dict().get('device_id')
		deviceInfo["device_id"] = deviceId
		twin = iothub_registry_manager.get_twin(device_id=deviceId)
		try:
			deviceInfo["coordinator"] = twin.properties.desired["coordinator"]
		
		except KeyError:
			deviceInfo["coordinator"] = "Not a device"

		finally:
			deviceInfoList.append(deviceInfo)
	
	return deviceInfoList

def getDeviceId():
	device = getDevices()
	devicesId= []
	for dev in device:
		deviceId = dev.as_dict().get('device_id')
		devicesId.append(deviceId)
	return devicesId

@app.route('/')
def hello_world():
	devices = getDevices()
	#deviceIDs = getDeviceId()
	table = ItemTable(devices)
	return table.__html__()


@app.route('/hey')
def hey():
	deviceId =  request.args.get('device_id')
	coordinator =  request.args.get('coordinator')
	util.cloudToDeviceMessage(deviceId,coordinator)

	result = []

	while(redisClient.llen(deviceId)!=0):
		result.append(redisClient.lpop(deviceId))

	return "Message send to " + deviceId + " result is " + str(result)
 
if __name__ == '__main__':
	x = threading.Thread(target=event.startEventHub, args=(), daemon=True)
	x.start()
	app.run()