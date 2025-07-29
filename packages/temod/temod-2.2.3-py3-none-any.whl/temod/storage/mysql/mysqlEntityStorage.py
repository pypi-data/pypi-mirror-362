from temod.base.attribute import *
from temod.base.condition import *
from temod.base.entity import *

from .mysqlAttributesTranslator import MysqlAttributesTranslator
from .mysqlConditionsTranslator import MysqlConditionsTranslator
from .mysqlStorage import MysqlStorage

from temod.storage.exceptions import *

from copy import deepcopy

import sys


#############################################

# MAIN CLASS

class MysqlEntityStorage(MysqlStorage):
	"""docstring for MysqlEntityStorage"""
	def __init__(self, entity_type,**kwargs):
		super(MysqlEntityStorage, self).__init__(**kwargs)

		if not issubclass(entity_type,Entity):
			raise EntityStorageException(f"Entity type {entity_type.__name__} is not a subclass of Entity")
		if not hasattr(entity_type,'ATTRIBUTES'):
			raise EntityStorageException(f"Entity type {entity_type.__name__} has no ATTRIBUTES.")

		self.entity_type = entity_type
		self.entity_name = entity_type.ENTITY_NAME if hasattr(entity_type,'ENTITY_NAME') else entity_type.__name__

		attrs = deepcopy(entity_type.ATTRIBUTES)
		self.entity_attributes = {
			attr.pop('name'):attr for attr in attrs
		}


	#############################################

	# ENTITY GENERATION

	def entity_generator(self,dct,copy=False):
		dct = deepcopy(dct) if copy else dct
		return self.entity_type(*[
			attr['type'](n,value=attr['type'].decode(dct.pop(n)),**{a:b for a,b in attr.items() if not (a in ['type','required'])}) 
			for n,attr in self.entity_attributes.items()
			if attr.get('required',False)
		],*[
			attr['type'](n,value=attr['type'].decode(dct.pop(n,None)),**{a:b for a,b in attr.items() if not (a in ['type','required'])}) 
			for n,attr in self.entity_attributes.items()
			if not attr.get('required',False)
		])


	#############################################

	# VERIFICATIONS

	def _verify_entity(self,entity):
		if issubclass(type(entity),self.entity_type):
			return True
		if type(entity).__name__ == self.entity_type.__name__:
			return True
		raise EntityStorageException(f"Entity type {type(entity).__name__} cannot be stored in Entity {self.entity_type.__name__} storage")

	def _verify_entries(self,entries):
		print(entries)
		try:
			assert(all([
				issubclass(type(entry),Attribute) or issubclass(type(entry),Condition) 
				for entry in entries
			]))
		except AssertionError:
			raise EntityQueringException(f"Conditions must all be subtype of Attribute or Condition")

	#############################################

	# QUERY BUILDERS

	def _build_attributes(self,**attributes):
		return [
			self.entity_attributes[i]['type'](i,value=j,owner_name=self.entity_name,**{
				a:b for a,b in self.entity_attributes[i].items() if not( a in ['type',"required","no_check",'name','owner_name','value'] )
			},no_check=True)
			for i,j in attributes.items()
		]

	def _build_condition(self,*entries,**kwargs):
		self._verify_entries(entries)

		attributes = self._build_attributes(**kwargs)
		for attribute in entries:
			if issubclass(type(attribute),Attribute):
				if attribute.owner_name is None:
					attribute.owner_name = self.entity_name
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

	##############################################

	##############################################

	# VALUES GENERATION

	def generate_unused_value(self,attribute):
		return self.generate_value(attribute)

	def generate_value(self,attribute,unused=True):
		if issubclass(type(attribute),Attribute):
			attr = attribute
		else:
			attr = self.entity_attributes[attribute]['type'](attribute)
		attr.value = type(attr).generate_random_value(**self.entity_attributes[attribute])
		while unused and self.get(attr) is not None:
			attr.value = type(attr).generate_random_value(**self.entity_attributes[attribute])
		return attr.value

	##############################################

	##############################################

	# SINGLE TABLE & ROWS OPERATIONS

	def get(self,*conditions,orderby=None,skip=None,**kwargs):
		condition = self._build_condition(*conditions,**kwargs)

		query = f"SELECT * FROM {self.entity_name}"
		if condition is not None:
			try:
				query += f" WHERE {MysqlConditionsTranslator.translate(condition)}"
			except BeforeHandUnmatchedCondition:
				return None

		if orderby is not None:
			query += f" ORDERBY {orderby}"

		if skip is not None:
			query += f" SKIP {skip}"

		result = self.getOne(query+" LIMIT 1")
		if result is not None:
			return self.entity_generator(result)

	def delete(self,*conditions,many=False,skip=None,limit=None,**kwargs):
		condition = self._build_condition(*conditions,**kwargs)

		query = f"DELETE FROM {self.entity_name}"
		if condition is not None:
			try:
				query += f" WHERE {MysqlConditionsTranslator.translate(condition)}"
			except BeforeHandUnmatchedCondition:
				return None

		if not many:
			limit = 1

		if skip is not None:
			query += f" SKIP {skip}"
			
		if limit is not None:
			query += f" LIMIT {limit}"

		return self.executeAndCommit(query).lastrowid

	def create(self,*entities):
		if len(entities) == 0:
			raise EntityStorageException("At least one entity is needed")
		if len(entities) > 1:
			return self.createMultiple(entities)
		entity = entities[0]

		self._verify_entity(entity)
		values = [
			(attr,MysqlAttributesTranslator.translate(value)) 
			for attr,value in entity.attributes.items() if not value.is_auto
		]
		query = f"INSERT INTO {self.entity_name} ({','.join([v[0] for v in values])}) VALUES ({','.join([v[1] for v in values])})"

		return self.executeAndCommit(query).lastrowid

	def update(self,updates,*conditions,limit=None,skip=None,updateID=False,**kwargs):
		condition = self._build_condition(*conditions,**kwargs)
		try:
			assert(updates is not None and len(updates) > 0)
		except:
			raise EntityStorageException("At least one attribute to update is necessary")
		if type(updates) is dict:
			attributes = [
				attr['type'](name,value=updates[name],**{k:v for k,v in attr.items() if not k in ['type','required']})
				for name,attr in self.entity_attributes.items() if name in updates
			]
		elif issubclass(type(updates),Attribute):
			attributes = [updates]
		else:
			raise Exception("Updates must be a dict or an Attribute")
		query = f"UPDATE {self.entity_name} SET {','.join([attribute.name+' = '+MysqlAttributesTranslator.translate(attribute) for attribute in attributes])}"
		if condition is not None:
			try:
				query +=  f" WHERE {MysqlConditionsTranslator.translate(condition)}"
			except BeforeHandUnmatchedCondition:
				return None
		if skip is not None:
			query += f" SKIP {skip}"
		if limit is not None:
			query += f" LIMIT {limit}"
		return self.executeAndCommit(query).lastrowid

	def list(self,*conditions,orderby=None,skip=None,limit=None,**kwargs):
		condition = self._build_condition(*conditions,**kwargs)
		base = f'SELECT * FROM {self.entity_name}'
		yield_fake = False
		if condition is not None:
			try:
				condition = MysqlConditionsTranslator.translate(condition)
			except:
				yield_fake = True

		if not yield_fake:
			for row in self.searchMany(base,condition=condition,orderby=orderby,skip=skip,limit=limit):
				yield self.entity_generator(row)
		else:
			for fake in []:
				yield fake

	def count(self,*conditions,skip=None,**kwargs):
		condition = self._build_condition(*conditions,**kwargs)

		query = f"SELECT count(*) as counted FROM {self.entity_name}"
		if condition is not None:
			try:
				query += f" WHERE {MysqlConditionsTranslator.translate(condition)}"
			except BeforeHandUnmatchedCondition:
				return 0

		return self.getOne(query)['counted']


	##############################################


	##############################################

	# SINGLE TABLE & MULTIPLE ROWS OPERATIONS

	def createMultiple(self,entities):
		[self._verify_entity(entity) for entity in entities]
		values = []
		columns = None
		for entity in entities:
			if columns is None:
				columns = [attr for attr,value in entity.attributes.items() if not value.is_auto]
			values.append('('+ ','.join([MysqlAttributesTranslator.translate(entity.attributes[column]) for column in columns]) +')')
		query = f"INSERT INTO {self.entity_name} ({','.join([column for column in columns])}) VALUES {' ,'.join(values)}"
		return self.executeAndCommit(query).lastrowid
		
	##############################################
		
	##############################################

	# FURTHER FUNCTIONNALITIES

	def updateOne(self,entity,attributes=None,updateID=False):
		self._verify_entity(entity)
		toUpdate = [] if attributes is None else [
			attr if type(attr) is str else attr.name for attr in attributes
		]
		values = [
			(attr,MysqlAttributesTranslator.translate(value)) 
			for attr,value in entity.attributes.items() 
			if not value.is_auto and attr in toUpdate and (updateID or not value.is_id)
		]
		ids = [
			(attr,MysqlAttributesTranslator.translate(value))
			for attr,value in entity.attributes.items()
			if value.is_id
		]
		condition = " and ".join([i[0]+"="+i[1] for i in ids])
		query = f"UPDATE {self.entity_name} SET {','.join([v[0]+'='+v[1] for v in values])} WHERE {condition}"
		return self.executeAndCommit(query).lastrowid

	def updateOnSnapshot(self,entity,updateID=False):
		self._verify_entity(entity)
		if entity.snapshot is None:
			raise EntitySnapshotException("No snapshot to recover data from")
		updates = [
			attribute for attribute in entity.attributes.values()
			if not (entity.snapshot[attribute.name].compare(attribute))
		]
		if len(updates) > 0:
			return self.updateOne(entity,attributes=updates,updateID=updateID)
		return False

		
	##############################################