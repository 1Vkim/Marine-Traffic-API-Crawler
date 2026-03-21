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
        message = message.decode("utf-8") #Decode the message from bytes to string
        data = json.loads(message)
        
        print(f"Received data from Redis: {data}")
        ship_name = data.get("ship_name")
        speed = data.get("speed")
        time = data.get("timestamp")
        lat = data.get("latitude")
        lon = data.get("longitude")
        mmsi = data.get("mmsi")     


        #Insert data into the table to store vessel positions
        cur.execute(
            """
            INSERT INTO vessel_positions (ship_name,time_stamp,mmsi,speed, latitude, longitude)
            VALUES (%s , %s, %s, %s, %s, %s)
            """,
            (ship_name, time, mmsi, speed, lat, lon)
        )
        
        conn.commit()

    except Exception as e:
        with open("crawler-with-selenium/error_log.txt", "a") as f:
            f.write(f"Error inserting data into database: {e}\n")
      