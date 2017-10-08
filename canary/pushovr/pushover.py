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
import sys

import canary.settings


def load_pushover_settings():
    """
    Opens settings.json and checks all values have been set, if they have, creates a list containing these details.

    If not exits and notifies user of misconfiguration

    :return: list containing options to use Pushover API
    """
    pushover_settings = canary.settings.open_settings()

    pushover = pushover_settings['settings']['pushover']

    try:
        # sanity check that the user has actually supplied data
        if not pushover['user_key']:
            print('Pushover user key has been left blank')
            sys.exit(412)
        elif not pushover['api_token']:
            print('Pushover API token has been left blank')
            sys.exit(413)
        elif not pushover['priority']:
            print('Pushover message priority has been left blank')
            sys.exit(414)
        else:
            return pushover
    except KeyError:
        print('Pushover key missing in the settings file')
        sys.exit(415)
