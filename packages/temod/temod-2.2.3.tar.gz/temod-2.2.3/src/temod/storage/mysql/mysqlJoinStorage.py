from .mysqlAttributesTranslator import MysqlAttributesTranslator
from .mysqlConditionsTranslator import MysqlConditionsTranslator
from .mysqlEntityStorage import MysqlEntityStorage
from .mysqlStorage import MysqlStorage

from temod.base.attribute import *
from temod.base.condition import *
from temod.base.entity import Entity
from temod.base.join import Join

from temod.storage.exceptions import *

from copy import deepcopy

#############################################

# MAIN CLASS

class MysqlJoinStorage(MysqlStorage):
	"""docstring for MysqlJoinStorage"""
	def __init__(self, join_type, **kwargs):
		super(MysqlJoinStorage, self).__init__(**kwargs)
		if not issubclass(join_type,Join):
			raise JoinStorageException("join_type must be a subclass of Join")
		if not hasattr(join_type,"STRUCTURE"):
			raise JoinStorageException("The joined entity structure must be specified")

		self.join_type = join_type
		if hasattr(join_type,"DEFAULT_ENTRY"):
			self.default_entry = join_type.DEFAULT_ENTRY
		else:
			self.default_entry = join_type.STRUCTURE[0].default_entry()

		if not issubclass(self.default_entry,Entity):
			raise JoinStorageException("join default entry must be a subclass of Entity")

		self.default_entry_name = getattr(self.default_entry,"ENTITY_NAME",self.default_entry.__name__)


	#############################################

	# ENTITY GENERATION

	def _entity_gen(entity_type,dct,copy=False):
		dct = deepcopy(dct) if copy else dct
		return entity_type(*[
			attr['type'](attr['name'],value=attr['type'].decode(dct.pop(attr['name'])),**{a:b for a,b in attr.items() if not (a in ['name','type','required'])}) 
			for attr in entity_type.ATTRIBUTES 
			if attr.get('required',False)
		],*[
			attr['type'](attr['name'],value=attr['type'].decode(dct.pop(attr['name'],None)),**{a:b for a,b in attr.items() if not (a in ['name','type','required'])}) 
			for attr in entity_type.ATTRIBUTES 
			if not attr.get('required',False)
		])

	#############################################

	# VERIFICATIONS

	def verify_entries(self,*entries):
		try:
			assert(all([
				issubclass(type(entry),Attribute) or issubclass(type(entry),Condition) 
				for entry in entries
			]))
		except AssertionError:
			raise JoinQueryingException(f"Conditions must all be subtype of Attribute or Condition")

	#############################################

	# SQL BUILDERS

	def _build_entities_list(self,entry):
		entities_list = [entry]
		for constraint in self.join_type.STRUCTURE:
			ctype =  "" if (constraint.multiplicity.start == 1 and constraint.multiplicity.end == 1) else "LEFT"
			for entity in constraint.entities():
				if not (entity in entities_list):
					entities_list.append((
						entity, constraint.condition(), ctype
					))
					break
		return entities_list

	def _build_attributes(self,class_,**attributes):
		try:
			attrs = []
			for i,j in attributes.items():
				ar = [attr for attr in class_.ATTRIBUTES if attr['name'] == i][0]
				attrs.append(ar['type'](i,value=j,owner_name=class_.ENTITY_NAME, **{
					a:b for a,b in ar.items() if not (a in ['type','required','no_check','name','owner_name','value'])
				},no_check=True))
			return attrs
		except IndexError as e:
			absent = [attr for attr in attributes if not(attr in [a['name'] for a in class_.ATTRIBUTES])]
			raise JoinException(f"Entity {class_.ENTITY_NAME} does not have following attributes: {','.join(absent)}")

	def _build_condition(self,entry,*entries,**kwargs):
		self.verify_entries(*entries)

		attributes = self._build_attributes(entry,**kwargs)
		for attribute in entries:
			if issubclass(type(attribute),Attribute):
				if attribute.owner_name is None:
					attribute.owner_name = getattr(entry,'ENTITY_NAME',entry.__name__)
				attributes.append(attribute)

		all_conditions = [Equals(attribute,None) for attribute in attributes]
		all_conditions.extend([condition for condition in entries if issubclass(type(condition),Condition)])

		if len(all_conditions) == 0:
			condition = None
		elif len(all_conditions) == 1:
			condition = all_conditions[0]
		else:
			condition = And(*all_conditions)
		return condition

	def _build_join(self, constraints):
		join_query = ""
		for join in constraints:
			name = getattr(join[0],"ENTITY_NAME",join[0].__name__)
			join_query += f" {join[2]} JOIN {name} ON {MysqlConditionsTranslator.translate(join[1])}"
		return join_query

	def _build_selection(self, entities_list):
		to_sel = []
		for entity in entities_list:
			name = entity.ENTITY_NAME if hasattr(entity,"ENTITY_NAME") else entity.__name__
			to_sel.append(",".join([
				f"{name}.{attr['name']} as {name}__{attr['name']}" for attr in entity.ATTRIBUTES]
			))
		return ", ".join(to_sel)

	#############################################

	# BASIC OPERATIONS

	def get(self,*conditions,orderby=None,skip=None,entry=None,**kwargs):
		entry = self.default_entry if (entry is None) else entry
		condition = self._build_condition(entry,*conditions,**kwargs)
		list_ = self._build_entities_list(entry)
		entities = [list_[0]]+[entity[0] for entity in list_[1:]]
		entities_names = [(entity.ENTITY_NAME if hasattr(entity,"ENTITY_NAME") else entity.__name__) for entity in entities]

		query = f"""
			SELECT {self._build_selection(entities)} 
			FROM {getattr(list_[0],'ENTITY_NAME',list_[0].__name__)} {self._build_join(list_[1:])}
		"""
		if condition is not None:
			try:
				query += f" WHERE {MysqlConditionsTranslator.translate(condition)}"
			except BeforeHandUnmatchedCondition:
				return None
		
		result = self.getOne(query+" LIMIT 1")
		if result is not None:
			to_join = []; i = 0
			for entity,name in zip(entities,entities_names):
				try:
					to_join.append(MysqlJoinStorage._entity_gen(entity,{
						col.replace(f'{name}__',''):value for col,value in result.items() if col.startswith(f'{name}__')
					}))
				except:
					# Check if this might be caused by a left or right join
					if i == 0 or list_[i][2] == "":
						raise
				i += 1
			return self.join_type(*to_join,**getattr(self.join_type,'SHORTCUTS',{}))

	def create(self,join):
		if not type(join) is self.join_type:
			raise JoinStorageException(f'Cannot store {type(join)} into a MysqlJoinStorage of {self.join_type}')

		query = f"""
			SELECT {self._build_selection(entities)} 
			FROM {getattr(list_[0],'ENTITY_NAME',list_[0].__name__)} {self._build_join(list_[1:])}
		"""
		if condition is not None:
			try:
				query += f" WHERE {MysqlConditionsTranslator.translate(condition)}"
				result = self.getOne(query+" LIMIT 1")
			except BeforeHandUnmatchedCondition:
				result = None

		result = self.getOne(query+" LIMIT 1")
		if result is not None:
			to_join = []
			for entity,name in zip(entities,entities_names):
				try:
					to_join.append(MysqlJoinStorage._entity_gen(entity,{
						col.replace(f'{name}__',''):value for col,value in result.items() if col.startswith(f'{name}__')
					}))
				except:
					pass
			return self.join_type(*to_join,**getattr(self.join_type,'SHORTCUTS',{}))

	def delete(self,*conditions,many=False,**kwargs):
		condition = self._build_condition(*conditions,**kwargs)

		query = f"DELETE {self._build_selection()} FROM {self.base_name} {self._build_join()}"
		if condition is not None:
			try:
				query += f" WHERE {MysqlConditionsTranslator.translate(condition)}"
			except BeforeHandUnmatchedCondition:
				return None
		if not many:
			query += " LIMIT 1"
		return self.executeAndCommit(query).lastrowid


	def list(self,*conditions,orderby=None,skip=None,limit=None,entry=None,**kwargs):
		entry = self.default_entry if (entry is None) else entry
		condition = self._build_condition(entry,*conditions,**kwargs)
		list_ = self._build_entities_list(entry)
		entities = [list_[0]]+[entity[0] for entity in list_[1:]]
		entities_names = [(entity.ENTITY_NAME if hasattr(entity,"ENTITY_NAME") else entity.__name__) for entity in entities]

		query = f"""
			SELECT {self._build_selection(entities)} 
			FROM {getattr(list_[0],'ENTITY_NAME',list_[0].__name__)} {self._build_join(list_[1:])}
		"""

		if condition is not None:
			try:
				query += f" WHERE {MysqlConditionsTranslator.translate(condition)}"
			except BeforeHandUnmatchedCondition:
				for fake in []:
					yield fake

		for row in self.searchMany(query,orderby=orderby,skip=skip,limit=limit):
			to_join = []; i = 0
			for entity,name in zip(entities,entities_names):
				try:
					to_join.append(MysqlJoinStorage._entity_gen(entity,{
						col.replace(f'{name}__',''):value for col,value in row.items() if col.startswith(f'{name}__')
					}))
				except:
					# Check if this might be caused by a left or right join
					if i == 0 or list_[i][2] == "":
						raise
				i += 1
			yield self.join_type(*to_join,**getattr(self.join_type,'SHORTCUTS',{}))


	def count(self,*conditions,skip=None,entry=None,**kwargs):
		entry = self.default_entry if (entry is None) else entry
		condition = self._build_condition(entry, *conditions,**kwargs)
		list_ = self._build_entities_list(entry)
		entities = [list_[0]]+[entity[0] for entity in list_[1:]]
		entities_names = [(entity.ENTITY_NAME if hasattr(entity,"ENTITY_NAME") else entity.__name__) for entity in entities]

		query = f"SELECT count(*) as counted FROM {getattr(list_[0],'ENTITY_NAME',list_[0].__name__)} {self._build_join(list_[1:])}"
		if condition is not None:
			try:
				query += f" WHERE {MysqlConditionsTranslator.translate(condition)}"
			except BeforeHandUnmatchedCondition:
				return 0

		return self.getOne(query)['counted']

	#############################################

	def updateOnSnapshot(self,join,updateID=False):
		if not type(join) is self.join_type:
			raise JoinStorageException(f'Cannot store {type(join)} into a MysqlJoinStorage of {self.join_type}')

		if any([not hasattr(entity,"snapshot") for entity in join.entities.values()]):
			raise EntitySnapshotException(f"No snapshot to recover data from enitiy {[not hasattr(entity,'snapshot') for entity in join.entities.values()][0]}")

		return [MysqlEntityStorage(type(entity),**self.credentials,connexion=self.connexion).updateOnSnapshot(entity,updateID=updateID) for entity in join.entities.values()]
		
	##############################################



		