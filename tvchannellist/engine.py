"""The TV Channel List module."""
import logging

from abc import ABC, abstractmethod

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
        """Load channels from selected provider."""

    @abstractmethod
    def load_providers(self):
        """Load Provider list."""

    def add_channel_mapping(self, name, is_hd, lcn):
        """Add a new Mapping to the lookup list.

        name: the name of the channel
        hd: True if the channel is HD
        lcn: the Logical Channel Name of the channel.
        """
        if is_hd:
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
    def normalize_channel_name(self, channel):
        """Normalize channel name."""
