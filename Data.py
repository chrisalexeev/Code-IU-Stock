# this should be, at its core, a dictionary of lists
class Data(dict):
	def __init__(self, data=None):
		super().__init__()
		if data is not None:
			for key, val in data.items():
				self.add_data(key, val)

	def add_data(self, name, data):
		self[name] = data

	def __len__(self):
		return len(self[list(self.keys())[0]])