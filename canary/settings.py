# coding=utf-8
import json
import os

import sys

import time

supported_operating_systems = ['linux']
file_path = os.path.dirname(__file__) + '/../settings.json'


def save_settings(options):
    json.dump(options, open(file_path, 'w'))


def open_settings():
    try:
        with open(file_path, 'r') as settings_file:

            settings = json.load(settings_file)
            settings_file.close()

            return settings
    except IOError:
        print "File {} not found".format(file_path)
    except ValueError:
        print "No JSON object could be decoded"


def check_paranoid_set(paranoid_option):
    paranoid_set_true = paranoid_option is True
    paranoid_set_false = paranoid_option is False

    if paranoid_set_true or paranoid_set_false:
        return True
    else:
        sys.exit(1)


def check_screensaver(screensaver_option):
    if screensaver_option:
        return True
    else:
        sys.exit(1)


def get_supported_operating_systems():
    return supported_operating_systems


def print_message(message):
    time.ctime()
    print '{} - {}'.format(time.strftime('%l:%M%p %Z on %b %d, %Y'), message)
