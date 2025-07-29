from .mysqlAttributesTranslator import MysqlAttributesTranslator
from .mysqlConditionsTranslator import MysqlConditionsTranslator
from .mysqlEntityStorage import MysqlEntityStorage
from .mysqlJoinStorage import MysqlJoinStorage
from .mysqlStorage import MysqlStorage

from temod.base.condition import *
from temod.base.attribute import *
from temod.base.entity import Entity
from temod.base.join import Join
from temod.base.cluster import *



#############################################

# EXCEPTIONS

class ClusterStorageException(Exception):
	"""docstring for ClusterStorageException"""
	def __init__(self, *args, **kwargs):
		super(ClusterStorageException, self).__init__(*args, **kwargs)

class ClusterQueryingException(Exception):
	"""docstring for ClusterQueryingException"""
	def __init__(self, *args, **kwargs):
		super(ClusterQueryingException, self).__init__(*args, **kwargs)


#############################################

# MAIN CLASS

class MysqlClusterStorage(MysqlStorage):
	"""docstring for MysqlClusterStorage"""
	def __init__(self, cluster_type,**kwargs):
		super(MysqlClusterStorage, self).__init__(**kwargs)
		try:
			assert(issubclass(cluster_type,Cluster))
			self.cluster = cluster_type
		except AssertionError:
			raise ClusterStorageException("cluster_type must be a subclass of Cluster")

	#############################################

	# VERIFICATIONS

	def verify_entries(self,entries):
		try:
			assert(all([
				issubclass(type(entry),Attribute) or issubclass(type(entry),Condition) 
				for entry in entries
			]))
		except AssertionError:
			raise ClusterQueryingException(f"Conditions must all be subtype of Attribute or Condition")

	#############################################

	# QUERY BUILDING

	def _build_attributes(self,class_,**attributes):
		if issubclass(class_,Join):
			raise Exception("Not done yet")
		elif issubclass(class_,Entity):
			try:
				return [
					[attr for attr in class_.ATTRIBUTES if attr['name'] == i][0]['type'](i,value=j,owner_name=class_.ENTITY_NAME)
					for i,j in attributes.items()
				]
			except:
				absent = [attr for attr in attributes if not(attr in [a['name'] for a in class_.ATTRIBUTES])]
				raise ClusterStorageException(f"Entity {class_.ENTITY_NAME} does not have following attributes: {','.join(absent)}")
		raise ClusterStorageException("Can't build attributes for class of type ",class_)

	def _build_condition(self,base_class,*entries,**kwargs):
		self.verify_entries(entries)

		if issubclass(base_class,Entity):
			base_entity = base_class
		elif issubclass(base_class,Join):
			base_entity = getattr(base_class,'default_entry',base_class.STRUCTURE[0].attributes[0].owner_type)
			
		attributes = self._build_attributes(base_entity,**kwargs)

		attributes.extend([attribute for attribute in entries if issubclass(type(attribute),Attribute)])
		for attribute in attributes:
			if attribute.owner_name is None:
				attribute.owner_name = base_entity.ENTITY_NAME

		all_conditions = [Equals(attribute,None) for attribute in attributes]
		all_conditions.extend([condition for condition in entries if issubclass(type(condition),Condition)])

		if len(all_conditions) <= 1:
			condition = all_conditions
		else:
			condition = [And(*all_conditions)]
		return condition


	#############################################

	# QUERY Execution

	def _fill_node(self,graph,node,condition,orderby=None,skip=None,limit=None,one=True):
		
		data = graph.nodes[node]
		
		if issubclass(data['type'],Entity):
			if not one:
				queried = MysqlEntityStorage(data['type'],**self.credentials).list(condition,orderby=orderby,skip=skip,limit=limit)
			else:
				queried = MysqlEntityStorage(data['type'],**self.credentials).get(condition,orderby=orderby,skip=skip)
		elif issubclass(data['type'],Join):
			if not one:
				queried = MysqlJoinStorage(data['type'],**self.credentials).list(condition,orderby=orderby,skip=skip,limit=limit)
			else:
				queried = MysqlJoinStorage(data['type'],**self.credentials).get(condition,orderby=orderby,skip=skip)

		data['__object'] = queried
		data['__queried'] = True
		if queried is None:
			return
		for target,link in graph.getLinked(node):
			if graph.nodes[target]['__queried']:
				continue
			new_condition = link['condition'](queried)
			self._fill_node(
				graph,target,new_condition,orderby=link.get('orderby',None),skip=link.get('skip',None),limit=link.get('limit',None),
				one=not link.get('one_to_many',False)
			)


	#############################################

	# Public methods


	def get(self,*conditions,orderby=None,skip=None,base_node=None,**kwargs):

		graph = self.cluster.structure_to_graph(self.cluster.CLUSTER_STRUCTURE)
		entry_point = self.cluster.CLUSTER_STRUCTURE['store_as'] if base_node is None else base_node
		starting_node = graph.nodes[entry_point]

		condition = self._build_condition(starting_node['type'],*conditions,**kwargs)
		self._fill_node(graph,entry_point,*condition,orderby=orderby,skip=skip)
		return self.cluster(graph) if graph.nodes[entry_point]['__object'] is not None else None


	def list(self,*conditions,orderby=None,skip=None,limit=None,base_node=None,**kwargs):

		graph = self.cluster.structure_to_graph(self.cluster.CLUSTER_STRUCTURE)
		entry_point = self.cluster.CLUSTER_STRUCTURE['store_as'] if base_node is None else base_node
		starting_node = graph.nodes[entry_point]

		condition = self._build_condition(starting_node['type'],*conditions,**kwargs)

		if issubclass(starting_node['type'],Entity):
			queried = MysqlEntityStorage(starting_node['type'],**self.credentials).list(*condition,orderby=orderby,skip=skip,limit=limit)
		elif issubclass(starting_node['type'],Join):
			queried = MysqlJoinStorage(starting_node['type'],**self.credentials).list(*condition,orderby=orderby,skip=skip,limit=limit)

		for obj in queried:
			starting_node['__object'] = obj; starting_node['__queried'] = True
			for target,link in graph.getLinked(entry_point):
				if graph.nodes[target]['__queried']:
					continue
				if obj is None:
					continue
				new_condition = link['condition'](obj)
				self._fill_node(
					graph,target,new_condition,orderby=link.get('orderby',None),skip=link.get('skip',None),limit=link.get('limit',None),
					one=not link.get('one_to_many',False)
				)
			yield self.cluster(graph)
			graph = self.cluster.structure_to_graph(self.cluster.CLUSTER_STRUCTURE)
			starting_node = graph.nodes[entry_point]

		













