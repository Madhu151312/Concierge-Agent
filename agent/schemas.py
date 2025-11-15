# Simple schemas and constants for tool-call protocol

TOOL_CALL_EXAMPLE = {
    "tool": "calendar",
    "action": "create_event",
    "args": {
        "title": "Meeting",
        "start": "2025-11-21T10:00:00+05:30",
        "end": "2025-11-21T10:30:00+05:30",
        "attendees": ["a@example.com"]
    }
}
