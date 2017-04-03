import sys

import canary.settings
import canary.slack.slack_bot


def load_slack_settings():
    """
    Opens settings.json and checks all values have been set,
    if they have, creates a list containing these details
    and sets up Slack bot.

    If not exits and notifies user of misconfiguration

    :return: list containing options to use Slack API
    """
    slack_settings = canary.settings.open_settings()

    slack = slack_settings['settings']['slack']
    # sanity check that the user has actually supplied data
    api_key = not slack["api_key"]
    botname = not slack["botname"]
    channel_name = not slack["channel_name"]

    if botname and api_key and channel_name:
        sys.exit(124)

    canary.slack.slack_bot.setup(slack, channel_name)

    return slack
