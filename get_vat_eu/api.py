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
        CannotGetTraderAddress,
        CannotGetTraderName,
        VatNotValid,
        AddressStringNotCorrespondingToExpectedFormat,
        CountryCodeNotImplemented)


# TODO handle exceptions:
# TODO they get raised like this: zeep.exceptions.Fault: SERVICE_UNAVAILABLE
"""
    - INVALID_INPUT: The provided CountryCode is invalid or the VAT number is empty; 
    - GLOBAL_MAX_CONCURRENT_REQ: Your Request for VAT validation has not been processed; the maximum number of concurrent requests has been reached. Please re-submit your request later or contact TAXUD-VIESWEB@ec.europa.eu for further information": Your request cannot be processed due to high traffic on the web application. Please try again later; 
    - MS_MAX_CONCURRENT_REQ: Your Request for VAT validation has not been processed; the maximum number of concurrent requests for this Member State has been reached. Please re-submit your request later or contact TAXUD-VIESWEB@ec.europa.eu for further information": Your request cannot be processed due to high traffic towards the Member State you are trying to reach. Please try again later. 
    - SERVICE_UNAVAILABLE: an error was encountered either at the network level or the Web application level, try again later; 
    - MS_UNAVAILABLE: The application at the Member State is not replying or not available. Please refer to the Technical Information page to check the status of the requested Member State, try again later; 
    - TIMEOUT: The application did not receive a reply within the allocated time period, try again later. 
"""

def request_vat_information(vat_number: str, country_code: str = countries['code']['default']):
    r"""Make a SOAP request and expect a response."""

    client = zeep.Client(urls['ec check vat api'])
    response = client.service.checkVatApprox(country_code, vat_number)

    return response


def parse_address_string(address_string: str, country_code: str):
    r"""Get relevant information from the address string.
    :param strict: check that every aspect of the address string
        corresponds to the expected input.


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
            trader_information['post code'] = postal_code
            trader_information['province'] = province
            trader_information['city'] = city
        else:
            raise AddressStringNotCorrespondingToExpectedFormat

    return trader_information


def parse_response(response: dict):
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
    # These variables must be defined.
    assert response['countryCode'] is not None
    assert response['vatNumber'] is not None
    assert response['requestDate'] is not None
    assert response['valid'] is not None
    assert isinstance(response['valid'], bool)

    # Return trader name as well

    trader_information = dict()

    # 'valid' is compulsory.
    if response['valid']:
        # 'contryCode' is compulsory.
        if response['countryCode'] == 'IT':

            # FIXME.
            trader_information['name'] = response['traderName']

            # TODO: check that the VAT number adheres to the
            # TODO: specifications: https://it.wikipedia.org/wiki/Partita_IVA
            # if response['vatNumber']
            if (response['traderStreet'] is None or response['traderCity'] is None
                    or response['traderPostcode'] is None):
                if response['traderAddress'] is None:
                    raise CannotGetTraderAddress
                else:
                    trader = parse_address_string(response['traderAddress'], response['countryCode'])
                    trader_information['address'] = trader['address']
                    trader_information['city'] = trader['city']
                    trader_information['province'] = trader['province']
                    trader_information['post code'] = trader['post code']
            else:
                trader_information['address'] = trader['address']
                trader_information['city'] = response['traderCity']
                trader_information['province'] = response['traderCity']
                trader_information['post code'] = response['traderPostCode']
        # A generic country.
        else:
            raise CountryCodeNotImplemented
    else:
        raise VatNotValid

    return trader_information

def prettify_trader_information(information: dict, country_code: str = countries['code']['default']):
    # TODO: Assertions
    if country_code == 'IT':
        information['name'] = string.capwords(information['name'])
        information['address'] = string.capwords(information['address'])
        information['city'] = string.capwords(information['city'])

def dict_to_json(information: dict):
    return json.dumps(information)

def pipeline(vat_number: str, country_code: str = countries['code']['default'], trader_information_pretty=False):
    response = request_vat_information(vat_number, country_code)
    trader_information = parse_response(response)
    if trader_information_pretty:
        prettify_trader_information(trader_information, country_code)
    return dict_to_json(trader_information)
