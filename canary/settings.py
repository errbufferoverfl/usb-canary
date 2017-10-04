# coding=utf-8

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
import json
import logging
import os
import sys

supported_operating_systems = ['linux', 'darwin']

settings_file_path = os.path.dirname(__file__) + '/../settings.json'


def save_settings(options):
    logging.debug('Saving settings to {}'.format(os.path.abspath(settings_file_path)))
    json.dump(options, open(settings_file_path, 'w'))


def open_settings():
    logging.debug('Attempting to open settings.json as read-only')
    try:
        with open(settings_file_path, 'r') as settings_file:
            settings = json.load(settings_file)
            return settings
    except IOError:
        print('File {} not found'.format(settings_file_path))
        logging.critical('Aborting... File {} not found.'.format(os.path.abspath(settings_file_path)))
        sys.exit(501)
    except ValueError:
        print('No JSON object could be decoded')
        logging.critical('Aborting... No JSON object could be decoded')
        sys.exit(502)


def check_paranoid_setting(paranoid_option):
    paranoid_set_true = paranoid_option is True
    paranoid_set_false = paranoid_option is False

    logging.debug('Checking if paranoid option has been set correctly.')
    if paranoid_set_true or paranoid_set_false:
        return True
    else:
        print('Aborting... Paranoid option has not set to "True" or "False"')
        logging.critical('{} is not a valid selection. Please set to "True" or "False".')
        sys.exit(503)


def check_screensaver_setting(screensaver_option):
    logging.debug('Checking if screensaver option has been set.')
    if screensaver_option:
        return True
    else:
        print('Aborting... Screensaver option has not been set.')
        logging.critical('Screensaver option has not been set.')
        sys.exit(504)


def check_logging_verbosity(verbose_option):
    if verbose_option is True:
        return True
    elif verbose_option is False:
        return False
    else:
        print('Aborting... Verbose option has not been set.')
        logging.critical('Verbose option has not been set.')
        sys.exit(507)


def get_supported_operating_systems():
    return supported_operating_systems
