# USB Canary

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0) [![Build Status](https://travis-ci.org/probablynotablog/usb-canary.svg?branch=master)](https://travis-ci.org/probablynotablog/usb-canary)

USB Canary is a Linux tool that uses pyudev to monitor USB devices either around the clock, or just while it's locked. It can be configured to send you an SMS via the Twilio API, or notify a Slack channel with it's inbuilt Slack bot. 

## About the Project
USB Canary was a personal project started while between jobs after looking for a tool to monitor USB ports on my Linux computers while they were unattended, while there are many great tools already out there many require the user to login before they are notified - while many people would also argue to just turn USB ports off at a hardware level or fill them with epoxy, I still need my USB ports for keyboards and mice etc.

It was recently featured on [Bleeping Computer](https://www.bleepingcomputer.com/news/software/usb-canary-sends-an-sms-when-someone-tinkers-with-your-usb-ports/) and appreciate feedback and support received from the community.

I am currently looking into an OSX and Windows versions, the exact details of these versions are still uncertain as I work out of the details of particular functions in their respective operating systems.

### Why are you using 3rd party libraries?
A few people online have disagreed with the usage of third-party libraries and the reliance on a programming language such as Python to reliably monitor USB devices. The decision to create USB Canary in Python was a personal choice, this was originally a personal project I had kicking around at the start of the year that I decided to release to the wider community so someone might get a kick out of it.

The usage of third-party libraries specifically `pyudev` meant that in the long term I had a code base that was easy to maintain and update for myself and didn't need to make kernel level calls and parse that information reliably.

## Getting Started

There are a couple of 3rd party libraries to get USB Canary running. Below we will go through the 3rd party libraries, so those who are so inclined can check them out before installing.

### Prerequisites

- [slackclient](https://github.com/slackapi/python-slackclient) - A basic client for Slack.com, which can optionally connect to the Slack Real Time Messaging (RTM) API.
- [twilio](https://github.com/twilio/twilio-python) - A Python module for communicating with the Twilio API and generating TwiML
- [pyudev](https://github.com/pyudev/pyudev) - Python bindings to libudev (with support for PyQt4, PySide, pygobject and wx)
- [sander-daemon](https://github.com/serverdensity/python-daemon) - Jejik daemon class improved by Server Density

These can all be installed via `pip`, in some cases you may need to use `pip` with `sudo`. You can install the packages as follows:

```
pip install slackclient
pip install twilio
pip install pyudev
pip install sander-daemon
```

Otherwise you can just run `pip install -r requirements.txt`

You will also need to install the pip [`apt` library](https://apt.alioth.debian.org/python-apt-doc/library/index.html) through `apt` (which doesn't get confusing fast) this can be done as follows:

```
sudo apt install python-apt
```

This library provides access to almost every functionality supported by the underlying apt-pkg and apt-inst libraries. In Debian Jessie it may come with the install but just double check to make sure it's there.

### Installing

Before running USB Canary, you will need to configure your `settings.json` file, which should be located in the root 
directory. If it is not found here, you will encounter an `IOError`.

An example `settings.json` file:

```json
{
  "settings": {
    "slack": {
      "api_key": "xoxb-111111111111-abcdefghijklmnopqrstuvwx",
      "botname": "slack bot name"
    },
    "twilio": {
      "auth_token": "l7cy56u3Nys72vPNRS8TAbaW3X1Ap4ma",
      "account_sid": "wP32p6qFNzJ25FD1IKM0YtX629eoHbrMiV",
      "twilio_number": "+61491570156",
      "mobile_number": "+61491570157"
    },
    "general": {
      "paranoid": true,
      "screensaver": "xscreensaver",
      "slack": false,
      "twilio": true
    }
  }
}
```

Note that `paranoid`, `slack`, and `twilio` are boolean values and should be set to `true` or `false`. If the file is formatted incorrectly and it cannot be parsed, you will get a `ValueError`, you can use [JSONLint](http://jsonlint.com/) if you find yourself having issues with this.
 
USB Canary, is sort of smart and can 'detect' if you are running `XScreenSaver` or `gnome-screensaver` on your 
computer, this is done by just checking which packages are installed via the `apt` library, if both of them are 
installed though, it will leave you to determine which one you are using - if you have an unsupported 
screensaver, don't fret, you can still run it in paranoid mode.
 
Paranoid mode is also suitable for people who want to monitor if their servers have had USB's plugged into them, 
although I haven't tested them on Linode, Amazon Web Services, or Digital Ocean it is suitable for those with 
physical servers that may need this sort of monitoring.
 
To start the application:
```shell
./usb_canary.py start | stop | restart
```

## Deployment
The following will outline the basic steps to deploying USB Canary to Slack and Twilio. As extra services are 
added, please ensure you add appropriate documentation with your PR.

### Twilio
To use the Twilio intergration you will need to get an:
- [Auth Token](https://support.twilio.com/hc/en-us/articles/223136027-Auth-Tokens-and-how-to-change-them)
- [Account SID](https://support.twilio.com/hc/en-us/articles/223136607-What-is-an-Application-SID-)
- Twilio Mobile Number with SMS support

### Slack
To use the Slack integration you will need to [setup a bot user](https://api.slack.com/bot-users)

## Exit Codes

| Exit Code | Reason | Solution |
|:-:|---|---|
| 0 | PASSED |  |
| 9 | Verify that your operating system is supported. | Currently known working operating systems include: Debian Jessie, Ubuntu ZestyZapus |
| 123 | Twilio credentials not provided. | Twilio flag has been set, but credentials not provided, check settings.json |
| 124 | Slack credentials not provided. | Slack flag has been set, but credentials not provided, check settings.json |
| 125 | Screensaver conflict. | Screensaver detected, but both packages have been found. The user needs to be manually specified in the settings.json file |
| 126 | Screensaver not found. | Screensaver not set, set incorrectly, or there was a problem detecting screensaver. Currently known working screensaver managers include: XScreenSaver and gnome-screensaver |
| 127 | Option not found. | Option not set, or error in logic flow - see error message for more details |

## File Structure
I have tried to keep the code fairly segregated and straightforward to follow for those wishing to contribute.
```
usb-canary
├──LICENSE.txt
├──settings.json
├──canary
│   ├──slack
│   │   ├──slack.py
│   │   ├──slack_bot.py
│   │   └──__init__.py
│   ├──settings.py
│   ├──message_handler.py
│   ├──setup.py
│   ├──__init__.py
│   ├──twilleo
│   │   ├──__init__.py
│   │   └──twilleo.py
│   └──screensaver
│       ├──helpers.py
│       ├──gnome-screensaver.py
│       ├──xscreensaver.py
│       └──__init__.py
├──README.md <---------------------------------- YOU ARE HERE
├──requirements.txt
├──ISSUE_TEMPLATE.md
├──PULL_REQUEST_TEMPLATE.md
└──usb_canary.py 
```
Under the main `canary` directory you will find folders for different services such as Twilio which is named `twilleo` 
to avoid clashes with the Twilio library. Screensaver support can be found under the `screensaver` directory with each 
Screensaver having their own file, just to keep things tidy.

## Built With

- [Python 2.7](https://www.python.org/download/releases/2.7/) - The one that is installed on most operating systems by default  (Preliminary support for Python 3 has recently been added)
- [pyudev](https://pyudev.readthedocs.io/en/latest/) - A pure python binding to libudev, the device and hardware management and information library of Linux
- [slackclient](https://github.com/slackapi/python-slackclient) - A basic client for Slack.com, which can optionally connect to the Slack Real Time Messaging (RTM) API.
- [twilio](https://github.com/twilio/twilio-python) - A Python module for communicating with the Twilio API and generating TwiML
- [python-apt](https://apt.alioth.debian.org/python-apt-doc/library/index.html) - A library that provides access to almost every functionality supported by the underlying apt-pkg and apt-inst libraries
- [sander-daemon](https://github.com/serverdensity/python-daemon) - Jejik daemon class improved by Server Density

## Contributing

See the [CONTRIBUTING](CONTRIBUTING.md) file for details.

## Versioning

We use a simple major.minor.patch versioning where
 - A major version change will make changes that are incompatible with previous versions
 - A minor version change will add backwards-compatible functionality or bug-fixes
 - A patch version change will add backwards-compatible bug-fixes

## Authors

- **errbufferoverfl** - *Initial work* - Security Tester by day, someone with too much time on their hands by night.

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Acknowledgements

- [timball](https://github.com/timball) - for recommending `sander-daemon`
- [cclauss](https://github.com/cclauss) - for intergrating Travis CI
