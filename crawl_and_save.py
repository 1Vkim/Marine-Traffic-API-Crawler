
import os
import requests
import time
from write_csv import write_csv
from dotenv import load_dotenv



load_dotenv()

API_KEY = os.getenv("MARINE_API_KEY")

url = f"https://api.marinesia.com/api/v1/vessel/357285000/location/latest?key={API_KEY}"

while True:
    try:
        response = requests.get(url)
        result = response.json()

        if result.get("error") == False and "data" in result:
            ship = result["data"]

            mmsi = ship.get("mmsi")
            lat = ship.get("lat")
            lon = ship.get("lng")
            speed = ship.get("sog")
            destination = ship.get("dest")
            time_stamp = ship.get("ts")

            print(f"MMSI : {mmsi}, LATITUDE : {lat}, Longitude : {lon}, Speed : {speed}, Destination : {destination}, Time : {time_stamp}")

            write_csv(mmsi, lat, lon, speed, destination, time_stamp)  

    except Exception as e:
            log_file = "error_log.txt"
            with open(log_file, "a") as log:
                log.write(f"Error writing to CSV: {e}\n")

    time.sleep(1800)  # wait 30 minutes before the next request