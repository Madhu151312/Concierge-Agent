from agent.controller import ConciergeAgent
from workflows.morning_briefing import morning_briefing
from workflows.auto_reply import auto_reply_demo

def cli():
    agent = ConciergeAgent()
    print('Concierge Agent CLI — type "exit" to quit. Try: "Schedule a 30 min meeting with Alice next week" or "Morning briefing"')
    while True:
        u = input('> ')
        if u.strip().lower() in ('exit','quit'):
            break
        if 'morning briefing' in u.lower():
            print(morning_briefing(agent))
            continue
        if 'auto reply' in u.lower():
            print(auto_reply_demo(agent))
            continue
        out = agent.handle(u)
        print(out)

if __name__ == '__main__':
    cli()
