#
# constants.py
#

common_defaults = dict()

urls = dict()

urls['ec check vat api'] = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'

countries = dict()

countries['code'] = dict()
countries['code']['default'] = 'IT'

countries['IT'] = dict()
countries['IT']['address string'] = dict()
countries['IT']['address string']['separator'] = '\n'
countries['IT']['address string']['delimiter'] = ' '

countries['IT']['address string']['expected fields'] = ['address', 'postal code', 'province', 'city']
