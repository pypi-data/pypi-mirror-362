class MalformedConditionException(Exception):
	"""docstring for MalformedConditionException"""
	def __init__(self, *args, **kwargs):
		super(MalformedConditionException, self).__init__(*args, **kwargs)
		
#################################################

class Condition(object):
	"""docstring for Condition"""
	def __init__(self):
		super(Condition, self).__init__()

class Not(Condition):
	"""docstring for Not"""
	def __init__(self,condition,**kwargs):
		super(Not, self).__init__(**kwargs)
		try:
			assert(issubclass(type(condition),Condition))
		except AssertionError:
			raise MalformedConditionException("condition must be a subclass of Condition")
		self.condition = condition

class And(Condition):
	"""docstring for And"""
	def __init__(self,*conditions,**kwargs):
		super(And, self).__init__(**kwargs)
		try:
			assert(all([issubclass(type(condition),Condition) for condition in conditions]))
		except AssertionError:
			raise MalformedConditionException("condition must be a subclass of Condition")
		self.conditions = conditions

class Or(Condition):
	"""docstring for Or"""
	def __init__(self,*conditions,**kwargs):
		super(Or, self).__init__(**kwargs)
		try:
			assert(all([issubclass(type(condition),Condition) for condition in conditions]))
		except AssertionError:
			raise MalformedConditionException("condition must be a subclass of Condition")
		self.conditions = conditions

#################################################

class Equals(Condition):
	"""docstring for Equals"""
	def __init__(self,field1,field2=None,**kwargs):
		super(Equals, self).__init__(**kwargs)
		self.field1 = field1
		self.field2 = field2

class Inferior(Condition):
	"""docstring for Inferior"""
	def __init__(self,field1,field2=None,strict=False,**kwargs):
		super(Inferior, self).__init__(**kwargs)
		self.field1 = field1
		self.field2 = field2
		self.strict = strict

class Superior(Condition):
	"""docstring for Superior"""
	def __init__(self,field1,field2=None,strict=False,**kwargs):
		super(Superior, self).__init__(**kwargs)
		self.field1 = field1
		self.field2 = field2
		self.strict = strict

class Between(Condition):
	"""docstring for Between"""
	def __init__(self,field,inf=None,sup=None,**kwargs):
		super(Between, self).__init__(**kwargs)
		self.field = field
		self.inf = inf
		self.sup = sup

#################################################

class StartsWith(Condition):
	"""docstring for StartsWith"""
	def __init__(self,field,case_sensitive=True,**kwargs):
		super(StartsWith, self).__init__(**kwargs)
		self.field = field
		self.case_sensitive = case_sensitive

class EndsWith(Condition):
	"""docstring for EndsWith"""
	def __init__(self,field,case_sensitive=True,**kwargs):
		super(EndsWith, self).__init__(**kwargs)
		self.field = field
		self.case_sensitive = case_sensitive

class Contains(Condition):
	"""docstring for Contains"""
	def __init__(self,field,case_sensitive=True,**kwargs):
		super(Contains, self).__init__(**kwargs)
		self.field = field
		self.case_sensitive = case_sensitive


#################################################

class In(Condition):
	"""docstring for In"""
	def __init__(self,field,*values,**kwargs):
		super(In, self).__init__(**kwargs)
		self.field = field
		self.values = values
		