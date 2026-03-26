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
ERROR_LOG  = os.path.join(os.path.dirname(__file__), "error_log.txt")
 
def get_db_connection():
    """Create a new DB connection with retries."""
    while True:
        try:
            conn = psycopg2.connect(conn_string)
            print("Database connected.")
            return conn
        except Exception as e:
            print(f"DB connection failed: {e}. Retrying in 5s...")
            time.sleep(5)
 
 #Connect to the database and create a cursor for executing queries
conn = get_db_connection()

cur = conn.cursor()

while True:
    _, message = r.blpop(QUEUE_NAME) #Waits for data to be available in the Redis queue
  
    try: 
        message = message.decode("utf-8") #Decode the message from bytes to string
        data = json.loads(message)
        
        #print(f"Received data from Redis: {data}")
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

    except psycopg2.OperationalError as e:
        # SSL dropped or connection lost — reconnect
        print(f"DB connection lost: {e}. Reconnecting...")
        try:
            conn.close()
        except Exception:
            pass
        conn = get_db_connection()
        cur  = conn.cursor()
 
    except Exception as e:
        print(f"Error: {e}")
        with open(ERROR_LOG, "a") as f:
            f.write(f"Error inserting data: {e}\n")
      