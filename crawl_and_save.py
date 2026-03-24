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

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

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
                metadata = message.get("MetaData", {})

                ship_name = metadata.get("ShipName", "Unknown") #Get ship name from the metadata and return unkown if not available 
                speed = ais_message.get("SOG", 0)  # Speed Over Ground in knots
                mmsi = ais_message.get("UserID")
                lat = ais_message.get("Latitude")   
                lon = ais_message.get("Longitude")

                #print(f"shpname: {ship_name},speed: {speed},mmsi: {mmsi},lat: {lat},lon: {lon}")
                
                if any (v is None for v in [ship_name, speed, mmsi, lat, lon]):
                    continue

                #clean payload for redis
                payload = {
                    "ship_name": ship_name,
                    "speed": speed,
                    "mmsi": mmsi,
                    "latitude": lat,
                    "longitude": lon,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }

                try:
                    # Push to redis queue
                    r.rpush(QUEUE_NAME, json.dumps(payload))
                    
                
                except Exception as e:
                    with open("crawler-with-selenium/error_log.txt", "a") as f:
                         f.write(f"Error pushing to Redis: {e}\n")
                
            except Exception as e:
                with open("crawler-with-selenium/error_log.txt", "a") as f:
                    f.write(f"Error processing message: {e}\n")

if __name__ == "__main__":
    asyncio.run(connect_and_stream())