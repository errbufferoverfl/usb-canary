import apt

import sys
import canary.settings

supported_screensavers = ['gnome-screensaver', 'xscreensaver']


def set_screensaver(screensaver_option):
    """
    Detects the screensaver - this can be specified by the user at install time, or detected if not set.
    If screensaver is specified, it is checked against the supported screensavers list.
    :param screensaver_option: the screensaver returned by the command line.
    :return: the identified screensaver as specified by the user, or detected by the program
    """
    if screensaver_option == "":
        screensaver_option = identify_screensaver()
        save_screensaver(screensaver_option)
    else:
        if screensaver_option in supported_screensavers:
            save_screensaver(screensaver_option)
        else:
            print
            sys.exit(126)
    return screensaver_option


def save_screensaver(screensaver):
    """
    Writes the screensaver to the settings.json file
    :param screensaver: the screensaver
    :return:
    """
    settings = canary.settings.open_settings()

    if settings['settings']['general']['screensaver']:
        print "Writing over screensaver value {}".format(settings['settings']['general']['screensaver'])
        settings['settings']['general']['screensaver'] = screensaver
        canary.settings.save_settings(settings)
    else:
        settings['settings']['general']['screensaver'] = screensaver
        canary.settings.save_settings(settings)


def identify_screensaver():
    cache = apt.Cache()

    if cache['xscreensaver'].is_installed and cache['gnome-screensaver'].is_installed:
        print "XScreenSaver and gnome-screensaver detected. Please select active screensaver in the settings file " \
              "before proceeding."
        sys.exit(125)
    if cache['xscreensaver'].is_installed:
        return 'xscreensaver'
    elif cache['gnome-screensaver'].is_installed:
        return 'gnome-screensaver'
    else:
        sys.exit(126)


def get_supported_screensavers():
    return supported_screensavers
