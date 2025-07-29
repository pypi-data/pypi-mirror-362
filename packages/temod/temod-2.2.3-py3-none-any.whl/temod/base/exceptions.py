COMMON_ERROR_CODE = "0x0"

class AttributeValueException(Exception):
	def __init__(self, attribute, *args, code=None, **kwargs):
		super(AttributeValueException, self).__init__(*args, **kwargs)
		self.attribute = attribute
		if code is not None:
			self.code = code
		elif hasattr(type(self),'CODE'):
			self.code = type(self).CODE

class NonNullableError(AttributeValueException):
	CODE = COMMON_ERROR_CODE+"0"

class WrongTypeError(AttributeValueException):
	CODE = COMMON_ERROR_CODE+"1"

class ForceCastError(AttributeValueException):
	CODE = COMMON_ERROR_CODE+"2"

""" StringAttribute Exceptions"""

STRING_ERROR_CODE = "0x1"

class OverMaxLengthError(AttributeValueException):
	CODE = STRING_ERROR_CODE+"0"

class BelowMinLengthError(AttributeValueException):
	CODE = STRING_ERROR_CODE+"1"

class EmptyStringError(AttributeValueException):
	CODE = STRING_ERROR_CODE+"2"

class StringFormatError(AttributeValueException):
	CODE = STRING_ERROR_CODE+"3"
		

""" NumericAttribute Exceptions"""

NUMERIC_ERROR_CODE = "0x2"

class NumericOverBoundError(AttributeValueException):
	CODE = NUMERIC_ERROR_CODE+"0"

class NumericBelowBoundError(AttributeValueException):
	CODE = NUMERIC_ERROR_CODE+"1"
		
		

""" DateAttribute Exceptions"""

DATE_ERROR_CODE = "0x3"

class DateOverBoundError(AttributeValueException):
	CODE = DATE_ERROR_CODE+"0"

class DateBelowBoundError(AttributeValueException):
	CODE = DATE_ERROR_CODE+"1"


""" EmailAttribute Exceptions"""

EMAIL_ERROR_CODE = "0x4"

class WrongEmailFormat(AttributeValueException):
	CODE = EMAIL_ERROR_CODE+"0"


""" PhoneNumberAttribute Exceptions"""

PHONE_NUMBER_ERROR_CODE = "0x5"

class WrongPhoneNumberFormat(AttributeValueException):
	CODE = PHONE_NUMBER_ERROR_CODE+"0"
		


""" EnumAttribute Exceptions"""

ENUM_ERROR_CODE = "0x6"

class UnknownValueError(AttributeValueException):
	CODE = ENUM_ERROR_CODE+"0"
		