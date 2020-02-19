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
    authentication = LinkCol('Poll Device','hey',url_kwargs=dict(device_id ='device_id')   )


iothub_connection_str = "HostName=MTreeIOTHub-01.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=hGoPyQiFID7w1ZorfXZdzLiTf/UOc5qpgRDowg+adUk="

def getDevices():
	iothub_registry_manager = IoTHubRegistryManager(iothub_connection_str)
	listOfDevices = iothub_registry_manager.get_devices(100)
	return listOfDevices

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
	items = [device.as_dict() for device in devices]
	deviceIDs = getDeviceId()
	table = ItemTable(items)
	return table.__html__()


@app.route('/hey')
def hey():
	deviceId =  request.args.get('device_id')
	util.cloudToDeviceMessage(deviceId)

	result = []

	while(redisClient.llen(deviceId)!=0):
		result.append(redisClient.lpop(deviceId))

	return "Message send to " + deviceId + " result is " + str(result)
 
if __name__ == '__main__':
	x = threading.Thread(target=event.startEventHub, args=(), daemon=True)
	x.start()
	app.run()