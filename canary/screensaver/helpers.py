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
import platform
import sys

import canary.settings

if platform.system().lower == 'linux':
    logging.debug('Importing the apt library.')
    import apt

supported_screensavers = ['gnome-screensaver', 'xscreensaver']


def set_screensaver(screensaver_option):
    """
    Detects the screensaver - this can be specified by the user at install time, or detected if not set.
    If screensaver is specified, it is checked against the supported screensavers list.
    :param screensaver_option: the screensaver returned by the command line.
    :return: the identified screensaver as specified by the user, or detected by the program
    """
    logging.debug('Checking screensaver manager.')
    if screensaver_option == "":
        logging.debug('No screensaver specified, attempting auto-detection.')
        screensaver_option = identify_screensaver()
        logging.debug('Saving detected screensaver.')
        save_screensaver(screensaver_option)
    else:
        logging.debug('Screensaver specified, checking if supported.')
        if screensaver_option in supported_screensavers:
            logging.debug('Saving supported screensaver.')
            save_screensaver(screensaver_option)
        else:
            print('Unable to run application, screensaver supported?')
            logging.critical('Aborting... Unable to run application, screensaver not supported.')
            sys.exit(402)
    return screensaver_option


def save_screensaver(screensaver):
    """
    Writes the screensaver to the settings.json file
    :param screensaver: the screensaver
    :return:
    """
    logging.debug('Opening settings.json.')
    settings = canary.settings.open_settings()
    logging.debug('Checking if screensaver option has been specified.')
    if settings['settings']['general']['screensaver']:
        logging.debug('Screensaver specified.')
        logging.debug('Writing over screensaver value {}'.format(settings['settings']['general']['screensaver']))
        settings['settings']['general']['screensaver'] = screensaver
        logging.debug('Saving settings.json.')
        canary.settings.save_settings(settings)
    else:
        logging.debug('Screensaver not specified.')
        settings['settings']['general']['screensaver'] = screensaver
        logging.debug('Saving settings.json.')
        canary.settings.save_settings(settings)


def identify_screensaver():
    cache = apt.Cache()
    logging.debug('Getting apt cache.')

    logging.debug('Checking if supported screensaver packages are installed.')
    if cache['xscreensaver'].is_installed and cache['gnome-screensaver'].is_installed:
        logging.debug('xscreensaver and gnome-screensaver installed. User must specify which package to monitor.')
        print("XScreenSaver and gnome-screensaver detected. Please select active screensaver in the settings file "
              "before proceeding.")
        sys.exit(403)
    if cache['xscreensaver'].is_installed:
        logging.debug('\txscreensaver installed.')
        return 'xscreensaver'
    elif cache['gnome-screensaver'].is_installed:
        logging.debug('\tgnome-screensaver installed.')
        return 'gnome-screensaver'
    else:
        print('Unable to run application, screensaver supported?')
        logging.critical('Aborting... Unable to run application, screensaver not supported.')
        sys.exit(402)


def get_supported_screensavers():
    return supported_screensavers
