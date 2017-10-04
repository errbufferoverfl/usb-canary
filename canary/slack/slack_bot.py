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

import slackclient

slack_client = ''
channel_name = ''


def setup(slack, channel):
    logging.debug('Setting up Slack Bot.')
    global slack_client
    slack_client = slackclient.SlackClient(slack['api_key'])
    logging.debug('\tSetting Slack API key.')
    logging.debug('\tSetting Slack channel name.')
    global channel_name
    channel_name = channel


def run_bot(message, channel):
    if slack_client.rtm_connect():
        logging.debug('Getting list of channels.')
        channel_list = slack_client.api_call('channels.list')['channels']
        channel_exists = False

        logging.debug('Checking existence of {} channel.'.format(channel_name))
        for dic in channel_list:
            if dic.get('name') == channel:
                logging.debug('\tSlack channel exists.')
                channel_exists = True
                break

        if channel_exists:
            logging.debug('\tPosting message to Slack.')
            slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=True)
        else:
            logging.info('\tChannel not found in Slack directory - posting to #general instead.')
            message = "Hi! :wave: It looks like some of my settings might be a little frazzled, and I can't post " \
                      "messages like normal."
            slack_client.api_call("chat.postMessage", channel='general', text=message, as_user=True)
    else:
        print('Aborting... Failed to connect to Slack. Invalid Slack token or bot ID?')
        logging.critical('Failed to connect to Slack. Invalid Slack API key or Bot ID.')
        sys.exit(405)
