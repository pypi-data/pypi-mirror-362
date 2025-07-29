from .attribute import Attribute, EnumAttribute
import inspect

class DuplicateNameError(Exception):
	pass

class MalformedEntityException(Exception):
	pass

class MissingRequiredAttributeError(Exception):
	pass


class Entity(object):
	"""docstring for Entity"""
	def __init__(self, *attributes,**kwargs):
		super(Entity, self).__init__()
		self.attributes = {}
		self.complements = {}
		self.snapshot = None
		for i,attribute in enumerate(attributes):
			if issubclass(type(attribute),Attribute):
				self.attributes[attribute.name] = attribute
			else:
				self.attributes[self.ATTRIBUTES[i]['name']] = self.ATTRIBUTES[i]['type'](
					self.ATTRIBUTES[i]['name'],value=attribute,
					**{a:b for a,b in self.ATTRIBUTES[i].items() if not (a in ['name','type','required'])}
				)
		for k,v in kwargs.items():
			if k in self.attributes:
				self.attributes[k].set_value(v)
			else:
				try:
					i = [attr['name'] for attr in self.ATTRIBUTES].index(k)
				except ValueError:
					raise MalformedEntityException(f"Entity {type(self).__name__} has no attribute named '{k}'")
				self.attributes[k] = self.ATTRIBUTES[i]['type'](
					k,value=v,**{a:b for a,b in self.ATTRIBUTES[i].items() if not (a in ['name','type','required'])}
				)
		for attr in self.ATTRIBUTES:
			if not (attr['name'] in self.attributes):
				if attr.get('required',False):
					raise MissingRequiredAttributeError(f'Entity {type(self).__name__} is missing the required attribute {attr["name"]}')
				self.attributes[attr['name']] = attr['type'](
					attr['name'],**{a:b for a,b in attr.items() if not (a in ['name','type','required'])}
				)

	#####################################################

	def setAttribute(self,attribute: str,value):
		self.attributes[attribute].set_value(value)

	def setAttributes(self,**kwargs):
		for k,v in kwargs.items():
			self.attributes[k].set_value(v)

	def setInfo(self, info: str, value):
		if info in self.attributes:
			raise DuplicateNameError("Complementary infos cannot share names with base attributes.")
		self.complements[info] = value

	def setInfos(self, **complements):
		for complement, value in complements.items():
			self.setInfo(complement, value)

	def scalarizeInfo(self, value, complements=False):
		if value is None:
			return None
		if(type(value) in [dict, str, int, float, bool]):
			return value
		if type(value) in [list, set]:
			return [self.scalarizeInfo(element, complements=complements) for element in value]
		if (issubclass(type(value), Attribute)):
			return value.to_scalar()
		if (issubclass(type(value), Entity)):
			return value.to_dict(complements=complements)
		raise Exception(f"Cannot scalarize info of type {type(value)}")

	def __getitem__(self,name):
		try:
			return self.attributes[name].value
		except Exception as e:
			try:
				return self.complements[name]
			except:
				pass
			raise e

	def __setitem__(self,name,value): 
		return self.setAttribute(name,value)

	#####################################################

	def enum(entity_type, attribute):
		attr_names = [attr['name'] for attr in getattr(entity_type,"ATTRIBUTES",[])]
		if not (attribute in attr_names):
			raise Exception(f'Enum attribute {attribute} not found in Attribute names')
		attr = [attr for attr in entity_type.ATTRIBUTES if attr['name'] == attribute][0]
		if not issubclass(attr['type'], EnumAttribute):
			raise Exception(f'{attribute} is not a valid Enum Attribute')
		return attr['type'](
			attr['name'],no_check=True,**{a:b for a,b in attr.items() if not (a in ['name','no_check','type','required'])}
		).enum

	#####################################################

	def takeSnapshot(self):
		self.snapshot = {
			name:attribute.shallow_copy() for name,attribute in self.attributes.items()
		}
		return self

	#####################################################

	def to_dict(self,include=None, complements=False, translator=None):
		dct = {}
		if complements:
			dct = {complement: self.scalarizeInfo(value, complements=True) for complement, value in self.complements.items()}
		dct.update({
			name:attr.to_scalar() if attr.value is not None else None
			for name,attr in self.attributes.items() if include is None or name in include
		})
		if translator is not None:
			return {translator.get(k,k):v for k,v in dct.items()}
		return dct

	def name(self):
		return getattr(self,'ENTITY_NAME',type(self).__name__)

	def __repr__(self):
		attributes = [f"{attr.name} ({type(attr).__name__}): {attr.value} ({type(attr.value).__name__})" for attr in self.attributes.values()]
		return f"""Entity {self.ENTITY_NAME}"""+((":\n\t"+"\n\t".join(attributes)) if len(self.attributes) > 0 else "")

	#####################################################


