from abc import ABC

class Subject(ABC):
	def __init__(self):
		self.observers = []

	def attach(self, observer):
		self.obser;;;vers.append(observer)

	def detach(self, observer):
		self.observers.remove(observer)

	def notify(self, action):
		for o in self.observers:
			o.update(action)
