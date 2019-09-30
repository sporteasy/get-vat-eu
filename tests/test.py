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

DEFAULT_COUNTRY = 'IT'

##################
# COUNTRY = 'IT' #
##################


"""

# City with spaces.
IT_VAT_EXPECTED_CITY_WITH_SPACES = 'MALBORGHETTO DI BOARA'
IT_CITY_WITH_SPACES_VAT_ADDRESS_STRING = (IT_SIMPLE_VAT_EXPECTED_ADDRESS + '\n' + ' ' + IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE
                                + ' ' + IT_VAT_EXPECTED_CITY_WITH_SPACES + ' ' + IT_SIMPLE_VAT_EXPECTED_PROVINCE + '\n')

IT_CITY_WITH_SPACES_VAT_EXPECTED_CITY_WITH_SPACES_S10 = S10 + 'MALBORGHETTO DI BOARA' + S10
IT_CITY_WITH_SPACES_VAT_ADDRESS_STRING_S10 = (IT_SIMPLE_VAT_EXPECTED_ADDRESS_S10 + '\n' + ' ' + IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE_S10
                                + ' ' + IT_CITY_WITH_SPACES_VAT_EXPECTED_CITY_WITH_SPACES_S10 + ' ' + IT_SIMPLE_VAT_EXPECTED_PROVINCE_S10 + '\n')

IT_CITY_WITH_SPACES_VAT_ADDRESS_STRING_NO_MIDDLE_SPACE = (IT_SIMPLE_VAT_EXPECTED_ADDRESS + '\n' + IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE
                                + ' ' + IT_VAT_EXPECTED_CITY_WITH_SPACES + ' ' + IT_SIMPLE_VAT_EXPECTED_PROVINCE + '\n')
"""

