
from email.message import Message
import os
import asyncio
import websockets
import json
from datetime import datetime, timezone
from write_csv import write_csv
from dotenv import load_dotenv



load_dotenv()

API_KEY = os.getenv("AIS_API_KEY")
AIS_URL = os.getenv("AIS_URL")

async def connect_and_stream():
    async with websockets.connect(AIS_URL) as websocket:
        await websocket.send(json.dumps({"type": "auth", "token": API_KEY}))
        subscribe_message = {"APIKey":API_KEY,
                             "BoundingBoxes" : [[[25.2732,55.1647],[27.3713,57.3419]]],
                              "FilterMessageTypes" : ["PositionReport"] }
        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)

        async for message_json in websocket:
            message = json.loads(message_json)
            message_type = message("MessageType")
            if message_type == "PositionReport":

                ais_messsage = message['Message']['PositionReport']
                print(f"[{datetime.now(timezone.utc)}] ShipId: {ais_message['UserID']} Latitude: {ais_message['Latitude']} Latitude: {ais_message['Longitude']}")


if __name__ == "__main__":
    asyncio.run(connect_and_stream())