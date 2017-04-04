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

from __future__ import absolute_import, division, print_function
import os
import platform
import socket
import sys
import time

import pyudev
from daemon import Daemon

from canary import message_handler
from canary import settings
from canary.message_handler import send_message
from canary.screensaver import helpers
from canary.slack import slack
from canary.twilleo import twilleo

twilio_settings = None
slack_settings = None


class Usb_Canary(Daemon):
    def run(self):
        while True:
            self.main()

    def main(self):
        options_file = settings.open_settings()
        options = options_file['settings']['general']

        if options['twilio']:
            global twilio_settings
            twilio_settings = twilleo.load_twilio_settings()

        if options['slack']:
            global slack_settings
            slack_settings = slack.load_slack_settings()

        if settings.check_paranoid_set(options['paranoid']):
            paranoid_setting = options['paranoid']

        screensaver_setting = helpers.set_screensaver(options['screensaver'])

        try:
            self.monitor(paranoid_setting, screensaver_setting)
        except AttributeError:
            print("Unable to start application, mode or screensaver have not been set properly")

    def monitor(self, paranoid, screensaver):
        operating_system = platform.system().lower()

        if operating_system in settings.get_supported_operating_systems():
            monitor, context = self.initialise_pyudev()
            if screensaver == 'xscreensaver':
                screensaver_monitor = os.popen('xscreensaver-command -watch')
                observer = pyudev.MonitorObserver(monitor, callback=self.set_device_event, name='monitor-observer')
                if paranoid:
                    observer.start()
                    settings.print_message('Observer started')
                elif not paranoid:
                    while True:
                        line = screensaver_monitor.readline()

                        if line.startswith('LOCK'):
                            observer.start()
                            settings.print_message('Observer started')

                        if line.startswith('UNLOCK'):
                            settings.print_message('Observer stopped')
                            observer.join()
                else:
                    sys.exit(127)
            elif screensaver == 'gnome-screensaver':
                if paranoid:
                    observer = pyudev.MonitorObserver(monitor, callback=self.set_device_event, name='monitor-observer')
                    observer.start()
                    settings.print_message('Observer started')
                elif not paranoid:
                    observer = pyudev.MonitorObserver(monitor, callback=send_message, name='monitor-observer')
                    observer.start()
                    settings.print_message('Observer started')
                else:
                    sys.exit(127)
            else:
                sys.exit(126)

    def initialise_pyudev(self):
        context = pyudev.Context()

        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb', device_type='usb_device')

        return monitor, context

    def set_device_event(self, device):
        time.ctime()  # TODO: Do we need this line?
        if device.action == 'remove':
            fmt = '{0} - {1} reported a USB was {2.action}d from node {2.device_node}'
        else:
            fmt = '{0} - {1} reported a USB was {2.action}ed to node {2.device_node}'
        alert = fmt.format(time.strftime('%l:%M%p %Z on %b %d, %Y'), socket.gethostname(), device)
        print(alert)
        message_handler.send_message(alert)


if __name__ == '__main__':
    daemon = Usb_Canary('/tmp/usbcanary.pid')
    try:
        func = {'start': daemon.start,
                'stop': daemon.stop,
                'restart': daemon.restart}.get(sys.argv[1].lower())
    except IndexError:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
    if func:
        sys.exit(func())
    else:
        print("Unknown command")
        sys.exit(2)
