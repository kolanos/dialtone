import os

from dialtone.utils import phone

#
# Flask configuration
#

DEBUG = True if os.getenv('DEBUG') else False

SECRET_KEY = os.getenv('SECRET_KEY')
assert SECRET_KEY, 'A SECRET_KEY environment variable is required.'

#
# Dialtone configuration
#

# Number of seconds to wait for phone to be answered
DIAL_TIMEOUT = int(os.getenv('CALL_TIMEOUT', 60))

# Text-to-speech language to use
# see: https://www.twilio.com/docs/api/twiml/say#attributes-alice
LANGUAGE = os.getenv('LANGUAGE', 'en-US')

# Number to use for outgoing phone calls
OUTGOING_NUMBER = os.getenv('OUTGOING_NUMBER')
assert OUTGOING_NUMBER, 'An OUTGOING_NUMBER environment variable is required.'

# List of phone numbers
PHONES = map(phone.normalize, os.getenv('PHONES', '').split(','))
assert PHONES, 'A PHONES environment variable is required.'

# Text-to-speech voice to use, default is recommended
VOICE = os.getenv('VOICE', 'alice')

#
# Twilio Configuration
#

# Twilio account sid
TWILIO_SID = os.getenv('TWILIO_SID')
assert TWILIO_SID, 'A TWILIO_SID environment variable is rquired.'

# Twilio auth token
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
assert TWILIO_TOKEN, 'A TWILIO_TOKEN environment variable is required.'
