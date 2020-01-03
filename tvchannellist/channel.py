"""The TV Channel List module."""
import difflib
import importlib
import logging
import os

from .engine import Engine

_LOGGER = logging.getLogger(__name__)


class ChannelList:
    """The Channel List class.

    The class is the public interface exposed to client.
    """

    def __init__(self):
        """Init for data."""
        self.engine = None

    def load_engine(self, country, zipcode=None):
        """Load channel engine."""
        if os.path.isfile(f"{os.path.dirname(__file__)}/engines/{country}.py"):
            importlib.import_module(f"{__package__}.engines.{country}")

        for cls in Engine.__subclasses__():
            if cls.__name__.lower()[-2:] == country:
                module = importlib.import_module(cls.__module__)
                class_ = getattr(module, cls.__name__)
                self.engine = class_(zipcode)

    def load_channels(self):
        """Load channels."""
        self.engine.load_channels()

    def get_providers(self):
        """Get provider list."""
        self.engine.load_providers()
        return self.engine.providers

    def set_provider(self, provider):
        """Set current channel provider."""
        self.engine.provider = provider

    def get_channel(self, channel, prefer_hd=False):
        """Get channel's LCN."""
        if channel:
            _LOGGER.debug("Requesting Match for channel: %s", channel)
            lookup = self.engine.lookup
            name = self.engine.normalize_channel_name(channel)
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
