from collections import deque

class Memory:
    def __init__(self, short_k=8):
        self.short = deque(maxlen=short_k)
        self.long = {}  # simple key-value store

    def add_short(self, user, assistant):
        self.short.append({"user": user, "assistant": assistant})

    def get_short(self):
        return list(self.short)

    def set_pref(self, key, value):
        self.long[key] = value

    def get_pref(self, key, default=None):
        return self.long.get(key, default)
