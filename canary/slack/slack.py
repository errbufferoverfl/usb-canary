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

import canary.settings
import canary.slack.slack_bot


def load_slack_settings():
    """
    Opens settings.json and checks all values have been set, if they have,
    creates a list containing these details and sets up Slack bot.

    If not exits and notifies user of misconfiguration

    :return: list containing options to use Slack API
    """
    logging.debug('Opening settings.json.')
    slack_settings = canary.settings.open_settings()

    logging.debug('Getting Slack settings.')
    slack = slack_settings['settings']['slack']
    # sanity check that the user has actually supplied data
    api_key = not slack["api_key"]
    botname = not slack["botname"]
    channel_name = not slack["channel_name"]

    logging.debug('Checking Slack Botname has been supplied.')
    logging.debug('Checking Slack API key has been supplied.')
    logging.debug('Checking Slack Channel Name has been supplied.')
    if botname and api_key and channel_name:
        print('Unable to run application, Slack credentials provided?')
        logging.critical('Aborting... Unable to run application, Slack credentials not supplied.')
        sys.exit(404)

    logging.debug('Slack credentials supplied. Starting Slack bot.')
    canary.slack.slack_bot.setup(slack, channel_name)

    return slack
