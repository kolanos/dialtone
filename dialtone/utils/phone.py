import phonenumbers


def format(number):
    """Formats a phone number into E164."""
    return str(phonenumbers.format_number(
        number, phonenumbers.PhoneNumberFormat.E164))


def normalize(number, country_code=None):
    """Attempt to normalize a phone number by parsing and formatting it."""
    try:
        parsed_number = phonenumbers.parse(number, country_code)
        return format(parsed_number)
    except Exception:
        return number


def valid(number, country_code=None):
    """Determine whether or not a phone number is valid."""
    try:
        phonenumbers.parse(number, country_code)
        return True
    except Exception:
        return False


def equals(number1, number2, country_code=None):
    """Determine whether or not two numbers are equal."""
    return normalize(number1, country_code) == normalize(number2, country_code)


def extract(message, country_code=None):
    """Extract a phone number from a text message."""
    for match in phonenumbers.PhoneNumberMatcher(message, country_code):
        return format(match.number)
