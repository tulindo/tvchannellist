"""The TV Channel List module."""
import logging
import difflib

from .engine import Engine
from .it import EngineIT
from .us import EngineUS

_LOGGER = logging.getLogger(__name__)


class ChannelList:
    """The Channel List class.

    The class is the public interface exposed to client.
    """

    def __init__(self, country, zipcode=None):
        """Init for data."""
        if country == "it":
            self.engine = EngineIT(zipcode)
        elif country == "us":
            self.engine = EngineUS(zipcode)
        else:
            pass

    def load_channels(self):
        self.engine.load_channels()

    def get_providers(self):
        self.engine.load_providers()
        return self.engine.providers

    def set_provider(self, provider):
        self.engine.provider = provider

    def get_channel(self, channel, prefer_hd=False):
        if channel:
            _LOGGER.debug("Requesting Match for channel: %s", channel)
            lookup = self.engine.lookup
            name = self.engine.format_channel_name(channel)
            result = difflib.get_close_matches(name, lookup.keys())
            if result:
                numbers = lookup[result[0]]
                if numbers[0] and not numbers[1]:
                    number = numbers[0]
                elif not numbers[0] and numbers[1]:
                    number = numbers[1]
                elif prefer_hd:
                    number = numbers[1]
                else:
                    number = numbers[0]
                if number:
                    _LOGGER.debug("Got channel number %d", number)
                    return number
        return None
