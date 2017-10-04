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
import socket
import time

import psutil

from canary import helpers
from canary.message_handler import send_message


def check_state(preserved_state):
    logging.debug('Getting current state of disk partitions.')
    current_state = psutil.disk_partitions()

    logging.debug('Comparing current state of disk partitions to the preserved state.')
    if len(current_state) < len(preserved_state):
        logging.debug('Found less disk partitions than in previous state. Checking difference.')
        devices = helpers.diff(preserved_state, current_state)
        logging.debug('Updating preserved state with current state.')
        preserved_state = current_state

        for device in devices:
            alert = '{} - {} reported {} was removed.'.format(
                time.strftime('%l:%M%p %Z on %b %d, %Y'), socket.gethostname(), device.mountpoint)
            send_message(alert)
        # logging.warning(alert)

    elif len(current_state) > len(preserved_state):
        logging.debug('Found more disk partitions than in previous state. Checking difference.')
        devices = helpers.diff(preserved_state, current_state)
        logging.debug('Updating preserved state with current state.')
        preserved_state = current_state

        for device in devices:
            alert = '{} - {} reported {} was added.'.format(
                time.strftime('%l:%M%p %Z on %b %d, %Y'), socket.gethostname(), device.mountpoint)
            send_message(alert)
        # logging.warning(alert)
    return preserved_state
