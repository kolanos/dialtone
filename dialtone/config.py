from collections import OrderedDict
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

# List of team members
TEAM = os.environ.get('TEAM', '').split(',')
TEAM = map(lambda s: tuple(s.split(':')), TEAM)
TEAM = map(lambda t: phone.normalize(t[1]), TEAM)
TEAM = OrderedDict(TEAM)

# Organization info
ORG_NAME = os.environ.get('ORG_NAME')

# Twilio account sid
TWILIO_SID = os.environ.get('TWILIO_SID')

# Twilio auth token
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')

# Number of seconds to wait for phone to be answered
TWILIO_TIMEOUT = int(os.environ.get('TWILIO_TIMEOUT', 180))
