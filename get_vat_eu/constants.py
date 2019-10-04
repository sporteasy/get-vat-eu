#
# constants.py
#

common_defaults = dict()

urls = dict()
urls['ec_check_vat_api'] = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'

vat = dict()
vat['regex'] = "((ATU|DK|FI|HU|LU|MT|SI)[0-9]{8}|(BE|BG)[0-9]{9,10}|(ES([0-9]|[A-Z])[0-9]{7}([A-Z]|[0-9]))|(HR|IT|LV)[0-9]{11}|CY[0-9]{8}[A-Z]|CZ[0-9]{8,10}|(DE|EE|EL|GB|PT)[0-9]{9}|FR[A-Z0-9]{2}[0-9]{8}[A-Z0-9]|IE[0-9]{7}[A-Z0-9]{2}|LT[0-9]{9}([0-9]{3})?|NL[0-9]{9}B([0-9]{2})|PL[0-9]{10}|RO[0-9]{2,10}|SK[0-9]{10}|SE[0-9]{12})"

countries = dict()

countries['code'] = dict()
countries['code']['default'] = 'IT'

countries['IT'] = dict()
countries['IT']['address_string'] = dict()
countries['IT']['address_string']['separator'] = '\n'
countries['IT']['address_string']['delimiter'] = ' '

countries['IT']['address_string']['expected_fields'] = ['address', 'postal_code', 'province', 'city']

countries['IT']['post_code'] = dict()
countries['IT']['post_code']['regex'] = "^\d{5}"

countries['IT']['province'] = dict()
countries['IT']['province']['regex'] = "^[A-Z]{2}$"
