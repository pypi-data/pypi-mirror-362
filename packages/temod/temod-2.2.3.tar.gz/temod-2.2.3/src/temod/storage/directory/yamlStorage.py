from .directoryStorage import DirectoryStorage
from temod.base.entity import Entity
from temod.base.attribute import *
from copy import deepcopy

import random
import yaml
import os


class YamlStorage(DirectoryStorage):
	"""docstring for YamlStorage"""
	def __init__(self, directory, mode="", encoding="utf-8",createDir=False):
		super(YamlStorage, self).__init__(directory,mode="",encoding=encoding,createDir=createDir)

	def save(self, id_, object_, encoding=None):
		self.write(id_, yaml.dump(object_), encoding=encoding if not encoding is None else self.encoding)

	def load(self, id_, encoding=None):
		return yaml.safe_load(self.read(id_,encoding=encoding if not encoding is None else self.encoding))

	def list(self, skip=None, limit=None, with_id=False):
		nb = -1; sent = 0;
		for file in self.content(only_files=True):
			nb += 1
			if skip is not None and nb <= skip:
				continue
			if limit is not None and sent == limit:
				break
			sent += 1
			if with_id:
				yield file, self.load(file)
			else:
				yield self.load(file)


class YamlEntityStorage(YamlStorage):
	"""docstring for YamlEntityStorage"""
	def __init__(self, directory, entity_type, **kwargs):
		super(YamlEntityStorage, self).__init__(directory,**kwargs)
		try:
			assert(issubclass(entity_type,Entity))
			self.entity_type = entity_type
		except AssertionError:
			raise EntityStorageException(f"Entity type {entity_type.__name__} is not a subclass of Entity")

	#############################################

	# VERIFICATIONS

	def verify_entity(self,entity):
		try:
			assert(issubclass(type(entity),self.entity_type))
		except AssertionError:
			raise EntityStorageException(f"Entity type {type(entity).__name__} cannot be stored in Entity {self.entity_type.__name__} storage")
		
	#############################################

	def create(self, entity):
		self.verify_entity(entity)
		ids = [value for attr,value in entity.attributes.items() if value.is_id]
		if len(ids) > 1 or len(ids) == 0:
			raise Exception("Only entites with one identifier can be stored")
		id_ = ids[0]
		if not issubclass(type(id_),StringAttribute) and not issubclass(type(id_),IntegerAttribute):
			raise Exception("Only entites with string or integer identifier can be stored")
		self.save(str(id_.value),entity.to_dict())
		return id_

	def get(self, *ids):
		if len(ids) == 0 or len(ids) > 0:
			raise Exception("Exactely one identifier is required to fetch entity.")
		return self.entity_type.from_dict(self.load(str(ids[0].value)))

	def list(self, skip=None, limit=None):
		nb = -1; sent = 0;
		for file in self.content(only_files=True):
			nb += 1
			if skip is not None and nb <= skip:
				continue
			if limit is not None and sent == limit:
				break
			sent += 1
			yield self.entity_type.from_dict(self.load(file))


class YamlEntitiesStorage(YamlStorage):
	"""docstring for YamlEntitiesStorage"""
	def __init__(self, directory, entity_type, keep_loaded=False, **kwargs):
		super(YamlEntitiesStorage, self).__init__(directory,**kwargs)
		try:
			assert(issubclass(entity_type,Entity))
			self.entity_type = entity_type
		except AssertionError:
			raise EntityStorageException(f"Entity type {entity_type.__name__} is not a subclass of Entity")
		self.entity_name = entity_type.ENTITY_NAME if hasattr(entity_type,'ENTITY_NAME') else entity_type.__name__

		attrs = deepcopy(entity_type.ATTRIBUTES)
		self.entity_attributes = {
			attr.pop('name'):attr for attr in attrs
		}
		entity_ids = [attr for attr, value in self.entity_attributes.items() if value.get('is_id',False)]
		
		if len(entity_ids) > 1 or len(entity_ids) == 0:
			raise Exception("Only entites with one identifier can be stored")
		self.entity_id = entity_ids[0]
		id_type = self.entity_attributes[self.entity_id]['type']
		if not issubclass(id_type,StringAttribute) and not issubclass(id_type,IntegerAttribute):
			raise Exception("Only entites with string or integer identifier can be stored")
		self.file = os.path.join(self.directory, f'{self.entity_name}.yml')
		self.keep_loaded = keep_loaded
		self._loaded_content = None

	#############################################

	# VERIFICATIONS

	def verify_entity(self,entity):
		try:
			assert(issubclass(type(entity),self.entity_type))
		except AssertionError:
			raise EntityStorageException(f"Entity type {type(entity).__name__} cannot be stored in Entity {self.entity_type.__name__} storage")
		
	#############################################

	def _generate_random_str(length=5):
		alp = ["abcdefghijklmnopqrstuvwxyz"]
		return "".join([alp[random.randint(0,len(alp)-1)] for _ in range(length)])

	def _load_content(self, force_reload=False):
		if not force_reload and self.keep_loaded:
			if self._loaded_content is None:
				self._loaded_content = self._load_content(force_reload=True)
			return self._loaded_content
		if not os.path.isfile(self.file):
			return {}
		with open(self.file) as file:
			content = yaml.safe_load(file.read())
		return {entity[self.entity_id]:self.entity_type(**entity) for entity in content}

	def _save_content(self, content):
		if self.keep_loaded:
			self._loaded_content = content
		temp_file_name = None
		while temp_file_name is None or os.path.isfile(temp_file_name):
			temp_file_name = os.path.join(self.directory,f'{self.entity_name}.temp{YamlEntitiesStorage._generate_random_str()}.yml')
		try:
			with open(temp_file_name,'w') as file:
				file.write(yaml.dump([entity.to_dict() for entity in content.values()]))
		except:
			raise
		else:
			os.rename(temp_file_name,self.file)

	#############################################

	def create(self, entity):
		self.verify_entity(entity)
		content = self._load_content()
		if entity[self.entity_id] in content:
			raise Exception(f'{self.entity_type} with id {id_} already exists')
		content[entity[self.entity_id]] = entity
		self._save_content(content)
		return entity[self.entity_id]

	def get(self, *attributes, **kwargs):
		content = self._load_content()
		for entity in content.values():
			if all([attr == entity.attributes[attr.name] for attr in attributes]):
				if all([entity[k] == v for k,v in kwargs.items()]):
					return entity

	def list(self, *attributes, skip=None, limit=None, **kwargs):
		nb = 0; sent = 0;
		content = self._load_content()
		for entity in content.values():
			if any([attr != entity.attributes[attr.name] for attr in attributes]):
				if any([entity[k] != v for k,v in kwargs.items()]):
					continue
			nb += 1
			if skip is not None and nb <= skip:
				continue
			if limit is not None and sent == limit:
				break
			sent += 1
			yield entity

	def updateOnSnapshot(self,entity,overwrite_existant=False):
		self._verify_entity(entity)
		if entity.snapshot is None:
			raise EntitySnapshotException("No snapshot to recover data from")
		updates = [
			attribute for attribute in entity.attributes.values()
			if entity.snapshot[attribute.name].value != attribute.value
		]
		if len(updates) > 0:
			content = self._load_content()
			updated_id = [attribute for attribute in updates if attribute.is_id]
			if len(updated_id) > 0 and not overwrite_existant:
				if updated_id[0].value in content:
					raise Exception(f"Another entity with id {updated_id[0].value} already exists")
				content.pop(updated_id[0].value)
			content[entity[self.entity_id]] = entity
			self._save_content(content)
			return entity
		return False