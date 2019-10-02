#
# tests.py
#
"""The tests module."""

from get_vat_eu import (api, exceptions, constants)
import unittest
import copy

S1 = ' '
S2 = 2 * ' '
S3 = 3 * ' '
S4 = 4 * ' '
S5 = 5 * ' '
S10 = 10 * ' '

class TestApi(unittest.TestCase):
    r"""Test the main API."""

    def _test_parse_address_string_IT_default(self, expected: dict, variables: dict):

        COUNTRY_CODE = 'IT'

        self.assertEqual(api.parse_address_string(variables['ADDRESS_STRING'], COUNTRY_CODE), expected)
        self.assertEqual(api.parse_address_string(variables['ADDRESS_STRING'], COUNTRY_CODE, strict=True), expected)
        self.assertEqual(api.parse_address_string(variables['ADDRESS_STRING_S10'], COUNTRY_CODE), expected)
        self.assertEqual(api.parse_address_string(variables['ADDRESS_STRING_S10'], COUNTRY_CODE, strict=True), expected)
        self.assertEqual(api.parse_address_string(variables['ADDRESS_STRING_NO_MIDDLE_SEPARATOR'], COUNTRY_CODE), expected)
        self.assertEqual(api.parse_address_string(variables['ADDRESS_STRING_NO_MIDDLE_SEPARATOR'], COUNTRY_CODE, strict=True), expected)

        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(variables['ADDRESS_STRING_MISSING_FIRST_DELIMITER'], COUNTRY_CODE)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(variables['ADDRESS_STRING_MISSING_FIRST_DELIMITER'], COUNTRY_CODE, strict=True)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(variables['ADDRESS_STRING_MISSING_LAST_DELIMITER'], COUNTRY_CODE)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(variables['ADDRESS_STRING_MISSING_LAST_DELIMITER'], COUNTRY_CODE, strict=True)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(variables['ADDRESS_STRING_MISSING_BOTH_DELIMITERS'], COUNTRY_CODE)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(variables['ADDRESS_STRING_MISSING_BOTH_DELIMITERS'], COUNTRY_CODE, strict=True)

        expected_patch = copy.copy(expected)
        expected_patch['postal code'] = variables['EXPECTED_POSTAL_CODE'][:-1]
        self.assertEqual(api.parse_address_string(variables['ADDRESS_STRING_POSTAL_CODE_NOT_CONFORMING'], COUNTRY_CODE), expected_patch)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            self.assertEqual(api.parse_address_string(variables['ADDRESS_STRING_POSTAL_CODE_NOT_CONFORMING'], COUNTRY_CODE, strict=True), expected_patch)

        expected_patch = copy.copy(expected)
        expected_patch['province'] = variables['EXPECTED_PROVINCE'][:-1]
        self.assertEqual(api.parse_address_string(variables['ADDRESS_STRING_PROVINCE_NOT_CONFORMING'], COUNTRY_CODE), expected_patch)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            self.assertEqual(api.parse_address_string(variables['ADDRESS_STRING_PROVINCE_NOT_CONFORMING'], COUNTRY_CODE, strict=True), expected_patch)

        # No postal code.
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(variables['ADDRESS_STRING_POSTAL_CODE_NOT_EXISTS'], COUNTRY_CODE)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(variables['ADDRESS_STRING_POSTAL_CODE_NOT_EXISTS'], COUNTRY_CODE, strict=True)

        # No city.
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(variables['ADDRESS_STRING_CITY_NOT_EXISTS'], COUNTRY_CODE)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(variables['ADDRESS_STRING_CITY_NOT_EXISTS'], COUNTRY_CODE, strict=True)

        # No province.
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(variables['ADDRESS_STRING_PROVINCE_NOT_EXISTS'], COUNTRY_CODE)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(variables['ADDRESS_STRING_PROVINCE_NOT_EXISTS'], COUNTRY_CODE, strict=True)


    def test_parse_address_string_IT(self):
        r"""

        .. note:: variable naming schema:
                   field = ${CASE}_EXPECTED_${FIELD}[_${EXCEPTION_TO_THE_ORIGINAL_CASE}]
                   BASE_ADDRESS_STRING[_${EXCEPTIONS_TO_THE_ORIGINAL_CASE}] = (${fields})
        """

        variables = dict()

        # Base case.
        BASE_EXPECTED_ADDRESS = 'FORNO SCALDOTTO DI FEFFO FORNI 10 INT 8'
        BASE_EXPECTED_POSTAL_CODE = '44123'
        BASE_EXPECTED_CITY = 'FERRARA'
        BASE_EXPECTED_PROVINCE = 'FE'
        # FIXME.
        variables['EXPECTED_POSTAL_CODE'] = BASE_EXPECTED_POSTAL_CODE
        variables['EXPECTED_PROVINCE'] = BASE_EXPECTED_PROVINCE
        variables['ADDRESS_STRING'] = (BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE
                                   + ' ' + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        # Prepend and append a fixed number of spaces.
        BASE_EXPECTED_ADDRESS_S10 = S10 + BASE_EXPECTED_ADDRESS + S10
        BASE_EXPECTED_POSTAL_CODE_S10 = S10 + BASE_EXPECTED_POSTAL_CODE + S10
        BASE_EXPECTED_CITY_S10 = S10 + BASE_EXPECTED_CITY + S10
        BASE_EXPECTED_PROVINCE_S10 = S10 + BASE_EXPECTED_PROVINCE + S10
        variables['ADDRESS_STRING_S10'] = (BASE_EXPECTED_ADDRESS_S10 + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE_S10
                                        + ' ' + BASE_EXPECTED_CITY_S10 + ' ' + BASE_EXPECTED_PROVINCE_S10 + '\n')

        # Remove the middle space from the string.
        variables['ADDRESS_STRING_NO_MIDDLE_SEPARATOR'] = (BASE_EXPECTED_ADDRESS + '\n' + BASE_EXPECTED_POSTAL_CODE
                                        + ' ' + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        variables['ADDRESS_STRING_MISSING_FIRST_DELIMITER'] = (BASE_EXPECTED_ADDRESS + ' ' + BASE_EXPECTED_POSTAL_CODE
                                        + ' ' + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        variables['ADDRESS_STRING_MISSING_LAST_DELIMITER'] = (BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE
                                        + ' ' + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE)

        variables['ADDRESS_STRING_MISSING_BOTH_DELIMITERS'] = (BASE_EXPECTED_ADDRESS + ' ' + BASE_EXPECTED_POSTAL_CODE
                                        + ' ' + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE)

        variables['ADDRESS_STRING_POSTAL_CODE_NOT_CONFORMING'] = (BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE[:-1]
                                        + ' ' + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        variables['ADDRESS_STRING_PROVINCE_NOT_CONFORMING'] = (BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE
                                        + ' ' + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE[:-1] + '\n')

        variables['ADDRESS_STRING_POSTAL_CODE_NOT_EXISTS'] = (BASE_EXPECTED_ADDRESS + '\n' + ' ' + ' '
                                        + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        variables['ADDRESS_STRING_CITY_NOT_EXISTS'] = (BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE
                                        + ' ' + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        variables['ADDRESS_STRING_PROVINCE_NOT_EXISTS'] = (BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE
                                        + ' ' + BASE_EXPECTED_CITY + ' ' + '\n')

        ##############################
        # City field without spaces. #
        ##############################

        # A generic valid VAT record.
        expected_base = {
            'address': BASE_EXPECTED_ADDRESS,
            'postal code': BASE_EXPECTED_POSTAL_CODE,
            'city': BASE_EXPECTED_CITY,
            'province': BASE_EXPECTED_PROVINCE
        }

        self._test_parse_address_string_IT_default(expected_base, variables)

        ###########################
        # City field with spaces. #
        ###########################
        COMPLEX_EXPECTED_CITY = 'MALBORGHETTO DI BOARA'
        COMPLEX_ADDRESS_STRING = (BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE
                                   + ' ' + COMPLEX_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        COMPLEX_EXPECTED_CITY_S10 = S10 + COMPLEX_EXPECTED_CITY + S10
        COMPLEX_ADDRESS_STRING_S10 = (BASE_EXPECTED_ADDRESS_S10 + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE_S10
                                        + ' ' + COMPLEX_EXPECTED_CITY_S10 + ' ' + BASE_EXPECTED_PROVINCE_S10 + '\n')

        # Remove the middle space from the string.
        COMPLEX_ADDRESS_STRING_NO_MIDDLE_SEPARATOR = (BASE_EXPECTED_ADDRESS + '\n' + BASE_EXPECTED_POSTAL_CODE
                                        + ' ' + COMPLEX_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')


        expected_complex = {
            'address': BASE_EXPECTED_ADDRESS,
            'postal code': BASE_EXPECTED_POSTAL_CODE,
            'city': COMPLEX_EXPECTED_CITY,
            'province': BASE_EXPECTED_PROVINCE
        }

