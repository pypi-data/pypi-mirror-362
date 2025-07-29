from .attribute import Attribute
from .entity import Entity

from .condition import Equals, And, Or

from typing import Type



class ConstraintException(Exception):
	pass


class Multiplicity(object):
	def __init__(self, start=None, end=None, min_start=None, max_start=None, min_end=None, max_end=None):
		if start is not None:
			min_start = start; max_start = start
		if end is not None:
			min_end = end; max_end = end
		self.start = start
		self.end = end
		self.min_start = min_start
		self.min_end = min_end
		self.max_start = max_start
		self.max_end = max_end

class Constraint(object):
	"""docstring for Constraint"""
	def __init__(self, multiplicity=None,**kwargs):
		super(Constraint, self).__init__()
		self.multiplicity = getattr(self,"MULTIPLICITY",multiplicity)
		if self.multiplicity is None:
			self.multiplicity = Multiplicity(start=1,end=1)


class AttributesConstraint(Constraint):

	def __init__(self, *attributes, **kwargs):
		super(AttributesConstraint, self).__init__(**kwargs)
		self.attributes = list(attributes)
		if len(self.attributes) == 0:
			for attr in getattr(self,'ATTRIBUTES',[]):
				found = [a for a in attr['entity'].ATTRIBUTES if a['name'] == attr['name']][0]
				self.attributes.append(found['type'](found['name'],owner_type=attr['entity']))

	def entities(self):
		print(self.attributes)
		for attribute in self.attributes:
			print(attribute)
			yield attribute.owner_type


class NestedConstraint(Constraint):

	def __init__(self, *constraints, **kwargs):
		super(NestedConstraint, self).__init__(**kwargs)
		self.constraints = list(constraints)

	def entities(self):
		for constraint in self.constraints:
			for entity in constraint.entities():
				yield entity


class EqualityConstraint(AttributesConstraint):
	def condition(self):
		return Equals(*self.attributes)


class BindConstraint(NestedConstraint):
	"""docstring for Constraint"""
	def __init__(self, *constraints, **kwargs):
		super(BindConstraint,self).__init__(*constraints,**kwargs)
		if len(self.constraints) == 0:
			for constraint in getattr(self,'CONSTRAINTS',[]):
				attributes = []
				for attr in constraint:
					found = [a for a in attr['entity'].ATTRIBUTES if a['name'] == attr['name']][0]
					attributes.append(found['type'](found['name'],owner_type=attr['entity']))
				self.constraints.append(EqualityConstraint(*attributes,multiplicity=self.multiplicity))

		if len(self.constraints) < 2:
			raise ConstraintException("At least two constraints must be specified")

	def condition(self):
		return And(*[Equals(*constraint.attributes) for constraint in self.constraints])



class RelaxedConstraint(NestedConstraint):

	def __init__(self, *constraints, **kwargs):
		super(RelaxedConstraint,self).__init__(*constraints,**kwargs)
		if len(self.constraints) == 0:
			for constraint in getattr(self,'CONSTRAINTS',[]):
				attributes = []
				for attr in constraint:
					found = [a for a in attr['entity'].ATTRIBUTES if a['name'] == attr['name']][0]
					attributes.append(found['type'](found['name'],owner_type=attr['entity']))
				self.constraints.append(EqualityConstraint(*attributes,multiplicity=self.multiplicity))

		if len(self.constraints) < 2:
			raise ConstraintException("At least two constraints must be specified")

	def condition(self):
		return Or(*[Equals(*constraint.attributes) for constraint in self.constraints])