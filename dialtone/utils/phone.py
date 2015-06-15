import phonenumbers


def format(num):
    return str(phonenumbers.format_number(
        num, phonenumbers.PhoneNumberFormat.INTERNATIONAL))


def normalize(num, country_code=None):
    try:
        number = phonenumbers.parse(num, country_code)
        return format(number)
    except Exception:
        return num


def valid(num, country_code=None):
    try:
        phonenumbers.parse(num, country_code)
        return True
    except Exception:
        return False


def equals(num1, num2, country_code=None):
    return normalize(num1, country_code) == normalize(num2, country_code)


def extract(msg, country_code=None):
    for match in phonenumbers.PhoneNumberMatcher(msg, country_code):
        return format(match.number)
