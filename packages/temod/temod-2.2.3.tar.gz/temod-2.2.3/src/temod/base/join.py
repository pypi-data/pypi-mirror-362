from .entity import Entity
from .constraint import *


class MalformedJoin(Exception):
	pass
		

class Join(object):
	"""docstring for Join"""
	def __init__(self, *entities,**kwargs):
		super(Join, self).__init__()
		try:
			assert(all([issubclass(type(entity),Entity) for entity in entities]))
			self.entities = {entity.name():entity for entity in entities}
		except AssertionError:
			raise MalformedJoin(f"all args must be of type Entity")
		self.exoskeleton = kwargs
		self._complete_exoskeleton(*entities)

	def add_entity(self,entity):
		if not issubclass(type(entity),Entity) :
			raise MalformedJoin(f"added entity must be of type Entity not {type(entity)}")
		self.entities[entity.name()] = entity
		self._complete_exoskeleton(entity)

	def _complete_exoskeleton(self,*entities):
		for entity in entities:
			for attr in entity.ATTRIBUTES:
				if not attr['name'] in self.exoskeleton:
					self.exoskeleton[attr['name']] = f"{entity.name()}.{attr['name']}"

	#####################################################

	def __getitem__(self,name): 
		if name in self.entities:
			return self.entities[name]
		if name in self.exoskeleton:
			path = self.exoskeleton[name].split('.')
			return self.entities[path[0]][path[1]]
		raise ValueError(f'Unknown attribute/entity {name}')

	def __setitem__(self,name,value): 
		if name in self.entities and issubclass(type(value),Entity) and value.name() == name:
			self.entities[name] = value

		if name in self.exoskeleton:
			path = self.exoskeleton[name].split('.')
			self.entities[path[0]][path[1]] = value

	#####################################################

	def takeSnapshot(self):
		for entity in self.entities.values():
			entity.takeSnapshot()
		return self

	#####################################################

	def to_dict(self,include=None):
		include = include if include is not None else {}
		return {
			name:entity.to_dict(include=include.get(name,None)) for name,entity in self.entities.items()
		}

	def __repr__(self):
		entities = []
		for entity in self.entities.values():
			attributes = [f"{attr.name} ({type(attr).__name__}): {attr.value} ({type(attr.value).__name__})" for attr in entity.attributes.values()]
			entities.append(f"""Entity {entity.name()}"""+((":\n\t\t"+"\n\t\t".join(attributes)) if len(attributes) > 0 else ""))
		return f"""Join {type(self).__name__}"""+((":\n\t"+"\n\t".join(entities)) if len(self.entities) > 0 else "")

	#####################################################


		