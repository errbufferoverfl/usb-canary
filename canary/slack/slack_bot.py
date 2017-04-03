import slackclient
import sys

slack_client = None
channel_name = None


def setup(slack, channel):
    global slack_client
    slack_client = slackclient.SlackClient(slack['api_key'])
    global channel_name
    channel_name = channel


def run_bot(message, channel):
    if slack_client.rtm_connect():
        channel_list = slack_client.api_call('channels.list')['channels']
        channel_exists = False

        for dic in channel_list:
            if dic.get('name') == channel:
                channel_exists = True
                break

        if channel_exists:
            slack_client.api_call("chat.postMessage", channel=channel, text=message, as_user=True)
        else:
            message = "Hi! :wave: It looks like some of my settings might be a little frazzled, and I can't post " \
                  "messages like normal."
            slack_client.api_call("chat.postMessage", channel='general', text=message, as_user=True)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
        sys.exit(465564)
