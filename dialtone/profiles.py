class Profile(object):
    @property
    def messages(self):
        return {
            # Visitor
            'call_error': (
                'Your call could not be processed at the moment. '
                'Sorry for the inconvenience'),
            'call_welcome': (
                'Thanks for calling {name}, your call will be transfered to '
                'one of our team members'),
            'call_unavailable': (
                'All of our team members are currently busy, please record'
                'your message after the signal, then press #'),
            'call_confirm': (
                'Hi {name}, we have an incoming call from {from}, press # to '
                'accept the call'),
            'call_record': (
                'Thank you, your message has been recorded, our team will '
                'get in touch with you soon'),

            # Team
            'team_promp_number': (
                'Hello {name}, Enter the number to call, then press #'),
            'team_failed': (
                'Sorry, the call has failed, please try again later'),

            # SMS
            'sms_error': (
                'Your sms could not be processed at the moment. Sorry for '
                'the inconvenience'),
            'sms_received': (
                'Your message has been forwarded to one of our team members'),
            'sms_already_handled': (
                'This conversation is already being taken care of by '
                '{name}'),
            'sms_forward': (
                "Hi {name}, we've received a text message from {from}, "
                "just reply to this message to start the "
                "conversation:\n\n{body}"),

            # SMS Actions
            'sms_action_stop': (
                'Ok {name}, I stopped your sms conversation '
                'with {to}'),
            'sms_action_unknown': "Sorry, I didn't understand your message",
            'sms_action_text': (
                "Ok, you're now in conversation with {to}, all your messages "
                "will be forward to them"),
            'sms_action_call': (
                "Ok, you'll soon receive a call to connect you to {to}")
        }


class Alice(Profile):
    name = 'Alice'
    voice = 'woman'
    language = 'en-us'


class Ben(Profile):
    name = 'Ben'
    voice = 'man'
    language = 'en-us'


class Catherine(Profile):
    name = 'Catherine'
    voice = 'alice'
    language = 'fr-fr'
