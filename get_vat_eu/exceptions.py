#
# exceptions.py
#

"""Exceptions file."""

class CannotGetAnyRelevantInformation(Exception):
    """The API does not know what to return."""

class VatNotValid(Exception):
    """The input VAT is not valid."""

class AddressStringNotCorrespondingToExpectedFormat(Exception):
    """The address string does not correspond to the expected format."""
