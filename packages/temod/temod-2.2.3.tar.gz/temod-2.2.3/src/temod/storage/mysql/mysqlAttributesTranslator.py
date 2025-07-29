from temod.storage.exceptions import *

from temod.base.attribute import *

import binascii
import base64

STRING_ESCAPE = str.maketrans({'"':  r'\"'})

class MysqlAttributesTranslator(object):
	"""docstring for MysqlAttributesTranslator"""

	def translate(attribute):
		if attribute.value is None:
			return "null"
		if type(attribute) in [StringAttribute, EmailAttribute, PhoneNumberAttribute, UUID4Attribute]:
			return MysqlAttributesTranslator.translateString(attribute)
		if type(attribute) in [BytesAttribute, BCryptedAttribute]:
			return MysqlAttributesTranslator.translateBytes(attribute)
		elif type(attribute) is IntegerAttribute:
			return MysqlAttributesTranslator.translateInteger(attribute)
		elif type(attribute) is RealAttribute:
			return MysqlAttributesTranslator.translateReal(attribute)
		elif type(attribute) is BooleanAttribute:
			return MysqlAttributesTranslator.translateBool(attribute)
		elif type(attribute) is DateAttribute:
			return MysqlAttributesTranslator.translateDate(attribute)
		elif type(attribute) is TimeAttribute:
			return MysqlAttributesTranslator.translateTime(attribute)
		elif type(attribute) is DateTimeAttribute:
			return MysqlAttributesTranslator.translateDatetime(attribute)
		elif type(attribute) is UTF8BASE64Attribute:
			return MysqlAttributesTranslator.translateBase64UTF8(attribute)
		elif type(attribute) is RangeAttribute:
			return MysqlAttributesTranslator.translateInteger(attribute)
		elif type(attribute) is EnumAttribute:
			return MysqlAttributesTranslator.translateEnum(attribute)
		else:
			raise AttributeTranslatorException(f"Can't translate attribute of type {type(attribute).__name__}")

	####################################
	# BASIC TRANSLATORS
	####################################

	def translateString(attribute):
		return f'"{attribute.value.translate(STRING_ESCAPE)}"'

	def translateBytes(attribute):
		return f'0x{binascii.hexlify(attribute.value).decode()}'

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

	def translateTime(attribute):
		return f'"{attribute.value.strftime("%H:%M:%S")}"'

	def translateDatetime(attribute):
		return f'"{attribute.value.strftime("%Y-%m-%d %H:%M:%S")}"'

	def translateBase64UTF8(attribute):
		return f'"{base64.b64encode(attribute.value.encode()).decode("utf-8")}"'

	def translateEnum(attribute):
		return f'{attribute.value.value}'