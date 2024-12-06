from app.exceptions import EventNotFoundException
from app.schemas import Event, EventUpdate
from uuid import uuid4
import json
from redis import Redis

class EventLoggerController:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def create_event(self, event: Event):
        event_id = str(uuid4())
        event_data = {
            "event_id": event_id,
            "user_id": event.user_id,
            "description": event.description,
            "status": "pending",
        }
        self.redis_client.hset(f"event:{event_id}", mapping=event_data)
        self.redis_client.rpush("event_queue", json.dumps(event_data))
        return event_id
    
    def update_event(self, event_id: str, update_data: EventUpdate):
        event_key = f"event:{event_id}"
        if not self.redis_client.exists(event_key):
            raise EventNotFoundException(event_id)
        self.redis_client.hset(event_key, "status", update_data.status)
        return event_id
    
    def get_event(self, event_id: str):
        event_key = f"event:{event_id}"
        if not self.redis_client.exists(event_key):
            raise EventNotFoundException(event_id)
        event_data = self.redis_client.hgetall(event_key)
        return event_data