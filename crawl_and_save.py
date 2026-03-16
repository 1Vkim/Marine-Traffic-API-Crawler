import os
import asyncio
import websockets
import json
from datetime import datetime, timezone
from write_csv import write_csv
from dotenv import load_dotenv
from kafka import KafkaProducer


load_dotenv()

API_KEY = os.getenv("AIS_API_KEY")


producer = kafkaproduce(
    bootstrap_servers = 'localhost:9092',
    value_serializer = lambda v : json.dumps(v).encode("utf-8")
)


async def connect_and_stream():
    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey":API_KEY,
                             "BoundingBoxes" : [[[25.2732,55.1647],
                                                 [27.3713,57.3419]]],
                              "FilterMessageTypes" : ["PositionReport"] }
        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
            message_type = message.get("MessageType")
            if message_type == "PositionReport":

                ais_message = message['Message']['PositionReport']
                print(f"[{datetime.now(timezone.utc)}] ShipId: {ais_message['UserID']} Latitude: {ais_message['Latitude']} Longitude: {ais_message['Longitude']}")


if __name__ == "__main__":
    asyncio.run(asyncio.run(connect_and_stream()))