class TasksTool:
    def __init__(self):
        self.tasks = []

    def add_task(self, args):
        task = {"id": f"task_{len(self.tasks)+1}", **args}
        self.tasks.append(task)
        return {"status":"created","task": task}

    def list_today(self):
        return self.tasks[:10]
