# USB Canary
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Build Status](https://travis-ci.org/errbufferoverfl/usb-canary.svg?branch=v1.0.2)](https://travis-ci.org/errbufferoverfl/usb-canary)

USB Canary is a Linux and OSX tool that uses psutil to monitor USB devices
either around the clock, or just while your computer is locked. It can
be configured to send you an SMS via the Twilio API, notify a Slack
channel with it's inbuilt Slack bot, or send a push message through Pushover.

**Disclaimer**: Under no circumstances should USB Canary be used for production, production-like 
systems or critical infrastructure.

## Getting Started

There are a couple of 3rd party libraries to get USB Canary running - so
Linux and OSX users should read the prerequisites for their distribution.

### Prerequisites

- [slackclient](https://github.com/slackapi/python-slackclient) - A
basic client for Slack.com, which can optionally connect to the Slack
Real Time Messaging (RTM) API.
- [twilio](https://github.com/twilio/twilio-python) - A Python module
for communicating with the Twilio API and generating TwiML.
- [pushover](https://github.com/Thibauth/python-pushover) - Comprehensive bindings and command line utility for the Pushover notification service
- [psutil](https://pypi.python.org/pypi/psutil) - Cross-platform lib
for process and system monitoring in Python.
- [gcc](https://gcc.gnu.org/) - GNU Compiler Collection
- [Xcode](https://developer.apple.com/xcode/) - Integrated development
environment for macOS
- [Quartz](https://pypi.python.org/pypi/pyobjc-framework-Quartz) -
Wrappers for the Quartz frameworks on macOS.

#### Installing Prerequisites on *Nix

Ubuntu and Debian users will need to make sure they have installed a C
compiler such as `gcc` as well as the `python-dev` package.

```
sudo apt-get install gcc python-dev python-pip
pip install psutil
```
Major Linux distros also provide binary distributions of psutil. However
this is not recommended as *Nix generall ship older versions.
```
sudo apt-get install python-psutil
```

You will also need to install the pip
[`apt` library](https://apt.alioth.debian.org/python-apt-doc/library/index.html)
through `apt` this can be done as follows:

```
sudo apt install python-apt
```

This library provides access to almost every functionality supported by
the underlying apt-pkg and apt-inst libraries. In Debian Jessie it may
come with the install but just double check to make sure it's there.

#### Installing Prerequisites on OSX

OSX users will need to install [Xcode](https://developer.apple.com/downloads/?name=Xcode) first then:
```
pip install psutil==5.3.1
```

OSX users will also need to manually install the [Quartz](https://pypi.python.org/pypi/pyobjc-framework-Quartz)
Python library as follows:
```
pip install pyobjc-framework-Quartz
```

Once distribution specific instractions have been followed the following
packages can all be installed via `pip`, in some cases you may need to
use `pip` with `sudo`. You can install the packages as follows:

```
pip install slackclient==1.0.9
pip install twilio==5.7.0
pip install python-pushover==0.3
pip install psutil==5.3.1
pip install sander-daemon==1.0.0
```

### Installing

Before running USB Canary, you will need to configure your `settings.json`
file, which should be located in the root directory. If it is not found
here, you will encounter an `IOError`.

An example `settings.json` file:

```json
{
  "settings": {
    "slack": {
      "api_key": "xoxb-111111111111-abcdefghijklmnopqrstuvwx",
      "channel_name": "usb_canary",
      "botname": "USB Canary"
    },
    "twilio": {
      "auth_token": "l7cy56u3Nys72vPNRS8TAbaW3X1Ap4ma",
      "account_sid": "wP32p6qFNzJ25FD1IKM0YtX629eoHbrMiV",
      "twilio_number": "+61491570156",
      "mobile_number": "+61491570157"
    },
    "pushover": {
      "priority": 1,
      "user_key": "youruserkeygoeshere",
      "api_token": "yourapitokengoeshere"
    },
    "general": {
      "paranoid": true,
      "screensaver": "xscreensaver",
      "slack": false,
      "twilio": true,
      "pushover": false,
    }
  }
}
```

Note that `paranoid`, `slack` and `twilio` are boolean values and
should be set to `true` or `false`. If the file is formatted incorrectly
and it cannot be parsed, you will get a `ValueError`, you can use
[JSONLint](http://jsonlint.com/) if you find yourself having issues with
this.

# Linux

USB Canary, can 'detect' if you are running
`XScreenSaver` or `gnome-screensaver` on your computer, this is done by
just checking which packages are installed via the `apt` library, if
both of them are installed though, it will leave you to determine which
one you are using - if you have an unsupported screensaver, don't fret,
you can still run it in paranoid mode.

Paranoid mode is also suitable for people who want to monitor if their
servers have had USB's plugged into them,
although I haven't tested them on Linode, Amazon Web Services, or
Digital Ocean it is suitable for those with
physical servers that may need this sort of monitoring.

To start the application:
```shell
# Linux users
./usb_canary.py start | stop | restart
```

```shell
# OSX users
sudo ./usb_canary.py start | stop | restart

```

## Deployment

The following will outline the basic steps to deploying USB Canary to
Slack and Twilio.

### Twilio

To use the Twilio integration you will need to get an:
- [Auth Token](https://support.twilio.com/hc/en-us/articles/223136027-Auth-Tokens-and-how-to-change-them)
- [Account SID](https://support.twilio.com/hc/en-us/articles/223136607-What-is-an-Application-SID-)
- Twilio Mobile Number with SMS support

### Slack

To use the Slack integration you will need to [setup a bot user](https://api.slack.com/bot-users)

### Pushover

To use Pushover API for sending push messages to your devices, you need to create an [account and application](https://pushover.net/faq#overview-what)

## Exit Codes

| Exit Code | Reason | Solution |
|:-:|---|---|
| 0 | PASSED |  |
| 400 | Unknown command. | Usage: `./usb_canary start | stop | restart` |
| 401 | Paranoid option not set. | Check that paranoid is set to `true` or `false` |
| 402 | Screensaver is not supported. | Currently known working screensavers include: XScreenSaver, gnome-screensaver |
| 403 | Screensaver conflict. | Screensaver detected, but both packages have been found. The user needs to be manually specified in the `settings.json` file |
| 404 | Slack credentials not provided. | Slack flag has been set, but credentials not provided, check `settings.json` |
| 405 | Slack credentials incorrect. | Slack flag has been set, but credentials are not correct, check `settings.json` |
| 406 | Twilio credentials not correct. | Twilio flag has been set, but credentials not provided, check `settings.json` |
| 407 | Twilio account SID not set | Twilio SID value has not been set, check `settings.json` |
| 408 | Twilio API token is blank | Twilio API token has not been set, check `settings.json` |
| 409 | Receiving mobile # is blank  | Twilio receiving mobile number has not been set, check `settings.json` |
| 410 | Twilio mobile # is blank | Twilio allocated mobile number has not been set, check `settings.json` |
| 411 | Twilio key missing in settings.json | Twilio JSON block is not in settings file, check `settings.json` |
| 412 | Pushover user key missing in settings.json | Pushover user key (per account) is missing, check `settings.json` |
| 413 | Pushover user key missing in settings.json | Pushover api key (per registered app) is missing, check `settings.json` |
| 414 | Pushover priority level missing in settings.json | Pushover priority level is missing, check `settings.json` |
| 415 | Pushover key missing in settings.json | Pushover JSON block is not in settings file, check `settings.json` |
| 501 | `settings.json` file missing. | Download setting.json from Github |
| 502 | Unable to parse settings.json | Check for erroneous symbols, use [JSONLint](http://jsonlint.com/) to check formatting |
| 503 | Paranoid option not set correctly. | Paranoid option not set, or set incorrectly |
| 504 | Screensaver not found. | Screensaver not set, set incorrectly, or there was a problem detecting screensaver. |
| 505 | Verify that your operating system is supported. | Currently known working operating systems include: Debian Jessie, Debian Stretch, Ubuntu ZestyZapus |
| 506 | Screensaver or paranoid setting is not set correctly. | Check settings.json |
| 507 | Verbose logging option not set. | Check that verbose is set to `true` or `false` (without the quotes). True enables debugging, False enables info and higher |

## Built With

- [Python 3](https://www.python.org/download/releases/3.0/)
- [slackclient](https://github.com/slackapi/python-slackclient) - A basic client for Slack.com, which can optionally connect to the Slack Real Time Messaging (RTM) API.
- [twilio](https://github.com/twilio/twilio-python) - A Python module for communicating with the Twilio API and generating TwiML
- [psutil](https://pypi.python.org/pypi/psutil) - Cross-platform lib for process and system monitoring in Python.
- [Quartz](https://pypi.python.org/pypi/pyobjc-framework-Quartzhttps://pypi.python.org/pypi/pyobjc-framework-Quartz) - Wrappers for the Quartz frameworks on macOS
- [python-apt](https://apt.alioth.debian.org/python-apt-doc/library/index.html) - A library that provides access to almost every functionality supported by the underlying apt-pkg and apt-inst libraries

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

This project is licensed under the GNU GPLv3 License - see the
[LICENSE](LICENSE.txt) file for details.

## Acknowledgements

- [timball](https://github.com/timball) - for recommending `sander-daemon`
- [cclauss](https://github.com/cclauss) - for integrating Travis CI
- [helpsterTee](https://github.com/helpsterTee) - for adding Pushover support
