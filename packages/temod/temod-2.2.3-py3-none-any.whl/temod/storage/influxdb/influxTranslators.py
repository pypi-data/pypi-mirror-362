from temod.storage.exceptions.translators import *
from temod.base.aggregation import *
from temod.base.condition import *
from temod.base.attribute import *

import base64


STRING_ESCAPE = str.maketrans({'"':  r'\"'})

class InfluxAttributesTranslator(object):
	"""docstring for InfluxAttributesTranslator"""

	def translate(attribute):
		if attribute.value is None:
			return "null"
		if type(attribute) is StringAttribute:
			return InfluxAttributesTranslator.translateString(attribute)
		elif type(attribute) is IntegerAttribute:
			return InfluxAttributesTranslator.translateInteger(attribute)
		elif type(attribute) is RealAttribute:
			return InfluxAttributesTranslator.translateReal(attribute)
		elif type(attribute) is BooleanAttribute:
			return InfluxAttributesTranslator.translateBool(attribute)
		elif type(attribute) is DateAttribute:
			return InfluxAttributesTranslator.translateDate(attribute)
		elif type(attribute) is DateTimeAttribute:
			return InfluxAttributesTranslator.translateDatetime(attribute)
		elif type(attribute) is UUID4Attribute:
			return InfluxAttributesTranslator.translateString(attribute)
		elif type(attribute) is UTF8BASE64Attribute:
			return InfluxAttributesTranslator.translateBase64UTF8(attribute)
		else:
			raise MysqlAttributeException(f"Can't translate attribute of type {type(attribute).__name__}")

	####################################
	# BASIC TRANSLATORS
	####################################

	def translateString(attribute):
		return f'"{attribute.value.translate(STRING_ESCAPE)}"'

	def translateInteger(attribute):
		return str(attribute.value)

	def translateReal(attribute):
		return str(attribute.value)

	def translateBool(attribute):
		if attribute.value is True:
			return "1"
		elif attribute.value is False:
			return "0"
		raise MysqlAttributeException(f"Can't translate value {attribute.value} for boolean attribute")

	def translateDate(attribute):
		return f'"{attribute.value.strftime("%Y-%m-%d")}"'

	def translateDatetime(attribute):
		return f'"{attribute.value.strftime("%Y-%m-%d %H:%M:%S")}"'

	def translateBase64UTF8(attribute):
		return f'"{base64.b64encode(attribute.value.encode()).decode("utf-8")}"'



class InfluxConditionsTranslator(object):
	"""docstring for InfluxConditionsTranslator"""

	def translate_field(attribute,var="r",measurement=None):
		if attribute.name == measurement:
			return f"{var}._measurement"
		return f"{var}.{attribute.name}"

	def translate(condition,measurement=None):
		if type(condition) is And:
			return InfluxConditionsTranslator.translate_and(condition,measurement=measurement)
		elif type(condition) is Or:
			return InfluxConditionsTranslator.translate_or(condition,measurement=measurement)
		elif type(condition) is Not:
			return InfluxConditionsTranslator.translate_not(condition,measurement=measurement)
		elif type(condition) is Equals:
			return InfluxConditionsTranslator.translate_equals(condition,measurement=measurement)
		elif type(condition) is StartsWith:
			return InfluxConditionsTranslator.translate_startswith(condition,measurement=measurement)
		elif type(condition) is In:
			return InfluxConditionsTranslator.translate_in(condition,measurement=measurement)
		else:
			raise ConditionTranslatorException(f"Can't translate condition of type {type(condition).__name__}")

	def translate_and(condition,measurement=None):
		return " and ".join(["("+InfluxConditionsTranslator.translate(sub_condition,measurement=measurement)+")" for sub_condition in condition.conditions])

	def translate_or(condition,measurement=None):
		return " or ".join(["("+InfluxConditionsTranslator.translate(sub_condition,measurement=measurement)+")" for sub_condition in condition.conditions])

	def translate_not(condition,measurement=None):
		return f" not ({InfluxConditionsTranslator.translate(condition.condition,measurement=measurement)})"

	def translate_startswith(condition,measurement=None):
		if condition.case_sensitive:
			condition.field.value = condition.field.value+"%"
			return f"{InfluxConditionsTranslator.translate_field(condition.field,measurement=measurement)} LIKE {InfluxAttributesTranslator.translate(condition.field)}"
		else:
			condition.field.value = condition.field.value.lower()+"%"
			return f"lower({InfluxConditionsTranslator.translate_field(condition.field,measurement=measurement)}) LIKE {InfluxAttributesTranslator.translate(condition.field)}"

	def translate_equals(condition,measurement=None):
		if condition.field2 is None:
			if condition.field1.value is None:
				return f'{InfluxConditionsTranslator.translate_field(condition.field1,measurement=measurement)} is null'
			return f'{InfluxConditionsTranslator.translate_field(condition.field1,measurement=measurement)} == {InfluxAttributesTranslator.translate(condition.field1)}'
		return f"{InfluxConditionsTranslator.translate_field(condition.field1,measurement=measurement)} == {InfluxConditionsTranslator.translate_field(condition.field2,measurement=measurement)}"

	def translate_in(condition,measurement=None):
		return f"{InfluxConditionsTranslator.translate_field(condition.field,measurement=measurement)} in ({','.join([InfluxAttributesTranslator.translate(attr) for attr in condition.values])})"
		


class InfluxAggregationsTranslator(object):
	"""docstring for InfluxAggregationsTranslator"""

	def translate(aggregation):
		if type(aggregation) is Window:
			return InfluxAggregationsTranslator.translate_window(aggregation)
		if type(aggregation) is Sum:
			return InfluxAggregationsTranslator.translate_sum(aggregation)
		else:
			raise ConditionTranslatorException(f"Can't translate aggregation of type {type(aggregation).__name__}")

	def translate_window(window):
		return f"aggregateWindow(every:{window.size}s, fn:{InfluxAggregationsTranslator.translate(window.function)}, createEmpty: {str(window.fill).lower()})"
	
	def translate_sum(sum_):
		return "sum"
