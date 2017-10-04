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


def is_active():
    logging.debug('Opening gnome-screensaver-command -q.')
    logging.debug('gnome-screensaver-command -q.')
    screensaver_monitor = os.popen('gnome-screensaver-command -q')
    line = screensaver_monitor.readline()
    logging.debug('{}'.format(line))

    logging.debug('Checking if screensaver is currently active.')
    if 'is active' in line:
        logging.debug('Screensaver is active.')
        return True
