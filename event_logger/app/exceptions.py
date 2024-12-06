class EventNotFoundException(Exception):
    def __init__(self, event_id: str):
        self.event_id = event_id
        self.message = f"Event with ID '{event_id}' not found."
        super().__init__(self.message)