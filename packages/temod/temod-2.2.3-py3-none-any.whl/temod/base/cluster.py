from temod.utils.exoskeleton import ExoSkeleton
from temod.utils.graphs import ClusterStructure


class Cluster(object):
	"""docstring for Cluster"""
	def __init__(self, graph, **kwargs):
		super(Cluster, self).__init__()
		self.graph = graph
		self.exoskeleton = kwargs

	def __getitem__(self,name): 
		try:
			return self.graph.nodes[name]["__object"]
		except:
			if name in self.exoskeleton:
				path = self.exoskeleton[name].split('.')
				return self[path[0]][path[1]]
			raise

	def expand_graph(graph,element,pred=None):
		data = {s:v for s,v in element.items() if not (s in ['store_as','links',"condition"])}
		data.update({"__queried":False,"__object":None})
		graph.addElement(element["store_as"],**data)
		if pred is not None:
			graph.addLink(pred,element['store_as'],
				condition=element['condition'],one_to_many=element['one_to_many'],
				limit=element.get('limit',None),skip=element.get('skip',None),orderby=element.get('orderby',None)
			)
		for link in element.get('links',[]):
			Cluster.expand_graph(graph,link,pred=element['store_as'])
		return graph

	def structure_to_graph(structure):
		return Cluster.expand_graph(ClusterStructure(),structure)

	def to_dict(self,include=None):
		dct = {}; include = include if include is not None else {}
		for i,j in self.graph.nodes.items():
			if type(j['__object']).__name__ == "generator":
				j['__object'] = list(j['__object'])
				dct[i] = [obj.to_dict(include=include.get(i,None)) if hasattr(obj,"to_dict") else obj for obj in j['__object']]
			else:
				dct[i] = j['__object'].to_dict(include=include.get(i,None)) if hasattr(j['__object'],"to_dict") else j['__object']
		return dct