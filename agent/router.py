# agent/router.py
import json
from agent.llm import GeminiLLM

# A small helper to normalize names
def normalize_tool_name(name: str) -> str:
    if not name:
        return name
    n = name.lower()
    # common suffixes / variants
    n = n.replace("_tool", "").replace("tool_", "").replace("-tool", "")
    n = n.replace("tool", "") if n.endswith("tool") else n
    n = n.strip()
    # map common vendor names to our local tool keys if needed
    aliases = {
        "calendar": "calendar",
        "calendarservice": "calendar",
        "calendar_tool": "calendar",
        "email": "email",
        "emailtool": "email",
        "email_tool": "email",
        "tasks": "tasks",
        "task": "tasks",
        "task_tool": "tasks",
        "websearch": "websearch",
        "search": "websearch",
        "search_tool": "websearch",
    }
    return aliases.get(n, n)

# Map LLM action names to actual tool methods if the JSON uses different verbs
ACTION_ALIASES = {
    # calendar
    "schedule_meeting": "create_event",
    "create_meeting": "create_event",
    "create_event": "create_event",
    "find_free": "find_free",
    # email
    "summarize_unread_emails": "fetch_unread",   # summarization is done by LLM; tool returns content
    "draft_reply": "draft_reply",
    "send_email": "send",
    # tasks
    "add_task": "add_task",
    "create_task": "add_task",
    "list_tasks": "list_today",
    # search
    "search": "search"
}

def _extract_tool_call(text_or_obj):
    """
    Accept either:
    - Python dict
    - JSON string
    Return normalized tuple: (tool_key, action_method_name, args_dict) or (None,None,None)
    """
    obj = None
    if isinstance(text_or_obj, str):
        try:
            obj = json.loads(text_or_obj.strip())
        except Exception:
            return None, None, None
    elif isinstance(text_or_obj, dict):
        obj = text_or_obj
    else:
        return None, None, None

    # Accept multiple key variants
    tool_raw = obj.get("tool") or obj.get("tool_name") or obj.get("toolName") or obj.get("toolName") if obj else None
    action_raw = obj.get("action") or obj.get("verb") or obj.get("operation")
    args_raw = obj.get("args") or obj.get("parameters") or obj.get("arguments") or {}

    tool_key = normalize_tool_name(tool_raw) if tool_raw else None
    # map action aliases
    action_mapped = ACTION_ALIASES.get(action_raw, action_raw)
    return tool_key, action_mapped, args_raw or {}

class Router:
    def __init__(self, memory, tools: dict):
        """
        tools: a dict mapping normalized tool name -> tool instance
        Example: {"calendar": CalendarTool(), "email": EmailTool(), ...}
        """
        self.llm = GeminiLLM()
        self.memory = memory
        self.tools = tools

    def _confirm_and_execute(self, tool, action_name, args):
        """
        Ask user for confirmation for non-read-only actions.
        Returns string result or message.
        """
        # define which actions require explicit confirmation
        confirm_required_for = {"create_event", "send", "delete", "update", "send_email", "add_task"}

        pretty_preview = f"Tool: {tool.__class__.__name__}\nAction: {action_name}\nArgs: {json.dumps(args, indent=2)}"
        if action_name in confirm_required_for:
            print("Agent proposes the following action:")
            print(pretty_preview)
            # ask user to confirm
            resp = input("Confirm and execute this action? (yes/no): ").strip().lower()
            if resp not in ("y","yes"):
                return "Action cancelled by user."
        # Execute the method if exists
        fn = getattr(tool, action_name, None)
        if not fn:
            return f"Tool '{tool.__class__.__name__}' has no action '{action_name}'."
        try:
            result = fn(args)
            return f"[Tool:{tool.__class__.__name__}.{action_name}] -> {result}"
        except Exception as e:
            return f"[Tool:{tool.__class__.__name__}.{action_name}] ERROR: {type(e).__name__} {e}"

    def process(self, user_message):
        """
        Main entry point: calls Gemini with a tool-call protocol, then executes the tool if JSON returned.
        If Gemini returns plain text, returns it to caller.
        """
        # Build prompt with short context
        history = self.memory.get_short()
        ctx = "\n".join([f"User: {h['user']}\nAssistant: {h['assistant']}" for h in history[-6:]])
        prompt = f"You are a concierge agent. If you want to call a tool, respond with JSON exactly.\n{ctx}\nUser: {user_message}\nAssistant:"
        llm_output = self.llm.generate(prompt)

        # Try to parse the LLM output: it may be plain text or JSON describing a tool call.
        tool_key, action_name, args = _extract_tool_call(llm_output)

        if not tool_key:
            # Not a tool call — save and return textual reply
            return llm_output

        # If tool key present, find matching tool instance
        tool = self.tools.get(tool_key)
        if not tool:
            # try fallback: maybe user provided 'calendar_tool' -> normalized above; nothing matched
            return f"Error: tool '{tool_key}' not available."

        # Map some action names if necessary (already done in _extract_tool_call),
        # but permit direct method name if action_name matches a callable.
        # Final guard: if the action_name is None, attempt to choose a default
        if not action_name:
            # choose default action per tool
            defaults = {"calendar":"find_free", "email":"fetch_unread", "tasks":"list_today", "websearch":"search"}
            action_name = defaults.get(tool_key)

        # Execute (with confirmation if needed)
        return self._confirm_and_execute(tool, action_name, args)
