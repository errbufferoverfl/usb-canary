# usb_canary - a Linux tool that uses pyudev to monitor devices while
# your computer is locked. In the case it detects someone plugging in
# or unplugging devices it can be configured to make a noise or send
# you an SMS alerting to you of the potential security breach.

# Copyright (C) 2017 errbufferoverfl
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import logging
import sys

from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

from canary import settings
from canary.slack import slack_bot
from canary.slack.slack import load_slack_settings
from canary.twilleo.twilleo import load_twilio_settings

from canary.pushovr.pushover import load_pushover_settings
from pushover import Client


def send_message(alert):
    logging.debug('Opening settings.json.')
    settings_file = settings.open_settings()
    logging.debug('Getting Twilio settings.')
    twilio_enabled = settings_file['settings']['general']['twilio']
    logging.debug('Getting Slack settings.')
    slack_enabled = settings_file['settings']['general']['slack']
    logging.debug('Getting Pushover settings.')
    pushover_enabled = settings_file['settings']['general']['pushover']

    logging.debug('Checking if Twilio is enabled.')
    if twilio_enabled:
        logging.debug('Twilio enabled.')
        logging.debug('Loading Twilio settings.')
        twilio_settings = load_twilio_settings()
        logging.debug('Configuring Twilio client.')
        client = TwilioRestClient(twilio_settings["account_sid"], twilio_settings["auth_token"])
        try:
            logging.debug('Trying to send Twilio message.')
            client.messages.create(body=alert,
                                   to=twilio_settings['mobile_number'],
                                   from_=twilio_settings["twilio_number"])
        except TwilioRestException:
            print('Unable to run application, correct Twilio credentials provided?')
            logging.critical('Aborting... Unable to run application, Twilio credentials incorrect.')
            sys.exit(406)
    logging.debug('Checking if Slack is enabled.')
    if slack_enabled:
        logging.debug('Opening settings.json.')
        slack_settings = load_slack_settings()
        logging.debug('Staring up Slack Bot.')
        slack_bot.run_bot(alert, slack_settings['channel_name'])
    logging.debug('Checking if Pushover is enabled.')
    if pushover_enabled:
        logging.debug('Opening settings.json.')
        pushover_settings = load_pushover_settings()
        client = Client(pushover_settings['user_key'], api_token=pushover_settings['api_token'])
        client.send_message(alert, priority=pushover_settings['priority'])
