import os
import redis
#from kafka import KafkaConsumer
import psycopg2
import json
from dotenv import load_dotenv

load_dotenv()

conn_string = os.getenv("DATABASE_URL")   

#Redis Connection
r = redis.Redis(host='localhost', port=6379, db=0)

QUEUE_NAME = "ais_queue"

#consumer = KafkaConsumer(
#    "ais_positions",
#    bootstrap_servers=os.getenv("DB_HOST"),
#    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
#)




#Connecting to the Neon Database and inserting data from Redis
conn = psycopg2.connect(conn_string)

cur = conn.cursor()

while True:
    _, message = r.blpop(QUEUE_NAME) #Waits for data to be available in the Redis queue
    try: 
        data = json.loads(message)
        
        report = data.get("Message", {}).get("PositionReport", {})
        lat = report.get("Latitude")
        lon = report.get("Longitude")
        mmsi = report.get("UserID")     


        #Create the table to store vessel positions
        cur.execute(
            """
            INSERT INTO vessel_positions (time,mmsi, latitude, longitude)
            VALUES (NOW (), %s, %s, %s)
            """,
            (mmsi, lat, lon)
        )
        
        conn.commit()

    except EXCEPTION as e:
        print(f"Error:", e)
        conn.rollback()