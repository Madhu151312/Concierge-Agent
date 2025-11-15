from agent.memory import Memory
from agent.router import Router
from tools.calendar_tool import CalendarTool
from tools.email_tool import EmailTool
from tools.tasks_tool import TasksTool
from tools.websearch_tool import WebSearchTool

class ConciergeAgent:
    def __init__(self):
        self.memory = Memory()
        tools = {
            "calendar": CalendarTool(),
            "email": EmailTool(),
            "tasks": TasksTool(),
            "websearch": WebSearchTool()
        }
        self.router = Router(self.memory, tools)

    def handle(self, user_message):
        response = self.router.process(user_message)
        # Save into short-term memory
        self.memory.add_short(user_message, str(response))
        return response
