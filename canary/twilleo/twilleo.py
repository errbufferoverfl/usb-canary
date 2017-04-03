from __future__ import absolute_import, division, print_function
import sys
import canary.settings


def load_twilio_settings():
    """
    Opens settings.json and checks all values have been set, if they have, creates a list containing these details.

    If not exits and notifies user of misconfiguration

    :return: list containing options to use Twilio API
    """
    twilio_settings = canary.settings.open_settings()

    twilio = twilio_settings['settings']['twilio']

    try:
        # sanity check that the user has actually supplied data
        if not twilio['account_sid']:
            print('Error 40: Twilio Account SID has been left blank')
            sys.exit(40)
        elif not twilio['auth_token']:
            print('Error 41: Twilio API token has been left blank')
            sys.exit(41)
        elif not twilio['mobile_number']:
            print('Error 42: Receiving mobile number has been left blank')
            sys.exit(42)
        elif not twilio['twilio_number']:
            print('Error 43: Twilio mobile number has been left blank')
            sys.exit(43)
        else:
            return twilio
    except KeyError:
        print('Error 50: Twilio key missing in the settings file')
        sys.exit(50)
