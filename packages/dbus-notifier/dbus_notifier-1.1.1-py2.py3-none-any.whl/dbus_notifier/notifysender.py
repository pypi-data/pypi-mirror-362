"""
This module provides very simple dbus notifications.
"""
import os

import dbusnotify
from dotenv import dotenv_values


class NotifySender:
    """
    This class represents a sender of dbus notifications. It can post individual messages, or you can initialise it
    with a dictionary of messages. If the dictionary is present, notifications can be posted by calling the method
    notify with a message selection key.
    """

    def __init__(self, title, messages=None):
        self._title = None
        self._messages = None
        self.title = title
        self.messages = messages

    @property
    def title(self):  # pylint: disable=missing-function-docstring
        return self._title

    @title.setter
    def title(self, in_str=None):
        self._title = in_str or ""

    @property
    def messages(self):
        """
        A dictionary of pre-prepared messages that can be selected using a key.
        :return: The value of a private member variable
        """
        return self._messages

    @messages.setter
    def messages(self, in_dict=None):
        self._messages = in_dict or {}

    def _post_notification(self, in_title="", in_description=""):
        """
        This private method posts notifications
        :param in_title: A string containing the notification title
        :param in_description: A string containing the notification message
        :return: void
        """
        ve_path = os.getenv("VIRTUAL_ENV")
        ve_config = dotenv_values(os.path.join(ve_path, ".env_dbus_notifier"))

        if ve_config:
            icon_file = os.path.join(ve_path, ve_config.get("DBUS_NOTIFIER_ICON", ''))
        else:
            config = dotenv_values(os.path.join(os.getcwd(), '.env_dbus_notifier'))
            icon_file = os.path.join(os.getcwd(), config.get("DBUS_NOTIFIER_ICON", ''))

        if not os.path.isfile(icon_file):
            icon_file = ""
        dbusnotify.write(
            in_description,
            title=in_title if in_title else self.title,
            icon=icon_file,  # On Windows .ico is required, on Linux - .png
        )

    def notify(self, message=None, select_key=None):
        """
        This method posts notifications.
        :param message: A string containing the notification message
        :param select_key: A key value to select a message from a dictionary of messages, if available (this key is
        not needed if `message` is provided)
        :return: void
        """
        title = self.title

        if select_key and self.messages:
            self._post_notification(title, self.messages.get(select_key, ""))
            return

        if not message:
            return

        self._post_notification(title, message)
