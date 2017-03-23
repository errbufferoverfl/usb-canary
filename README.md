# USB Canary
USB Canary is a Linux tool that uses pyudev to monitor USB devices either around the clock, or just while it's locked. It can be configured to send you an SMS via the Twilio API, or notify a Slack channel with it's inbuilt Slack bot. 

## Getting Started

There are a couple of 3rd party libraries to get USB canary running - for some this may seem like a bad idea, but it's better than recreating the wheel or rolling your own crypto. Below we will go through the 3rd party libraries, so those who are so inclined can check them out before installing.

### Prerequisites

- [slackclient](https://github.com/slackapi/python-slackclient) - A basic client for Slack.com, which can optionally connect to the Slack Real Time Messaging (RTM) API.
- [twilio](https://github.com/twilio/twilio-python) - A Python module for communicating with the Twilio API and generating TwiML
- [pyudev](https://github.com/pyudev/pyudev) - Python bindings to libudev (with support for PyQt4, PySide, pygobject and wx)

These can all be installed via `pip`, in some cases you may need to use `pip` with `sudo`. You can install the packages as follows:

```
pip install slackclient
pip install twilio
pip install pyudev
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
supported, please ensure you add appropriate documentation.

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
│   ├──daemon
│   │   ├──__init__.py
│   │   └──daemon.py
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
└──usb_canary.py 
```
Under the main `canary` directory you will find folders for different services such as Twilio which is named `twilleo` 
to avoid clashes with the Twilio library. Screensaver support can be found under the `screensaver` directory with each 
Screensaver having their own file, just to keep things tidy.

## Built With

- [Python 2.7](https://www.python.org/download/releases/2.7/) - The one that is installed on most operating systems by default
- [pyudev](https://pyudev.readthedocs.io/en/latest/) - A pure python binding to libudev, the device and hardware management and information library of Linux
- [slackclient](https://github.com/slackapi/python-slackclient) - A basic client for Slack.com, which can optionally connect to the Slack Real Time Messaging (RTM) API.
- [twilio](https://github.com/twilio/twilio-python) - A Python module for communicating with the Twilio API and generating TwiML
- [python-apt](https://apt.alioth.debian.org/python-apt-doc/library/index.html) - A library that provides access to almost every functionality supported by the underlying apt-pkg and apt-inst libraries

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request

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

- Sander Marechal - I don't know who you are, but you made damonizing this so much easier!
