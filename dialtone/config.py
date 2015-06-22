import os

from dialtone.utils import phone

#
# Flask configuration
#

DEBUG = True
SECRET_KEY = os.environ.get('SECREt_KEY', 'shhhh')

#
# Dialtone configuration
#

# Number of seconds to wait for phone to be answered
DIAL_TIMEOUT = int(os.environ.get('CALL_TIMEOUT', 60))

# Text-to-speech language to use
# see: https://www.twilio.com/docs/api/twiml/say#attributes-alice
LANGUAGE = os.environ.get('LANGUAGE', 'en-US')

# Number to use for outgoing phone calls
OUTGOING_NUMBER = os.environ.get('OUTGOING_NUMBER')

# List of phone numbers
PHONES = map(phone.normalize, os.environ.get('PHONES', '').split(','))

# Twilio account sid
TWILIO_SID = os.environ.get('TWILIO_SID')

# Twilio auth token
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')

# Text-to-speech voice to use, default is recommended
VOICE = os.environ.get('VOICE', 'alice')
