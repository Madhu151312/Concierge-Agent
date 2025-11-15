class EmailTool:
    def __init__(self):
        # In production: use Gmail API / IMAP with OAuth
        self.inbox = [
            {"from":"acme@example.com","subject":"Pricing update","snippet":"Please confirm pricing..."},
            {"from":"boss@example.com","subject":"Weekly sync","snippet":"We need the slide deck by Monday."}
        ]

    def fetch_unread(self, args):
        # args can include 'important_only'
        return self.inbox

    def draft_reply(self, message_id, draft_text):
        # returns a draft object
        return {"status":"drafted","message_id": message_id, "draft": draft_text}

    def send(self, message_id, draft_text):
        return {"status":"sent","message_id": message_id}
