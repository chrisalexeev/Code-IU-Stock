# this should be, at its core, a dictionary of lists
class Data(dict):
	def __init__(self, data=None):
		super().__init__()
		if data is not None:
			for key, val in data.items():
				self.add_data(key, val)

	# adds a list to the data
	def add_data(self, name, data):
		self[name] = data

	# adds a single value to a field, or creates a new one if it doesn't already exist
	def add_point(self, name,  point):
		if name not in self.keys():
			self[name] = []
		self[name].append(point)

	def has_field(self, name):
		return name in self.keys()

	def __len__(self):
		return len(self[list(self.keys())[0]])