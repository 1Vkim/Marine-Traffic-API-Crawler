import os
import asyncio
import websockets
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
import redis

#from kafka import KafkaProducer


load_dotenv()

API_KEY = os.getenv("AIS_API_KEY")


#producer = KafkaProducer(
#   bootstrap_servers = "localhost:9092",
#    value_serializer = lambda v : json.dumps(v).encode("utf-8")
#)

r = redis.Redis(host='localhost', port=6379, db=0)

QUEUE_NAME = "ais_queue"

async def connect_and_stream():
    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
 
        subscribe_message = {"APIKey":API_KEY,
                             "BoundingBoxes" : [[[25.2732,55.1647],
                                                 [27.3713,57.3419]]],
                              "FilterMessageTypes" : ["PositionReport"]\
                                  }
        
       
        await websocket.send(json.dumps(subscribe_message))
        print("Subscribed to AIS stream with bounding box and message type filters.")

        async for message_json in websocket:

            try:
                message = json.loads(message_json)

                if message.get("MessageType") != "PositionReport":
                    continue

                ais_message = message.get('Message', {}).get('PositionReport', {})

                mmsi = ais_message.get("UserID")
                lat = ais_message.get("Latitude")   
                lon = ais_message.get("Longitude")
                
                if not (mmsi and lat and lon):
                    continue

                #clean payload for redis
                payload = {
                    "mmsi": mmsi,
                    "latitude": lat,
                    "longitude": lon,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }

                # Push to redis queue
                r.rpush(QUEUE_NAME, json.dumps(payload))
                print (f"Sent position report to Redis : {payload}"
                       )
                
            except Exception as e:
                print(f"Error processing message: {e}")
                

if __name__ == "__main__":
    asyncio.run(connect_and_stream())