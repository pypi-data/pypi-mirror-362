


class Aggregation(object):
	"""docstring for Aggregation"""
	def __init__(self):
		super(Aggregation, self).__init__()


class Window(Aggregation):
	"""docstring for Window"""
	def __init__(self,size, function, fill=False):
		super(Window, self).__init__()
		self.size = size
		self.function = function
		self.fill = fill


class Sum(Aggregation):
	"""docstring for Sum"""
	def __init__(self):
		super(Sum, self).__init__()
		