class EntityFragment(Entity):
	"""docstring for EntityFragment"""
	def __init__(self, parentEntity, *attributes,**kwargs):
		self.snapshot = None
		self.attributes = {}
		for i,attribute in enumerate(attributes):
			if issubclass(type(attribute),Attribute):
				self.attributes[attribute.name] = attribute
			else:
				self.attributes[parentEntity.ATTRIBUTES[i]['name']] = parentEntity.ATTRIBUTES[i]['type'](
					parentEntity.ATTRIBUTES[i]['name'],value=attribute,
					**{a:b for a,b in parentEntity.ATTRIBUTES[i].items() if not (a in ['name','type','required'])}
				)
		for k,v in kwargs.items():
			if k in self.attributes:
				self.attributes[k].set_value(v)
			else:
				try:
					i = [attr['name'] for attr in parentEntity.ATTRIBUTES].index(k)
				except ValueError:
					continue
				self.attributes[k] = parentEntity.ATTRIBUTES[i]['type'](
					k,value=v,**{a:b for a,b in parentEntity.ATTRIBUTES[i].items() if not (a in ['name','type','required'])}
				)
		self.parentEntity = parentEntity

	def __repr__(self):
		attributes = [f"{attr.name} ({type(attr).__name__}): {attr.value} ({type(attr.value).__name__})" for attr in self.attributes.values()]
		return f"""EntityFragment of {self.parentEntity.ENTITY_NAME}"""+((":\n\t"+"\n\t".join(attributes)) if len(self.attributes) > 0 else "")

		
class AutoCompleteEntity(Entity):
	"""docstring for AutoCompleteEntity"""
	def __init__(self, *args, **kwargs):
		super(AutoCompleteEntity, self).__init__(*args, **kwargs)
		self.autocompletes = {}
		if len(self.COMPLETION_FIELDS) == 1:
			self.auto_complete = self.autocomplete_single
			self.field = self.COMPLETION_FIELDS[0]
		else:
			self.auto_complete = self.autocomplete_multiple
		self.auto_complete()

	#####################################################

	def autocomplete_single(self):
		key = getattr(self,self.field)
		for k,v in self.COMPLETION.get(key,{}).items():
			if hasattr(v,"__call__"):
				self.autocompletes[k] = v(self)
			else:
				self.autocompletes[k] = v

	def autocomplete_multiple(self):
		key = tuple([getattr(self,field) for field in self.COMPLETION_FIELDS])
		for k,v in self.COMPLETION.get(key,{}).items():
			if hasattr(v,"__call__"):
				self.autocompletes[k] = v(self)
			else:
				self.autocompletes[k] = v

	def __getattr__(self,name):
		try:
			return self.attributes[name].value
		except:
			return self.autocompletes[name]

	#####################################################

	def to_dict(self):
		dct = {k:v for k,v in self.autocompletes}
		dct.update({
			name:attr.to_scalar() if attr.value is not None else None
			for name,attr in self.attributes.items()
		})
		return dct

	def __repr__(self):
		attributes = [f"{attr.name} ({type(attr).__name__}): {attr.value} ({type(attr.value).__name__})" for attr in self.attributes.values()]
		return f"""Auto Completed Entity {self.ENTITY_NAME}"""+((":\n\t"+"\n\t".join(attributes)) if len(self.attributes) > 0 else "")

	#####################################################
