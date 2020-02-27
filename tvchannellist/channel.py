"""The TV Channel List module."""
import difflib
import importlib
import logging
import os
from typing import Any, List, Optional

from aiohttp import ClientSession

from .engine import Engine

_LOGGER = logging.getLogger(__name__)


class ChannelList:
    """The Channel List class.

    The class is the public interface exposed to client.
    """

    def __init__(self, session: ClientSession = None) -> None:
        """Init for data."""
        self.engine: Engine
        if session:
            self.session = session
        else:
            self.session = ClientSession()

    def load_engine(self, country: str, zipcode: int = None) -> None:
        """Load channel engine."""
        if os.path.isfile(f"{os.path.dirname(__file__)}/engines/{country}.py"):
            importlib.import_module(f"{__package__}.engines.{country}")

        for cls in Engine.__subclasses__():
            if cls.__name__.lower()[-2:] == country:
                module = importlib.import_module(cls.__module__)
                class_ = getattr(module, cls.__name__)
                self.engine = class_(zipcode)

    async def load_channels(self) -> None:
        """Load channels."""
        await self.engine.load_channels(self.session)

    async def get_providers(self) -> List[Any]:
        """Get provider list."""
        if self.engine.requires_provider:
            await self.engine.load_providers(self.session)
            return self.engine.providers
        return []

    def set_provider(self, provider: Any) -> None:
        """Set current channel provider."""
        if self.engine.requires_provider:
            self.engine.provider = provider

    def is_provider_required(self) -> bool:
        """Get if the engine requires provider."""
        return self.engine.requires_provider

    def get_channel(self, channel: str, prefer_hd: bool = False) -> Optional[int]:
        """Get channel's LCN."""
        if channel:
            _LOGGER.debug("Requesting Match for channel: %s", channel)
            lookup = self.engine.lookup
            name = self.engine.normalize_channel_name(channel)
            result = difflib.get_close_matches(name, lookup.keys())
            if result:
                numbers = lookup[str(result[0])]
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

    async def close_session(self):
        """Close aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()

    def override_channel(self, name: str, lcn: int) -> None:
        """Add a manual channel."""
        normalized = self.engine.normalize_channel_name(name)
        self.engine.add_channel_mapping(normalized, False, lcn)
        self.engine.add_channel_mapping(normalized, True, lcn)
