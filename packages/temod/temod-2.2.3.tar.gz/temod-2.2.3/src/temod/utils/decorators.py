from temod.base.entity import Entity
from temod.base.join import Join


class DecoratorException(Exception):
	pass



class DecoratedAttribute(object):
	"""docstring for DecoratedAttribute"""
	def __init__(self, attribute,decoration=None):
		super(DecoratedAttribute, self).__init__()
		for k,v in attribute.items():
			setattr(self,k,v)
		if not decoration is None:
			for k,v in decoration.items():
				setattr(self,k,v)



class EntityDecorator(object):
	"""docstring for EntityDecorator"""
	def __init__(self, entity_type, decorator,decoration=None):
		super(EntityDecorator, self).__init__()
		self.entity_type = entity_type
		self.decorator = decorator

		if not decoration is None:
			for k,v in decoration.items():
				setattr(self,k,v)

		if not issubclass(entity_type,Entity):
			raise DecoratorException(f"Entity type {entity_type.__name__} is not a subclass of Entity")

	def attributes(self,include_undecorated=True):
		for attribute in self.entity_type.ATTRIBUTES:
			decor = self.decorator.get(attribute['name'],None)
			if decor is None and not include_undecorated:
				continue
			yield DecoratedAttribute(attribute,decoration=decor)



class JoinDecorator(object):
	"""docstring for JoinDecorator"""
	def __init__(self, join_type, decorator):
		super(JoinDecorator, self).__init__()
		self.join_type = join_type
		self.decorator = decorator

		if not issubclass(join_type,Join):
			raise DecoratorException(f"Join type {join_type.__name__} is not a subclass of Join")

	def attributes(self,include_undecorated=True):
		entities = []

		for constraint in self.join_type.STRUCTURE:
			entities.extend([attribute.owner_type for attribute in constraint.attributes])

		for entity in set(entities):
			decor = self.decorator.get(getattr(entity,'ENTITY_NAME',entity.__name__),None)
			if decor is None and not include_undecorated:
				continue
			decorator = EntityDecorator(entity,decor)
			for attribute in decorator.attributes(include_undecorated=include_undecorated):
				yield attribute
		