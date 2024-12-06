import os
import json
from redis import Redis
import requests

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
EVENT_LOGGER_API = os.getenv("EVENT_LOGGER_API", "http://localhost:8000")

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def update_event(event_id):
    update_url = f"{EVENT_LOGGER_API}/events/{event_id}"
    response = requests.put(update_url, json={"status": "processed"})
    if response.status_code != 200:
        print(f"Failed to update event {event_id} status: {response.text}")
    else:
        print(f"Event updated {event_id} response {json.dumps(response.json())}")

def pull_event(event_data):
    _, raw_event = event_data
    event = json.loads(raw_event)
    print(f"Event {event['event_id']} has been sent to {event['user_id']}: {event['description']}")
    return event['event_id']

def worker():
    while True:
        event_data = redis_client.blpop("event_queue", timeout=0)
        if event_data:
            event_id = pull_event(event_data=event_data)
            update_event(event_id=event_id)

if __name__ == "__main__":
    worker()
