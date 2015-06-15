from nltk.tokenize import wordpunct_tokenize

from dialtone.utils import phone

ACTIONS = {
    # Start a call with a specific number
    'call': {
        'keywords': ['call'],
        'attributes': {
            'phone': phone.extract
        }
    },

    # Start a text message with a specific number
    'text': {
        'keywords': ['text', 'sms'],
        'attributes': {
            'phone': phone.extract
        }
    },

    # Stop current sms conversation
    'stop': {
        'keywords': ['stop']
    }
}


def parse(msg, **opts):
    opts.setdefault('receptionist', 'alice')
    tokens = map(str.lower, wordpunct_tokenize(msg))
    if tokens[0] != opts['receptionist'].lower():
        return None
    for action, criteria in ACTIONS.items():
        matching_keywords = set(criteria['keywords']) & set(tokens)
        if not matching_keywords or len(matching_keywords) == len(tokens):
            continue
        result = {'type': action}
        if 'attributes' in criteria:
            for field, matcher in criteria['attributes'].items():
                matching_attribute = matcher(msg)
                if matching_attribute:
                    result[field] = matching_attribute
            if len(result) != len(criteria['attributes']) + 1:
                continue
        return result
    return None
