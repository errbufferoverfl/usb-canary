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
import os
import sys

import psutil

from canary.operating_system.helpers import check_state
from canary.screensaver import gnome_screensaver

preserved_state = None


def monitor(paranoid, screensaver):
    preserved_state = psutil.disk_partitions()
    logging.debug('Creating preserved state.')

    logging.debug('Checking if paranoid.')
    if paranoid:
        logging.debug('Paranoid mode enabled.')
        while True:
            logging.debug('Checking state.')
            preserved_state = check_state(preserved_state)
    elif not paranoid:
        logging.debug('Paranoid mode disabled.')
        logging.debug('Checking screensaver manager.')
        logging.debug('Screensaver set to: {}.'.format(screensaver.lower))
        if screensaver.lower() == 'xscreensaver':
            screensaver_monitor = os.popen('xscreensaver-command -watch')
            logging.debug('Opening xscreensaver-command -watch.')
            logging.debug('Reading xscreensaver-command -watch.')
            line = screensaver_monitor.readline()
            logging.debug('{}'.format(line))

            while line.startswith('LOCK'):
                logging.debug('Screen is locked.')
                logging.debug('Checking state.')
                preserved_state = check_state(preserved_state)
        elif screensaver.lower() == 'gnome-screensaver':
            if gnome_screensaver.is_active():
                preserved_state = check_state(preserved_state)
        else:
            print('Unable to run application, paranoid mode set correctly?')
            logging.critical('Aborting... Unable to run application, paranoid mode not set correctly.')
            sys.exit(401)
