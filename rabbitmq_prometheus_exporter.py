import os
import time
import requests
from prometheus_client import start_http_server, Gauge

# Get RabbitMQ credentials from environment variables, default to guest/guest
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
RABBITMQ_API_URL = f"http://{RABBITMQ_HOST}:15672/api/queues"

# Prometheus metrics
queue_messages = Gauge(
    "rabbitmq_individual_queue_messages",
    "Total count of messages in queue",
    ["host", "vhost", "name"]
)
queue_messages_ready = Gauge(
    "rabbitmq_individual_queue_messages_ready",
    "Messages ready for delivery",
    ["host", "vhost", "name"]
)
queue_messages_unack = Gauge(
    "rabbitmq_individual_queue_messages_unacknowledged",
    "Messages unacknowledged",
    ["host", "vhost", "name"]
)

def fetch_queue_metrics():
    try:
        response = requests.get(RABBITMQ_API_URL, auth=(RABBITMQ_USER, RABBITMQ_PASSWORD), timeout=5)
        response.raise_for_status()
        queues = response.json()
        
        for queue in queues:
            vhost = queue.get("vhost", "unknown")
            name = queue.get("name", "unknown")
            messages = queue.get("messages", 0)
            messages_ready = queue.get("messages_ready", 0)
            messages_unack = queue.get("messages_unacknowledged", 0)
            
            queue_messages.labels(host=RABBITMQ_HOST, vhost=vhost, name=name).set(messages)
            queue_messages_ready.labels(host=RABBITMQ_HOST, vhost=vhost, name=name).set(messages_ready)
            queue_messages_unack.labels(host=RABBITMQ_HOST, vhost=vhost, name=name).set(messages_unack)
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching RabbitMQ metrics: {e}")

if __name__ == "__main__":
    start_http_server(9100) # Start Prometheus metrics server
    print(f"Starting RabbitMQ Prometheus Exporter on port 9100, monitoring {RABBITMQ_HOST}")
    
    while True:
        fetch_queue_metrics()
        time.sleep(10)  # Fetch metrics every 10 seconds
