# dbus-notifier #

This library offers a simple means of generating dbus notifications on Linux. 

## Installation and Usage

Make sure at least Python 3.* is installed on the target Linux system. 

Install virtualenv in which to install `dbus-notifier`.

In the virtual environment, run `pip3 install dbus-notifier`

In the Python code to use dbus-notifier:

```commandline
from dbusnotifier.dbusnotifier import NotifySender

```
The simplest code instantiating NotifySender and sending a dbus notification is this:

```commandline
    sender = NotifySender(title="My notifier")
    ...
    sender.notify(message="Hi!")
```
The above code results in a single message "Hi!" being posting in the notification area.

A more complex scenario supported by dbus-notifier is to create a dictionary with a selection of messages, where each
key identifies a message. The code below illustrates this case:

```
    sender = NotifySender(title="My notifier", messages={'0': "Success", '1': "Failed"})
    
    sender.notify(select_key='0')
```


## Dependencies

Please see `pyproject.toml`.

## Status

Mar 2023 First draft, tested locally on Manjaro Linux.
Apr 2025 release.

## Copyright

Copyright Adam Bukolt

Note that the copyright refers to the code and scripts in this repository and
expressly not to any third-party dependencies.

## License

MIT

Icons included with this program were created by and are the sole property of the copyright holder.

Note that separate licenses apply to third-party dependencies.
