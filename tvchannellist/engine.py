"""The TV Channel List module."""
from abc import ABC, abstractmethod
import logging
import re
import time
import requests
import difflib

# import sslkeylog

_LOGGER = logging.getLogger(__name__)


class Engine(ABC):
    """The Channel Engine base class.

    The class is the working class that handles the communication
    with Metronet IESS cloud platform.
    """

    def __init__(self, zipcode):
        """Init for data."""
        self.lookup = {}
        self.zipcode = zipcode
        self.providers = []
        self.provider = None
        super().__init__()

    @abstractmethod
    def load_channels(self):
        pass

    @abstractmethod
    def load_providers(self):
        pass

    def add_channel_mapping(self, name, hd, lcn):
        """Add a new Mapping to the lookup list.

        name: the name of the channel
        hd: True if the channel is HD
        lcn: the Logical Channel Name of the channel.
        """
        if hd:
            if name not in self.lookup:
                self.lookup[name] = [None, lcn]
            else:
                if not self.lookup[name][1]:
                    self.lookup[name][1] = lcn
        else:
            if name not in self.lookup:
                self.lookup[name] = [lcn, None]
            else:
                if not self.lookup[name][0]:
                    self.lookup[name][0] = lcn

    @abstractmethod
    def format_channel_name(self, channel):
        pass

    # def GetChannel(self, channel):
    #     if channel:
    #         _LOGGER.debug("Requesting Match for channel: %s", channel)
    #         tmp = channel.lower().replace(" ",'')
    #         result = difflib.get_close_matches(self.FormatChannelName(channel), lookup.keys())
    #         number = lookup[result[0]]
    #         _LOGGER.debug("Got channel number %d", number)
    #         return number

    #     return None
