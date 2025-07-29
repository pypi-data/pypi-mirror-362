################ ENTITIES #######################

class EntityStorageException(Exception):
	"""docstring for EntityStorageException"""
	def __init__(self, *args, **kwargs):
		super(EntityStorageException, self).__init__(*args, **kwargs)

class EntitySnapshotException(Exception):
	"""docstring for EntitySnapshotException"""
	def __init__(self, *args, **kwargs):
		super(EntitySnapshotException, self).__init__(*args, **kwargs)

class EntityQueringException(Exception):
	"""docstring for EntityQueringException"""
	def __init__(self, *args, **kwargs):
		super(EntityQueringException, self).__init__(*args, **kwargs)

class EntityRelationException(Exception):
	"""docstring for EntityRelationException"""
	def __init__(self, *args, **kwargs):
		super(EntityRelationException, self).__init__(*args, **kwargs)


################ JOINS #######################

class JoinException(Exception):
	"""docstring for JoinException"""
	def __init__(self, *args, **kwargs):
		super(JoinException, self).__init__(*args, **kwargs)

class JoinStorageException(Exception):
	"""docstring for JoinStorageException"""
	def __init__(self, *args, **kwargs):
		super(JoinStorageException, self).__init__(*args, **kwargs)

class JoinQueryingException(Exception):
	"""docstring for JoinQueryingException"""
	def __init__(self, *args, **kwargs):
		super(JoinQueryingException, self).__init__(*args, **kwargs)


################ TRANSLATION #######################

class AttributeTranslatorException(Exception):
	"""docstring for AttributeTranslatorException"""
	def __init__(self, *args, **kwargs):
		super(AttributeTranslatorException, self).__init__(*args, **kwargs)

class ConditionTranslatorException(Exception):
	"""docstring for ConditionTranslatorException"""
	def __init__(self, *args, **kwargs):
		super(ConditionTranslatorException, self).__init__(*args, **kwargs)

class BeforeHandUnmatchedCondition(Exception):
	"""docstring for BeforeHandUnmatchedCondition"""
	def __init__(self, *args, **kwargs):
		super(BeforeHandUnmatchedCondition, self).__init__(*args, **kwargs)