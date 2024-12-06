from app.controller import EventLoggerController
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from app.exceptions import EventNotFoundException
from app.schemas import Event, EventUpdate
from app.redis_provider import get_redis_client
app = FastAPI()

@app.exception_handler(EventNotFoundException)
async def event_not_found_handler(request, exc: EventNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )

def get_event_logger_controller():
    redis_client = get_redis_client()
    return EventLoggerController(redis_client=redis_client)


@app.post("/events")
async def create_event(
    event: Event,
    controller: EventLoggerController = Depends(get_event_logger_controller),
):
    event_id = controller.create_event(event)
    return {"event_id": event_id}


@app.put("/events/{event_id}")
async def update_event(
    event_id: str,
    update_data: EventUpdate,
    controller: EventLoggerController = Depends(get_event_logger_controller),
):
    event_id = controller.update_event(event_id, update_data)
    return {"message": f"Event {event_id} updated successfully"}


@app.get("/events/{event_id}")
async def get_event(
    event_id: str,
    controller: EventLoggerController = Depends(get_event_logger_controller),
):
    event_data = controller.get_event(event_id)
    return event_data
