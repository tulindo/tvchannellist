"""The TV Channel List module."""
from abc import ABC, abstractmethod
import logging
from typing import Any, Dict, List, Optional

import aiohttp
from aiohttp import ClientSession

_LOGGER = logging.getLogger(__name__)


class Engine(ABC):
    """The Channel Engine base class.

    The class is the working class that handles the communication
    with Metronet IESS cloud platform.
    """

    def __init__(self, zipcode: int):
        """Init for data."""
        self.lookup: Dict[str, List[Any]] = {}
        self.zipcode: int = zipcode
        self.providers: List[Any] = []
        self.provider: Optional[int] = None
        self.requires_provider: bool = True
        super().__init__()

    @staticmethod
    async def get_response(url, session: ClientSession) -> Optional[str]:
        """Get page text."""
        try:
            page = await session.request(method="GET", url=url)
            page.raise_for_status()
            return await page.text()
        except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError):
            return None
        return None

    @abstractmethod
    async def load_channels(self, session: ClientSession):
        """Load channels from selected provider."""

    @abstractmethod
    async def load_providers(self, session: ClientSession):
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
    def normalize_channel_name(self, channel: str) -> str:
        """Normalize channel name."""
