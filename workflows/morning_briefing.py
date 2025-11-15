def morning_briefing(agent):
    # This function demonstrates a simple morning briefing workflow using tools.
    inbox = agent.router.tools['email'].fetch_unread({})
    events = agent.router.tools['calendar'].find_free({'range':'today'})
    tasks = agent.router.tools['tasks'].list_today()
    summary = f"Morning Briefing:\n- {len(events)} suggested free slots\n- {len(inbox)} unread important emails\- {len(tasks)} tasks today\n"
    return summary
