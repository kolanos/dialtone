import os

from dialtone.utils import phone

#
# Flask configuration
#

SECRET_KEY = os.environ.get('SECREt_KEY', 'shhhh')

#
# Dialtone configuration
#

# Number to use for outgoing phone calls
OUTGOING_NUMBER = os.environ.get('OUTGOING_NUMBER')

# List of phone numbers
PHONES = map(phone.normalize, os.environ.get('PHONES', '').split(','))

# Voice profile to use
PROFILE = os.environ.get('PROFILE', 'alice')

# Twilio account sid
TWILIO_SID = os.environ.get('TWILIO_SID')

# Twilio auth token
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')

# Number of seconds to wait for phone to be answered
TWILIO_TIMEOUT = int(os.environ.get('TWILIO_TIMEOUT', 180))
