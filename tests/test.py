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
IT_SIMPLE_VAT_EXPECTED_ADDRESS = 'FORNO SCALDOTTO DI FEFFO FORNI 10 INT 8'
IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE = '44123'
IT_SIMPLE_VAT_EXPECTED_CITY = 'FERRARA'
IT_SIMPLE_VAT_EXPECTED_PROVINCE = 'FE'
IT_SIMPLE_VAT_ADDRESS_STRING = (IT_SIMPLE_VAT_EXPECTED_ADDRESS + '\n' + ' ' + IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE
                                + ' ' + IT_SIMPLE_VAT_EXPECTED_CITY + ' ' + IT_SIMPLE_VAT_EXPECTED_PROVINCE + '\n')

IT_SIMPLE_VAT_EXPECTED_ADDRESS_S10 = S10 + IT_SIMPLE_VAT_EXPECTED_ADDRESS + S10
IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE_S10 = S10 + IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE + S10
IT_SIMPLE_VAT_EXPECTED_CITY_S10 = S10 + IT_SIMPLE_VAT_EXPECTED_CITY + S10
IT_SIMPLE_VAT_EXPECTED_PROVINCE_S10 = S10 + IT_SIMPLE_VAT_EXPECTED_PROVINCE + S10
IT_SIMPLE_VAT_ADDRESS_STRING_S10 = (IT_SIMPLE_VAT_EXPECTED_ADDRESS_S10 + '\n' + ' ' + IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE_S10
                                + ' ' + IT_SIMPLE_VAT_EXPECTED_CITY_S10 + ' ' + IT_SIMPLE_VAT_EXPECTED_PROVINCE_S10 + '\n')

IT_SIMPLE_VAT_ADDRESS_STRING_NO_MIDDLE_SPACE = (IT_SIMPLE_VAT_EXPECTED_ADDRESS + '\n' + IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE
                                + ' ' + IT_SIMPLE_VAT_EXPECTED_CITY + ' ' + IT_SIMPLE_VAT_EXPECTED_PROVINCE + '\n')

IT_SIMPLE_VAT_NOT_VALID_FIRST_CASE = (IT_SIMPLE_VAT_EXPECTED_ADDRESS + ' ' + IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE
                                + ' ' + IT_SIMPLE_VAT_EXPECTED_CITY + ' ' + IT_SIMPLE_VAT_EXPECTED_PROVINCE + '\n')

IT_SIMPLE_VAT_NOT_VALID_SECOND_CASE = (IT_SIMPLE_VAT_EXPECTED_ADDRESS + '\n' + ' ' + IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE
                                + ' ' + IT_SIMPLE_VAT_EXPECTED_CITY + ' ' + IT_SIMPLE_VAT_EXPECTED_PROVINCE)

IT_SIMPLE_VAT_STRICT_NOT_VALID_POSTAL_CODE_CASE = (IT_SIMPLE_VAT_EXPECTED_ADDRESS + '\n' + ' ' + IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE[:-1]
                                + ' ' + IT_SIMPLE_VAT_EXPECTED_CITY + ' ' + IT_SIMPLE_VAT_EXPECTED_PROVINCE + '\n')

IT_SIMPLE_VAT_STRICT_NOT_VALID_PROVINCE_CASE = (IT_SIMPLE_VAT_EXPECTED_ADDRESS + '\n' + ' ' + IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE
                                + ' ' + IT_SIMPLE_VAT_EXPECTED_CITY + ' ' + IT_SIMPLE_VAT_EXPECTED_PROVINCE[:-1] + '\n')

IT_SIMPLE_VAT_ADDRESS_STRING = (IT_SIMPLE_VAT_EXPECTED_ADDRESS + '\n' + ' ' + IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE
                                + ' ' + IT_SIMPLE_VAT_EXPECTED_CITY + ' ' + IT_SIMPLE_VAT_EXPECTED_PROVINCE + '\n')

class TestApi(unittest.TestCase):
    r"""Test the main API."""

    def test_parse_address_string_IT(self):
        # A generic valid VAT record.
        expected_simple = {
            'address': IT_SIMPLE_VAT_EXPECTED_ADDRESS,
            'postal code': IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE,
            'city': IT_SIMPLE_VAT_EXPECTED_CITY,
            'province': IT_SIMPLE_VAT_EXPECTED_PROVINCE
        }
        self.assertEqual(api.parse_address_string(IT_SIMPLE_VAT_ADDRESS_STRING, DEFAULT_COUNTRY), expected_simple)
        self.assertEqual(api.parse_address_string(IT_SIMPLE_VAT_ADDRESS_STRING, DEFAULT_COUNTRY, strict=True), expected_simple)
        self.assertEqual(api.parse_address_string(IT_SIMPLE_VAT_ADDRESS_STRING_S10, DEFAULT_COUNTRY), expected_simple)
        self.assertEqual(api.parse_address_string(IT_SIMPLE_VAT_ADDRESS_STRING_S10, DEFAULT_COUNTRY, strict=True), expected_simple)
        self.assertEqual(api.parse_address_string(IT_SIMPLE_VAT_ADDRESS_STRING_NO_MIDDLE_SPACE, DEFAULT_COUNTRY), expected_simple)
        self.assertEqual(api.parse_address_string(IT_SIMPLE_VAT_ADDRESS_STRING_NO_MIDDLE_SPACE, DEFAULT_COUNTRY, strict=True), expected_simple)

        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(IT_SIMPLE_VAT_NOT_VALID_FIRST_CASE, DEFAULT_COUNTRY)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(IT_SIMPLE_VAT_NOT_VALID_SECOND_CASE, DEFAULT_COUNTRY)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(IT_SIMPLE_VAT_NOT_VALID_FIRST_CASE, DEFAULT_COUNTRY, strict=True)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(IT_SIMPLE_VAT_NOT_VALID_SECOND_CASE, DEFAULT_COUNTRY, strict=True)

        # Postal code not conforming case.
        expected_simple_patch = copy.copy(expected_simple)
        expected_simple_patch['postal code'] = IT_SIMPLE_VAT_EXPECTED_POSTAL_CODE[:-1]
        self.assertEqual(api.parse_address_string(IT_SIMPLE_VAT_STRICT_NOT_VALID_POSTAL_CODE_CASE, DEFAULT_COUNTRY), expected_simple_patch)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            self.assertEqual(api.parse_address_string(IT_SIMPLE_VAT_STRICT_NOT_VALID_POSTAL_CODE_CASE, DEFAULT_COUNTRY, strict=True), expected_simple_patch)

        # Province name not conforming case.
        expected_simple_patch = copy.copy(expected_simple)
        expected_simple_patch['province'] = IT_SIMPLE_VAT_EXPECTED_PROVINCE[:-1]
        self.assertEqual(api.parse_address_string(IT_SIMPLE_VAT_STRICT_NOT_VALID_PROVINCE_CASE, DEFAULT_COUNTRY), expected_simple_patch)
        with self.assertRaises(exceptions.AddressStringNotCorrespondingToExpectedFormat):
            self.assertEqual(api.parse_address_string(IT_SIMPLE_VAT_STRICT_NOT_VALID_PROVINCE_CASE, DEFAULT_COUNTRY, strict=True), expected_simple_patch)

