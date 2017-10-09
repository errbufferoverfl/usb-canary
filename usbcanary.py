#!/usr/bin/env python
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
import os
import platform
import sys

from daemon import Daemon

from canary import settings
from canary.operating_system import darwin
from canary.operating_system import linux
from canary.screensaver import helpers

twilio_settings = None
slack_settings = None
pushover_settings = None

file_path = os.path.dirname(__file__)


class UsbCanary(Daemon):
    def run(self):
        while True:
            self.main()

    def main(self):
        options = settings.open_settings()['settings']['general']

        if settings.check_paranoid_setting(options['paranoid']) is True:
            paranoid_enabled = True
        else:
            paranoid_enabled = False

        screensaver_enabled = helpers.set_screensaver(options['screensaver'])

        try:
            while True:
                self.run_canary(paranoid_enabled, screensaver_enabled)
        except AttributeError:
            print('Unable to start application, mode or screensaver has not been set properly')
            sys.exit(506)

    def run_canary(self, paranoid_enabled, screensaver_enabled):
        operating_system = platform.system().lower()

        if operating_system in settings.get_supported_operating_systems():
            if operating_system == 'linux':
                linux.monitor(paranoid_enabled, screensaver_enabled)
            elif operating_system == 'darwin':
                darwin.monitor(paranoid_enabled, screensaver_enabled)
        else:
            print('{} is unsupported at this time. Aborting...'.format(operating_system))
            sys.exit(505)


if __name__ == '__main__':
    daemon = UsbCanary('/tmp/usbcanary.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print('Unknown command {}'.format(sys.argv[1]))
            print('usage: {} start|stop|restart'.format(sys.argv[0]))
            sys.exit(400)
        sys.exit(0)
    else:
        print('usage: {} start|stop|restart'.format(sys.argv[0]))
        sys.exit(400)
