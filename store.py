import os
from kafka import KafkaConsumer
import psycopg2
import json
from dotenv import load_dotenv

load_dotenv()

conn_string = os.getenv("DATABASE_URL")


consumer = KafkaConsumer(
    "ais_positions",
    bootstrap_servers=os.getenv("DB_HOST"),
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)



conn = psycopg2.connect(conn_string)

cur = conn.cursor()

for msg in consumer:
    try: 
        data = msg.value
        
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