class TestApi(unittest.TestCase):
    r"""Test the main API."""

    def test_parse_address_string_IT(self):
        r"""

            Schema:
                   field = ${CASE}_EXPECTED_${FIELD}[_${EXCEPTION_TO_THE_ORIGINAL_CASE}]
                   BASE_ADDRESS_STRING[_${EXCEPTIONS_TO_THE_ORIGINAL_CASE}] = (${fields})
        """

        COUNTRY_CODE = 'IT'

        # Base case.
        BASE_EXPECTED_ADDRESS = 'FORNO SCALDOTTO DI FEFFO FORNI 10 INT 8'
        BASE_EXPECTED_POSTAL_CODE = '44123'
        BASE_EXPECTED_CITY = 'FERRARA'
        BASE_EXPECTED_PROVINCE = 'FE'
        BASE_ADDRESS_STRING = (BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE
                                   + ' ' + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        # Prepend and append a fixed number of spaces.
        BASE_EXPECTED_ADDRESS_S10 = S10 + BASE_EXPECTED_ADDRESS + S10
        BASE_EXPECTED_POSTAL_CODE_S10 = S10 + BASE_EXPECTED_POSTAL_CODE + S10
        BASE_EXPECTED_CITY_S10 = S10 + BASE_EXPECTED_CITY + S10
        BASE_EXPECTED_PROVINCE_S10 = S10 + BASE_EXPECTED_PROVINCE + S10
        BASE_ADDRESS_STRING_S10 = (BASE_EXPECTED_ADDRESS_S10 + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE_S10
                                        + ' ' + BASE_EXPECTED_CITY_S10 + ' ' + BASE_EXPECTED_PROVINCE_S10 + '\n')

        # Remove the middle space from the string.
        BASE_ADDRESS_STRING_NO_MIDDLE_SEPARATOR = (BASE_EXPECTED_ADDRESS + '\n' + BASE_EXPECTED_POSTAL_CODE
                                        + ' ' + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        BASE_ADDRESS_STRING_MISSING_FIRST_DELIMITER = (BASE_EXPECTED_ADDRESS + ' ' + BASE_EXPECTED_POSTAL_CODE
                                        + ' ' + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        BASE_ADDRESS_STRING_MISSING_LAST_DELIMITER = (BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE
                                        + ' ' + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE)

        BASE_ADDRESS_STRING_MISSING_BOTH_DELIMITERS = (BASE_EXPECTED_ADDRESS + ' ' + BASE_EXPECTED_POSTAL_CODE
                                        + ' ' + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE)

        BASE_ADDRESS_STRING_POSTAL_CODE_NOT_CONFORMING = (BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE[:-1]
                                        + ' ' + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        BASE_ADDRESS_STRING_PROVINCE_NOT_CONFORMING = (BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE
                                        + ' ' + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE[:-1] + '\n')

        BASE_ADDRESS_STRING_POSTAL_CODE_NOT_EXISTS = (BASE_EXPECTED_ADDRESS + '\n' + ' ' + ' '
                                        + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        BASE_ADDRESS_STRING_CITY_NOT_EXISTS = (BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE
                                        + ' ' + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        BASE_ADDRESS_STRING_PROVINCE_NOT_EXISTS = (BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POSTAL_CODE
                                        + ' ' + BASE_EXPECTED_CITY + ' ' + '\n')


        # A generic valid VAT record.
        expected_base = {
            'address': BASE_EXPECTED_ADDRESS,
            'postal code': BASE_EXPECTED_POSTAL_CODE,
            'city': BASE_EXPECTED_CITY,
            'province': BASE_EXPECTED_PROVINCE
        }
        self.assertEqual(api.parse_address_string(BASE_ADDRESS_STRING, COUNTRY_CODE), expected_base)
        self.assertEqual(api.parse_address_string(BASE_ADDRESS_STRING, COUNTRY_CODE, strict=True), expected_base)
        self.assertEqual(api.parse_address_string(BASE_ADDRESS_STRING_S10, COUNTRY_CODE), expected_base)
        self.assertEqual(api.parse_address_string(BASE_ADDRESS_STRING_S10, COUNTRY_CODE, strict=True), expected_base)
        self.assertEqual(api.parse_address_string(BASE_ADDRESS_STRING_NO_MIDDLE_SEPARATOR, COUNTRY_CODE), expected_base)
        self.assertEqual(api.parse_address_string(BASE_ADDRESS_STRING_NO_MIDDLE_SEPARATOR, COUNTRY_CODE, strict=True), expected_base)

        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(BASE_ADDRESS_STRING_MISSING_FIRST_DELIMITER, COUNTRY_CODE)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(BASE_ADDRESS_STRING_MISSING_FIRST_DELIMITER, COUNTRY_CODE, strict=True)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(BASE_ADDRESS_STRING_MISSING_LAST_DELIMITER, COUNTRY_CODE)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(BASE_ADDRESS_STRING_MISSING_LAST_DELIMITER, COUNTRY_CODE, strict=True)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(BASE_ADDRESS_STRING_MISSING_BOTH_DELIMITERS, COUNTRY_CODE)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(BASE_ADDRESS_STRING_MISSING_BOTH_DELIMITERS, COUNTRY_CODE, strict=True)

        expected_base_patch = copy.copy(expected_base)
        expected_base_patch['postal code'] = BASE_EXPECTED_POSTAL_CODE[:-1]
        self.assertEqual(api.parse_address_string(BASE_ADDRESS_STRING_POSTAL_CODE_NOT_CONFORMING, DEFAULT_COUNTRY), expected_base_patch)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            self.assertEqual(api.parse_address_string(BASE_ADDRESS_STRING_POSTAL_CODE_NOT_CONFORMING, DEFAULT_COUNTRY, strict=True), expected_simple_patch)

        expected_base_patch = copy.copy(expected_base)
        expected_base_patch['province'] = BASE_EXPECTED_PROVINCE[:-1]
        self.assertEqual(api.parse_address_string(BASE_ADDRESS_STRING_PROVINCE_NOT_CONFORMING, DEFAULT_COUNTRY), expected_base_patch)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            self.assertEqual(api.parse_address_string(BASE_ADDRESS_STRING_PROVINCE_NOT_CONFORMING, DEFAULT_COUNTRY, strict=True), expected_simple_patch)

        """
        # No postal code.
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(IT_SIMPLE_VAT_ADDRESS_STRING_NOT_VALID_NO_POSTAL_CODE, DEFAULT_COUNTRY)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(IT_SIMPLE_VAT_ADDRESS_STRING_NOT_VALID_NO_POSTAL_CODE, DEFAULT_COUNTRY, strict=True)

        # No city.
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(IT_SIMPLE_VAT_ADDRESS_STRING_NOT_VALID_NO_CITY, DEFAULT_COUNTRY)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(IT_SIMPLE_VAT_ADDRESS_STRING_NOT_VALID_NO_CITY, DEFAULT_COUNTRY, strict=True)

        # No province.
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(IT_SIMPLE_VAT_ADDRESS_STRING_NOT_VALID_NO_PROVINCE, DEFAULT_COUNTRY)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(IT_SIMPLE_VAT_ADDRESS_STRING_NOT_VALID_NO_PROVINCE, DEFAULT_COUNTRY, strict=True)

        ########################################
        # City with spaces: Repeat every test. #
        ########################################
        expected_city_with_spaces = {
            'address': IT_SIMPLE_VAT_EXPECTED_ADDRESS,
            'postal code': IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE,
            'city': IT_VAT_EXPECTED_CITY_WITH_SPACES,
            'province': IT_SIMPLE_VAT_EXPECTED_PROVINCE
        }

        self.assertEqual(api.parse_address_string(IT_CITY_WITH_SPACES_VAT_ADDRESS_STRING, DEFAULT_COUNTRY), expected_city_with_spaces)
        self.assertEqual(api.parse_address_string(IT_CITY_WITH_SPACES_VAT_ADDRESS_STRING, DEFAULT_COUNTRY, strict=True), expected_city_with_spaces)
        self.assertEqual(api.parse_address_string(IT_CITY_WITH_SPACES_VAT_ADDRESS_STRING_S10, DEFAULT_COUNTRY), expected_city_with_spaces)
        self.assertEqual(api.parse_address_string(IT_CITY_WITH_SPACES_VAT_ADDRESS_STRING_S10, DEFAULT_COUNTRY, strict=True), expected_city_with_spaces)
        self.assertEqual(api.parse_address_string(IT_CITY_WITH_SPACES_VAT_ADDRESS_STRING_NO_MIDDLE_SPACE, DEFAULT_COUNTRY), expected_city_with_spaces)
        self.assertEqual(api.parse_address_string(IT_CITY_WITH_SPACES_VAT_ADDRESS_STRING_NO_MIDDLE_SPACE, DEFAULT_COUNTRY, strict=True), expected_city_with_spaces)
        """
