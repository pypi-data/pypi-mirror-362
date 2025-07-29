class ForbiddenAccessKeyError(Exception):
	"""docstring for ForbiddenAccessKeyError"""
	def __init__(self, *args, **kwargs):
		super(ForbiddenAccessKeyError, self).__init__(*args, **kwargs)

class DuplicatedAccessKeyError(Exception):
	"""docstring for DuplicatedAccessKeyError"""
	def __init__(self, *args, **kwargs):
		super(DuplicatedAccessKeyError, self).__init__(*args, **kwargs)

		

class ExoSkeleton(object):
	"""docstring for ExoSkeleton"""
	FORBIDDEN_ACCESS_KEYS = set([
		"_access_func","_direct_access","_direct_access_auto","_direct_access_cluster","_add_path","_structure_","_unaccessible_","SHORTCUTS"
	])
	def __init__(self, exo_structure=None,protected_keys=None,structure_type="auto"):
		super(ExoSkeleton, self).__init__()
		structure = {} if exo_structure is None else dict(exo_structure)
		self._structure_ = {}
		for i,j in structure.items():
			ExoSkeleton._add_path(self,i,j)
		if protected_keys is not None:
			for key in protected_keys:
				ExoSkeleton.FORBIDDEN_ACCESS_KEYS.add(key)
		if structure_type == "auto":
			self._access_func = self._direct_access_auto
		elif structure_type == "cluster":
			self._access_func = self._direct_access_cluster

	def __getattribute__(self,name): 
		try:
			if not (name in ExoSkeleton.FORBIDDEN_ACCESS_KEYS):
				return ExoSkeleton._direct_access(self,name)
		except Exception as exc:
			pass
		return super(ExoSkeleton,self).__getattribute__(name)

	def _add_path(self,access_key,fullpath):
		if access_key in ExoSkeleton.FORBIDDEN_ACCESS_KEYS:
			raise ForbiddenAccessKeyError(f"Access Key '{access_key}' is not allowed")
		if access_key in super(ExoSkeleton,self).__getattribute__('_structure_'):
			raise DuplicatedAccessKeyError(f"The Exo _structure_ already has a access key named '{access_key}'")
		super(ExoSkeleton,self).__getattribute__('_structure_')[access_key] = fullpath.split('.')

	def _direct_access(self,path):
		return self._access_func(path)

	def _direct_access_auto(self,path):
		_c = self
		for var_ in super(ExoSkeleton,self).__getattribute__('_structure_')[path]:
			_c = getattr(_c,var_)
		return _c

	def _direct_access_cluster(self,path):
		_c = self
		for i,var_ in enumerate(super(ExoSkeleton,self).__getattribute__('_structure_')[path]):
			if i == 0:
				_c = _c[var_]
			else:
				_c = getattr(_c,var_)
		return _c