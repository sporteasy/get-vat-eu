#
# exceptions.py
#

"""Exceptions file."""

class ResponseIOError(Exception):
    """Input and expected output differ."""

class CannotGetTraderVatNumber(Exception):
    """The API does not know what the address."""

class ResponseVatAddressNotConforming(Exception):
    """The API does not know what the address."""

class CannotGetTraderName(Exception):
    """The API does not know what the address."""

class CannotGetTraderAddress(Exception):
    """The API does not know what the address is."""

class VatNotValid(Exception):
    """The input VAT is not valid."""

class AddressStringNotCorrespondingToExpectedFormat(Exception):
    """The address string does not correspond to the expected format."""

class CountryCodeNotImplemented(Exception):
    """The specified country has no implementation yet."""
