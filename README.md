# Real-Time AIS Vessel Tracking Pipeline

A real-time maritime data pipeline that ingests live AIS vessel position data, queues it using Redis, and stores it in a PostgreSQL database hosted on Neon.

This project demonstrates core data engineering concepts including streaming ingestion, message queueing, fault-tolerant consumers, and cloud database integration.

---

## Architecture

```
AISStream WebSocket
        ↓
crawl_and_save.py  (Producer)
        ↓
Redis Queue (ais_queue)
        ↓
store.py (Consumer)
        ↓
PostgreSQL (Neon Database)
```

The system runs as two independent processes:

* **Producer** — collects live vessel data
* **Consumer** — writes queued data to the database

This design improves reliability and scalability.

---

## Repository Structure

```
.
├── crawl_and_save.py     # AIS stream crawler (producer)
├── store.py              # Redis consumer that writes to PostgreSQL
├── schema.sql            # Database schema
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Optional container setup
├── start_site.sh         # Script to start services
├── error_log.txt         # Runtime logs
├── ARTICLE.md            # Medium article version of the project
├── README.md             # Project documentation
└── .gitignore
```

---

## Features

* Real-time AIS vessel tracking
* WebSocket streaming ingestion
* Redis-backed message queue
* Resilient consumer with auto-reconnect
* PostgreSQL storage (Neon cloud database)
* Designed for local deployment on WSL / Ubuntu
* Easily extendable for analytics and monitoring

---

## Requirements

* Python 3.10+
* Redis
* PostgreSQL (Neon recommended)
* pip
* tmux (optional but recommended)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/1Vkim/Marine-Traffic-API-Crawler
cd ais-vessel-tracking-pipeline
```

---

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Start Redis

If running locally:

```bash
redis-server
```

Or on WSL:

```bash
sudo service redis-server start
redis-cli ping
```

Expected output:

```
PONG
```

---

### 5. Setup Database

Connect to your Neon PostgreSQL instance and run:

```sql
\i schema.sql
```

Or paste the schema manually.

---

## Environment Variables

Create a `.env` file in the project root:

```
AIS_API_KEY=your_aisstream_api_key
DATABASE_URL=your_neon_connection_string
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## Running the Pipeline

### Start Producer

```bash
python crawl_and_save.py
```

### Start Consumer

```bash
python store.py
```

---

## Running in Background (Recommended)

Using tmux:

```bash
tmux new-session -d -s crawler "python3 crawl_and_save.py"
tmux new-session -d -s store "python3 store.py"

tmux ls
```

Attach to a session:

```bash
tmux attach -t crawler
```

Detach:

```
Ctrl + B, then D
```

---

## Verifying the Queue

Check if messages are arriving in Redis:

```bash
redis-cli
LLEN ais_queue
LRANGE ais_queue 0 5
```

---

## Checking Database Inserts

```sql
SELECT ship_name, mmsi, speed, latitude, longitude, time_stamp
FROM vessel_positions
ORDER BY time_stamp DESC
LIMIT 10;
```

---

## Example Output

Crawler:

```
ship: STANFORD HAWK | speed: 0 | mmsi: 376955000
ship: MARINE CHARGE | speed: 0 | mmsi: 563180700
```

Consumer:

```
Received data from Redis → inserting into database
```

---

## Common Issues

### Redis not connecting

Start Redis manually:

```
redis-server
```

---

### WSL Redis service error

Use:

```
sudo service redis-server start
```

---

### Ships not appearing in queue

Make sure you are not filtering out:

```
speed = 0
```

Anchored vessels often have zero speed.

---

## Future Improvements

* Grafana dashboard for vessel monitoring
* Real-time vessel map visualization
* Kafka-based streaming architecture
* AIS anomaly detection
* Vessel metadata enrichment
* Port traffic analytics

---

## Article

Full project write-up:

```
ARTICLE.md
```

---

## License

MIT License

---

## Author

Built as a real-time data engineering project exploring streaming systems and maritime datasets.
