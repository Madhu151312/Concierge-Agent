class CalendarTool:
    def __init__(self):
        # In a real implementation, wire to Google Calendar / Microsoft Graph OAuth tokens
        self.events = []

    def find_free(self, args):
        # args may contain 'range' or 'duration'; return stub slots
        return [
            {"start":"2025-11-21T10:00:00+05:30","end":"2025-11-21T10:30:00+05:30"},
            {"start":"2025-11-21T15:00:00+05:30","end":"2025-11-21T15:30:00+05:30"}
        ]

    def create_event(self, args):
        event = {"id": f"evt_{len(self.events)+1}", **args}
        self.events.append(event)
        return {"status":"ok", "event": event}
