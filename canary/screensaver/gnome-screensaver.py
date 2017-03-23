import os

from canary import message_handler


def check_mode(alert):
    screensaver_monitor = os.popen('gnome-screensaver-command -q')
    line = screensaver_monitor.readline()

    if "is active" in line:
        message_handler.send_message(alert)
