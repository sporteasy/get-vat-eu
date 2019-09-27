#
# tests.py
#
"""The tests module."""

from get_vat_eu import (api, exceptions, constants)
import unittest

SIMPLE_VAT_EXPECTED_ADDRESS = 'FORNO SCALDOTTO DI FEFFO FORNI 10 INT 8'
SIMPLE_VAT_EXPECTED_POSTAL_CODE = '44123'
SIMPLE_VAT_EXPECTED_CITY = 'FERRARA'
SIMPLE_VAT_EXPECTED_PROVINCE = 'FE'

SIMPLE_VAT_ADDRESS_STRING = (SIMPLE_VAT_EXPECTED_ADDRESS + '\n' + ' ' + SIMPLE_VAT_EXPECTED_POSTAL_CODE
                                + ' ' + SIMPLE_VAT_EXPECTED_CITY + ' ' + SIMPLE_VAT_EXPECTED_PROVINCE + '\n')

DEFAULT_COUNTRY = 'IT'

class TestApi(unittest.TestCase):
    r"""Test the main API."""

    def test_parse_address_string(self):
        # A generic valid VAT record.
        expected = {
            'address': SIMPLE_VAT_EXPECTED_ADDRESS,
            'postal code': SIMPLE_VAT_EXPECTED_POSTAL_CODE,
            'city': SIMPLE_VAT_EXPECTED_CITY,
            'province': SIMPLE_VAT_EXPECTED_PROVINCE
        }
        self.assertEqual(api.parse_address_string(SIMPLE_VAT_ADDRESS_STRING, DEFAULT_COUNTRY), expected)
        self.assertEqual(api.parse_address_string(SIMPLE_VAT_ADDRESS_STRING, DEFAULT_COUNTRY, strict=True), expected)
