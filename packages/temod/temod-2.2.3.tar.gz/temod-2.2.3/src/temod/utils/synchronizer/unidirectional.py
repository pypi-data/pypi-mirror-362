from temod.base.entity import Entity
from copy import deepcopy

class MasterSlaveSynchronizer(object):
	"""Achieve synchronization between one master storage and two or more slave storages insuring that the exact same entities existing in the master storage exist in slave storages"""
	def __init__(self, entity_type, master, *slaves):
		super(MasterSlaveSynchronizer, self).__init__()
		self.storages = [master]+list(slaves)
		self.master = master
		self.slaves = slaves
		if len(self.storages) < 2:
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
		if not all([issubclass(storage.entity_type,self.entity_type) for storage in self.storages]):
			raise Exception(f"Not all storages store the entity type {self.entity_type}")

	def synchronize(self):
		for entity in self.master.list():
			for slave in self.slaves:
				found = slave.get(**{id_:entity[id_] for id_ in self.entity_ids})
				if found is None:
					slave.create(entity)
				elif any([found[attr] != entity[attr] for attr in self.entity_attributes]):
					found.takeSnapshot()
					for attr in self.entity_attributes:
						found[attr] = entity[attr]
					slave.updateOnSnapshot(found)
		for slave in self.slaves:
			for entity in slave.list():
				ids = {id_:entity[id_] for id_ in self.entity_ids}
				found = self.master.get(**ids)
				if found is None:
					slave.delete(**ids)