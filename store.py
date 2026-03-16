import os
from kafka import KafkaConsumer
import psycopg2
import json
from dotenv import load_dotenv

load_dotenv()

conn_string = os.getenv("DATABASE_URL")


consumer = KafkaConsumer(
    "ais_positions",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)



conn = psycopg2.connect(
    dbname="ais",
    user="postgres",
    password="postgres",
    host="localhost"
)

cur = conn.cursor()

for msg in consumer:
    data = msg.value

    lat = data["lat"]
    lon = data["lon"]
    mmsi = data["mmsi"]

    cur.execute(
        "INSERT INTO vessel_positions VALUES (NOW(), %s, %s, %s)",
        (mmsi, lat, lon)
    )

    conn.commit()