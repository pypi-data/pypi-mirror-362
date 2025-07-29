from temod.base.entity import Entity
from copy import deepcopy

class SimpleSynchronizer(object):
	"""Achieve synchronization between two or more storages insuring that the exact same entities exists in both"""
	def __init__(self, entity_type, *storages):
		super(SimpleSynchronizer, self).__init__()
		self.storages = list(storages)
		if len(storages) < 2:
			raise Exception("At least two storages are needed to perform synchronization")
		try:
			assert(issubclass(entity_type,Entity))
			self.entity_type = entity_type
		except AssertionError:
			raise Exception(f"Entity type {entity_type.__name__} is not a subclass of Entity")

		self.entity_name = entity_type.ENTITY_NAME if hasattr(entity_type,'ENTITY_NAME') else entity_type.__name__
		attrs = deepcopy(entity_type.ATTRIBUTES)
		self.entity_attributes = {
			attr.pop('name'):attr for attr in attrs
		}
		self.entity_ids = [attr for attr, value in self.entity_attributes.items() if value.get('is_id',False)]
		if not all([issubclass(storage.entity_type,self.entity_type) for storage in storages]):
			raise Exception(f"Not all storages store the entity type {self.entity_type}")

	def synchronize_storage(self, storage):
		for entity in storage.list():
			for other in self.storages:
				if storage is other:
					continue
				found = other.get(**{id_:entity[id_] for id_ in self.entity_ids})
				if found is None:
					other.create(entity)
				elif any([found[attr] != entity[attr] for attr in self.entity_attributes]):
					found.takeSnapshot()
					for attr in self.entity_attributes:
						found[attr] = entity[attr]
					other.updateOnSnapshot(found)

	def synchronize(self):
		for storage in self.storages:
			self.synchronize_storage(storage)