#
# api.py
#
"""The main file."""

import re
import zeep
import json
import string
from .constants import (common_defaults, urls, vat, countries)
from .exceptions import (
        ResponseIOError,
        ResponseVatNumberNotConforming,
        CannotGetTraderName,
        CannotGetTraderAddress,
        VatNotValid,
        AddressStringNotCorrespondingToExpectedFormat,
        CountryCodeNotImplemented)


def request_vat_information(vat_number: str, country_code: str = countries['code']['default']) -> dict:
    r"""Make a SOAP request and expect a response.


    .. raises: zeep.exceptions.Fault or a built-in exception.
    """

    client = zeep.Client(urls['ec_check_vat_api'])
    response = client.service.checkVatApprox(country_code, vat_number)

    return response


def parse_address_string(address_string: str, country_code: str) -> dict:
    r"""Get relevant information from the address string.

    :param address_string: a string containing all the address information.
    :param country_code: a two letter uppercase country identifier.
    :type address_string: str
    :type country_code: str
    :returns: a data structure with keys differing from country code to country code.
    :rtype: dict
    :raises: AddressStringNotCorrespondingToExpectedFormat or a built-in exception.
    """
    assert len(country_code) == 2

    trader_information = dict()

    if country_code == 'IT':
        if (address_string.endswith(countries['IT']['address_string']['separator'])
            and countries['IT']['address_string']['separator'] in address_string[0:-1]):

            # Divide the original string in two parts. Ignore the final empty string.
            buf = address_string.split(countries['IT']['address_string']['separator'])[:-1]

            # The address part is the first substring. Remove spaces around the string borders.
            address_substring = buf[0].strip(countries['IT']['address_string']['delimiter'])

            # Postal code, city, province.
            pc_cty_prv_substring = buf[1]

            # Get the other substring into its various components.
            # Always be tolerant with the delimiters on the borders.
            # Remove empty substrings in case of unexpected address string formats.
            buf = list(filter(None,
                pc_cty_prv_substring.strip(
                    countries['IT']['address_string']['delimiter']).split(countries['IT']['address_string']['delimiter'])))

            # We expect at least 3 elements: postal code, province and city.
            if len(buf) < 3:
                raise AddressStringNotCorrespondingToExpectedFormat

            # We know that province and postal code are not composed by delimiters.
            postal_code = buf[0]
            province = buf[-1]
            # A city might contain spaces (delimiters).
            # Always be tolerant with the delimiters on the borders.
            city = countries['IT']['address_string']['delimiter'].join(buf[1:-1]).strip(countries['IT']['address_string']['delimiter'])

            # Check that the province is composed of 2 uppercase letter characters.
            # Check that the postal code correponds to the standard.
            if (not re.match(countries['IT']['post_code']['regex'], postal_code)
                or not re.match(countries['IT']['province']['regex'], province)):
                raise AddressStringNotCorrespondingToExpectedFormat

            trader_information['address'] = address_substring
            trader_information['post_code'] = postal_code
            trader_information['province'] = province
            trader_information['city'] = city
        else:
            raise AddressStringNotCorrespondingToExpectedFormat

    return trader_information

def vat_adheres_to_specifications(vat_number: str, country_code: str = countries['code']['default']) -> bool:
    """Chceck that the VAT number corresponds to the specifications."""
    assert len(country_code) == 2

    vat_conforming = True
    if not re.match(vat['regex'], country_code + vat_number):
        vat_conforming = False

    return vat_conforming

def parse_response(response: dict, vat_number: str, country_code: str = countries['code']['default']) -> dict:
    r"""Parses the response and get the relevant fields.

    :param response: a data structure containing the SOAP response.
    :param country_code: a two letter uppercase country identifier.
    :type response: dict
    :type country_code: str
    :returns: a data structure with keys differing from country code to country code.
    :rtype: dict
    :raises: ResponseIOError, ResponseVatNumberNotConforming or a built-in exception.
    """
    assert 'countryCode' in response
    assert 'vatNumber' in response
    assert 'requestDate' in response
    assert 'valid' in response
    assert 'traderName' in response
    assert 'traderCompanyType' in response
    assert 'traderAddress' in response
    assert 'traderStreet' in response
    assert 'traderPostcode' in response
    assert 'traderCity' in response
    assert 'traderNameMatch' in response
    assert 'traderCompanyTypeMatch' in response
    assert 'traderStreetMatch' in response
    assert 'traderPostcodeMatch' in response
    assert 'traderCityMatch' in response
    assert 'requestIdentifier' in response
    # The following variables must be defined.
    assert response['countryCode'] is not None
    assert response['vatNumber'] is not None
    assert response['requestDate'] is not None
    assert response['valid'] is not None
    assert isinstance(response['valid'], bool)
    assert isinstance(response['vatNumber'], str)

    if response['countryCode'] != country_code:
        raise ResponseIOError
    if response['vatNumber'] != vat_number:
        raise ResponseIOError

    trader_information = dict()

    # 'valid' is compulsory.
    if response['valid']:
        if not vat_adheres_to_specifications(response['vatNumber']):
            raise ResponseVatNumberNotConforming

        # 'contryCode' is compulsory.
        if response['countryCode'] == 'IT':

            if response['traderName'] is None:
                raise CannotGetTraderName
            else:
                trader_information['name'] = response['traderName']

            if (response['traderStreet'] is None or response['traderCity'] is None
                    or response['traderPostcode'] is None):
                if response['traderAddress'] is None:
                    raise CannotGetTraderAddress
                else:
                    trader = parse_address_string(response['traderAddress'], response['countryCode'])
                    trader_information['address'] = trader['address']
                    trader_information['city'] = trader['city']
                    trader_information['province'] = trader['province']
                    trader_information['post_code'] = trader['post_code']
            else:
                trader_information['address'] = trader['address']
                trader_information['city'] = response['traderCity']
                trader_information['province'] = response['traderCity']
                trader_information['post_code'] = response['traderPostCode']
        else:
            # A generic country.
            raise CountryCodeNotImplemented
    else:
        raise VatNotValid

    return trader_information

def prettify_trader_information(information: dict, country_code: str = countries['code']['default']):
    """Capitalize the first letter of each word in the fields.

    :param information: a data structure containing the trader information.
    :param country_code: a two letter uppercase country identifier.
    :type information: dict
    :type country_code: str
    :returns: None
    :rtype: None
    :raises: a built-in exception.
    """
    assert len(country_code) == 2

    if country_code == 'IT':
        # TODO: Assertions

        information['address'] = string.capwords(information['address'])
        information['city'] = string.capwords(information['city'])

def pipeline(vat_number: str, country_code: str = countries['code']['default'], trader_information_pretty=True, show_input=True) -> str:
    """Execute the pipeline.

    :returns: a string formatted according to JSON specifications.
    :rtype: str
    """
    response = request_vat_information(vat_number, country_code)
    trader_information = parse_response(response, vat_number, country_code)
    if trader_information_pretty:
        prettify_trader_information(trader_information, country_code)
    if show_input:
        trader_information['country_code'] = country_code
        trader_information['vat_number'] = vat_number
    return json.dumps(trader_information)
