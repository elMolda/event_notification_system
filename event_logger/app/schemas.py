from pydantic import BaseModel, Field

class Event(BaseModel):
    user_id: str = Field(..., description="User ID")
    description: str = Field(..., description="Event description")

class EventUpdate(BaseModel):
    status: str = Field(..., description="Status of the event")