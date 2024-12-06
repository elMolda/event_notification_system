import pytest
from unittest.mock import create_autospec
from uuid import uuid4
from app.schemas import Event, EventUpdate
from app.exceptions import EventNotFoundException
from app.controller import EventLoggerController
from redis import Redis


@pytest.fixture
def mock_redis_client():
    redis_mock = create_autospec(Redis)
    return redis_mock


@pytest.fixture
def controller(mock_redis_client):
    return EventLoggerController(redis_client=mock_redis_client)


def test_create_event(controller):
    event = Event(user_id="user123", description="Test event")
    controller.redis_client.hset.return_value = True
    controller.redis_client.rpush.return_value = 1
    event_id = controller.create_event(event)
    assert controller.redis_client.hset.called
    assert controller.redis_client.rpush.called
    assert isinstance(event_id, str)  # UUID
    event_key = f"event:{event_id}"
    controller.redis_client.hset.assert_called_with(
        event_key,
        mapping={
            "event_id": event_id,
            "user_id": event.user_id,
            "description": event.description,
            "status": "pending",
        },
    )


def test_update_event_success(controller):
    event_id = str(uuid4())
    update_data = EventUpdate(status="processed")
    event_key = f"event:{event_id}"
    controller.redis_client.exists.return_value = True
    result = controller.update_event(event_id, update_data)
    assert result == event_id
    controller.redis_client.hset.assert_called_with(event_key, "status", update_data.status)


def test_update_event_not_found(controller):
    event_id = str(uuid4())
    update_data = EventUpdate(status="processed")
    controller.redis_client.exists.return_value = False
    with pytest.raises(EventNotFoundException) as exc_info:
        controller.update_event(event_id, update_data)
    assert str(event_id) in str(exc_info.value)


def test_get_event_success(controller):
    event_id = str(uuid4())
    event_key = f"event:{event_id}"
    expected_event = {
        b"event_id": event_id.encode(),
        b"user_id": b"user123",
        b"description": b"Test event",
        b"status": b"pending",
    }
    controller.redis_client.exists.return_value = True
    controller.redis_client.hgetall.return_value = expected_event
    event_data = controller.get_event(event_id)
    assert event_data == expected_event
    controller.redis_client.exists.assert_called_with(event_key)
    controller.redis_client.hgetall.assert_called_with(event_key)


def test_get_event_not_found(controller):
    event_id = str(uuid4())
    controller.redis_client.exists.return_value = False
    with pytest.raises(EventNotFoundException) as exc_info:
        controller.get_event(event_id)
    assert str(event_id) in str(exc_info.value)
