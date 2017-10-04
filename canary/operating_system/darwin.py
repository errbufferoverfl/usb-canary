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

import psutil

from canary.operating_system.helpers import check_state

preserved_state = None

if platform.system().lower() == 'darwin':
    logging.debug('Importing the Quartz library.')
    import Quartz


def monitor(paranoid, screensaver):
    global preserved_state
    preserved_state = psutil.disk_partitions()
    logging.debug('Creating preserved state.')

    logging.debug('Checking if paranoid.')
    if paranoid is True:
        logging.debug('Paranoid mode enabled.')
        while True:
            logging.debug('Checking state.')
            preserved_state = check_state(preserved_state)
    elif paranoid is False:
        logging.debug('Paranoid mode disabled.')
        logging.debug('Checking screensaver manager.')

        osx_state = Quartz.CGSessionCopyCurrentDictionary()
        logging.debug('Getting CGSessionCopyCurrentDictionary.')
        screen_locked = osx_state.get("CGSSessionScreenIsLocked", 0)
        logging.debug('Getting CGSSessionScreenIsLocked key.')
        logging.debug('Screensaver status {}'.format(screen_locked))

        while screen_locked is True:
            logging.debug('Screen is locked.')
            logging.debug('Checking state.')
            preserved_state = check_state(preserved_state)
            screen_locked = osx_state.get("CGSSessionScreenIsLocked", 0)
    else:
        print('Unable to run application, paranoid mode set correctly?')
        logging.critical('Aborting... Unable to run application, paranoid mode not set correctly.')
        sys.exit(401)
