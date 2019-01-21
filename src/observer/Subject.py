from abc import ABC


class Subject(ABC):
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    async def notify(self, action, *args):
        for o in self.observers:
            await o.update(action, *args)
