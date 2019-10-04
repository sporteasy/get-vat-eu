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

    def _test_parse_address_string_IT_common(self, expected: dict,
                                             variables: dict):
        """Common tests."""
        COUNTRY_CODE = 'IT'

        self.assertEqual(
            api.parse_address_string(variables['ADDRESS_STRING'],
                                     COUNTRY_CODE), expected)
        self.assertEqual(
            api.parse_address_string(variables['ADDRESS_STRING_S10'],
                                     COUNTRY_CODE), expected)
        self.assertEqual(
            api.parse_address_string(
                variables['ADDRESS_STRING_NO_MIDDLE_SEPARATOR'], COUNTRY_CODE),
            expected)

        with self.assertRaises(
                exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(
                variables['ADDRESS_STRING_MISSING_FIRST_DELIMITER'],
                COUNTRY_CODE)
        with self.assertRaises(
                exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(
                variables['ADDRESS_STRING_MISSING_LAST_DELIMITER'],
                COUNTRY_CODE)
        with self.assertRaises(
                exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(
                variables['ADDRESS_STRING_MISSING_BOTH_DELIMITERS'],
                COUNTRY_CODE)

        expected_patch = copy.copy(expected)
        expected_patch['post_code'] = variables['EXPECTED_POST_CODE'][:-1]
        with self.assertRaises(
                exceptions.AddressStringNotCorrespondingToExpectedFormat):
            self.assertEqual(
                api.parse_address_string(
                    variables['ADDRESS_STRING_POST_CODE_NOT_CONFORMING'],
                    COUNTRY_CODE), expected_patch)

        expected_patch = copy.copy(expected)
        expected_patch['province'] = variables['EXPECTED_PROVINCE'][:-1]
        with self.assertRaises(
                exceptions.AddressStringNotCorrespondingToExpectedFormat):
            self.assertEqual(
                api.parse_address_string(
                    variables['ADDRESS_STRING_PROVINCE_NOT_CONFORMING'],
                    COUNTRY_CODE), expected_patch)

        # No postal code.
        with self.assertRaises(
                exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(
                variables['ADDRESS_STRING_POST_CODE_NOT_EXISTS'], COUNTRY_CODE)

        # No city.
        with self.assertRaises(
                exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(
                variables['ADDRESS_STRING_CITY_NOT_EXISTS'], COUNTRY_CODE)

        # No province.
        with self.assertRaises(
                exceptions.AddressStringNotCorrespondingToExpectedFormat):
            api.parse_address_string(
                variables['ADDRESS_STRING_PROVINCE_NOT_EXISTS'], COUNTRY_CODE)

    def test_parse_address_string_IT(self):
        r"""Test.

        .. note:: variable naming schema:
                   field = ${CASE}_EXPECTED_${FIELD}[_${EXCEPTION_TO_THE_ORIGINAL_CASE}]
                   BASE_ADDRESS_STRING[_${EXCEPTIONS_TO_THE_ORIGINAL_CASE}] = (${fields})
        """
        ##############################
        # City field without spaces. #
        ##############################

        variables = dict()

        BASE_EXPECTED_ADDRESS = 'FORNO SCALDOTTO DI FEFFO FORNI 10 INT 8'
        BASE_EXPECTED_POST_CODE = '44123'
        BASE_EXPECTED_CITY = 'FERRARA'
        BASE_EXPECTED_PROVINCE = 'FE'
        variables['EXPECTED_POST_CODE'] = BASE_EXPECTED_POST_CODE
        variables['EXPECTED_PROVINCE'] = BASE_EXPECTED_PROVINCE
        variables['ADDRESS_STRING'] = (
            BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POST_CODE + ' '
            + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        # Prepend and append a fixed number of spaces.
        BASE_EXPECTED_ADDRESS_S10 = S10 + BASE_EXPECTED_ADDRESS + S10
        BASE_EXPECTED_POST_CODE_S10 = S10 + BASE_EXPECTED_POST_CODE + S10
        BASE_EXPECTED_CITY_S10 = S10 + BASE_EXPECTED_CITY + S10
        BASE_EXPECTED_PROVINCE_S10 = S10 + BASE_EXPECTED_PROVINCE + S10
        variables['ADDRESS_STRING_S10'] = (
            BASE_EXPECTED_ADDRESS_S10 + '\n' + ' ' +
            BASE_EXPECTED_POST_CODE_S10 + ' ' + BASE_EXPECTED_CITY_S10 + ' ' +
            BASE_EXPECTED_PROVINCE_S10 + '\n')

        # Remove the middle space from the string.
        variables['ADDRESS_STRING_NO_MIDDLE_SEPARATOR'] = (
            BASE_EXPECTED_ADDRESS + '\n' + BASE_EXPECTED_POST_CODE + ' ' +
            BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        variables['ADDRESS_STRING_MISSING_FIRST_DELIMITER'] = (
            BASE_EXPECTED_ADDRESS + ' ' + BASE_EXPECTED_POST_CODE + ' ' +
            BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        variables['ADDRESS_STRING_MISSING_LAST_DELIMITER'] = (
            BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POST_CODE + ' '
            + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE)

        variables['ADDRESS_STRING_MISSING_BOTH_DELIMITERS'] = (
            BASE_EXPECTED_ADDRESS + ' ' + BASE_EXPECTED_POST_CODE + ' ' +
            BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE)

        variables['ADDRESS_STRING_POST_CODE_NOT_CONFORMING'] = (
            BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POST_CODE[:-1] +
            ' ' + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        variables['ADDRESS_STRING_PROVINCE_NOT_CONFORMING'] = (
            BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POST_CODE + ' '
            + BASE_EXPECTED_CITY + ' ' + BASE_EXPECTED_PROVINCE[:-1] + '\n')

        variables['ADDRESS_STRING_POST_CODE_NOT_EXISTS'] = (
            BASE_EXPECTED_ADDRESS + '\n' + ' ' + ' ' + BASE_EXPECTED_CITY + ' '
            + BASE_EXPECTED_PROVINCE + '\n')

        variables['ADDRESS_STRING_CITY_NOT_EXISTS'] = (
            BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POST_CODE + ' '
            + ' ' + BASE_EXPECTED_PROVINCE + '\n')

        variables['ADDRESS_STRING_PROVINCE_NOT_EXISTS'] = (
            BASE_EXPECTED_ADDRESS + '\n' + ' ' + BASE_EXPECTED_POST_CODE + ' '
            + BASE_EXPECTED_CITY + ' ' + '\n')

        # A generic valid VAT record.
        expected_base = {
            'address': BASE_EXPECTED_ADDRESS,
            'post_code': BASE_EXPECTED_POST_CODE,
            'city': BASE_EXPECTED_CITY,
            'province': BASE_EXPECTED_PROVINCE
        }
        self._test_parse_address_string_IT_common(expected_base, variables)

        ###########################
        # City field with spaces. #
        ###########################

        variables = dict()

        COMPLEX_EXPECTED_ADDRESS = 'FORNO SCALDOTTO DI FEFFO FORNI 10 INT 8'
        COMPLEX_EXPECTED_POST_CODE = '44123'
        COMPLEX_EXPECTED_CITY = 'MALBORGETTO DI BOARA'
        COMPLEX_EXPECTED_PROVINCE = 'FE'
        variables['EXPECTED_POST_CODE'] = COMPLEX_EXPECTED_POST_CODE
        variables['EXPECTED_PROVINCE'] = COMPLEX_EXPECTED_PROVINCE
        variables['ADDRESS_STRING'] = (
            COMPLEX_EXPECTED_ADDRESS + '\n' + ' ' + COMPLEX_EXPECTED_POST_CODE
            + ' ' + COMPLEX_EXPECTED_CITY + ' ' + COMPLEX_EXPECTED_PROVINCE +
            '\n')

        # Prepend and append a fixed number of spaces.
        COMPLEX_EXPECTED_ADDRESS_S10 = S10 + COMPLEX_EXPECTED_ADDRESS + S10
        COMPLEX_EXPECTED_POST_CODE_S10 = S10 + COMPLEX_EXPECTED_POST_CODE + S10
        COMPLEX_EXPECTED_CITY_S10 = S10 + COMPLEX_EXPECTED_CITY + S10
        COMPLEX_EXPECTED_PROVINCE_S10 = S10 + COMPLEX_EXPECTED_PROVINCE + S10
        variables['ADDRESS_STRING_S10'] = (
            COMPLEX_EXPECTED_ADDRESS_S10 + '\n' + ' ' +
            COMPLEX_EXPECTED_POST_CODE_S10 + ' ' + COMPLEX_EXPECTED_CITY_S10 +
            ' ' + COMPLEX_EXPECTED_PROVINCE_S10 + '\n')

        # Remove the middle space from the string.
        variables['ADDRESS_STRING_NO_MIDDLE_SEPARATOR'] = (
            COMPLEX_EXPECTED_ADDRESS + '\n' + COMPLEX_EXPECTED_POST_CODE + ' '
            + COMPLEX_EXPECTED_CITY + ' ' + COMPLEX_EXPECTED_PROVINCE + '\n')

        variables['ADDRESS_STRING_MISSING_FIRST_DELIMITER'] = (
            COMPLEX_EXPECTED_ADDRESS + ' ' + COMPLEX_EXPECTED_POST_CODE + ' ' +
            COMPLEX_EXPECTED_CITY + ' ' + COMPLEX_EXPECTED_PROVINCE + '\n')

        variables['ADDRESS_STRING_MISSING_LAST_DELIMITER'] = (
            COMPLEX_EXPECTED_ADDRESS + '\n' + ' ' + COMPLEX_EXPECTED_POST_CODE
            + ' ' + COMPLEX_EXPECTED_CITY + ' ' + COMPLEX_EXPECTED_PROVINCE)

        variables['ADDRESS_STRING_MISSING_BOTH_DELIMITERS'] = (
            COMPLEX_EXPECTED_ADDRESS + ' ' + COMPLEX_EXPECTED_POST_CODE + ' ' +
            COMPLEX_EXPECTED_CITY + ' ' + COMPLEX_EXPECTED_PROVINCE)

        variables['ADDRESS_STRING_POST_CODE_NOT_CONFORMING'] = (
            COMPLEX_EXPECTED_ADDRESS + '\n' + ' ' +
            COMPLEX_EXPECTED_POST_CODE[:-1] + ' ' + COMPLEX_EXPECTED_CITY + ' '
            + COMPLEX_EXPECTED_PROVINCE + '\n')

        variables['ADDRESS_STRING_PROVINCE_NOT_CONFORMING'] = (
            COMPLEX_EXPECTED_ADDRESS + '\n' + ' ' + COMPLEX_EXPECTED_POST_CODE
            + ' ' + COMPLEX_EXPECTED_CITY + ' ' +
            COMPLEX_EXPECTED_PROVINCE[:-1] + '\n')

        variables['ADDRESS_STRING_POST_CODE_NOT_EXISTS'] = (
            COMPLEX_EXPECTED_ADDRESS + '\n' + ' ' + ' ' + COMPLEX_EXPECTED_CITY
            + ' ' + COMPLEX_EXPECTED_PROVINCE + '\n')

        variables['ADDRESS_STRING_CITY_NOT_EXISTS'] = (
            COMPLEX_EXPECTED_ADDRESS + '\n' + ' ' + COMPLEX_EXPECTED_POST_CODE
            + ' ' + ' ' + COMPLEX_EXPECTED_PROVINCE + '\n')

        variables['ADDRESS_STRING_PROVINCE_NOT_EXISTS'] = (
            COMPLEX_EXPECTED_ADDRESS + '\n' + ' ' + COMPLEX_EXPECTED_POST_CODE
            + ' ' + COMPLEX_EXPECTED_CITY + ' ' + '\n')

        # A generic valid VAT record.
        expected_complex = {
            'address': COMPLEX_EXPECTED_ADDRESS,
            'post_code': COMPLEX_EXPECTED_POST_CODE,
            'city': COMPLEX_EXPECTED_CITY,
            'province': COMPLEX_EXPECTED_PROVINCE
        }
        self._test_parse_address_string_IT_common(expected_complex, variables)

    def test_parse_response_IT(self):
        """Test."""
        ADDRESS = 'FORNO SCALDOTTO DI FEFFO FORNI 10 INT 8\n 44100 FERRARA FE\n'
        REQUEST_DATE = 'some date'
        VAT_NUMBER = '12345678901'
        COUNTRY_CODE = 'IT'
        FAKE_COUNTRY_CODE = 'ZZ'
        TRADER_NAME = 'LOL'
        response = {
            'countryCode': COUNTRY_CODE,
            'vatNumber': VAT_NUMBER,
            'requestDate': REQUEST_DATE,
            'valid': True,
            'traderStreet': None,
            'traderCity': None,
            'traderAddress': ADDRESS,
            'traderName': TRADER_NAME,
            'traderCompanyType': None,
            'traderStreet': None,
            'traderPostcode': None,
            'traderNameMatch': None,
            'traderCompanyTypeMatch': None,
            'traderStreetMatch': None,
            'traderPostcodeMatch': None,
            'traderCityMatch': None,
            'requestIdentifier': None
        }

        # Assert not raises.
        api.parse_response(response, VAT_NUMBER, COUNTRY_CODE)

        response['countryCode'] = FAKE_COUNTRY_CODE
        with self.assertRaises(exceptions.ResponseIOError):
            api.parse_response(response, VAT_NUMBER, COUNTRY_CODE)

        response['countryCode'] = COUNTRY_CODE
        response['vatNumber'] = VAT_NUMBER[:-1]
        with self.assertRaises(exceptions.ResponseVatNumberNotConforming):
            api.parse_response(response, VAT_NUMBER[:-1], COUNTRY_CODE)

        response['vatNumber'] = VAT_NUMBER
        response['traderName'] = None
        with self.assertRaises(exceptions.CannotGetTraderName):
            api.parse_response(response, VAT_NUMBER, COUNTRY_CODE)

        response['traderName'] = TRADER_NAME
        response['traderAddress'] = None
        with self.assertRaises(exceptions.CannotGetTraderAddress):
            api.parse_response(response, VAT_NUMBER, COUNTRY_CODE)

        response['traderAddress'] = ADDRESS
        response['valid'] = False
        with self.assertRaises(exceptions.VatNotValid):
            api.parse_response(response, VAT_NUMBER, COUNTRY_CODE)

        response['valid'] = True
        COUNTRY_CODE_FAKE = 'ZZ'
        response['countryCode'] = COUNTRY_CODE_FAKE
        with self.assertRaises(exceptions.CountryCodeNotImplemented):
            api.parse_response(response, VAT_NUMBER, COUNTRY_CODE_FAKE)
