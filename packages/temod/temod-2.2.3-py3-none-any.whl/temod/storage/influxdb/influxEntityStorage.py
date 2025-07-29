from temod.storage.exceptions.entities import *

from temod.base.attribute import *
from temod.base.condition import *
from temod.base.entity import *

from .influxTranslators import InfluxConditionsTranslator, InfluxAggregationsTranslator
from .influxStorage import InfluxStorage

from copy import deepcopy
import sys

class InfluxEntityStorage(InfluxStorage):
	"""docstring for InfluxEntityStorage"""
	def __init__(self, entity_type, measurement=None, timer=None, fields=None, tags=None, **kwargs):
		super(InfluxEntityStorage, self).__init__(**kwargs)

		if not issubclass(entity_type,Entity):
			raise EntityStorageException(f"Entity type {entity_type.__name__} is not a subclass of Entity")
		if not hasattr(entity_type,'ATTRIBUTES'):
			raise EntityStorageException(f"Entity type {entity_type.__name__} has no ATTRIBUTES.")

		self.entity_type = entity_type
		self.entity_name = entity_type.ENTITY_NAME if hasattr(entity_type,'ENTITY_NAME') else entity_type.__name__
		self.entity_generator = self._dict_gen if type(entity_type.ATTRIBUTES) is dict else self._direct_gen

		attrs = deepcopy(entity_type.ATTRIBUTES)
		self.entity_attributes = attrs if type(entity_type.ATTRIBUTES) is dict else {
			attr.pop('name'):attr for attr in attrs
		}

		try:
			if measurement is not None:
				self.measurement =  [attr for attr in self.entity_attributes if attr == measurement]
			else:
				self.measurement =  [attr for attr,params in self.entity_attributes.items() if params.get('is_id',False)]
			if len(self.measurement) == 0:
				raise
		except:
			raise EntityStorageException(f"InfluxEntityStorage need a valid measurement attribute either by specifying it clearly as measurement or by setting is_id True")

		if len(self.measurement) > 1:
			raise EntityStorageException(f"InfluxEntityStorage cannot handle more than one measurement per entity yet.{','.join(self.measurement)}")
		self.measurement = self.measurement[0]

		if not issubclass(self.entity_attributes[self.measurement]['type'],StringAttribute):
			raise EntityStorageException(f"InfluxEntityStorage measurement attribute must be of type/subtype of StringAttribute not {self.entity_attributes[self.measurement]['type']} (measurement: {self.measurement})")

		try:
			if timer is not None:
				self.timer =  [attr for attr in self.entity_attributes if attr == timer]
			else:
				self.timer =  [attr for attr,params in self.entity_attributes.items() if issubclass(params['type'],DateTimeAttribute)]
				self.timer +=  [attr for attr,params in self.entity_attributes.items() if issubclass(params['type'],DateAttribute)]
			if len(self.timer) == 0:
				raise
		except:
			raise EntityStorageException(f"InfluxEntityStorage need a valid timer attribute either by specifying it clearly as measurement or by having at least one ClockAttribute")

		if len(self.timer) > 1:
			raise EntityStorageException(f"InfluxEntityStorage cannot handle more than one timer per entity yet.{','.join(self.measurement)}")
		self.timer = self.timer[0]

		if not issubclass(self.entity_attributes[self.timer]['type'],ClockAttribute):
			raise EntityStorageException(f"InfluxEntityStorage measurement attribute must be of type/subtype of ClockAttribute not {self.entity_attributes[self.measurement]['type']} (measurement: {self.measurement})")

		fields = [] if fields is None else list(fields);tags = [] if tags is None else list(tags);
		self.fields = []; self.tags = [];
		for attr,params in self.entity_attributes.items():
			if attr == self.measurement or attr == self.timer:
				continue
			if attr in fields:
				if not issubclass(params['type'],NumericAttribute):
					raise EntityStorageException(f"InfluxEntityStorage field attributes must be of type/subtype of NumericAttribute not {self.entity_attributes[self.measurement]['type']} (field: {attr})")
				self.fields.append(attr)
			elif attr in tags:
				self.tags.append(attr)
			else:
				if issubclass(params['type'],NumericAttribute):
					self.fields.append(attr);print(attr,"set as field");continue
				self.tags.append(attr);print(attr,"set as tag")


	#############################################

	# ENTITY GENERATION

	def _dict_gen(self,dct,copy=False,set_field=False,allow_fragment=False):
		dct = deepcopy(dct) if copy else dct
		dct[self.measurement] = dct['_measurement']
		dct[self.timer] = dct['_time']
		if set_field:
			dct[dct['_field']] = dct['_value']
		try:
			return self.entity_type.from_dict(dct)
		except:
			if allow_fragment:
				return EntityFragment(self.entity_type).from_dict(dct)
			raise

	def _direct_gen(self,dct,copy=False,set_field=False,allow_fragment=False):
		dct = deepcopy(dct) if copy else dct
		dct[self.measurement] = dct['_measurement']
		dct[self.timer] = dct['_time']
		if set_field:
			dct[dct['_field']] = dct['_value']
		try:
			return self.entity_type(*[
				attr['type'](n,value=dct.pop(n),**{a:b for a,b in attr.items() if not (a in ['type','required'])}) 
				for n,attr in self.entity_attributes.items()
				if attr.get('required',False)
			],*[
				attr['type'](n,value=dct.pop(n,None),**{a:b for a,b in attr.items() if not (a in ['type','required'])}) 
				for n,attr in self.entity_attributes.items()
				if not attr.get('required',False)
			])
		except:
			if allow_fragment:
				return EntityFragment(self.entity_type,**dct)
			raise

	#############################################

	# VERIFICATIONS

	def _verify_entity(self,entity):
		try:
			assert(issubclass(type(entity),self.entity_type))
		except AssertionError:
			if type(entity).__name__ == self.entity_type.__name__:
				f1 = None; f2 = None
				try:
					try:
						try:
							f1 = type(entity).__file__
						except:
							f1 = sys.modules[type(entity).__module__].__file__
						try:
							f2 = self.entity_type.__file__
						except:
							f2 = sys.modules[self.entity_type.__module__].__file__
					except:
						pass
					if f1 is None or f2 is None or f1 != f2:
						raise
					else:
						return
				except:
					pass
			raise EntityStorageException(f"Entity type {type(entity).__name__} cannot be stored in Entity {self.entity_type.__name__} storage")

	def _verify_entries(self,entries):
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
			self.entity_attributes[i]['type'](i,value=j,owner_name=self.entity_name)
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

	# DATABASE OPERATIONS

	def get(self,range_,*conditions,skip=None,orderby=None,**kwargs):
		condition = self._build_condition(*conditions,**kwargs)

		where = ""
		if condition is not None:
			where = InfluxConditionsTranslator.translate(condition,measurement=self.measurement)

		result = self.getOne(self.entity_name,range_,condition=where,skip=skip,orderby=orderby)
		if result is not None:
			return self.entity_generator(result)

	def create(self,*entities):
		if len(entities) == 0:
			raise EntityStorageException("At least one entity is needed")
		if len(entities) > 1:
			return self.createMultiple(entities)
		entity = entities[0]

		self._verify_entity(entity)
		point = self.point(
			getattr(entity,self.measurement),
			tags=[(tag,getattr(entity,tag)) for tag in self.tags],
			fields=[(field,getattr(entity,field)) for field in self.fields]
		)
		return self.write(self.entity_name,point)

	def list(self,range_,*conditions,limit=None,skip=None,orderby=None,**kwargs):
		condition = self._build_condition(*conditions,**kwargs)

		where = ""
		if condition is not None:
			where = InfluxConditionsTranslator.translate(condition,measurement=self.measurement)

		for row in self.getMany(self.entity_name,range_,fields=self.fields,condition=where,orderby=orderby,skip=skip,limit=limit):
			yield self.entity_generator(row.values)

	def aggregate(self,aggregation,range_,*conditions,selector=None,limit=None,skip=None,orderby=None,**kwargs):
		condition = self._build_condition(*conditions,**kwargs)

		where = ""
		if condition is not None:
			where = InfluxConditionsTranslator.translate(condition,measurement=self.measurement)

		selectors = []
		if selector is not None:
			selectors = InfluxSelectorTranslator.translate(selector,fields=self.fields,tags=self.tags)
		
		if type(aggregation) is not list:
			aggregation = [aggregation]
		aggregations = [InfluxAggregationsTranslator.translate(agr) for agr in aggregation]

		for row in self.getMany(
				self.entity_name,range_,condition=where,orderby=orderby,
				skip=skip,limit=limit,selectors=selectors,aggregations=aggregations
			):
			yield self.entity_generator(row.values,set_field=True)