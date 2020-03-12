import asyncio
import os
from azure.eventhub.aio import EventHubConsumerClient
from flask import Flask, redirect, url_for
import redis
import json


CONNECTION_STR = "Endpoint=sb://ihsuprodbyres042dednamespace.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=hGoPyQiFID7w1ZorfXZdzLiTf/UOc5qpgRDowg+adUk=;EntityPath=iothub-ehub-mtreeiothu-2509244-fcc32d6a4d"
EVENTHUB_NAME = "iothub-ehub-mtreeiothu-2509244-fcc32d6a4d"

redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)

async def on_event(partition_context, event):
    
    print("Received event from partition: {}.".format(partition_context.partition_id))
    event_body = event.body_as_str().replace("\'","\"")
    deviceId = json.loads(event_body).get("deviceId")
    redisClient.lpush(deviceId,event_body)

    await partition_context.update_checkpoint(event)


async def on_partition_initialize(partition_context):
    # Put your code here.
    print("Partition: {} has been initialized.".format(partition_context.partition_id))


async def on_partition_close(partition_context, reason):
    # Put your code here.
    print("Partition: {} has been closed, reason for closing: {}.".format(
        partition_context.partition_id,
        reason
    ))


async def on_error(partition_context, error):
    # Put your code here. partition_context can be None in the on_error callback.
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


async def main():
    client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group="$default",
        eventhub_name=EVENTHUB_NAME
    )
    async with client:
        await client.receive(
            on_event=on_event,
            on_error=on_error,
            on_partition_close=on_partition_close,
            on_partition_initialize=on_partition_initialize # "-1" is from the beginning of the partition.
        )

def startEventHub():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())