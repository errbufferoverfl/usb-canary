from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

from canary.slack import slack_bot
from canary import settings


def send_message(alert):
    settings_file = settings.open_settings()

    twilio_enabled = settings_file['settings']['general']['twilio']
    slack_enabled = settings_file['settings']['general']['slack']

    if twilio_enabled:
        twilio_settings = settings_file['settings']['twilio']

        client = TwilioRestClient(twilio_settings["account_sid"], twilio_settings["auth_token"])
        try:
            client.messages.create(body=alert,
                                   to=twilio_settings['mobile_number'],
                                   from_=twilio_settings["twilio_number"])
        except TwilioRestException as e:
            print(e)

    if slack_enabled:
        slack_settings = settings_file['settings']['slack']
        slack_bot.run_bot(alert, slack_settings['channel_name'])
