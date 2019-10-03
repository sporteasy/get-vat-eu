#
# exceptions.py
#

"""Exceptions file."""

class CannotGetTraderAddress(Exception):
    """The API does not know what the address is."""

class CannotGetTraderName(Exception):
    """The API does not know what the address."""

class VatNotValid(Exception):
    """The input VAT is not valid."""

class AddressStringNotCorrespondingToExpectedFormat(Exception):
    """The address string does not correspond to the expected format."""

class CountryCodeNotImplemented(Exception):
    """The specified country has no implementation yet."""
