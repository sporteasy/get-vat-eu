#
# api.py
#
"""The main file."""

import re
import zeep
import json
import string
from .constants import (common_defaults, urls, countries)
from .exceptions import (
        ResponseIOError,
        CannotGetTraderVatNumber,
        ResponseVatAddressNotConforming,
        CannotGetTraderName,
        CannotGetTraderAddress,
        VatNotValid,
        AddressStringNotCorrespondingToExpectedFormat,
        CountryCodeNotImplemented)


def request_vat_information(vat_number: str, country_code: str = countries['code']['default']):
    r"""Make a SOAP request and expect a response.


    .. raises: zeep.exceptions.Fault or a built-in exception.
    """

    client = zeep.Client(urls['ec check vat api'])
    response = client.service.checkVatApprox(country_code, vat_number)

    return response


def parse_address_string(address_string: str, country_code: str):
    r"""Get relevant information from the address string.

    .. note:: From empirical evidence, an address string is structured like this:
        IT: '${address} ${house_number} \n${postal_code} ${city} ${PROVINCE}\n'
    """

    trader_information = dict()

    if country_code == 'IT':
        if (address_string.endswith(countries['IT']['address string']['separator'])
            and countries['IT']['address string']['separator'] in address_string[0:-1]):

            # Divide the original string in two parts. Ignore the final empty string.
            buf = address_string.split(countries['IT']['address string']['separator'])[:-1]

            # The address part is the first substring. Remove spaces around the string borders.
            address_substring = buf[0].strip(countries['IT']['address string']['delimiter'])

            # Postal code, city, province.
            pc_cty_prv_substring = buf[1]

            # Get the other substring into its various components.
            # Always be tolerant with the delimiters on the borders.
            # Remove empty substrings in case of unexpected address string formats.
            buf = list(filter(None,
                pc_cty_prv_substring.strip(
                    countries['IT']['address string']['delimiter']).split(countries['IT']['address string']['delimiter'])))

            # We expect at least 3 elements: postal code, province and city.
            if len(buf) < 3:
                raise AddressStringNotCorrespondingToExpectedFormat

            # We know that province and postal code are not composed by delimiters.
            postal_code = buf[0]
            province = buf[-1]
            # A city might contain spaces (delimiters).
            # Always be tolerant with the delimiters on the borders.
            city = countries['IT']['address string']['delimiter'].join(buf[1:-1]).strip(countries['IT']['address string']['delimiter'])

            # Check that the province is composed of 2 uppercase letter characters.
            # Check that the postal code correponds to the standard.
            if (not re.match("^\d{5}", postal_code)
                or not re.match("^[A-Z]{2}$", province)):
                raise AddressStringNotCorrespondingToExpectedFormat

            trader_information['address'] = address_substring
            trader_information['post_code'] = postal_code
            trader_information['province'] = province
            trader_information['city'] = city
        else:
            raise AddressStringNotCorrespondingToExpectedFormat

    return trader_information

def vat_adheres_to_specifications(vat_number: str, country_code: str = countries['code']['default']):
    """Chceck that the VAT number corresponds to the specifications."""
    # TODO assertions
    vat_conforming = True

    # https://it.wikipedia.org/wiki/Partita_IVA#Numeri_IVA_nell'Unione_europea
    wikipedia_vat_regex = "((ATU|DK|FI|HU|LU|MT|SI)[0-9]{8}|(BE|BG)[0-9]{9,10}|(ES([0-9]|[A-Z])[0-9]{7}([A-Z]|[0-9]))|(HR|IT|LV)[0-9]{11}|CY[0-9]{8}[A-Z]|CZ[0-9]{8,10}|(DE|EE|EL|GB|PT)[0-9]{9}|FR[A-Z0-9]{2}[0-9]{8}[A-Z0-9]|IE[0-9]{7}[A-Z0-9]{2}|LT[0-9]{9}([0-9]{3})?|NL[0-9]{9}B([0-9]{2})|PL[0-9]{10}|RO[0-9]{2,10}|SK[0-9]{10}|SE[0-9]{12})"
    if not re.match(wikipedia_vat_regex, country_code + vat_number):
        vat_conforming = False

    return vat_conforming

def parse_response(response: dict, vat_number: str, country_code: str = countries['code']['default']):
    r"""Parses the response and get the relevant fields."""
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

    if response['countryCode'] != country_code:
        raise ResponseIOError
    if response['vatNumber'] != vat_number:
        raise ResponseIOError

    trader_information = dict()

    # 'valid' is compulsory.
    if response['valid']:
        if response['vatNumber'] is None:
            raise CannotGetTraderVatNumber
        elif not vat_adheres_to_specifications(response['vatNumber']):
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
        # A generic country.
        else:
            raise CountryCodeNotImplemented
    else:
        raise VatNotValid

    return trader_information

def prettify_trader_information(information: dict, country_code: str = countries['code']['default']):
    # TODO: Assertions
    if country_code == 'IT':
        information['address'] = string.capwords(information['address'])
        information['city'] = string.capwords(information['city'])

def dict_to_json(information: dict):
    return json.dumps(information)

def pipeline(vat_number: str, country_code: str = countries['code']['default'], trader_information_pretty=True, show_input=True):
    response = request_vat_information(vat_number, country_code)
    trader_information = parse_response(response, vat_number, country_code)
    if trader_information_pretty:
        prettify_trader_information(trader_information, country_code)
    if show_input:
        trader_information['country_code'] = country_code
        trader_information['vat_number'] = vat_number
    return dict_to_json(trader_information)
