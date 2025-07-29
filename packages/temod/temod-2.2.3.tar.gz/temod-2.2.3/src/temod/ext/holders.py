from temod.base import Cluster, Entity, Join

from temod.storage.mysql import *

import traceback
import importlib
import os


STORAGE_FROM_NAME = {
	"mysql":{
		"entity":MysqlEntityStorage,
		"join":MysqlJoinStorage,
		"cluster":MysqlClusterStorage
	}
}


class temodHolderException(Exception):
	"""docstring for temodHolderException"""
	def __init__(self, *args, **kwargs):
		super(temodHolderException, self).__init__(*args, **kwargs)



class EntitiesHolder(object):
	"""docstring for EntitiesHolder"""
	def __init__(self):
		super(EntitiesHolder, self).__init__()
		self._entities_dir_ = None
		self._entities_ = {}

	def __getattribute__(self,name): 
		try:
			if name != "_entities_":
				et = self._entities_
				if name in et:
					return et['name']
				found = []
				for k,v in et.items():
					if name in v:
						found.append([k,name])
				if len(found) > 1:
					raise temodHolderException(f'The name {name} is ambigous for the holder. It can refer to any of the following {",".join([".".join(f) for f in found])}')
				return et[found[0][0]][found[0][1]]
		except:
			pass
		return super(EntitiesHolder,self).__getattribute__(name)

	def list(self):
		for entities in self._entities_.values():
			for name,entity in entities.items():
				if name == "__module__":
					continue
				yield entity

	def tuples(self):
		for category,entities in self._entities_.items():
			for name,entity in entities.items():
				if name == "__module__":
					continue
				yield category, name, entity

	def set_directory(self,directory):
		self._entities_dir_ = directory
		if not directory is None and os.path.isdir(directory):
			self._reload_entities()

	def set_unique_storage(self,type_,credentials,exceptions=None):
		if exceptions is None:
			exceptions = {}
		for k,v in self._entities_.items():
			for a,entity in v.items():
				if a == "__module__":
					continue
				if a in exceptions:
					storage = exceptions[a]
				else:
					storage = type_(entity,**credentials)
				if hasattr(entity,"storage"):
					entity.STORAGE = storage
				else:
					entity.storage = storage

	def _reload_entities(self):
		i = 0
		for file in os.listdir(self._entities_dir_):
			if file.endswith('.py'):
				module_name = file.rsplit('.py',1)[0]
				spec = importlib.util.spec_from_file_location(module_name, os.path.join(self._entities_dir_,file))
				self._entities_[module_name] = {'__module__':importlib.util.module_from_spec(spec)}
				try:
					spec.loader.exec_module(self._entities_[module_name]['__module__'])
					for content in dir(self._entities_[module_name]['__module__']):
						e = getattr(self._entities_[module_name]['__module__'],content)
						if type(e) is type:
							if issubclass(e,Entity) and not e in [Entity,AutoCompleteEntity]:
								self._entities_[module_name][e.__name__] = e
								e.__file__ = os.path.abspath(self._entities_[module_name]['__module__'].__file__)
								print(f"Entity {e.__name__} has been loaded successfully")
								i += 1
				except:
					print(f"Error while loading entity {module_name} from {os.path.join(self._entities_dir_,file)}")
					traceback.print_exc()
		print(f"{i} entities ve been loaded from {self._entities_dir_}")




class JoinsHolder(object):
	"""docstring for JoinsHolder"""
	def __init__(self):
		super(JoinsHolder, self).__init__()
		self._joins_dir_ = None
		self._joins_ = {}

	def __getattribute__(self,name): 
		try:
			if name != "_joins_":
				et = self._joins_
				if name in et:
					return et['name']
				found = []
				for k,v in et.items():
					if name in v:
						found.append([k,name])
				if len(found) > 1:
					raise temodHolderException(f'The name {name} is ambigous for the holder. It can refer to any of the following {", ".join([".".join(f) for f in found])}')
				return et[found[0][0]][found[0][1]]
		except:
			pass
		return super(JoinsHolder,self).__getattribute__(name)

	def list(self):
		for joins in self._joins_.values():
			for name,join in joins.items():
				if name == "__module__":
					continue
				yield join

	def tuples(self):
		for category,joins in self._joins_.items():
			for name,join in joins.items():
				if name == "__module__":
					continue
				yield category, name, join

	def set_directory(self,directory):
		self._joins_dir_ = directory
		if not directory is None and os.path.isdir(directory):
			self._reload_entities()

	def set_unique_storage(self,type_,credentials,exceptions=None):
		if exceptions is None:
			exceptions = {}
		for k,v in self._joins_.items():
			for a,join in v.items():
				if a == "__module__":
					continue
				if a in exceptions:
					storage = exceptions[a]
				else:
					storage = type_(join,**credentials)
				if hasattr(join,"storage"):
					join.STORAGE = storage
				else:
					join.storage = storage

	def _reload_entities(self):
		i = 0
		for file in os.listdir(self._joins_dir_):
			if file.endswith('.py'):
				module_name = file.rsplit('.py',1)[0]
				spec = importlib.util.spec_from_file_location(module_name, os.path.join(self._joins_dir_,file))
				self._joins_[module_name] = {"__module__":importlib.util.module_from_spec(spec)}
				try:
					spec.loader.exec_module(self._joins_[module_name]['__module__'])
					for content in dir(self._joins_[module_name]['__module__']):
						e = getattr(self._joins_[module_name]['__module__'],content)
						if type(e) is type:
							if issubclass(e,Join) and e is not Join:
								self._joins_[module_name][e.__name__] = e
								e.__file__ = os.path.abspath(self._joins_[module_name]['__module__'].__file__)
								print(f"Join {e.__name__} has been loaded successfully")
								i += 1
				except:
					print(f"Error while loading join {module_name} from {os.path.join(self._joins_dir_,file)}")
					traceback.print_exc()
		print(f"{i} joins have been loaded from {self._joins_dir_}")




