import networkx as nx


class ClusterStructure(nx.DiGraph):
	"""docstring for ClusterStructure"""
	def __init__(self, *args, **kwargs):
		super(ClusterStructure, self).__init__(*args, **kwargs)

	def addElement(self,label,**kwargs):
		self.add_node(label,**kwargs)
		return self

	def addLink(self,source_node,target_node,**kwargs):
		self.add_edge(source_node,target_node,**kwargs)

	def getLinked(self,node):
		for adj,link in self.adj[node].items():
			yield adj,link

	def to_dict(self):
		return nx.tree_data(self)



