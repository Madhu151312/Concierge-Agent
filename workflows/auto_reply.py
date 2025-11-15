def auto_reply_demo(agent, message_from='acme@example.com'):
    unread = agent.router.tools['email'].fetch_unread({})
    # pick first match
    for i,msg in enumerate(unread):
        if message_from in msg.get('from',''):
            draft = agent.router.tools['email'].draft_reply(i, "Thanks for the update. We'll review and revert shortly.")
            return draft
    return {'status':'no_message_found'}