class ClustersHolder(object):
	"""docstring for ClustersHolder"""
	def __init__(self):
		super(ClustersHolder, self).__init__()
		self._clusters_dir_ = None
		self._clusters_ = {}

	def __getattribute__(self,name): 
		try:
			if name != "_clusters_":
				et = self._clusters_
				if name in et:
					return et['name']
				found = []
				for k,v in et.items():
					if name in v:
						found.append([k,name])
				if len(found) > 1:
					raise temodHolderException(f'The name {name} is ambigous for the holder. It can refer to any of the following {", ".join([".".join(f) for f in found])}')
				return et[found[0][0]][found[0][1]]
		except:
			pass
		return super(ClustersHolder,self).__getattribute__(name)

	def list(self):
		for clusters in self._clusters_.values():
			for name,cluster in clusters.items():
				if name == "__module__":
					continue
				yield cluster

	def tuples(self):
		for category,clusters in self._clusters_.items():
			for name,cluster in clusters.items():
				if name == "__module__":
					continue
				yield category, name, cluster

	def set_directory(self,directory):
		self._clusters_dir_ = directory
		if not directory is None and os.path.isdir(directory):
			self._reload_entities()

	def set_unique_storage(self,type_,credentials,exceptions=None):
		if exceptions is None:
			exceptions = {}
		for k,v in self._clusters_.items():
			for a,cluster in v.items():
				if a == "__module__":
					continue
				if a in exceptions:
					storage = exceptions[a]
				else:
					storage = type_(cluster,**credentials)
				if hasattr(cluster,"storage"):
					cluster.STORAGE = storage
				else:
					cluster.storage = storage

	def _reload_entities(self):
		i = 0
		for file in os.listdir(self._clusters_dir_):
			if file.endswith('.py'):
				module_name = file.rsplit('.py',1)[0]
				spec = importlib.util.spec_from_file_location(module_name, os.path.join(self._clusters_dir_,file))
				self._clusters_[module_name] = {"__module__":importlib.util.module_from_spec(spec)}
				try:
					spec.loader.exec_module(self._clusters_[module_name]['__module__'])
					for content in dir(self._clusters_[module_name]['__module__']):
						e = getattr(self._clusters_[module_name]['__module__'],content)
						if type(e) is type:
							if issubclass(e,Cluster) and e is not Cluster:
								self._clusters_[module_name][e.__name__] = e
								e.__file__ = os.path.abspath(self._clusters_[module_name]['__module__'].__file__)
								print(f"Cluster {e.__name__} has been loaded successfully")
								i += 1
				except:
					print(f"Error while loading cluster {module_name} from {os.path.join(self._clusters_dir_,file)}")
					traceback.print_exc()
		print(f"{i} clusters have been loaded from {self._clusters_dir_}")





def init_holders(base_dir=None, entities_dir=None, joins_dir=None, clusters_dir=None, databases=None, db_credentials=None, exceptions=None):

	if base_dir is None and entities_dir is None and joins_dir is None and clusters_dir is None:
		raise temodHolderException('At least one of the following paths must be non null: base_dir, entities_dir, joins_dir or clusters_dir')

	entities_dir = entities_dir if not entities_dir is None else (None if base_dir is None else os.path.join(base_dir,'entities'))
	joins_dir = joins_dir if not joins_dir is None else (None if base_dir is None else os.path.join(base_dir,'joins'))
	clusters_dir = clusters_dir if not clusters_dir is None else (None if base_dir is None else os.path.join(base_dir,'objects'))

	entities.set_directory(entities_dir)
	joins.set_directory(joins_dir)
	clusters.set_directory(clusters_dir)

	if db_credentials is None:
		db_credentials = {}
	if exceptions is None:
		exceptions = {}

	if type(databases) is dict:
		raise Exception("Not implemented yet")
	elif type(databases) is str:
		if not databases in STORAGE_FROM_NAME:
			raise Exception(f'Unknown database type "{databases}". Use one of the following values {",".join(list(STORAGE_FROM_NAME))}')
		entities.set_unique_storage(STORAGE_FROM_NAME[databases]['entity'],db_credentials,exceptions=exceptions)
		joins.set_unique_storage(STORAGE_FROM_NAME[databases]['join'],db_credentials,exceptions=exceptions)
		clusters.set_unique_storage(STORAGE_FROM_NAME[databases]['cluster'],db_credentials,exceptions=exceptions)
	else:
		raise Exception("databases option must be either a dict or a string.")



def init_context():
	
	for category, name, entity in entities.tuples():
		if name in __builtins__:
			print(f'Warning: cannot register entity {name} in the global context as {name} is already used');continue
		__builtins__[name] = entity

	for category, name, join in joins.tuples():
		if name in __builtins__:
			print(f'Warning: cannot register join {name} in the global context as {name} is already used');continue
		__builtins__[name] = join

	for category, name, cluster in clusters.tuples():
		if name in __builtins__:
			print(f'Warning: cannot register cluster {name} in the global context as {name} is already used');continue
		__builtins__[name] = cluster


entities = EntitiesHolder()
joins = JoinsHolder()
clusters = ClustersHolder()