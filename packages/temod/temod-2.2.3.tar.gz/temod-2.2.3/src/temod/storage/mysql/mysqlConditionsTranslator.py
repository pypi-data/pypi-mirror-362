from .mysqlAttributesTranslator import MysqlAttributesTranslator


from temod.storage.exceptions import *

from temod.base.condition import *
from temod.base.attribute import *


class MysqlConditionsTranslator(object):
	"""docstring for MysqlConditionsTranslator"""

	def translate_field(attribute):
		if getattr(attribute,"owner_name",None) is None:
			if hasattr(attribute,"name"):
				return attribute.name
			return attribute
		return f"{attribute.owner_name}.{attribute.name}"

	def translate(condition):
		if hasattr(MysqlConditionsTranslator,f"translate_{type(condition).__name__.lower()}"):
			return getattr(MysqlConditionsTranslator,f"translate_{type(condition).__name__.lower()}")(condition)
		else:
			raise ConditionTranslatorException(f"Can't translate condition of type {type(condition).__name__}")

	def translate_and(condition):
		return " and ".join(["("+MysqlConditionsTranslator.translate(sub_condition)+")" for sub_condition in condition.conditions])

	def translate_or(condition):
		return " or ".join(["("+MysqlConditionsTranslator.translate(sub_condition)+")" for sub_condition in condition.conditions])

	def translate_not(condition):
		return f" not ({MysqlConditionsTranslator.translate(condition.condition)})"

	def translate_startswith(condition):
		if condition.case_sensitive:
			condition.field.value = condition.field.value+"%"
			return f"{MysqlConditionsTranslator.translate_field(condition.field)} LIKE {MysqlAttributesTranslator.translate(condition.field)}"
		else:
			condition.field.value = condition.field.value.lower()+"%"
			return f"lower({MysqlConditionsTranslator.translate_field(condition.field)}) LIKE {MysqlAttributesTranslator.translate(condition.field)}"

	def translate_endswith(condition):
		if condition.case_sensitive:
			condition.field.value = "%"+condition.field.value
			return f"{MysqlConditionsTranslator.translate_field(condition.field)} LIKE {MysqlAttributesTranslator.translate(condition.field)}"
		else:
			condition.field.value = "%"+condition.field.value.lower()
			return f"lower({MysqlConditionsTranslator.translate_field(condition.field)}) LIKE {MysqlAttributesTranslator.translate(condition.field)}"

	def translate_contains(condition):
		if condition.case_sensitive:
			condition.field.value = "%"+condition.field.value+"%"
			return f"{MysqlConditionsTranslator.translate_field(condition.field)} LIKE {MysqlAttributesTranslator.translate(condition.field)}"
		else:
			condition.field.value = "%"+condition.field.value.lower()+"%"
			return f"lower({MysqlConditionsTranslator.translate_field(condition.field)}) LIKE {MysqlAttributesTranslator.translate(condition.field)}"

	def translate_equals(condition):
		if condition.field2 is None:
			if condition.field1.value is None:
				return f'{MysqlConditionsTranslator.translate_field(condition.field1)} is null'
			return f'{MysqlConditionsTranslator.translate_field(condition.field1)} = {MysqlAttributesTranslator.translate(condition.field1)}'
		return f"{MysqlConditionsTranslator.translate_field(condition.field1)} = {MysqlConditionsTranslator.translate_field(condition.field2)}"

	def translate_inferior(condition):
		symbol = "<" if condition.strict else "<="
		if condition.field2 is None:
			return f'{MysqlConditionsTranslator.translate_field(condition.field1)} {symbol} {MysqlAttributesTranslator.translate(condition.field1)}'
		return f"{MysqlConditionsTranslator.translate_field(condition.field1)} {symbol} {MysqlConditionsTranslator.translate_field(condition.field2)}"

	def translate_superior(condition):
		symbol = ">" if condition.strict else ">="
		if condition.field2 is None:
			return f'{MysqlConditionsTranslator.translate_field(condition.field1)} {symbol} {MysqlAttributesTranslator.translate(condition.field1)}'
		return f"{MysqlConditionsTranslator.translate_field(condition.field1)} {symbol} {MysqlConditionsTranslator.translate_field(condition.field2)}"

	def translate_between(condition):
		if condition.inf is None:
			return MysqlConditionsTranslator.translate_less(condition)
		elif condition.sup is None:
			return MysqlConditionsTranslator.translate_more(condition)

		if issubclass(type(condition.inf),Attribute):
			if condition.inf.value is not None:
				born1 = MysqlAttributesTranslator.translate(condition.inf)
			else:
				born1 = MysqlConditionsTranslator.translate_field(condition.inf)
		else:
			born1 = condition.inf

		if issubclass(type(condition.inf),Attribute):
			if condition.sup.value is not None:
				born2 = MysqlAttributesTranslator.translate(condition.sup)
			else:
				born2 = MysqlConditionsTranslator.translate_field(condition.sup)
		else:
			born2 = condition.sup

		return f'{MysqlConditionsTranslator.translate_field(condition.field)} BETWEEN {born1} AND {born2}'

	def translate_in(condition):
		if len(condition.values) == 0:
			raise BeforeHandUnmatchedCondition()
		return f"{MysqlConditionsTranslator.translate_field(condition.field)} in ({','.join([MysqlAttributesTranslator.translate(attr) for attr in condition.values])})"
		