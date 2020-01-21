"""The TV Channel Engine Finland module."""

from csv import DictReader
from enum import Enum
import re

from bs4 import BeautifulSoup
import aiohttp

from ..engine import Engine


class _Provider(Enum):
    DIGITA = "Digita"
    DNA_WELHO = "DNA Welho"

    def __init__(self, title):
        self.title = title


class EngineFI(Engine):
    """The Channel Engine class for Finland."""

    def __init__(self, zipcode=None):
        """Init for data."""
        super().__init__(zipcode)

    async def load_providers(self, session):
        """Load providers."""
        for provider in _Provider:
            self.providers.append(provider.value)

    def normalize_channel_name(self, channel):
        """Normalize channel name."""
        return re.sub(
            r"\W+", "", channel.replace(" channel", "").replace("&", "ja")
        ).lower()

    async def load_channels(self, session):
        """Load channels."""
        if self.provider == _Provider.DIGITA.value:
            await self._load_channels_digita(session)
        elif self.provider == _Provider.DNA_WELHO.value:
            await self._load_channels_dna_welho(session)

    @staticmethod
    def _check_hd(name):
        is_hd = False
        if name[-2:] == "hd":
            name = name[:-2]
            is_hd = True
        return (name, is_hd)

    async def _load_channels_digita(self, session):
        """Load Digita channels."""
        try:
            page = await session.request(
                method="GET",
                url="https://www.digita.fi/kuluttajille/tv/"
                + "tv_ohjeet_ja_tietopankki/kanavajarjestys",
            )
            page.raise_for_status()
            text = await page.text()
            soup = BeautifulSoup(text, features="html.parser")
        except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError):
            return
        if soup is None:
            return
        for tag_table in soup.find_all("table", {"class": "p4table"}):
            for tag_tr in tag_table.findChildren("tr", recursive=True):
                tag_tds = tag_tr.findChildren("td")
                td0_text = tag_tds[0].text.strip().lower()
                if td0_text.startswith("kanava"):
                    continue  # header row
                lcn = int(td0_text)
                name = self.normalize_channel_name(tag_tds[1].text)
                name, is_hd = self._check_hd(name)
                self.add_channel_mapping(name, is_hd, lcn)

    async def _load_channels_dna_welho(self, session):
        """Load DNA Welho channels."""
        try:
            page = await session.request(
                method="GET", url="http://dvb.welho.fi/excel.php"
            )
            page.raise_for_status()
            resp = await page.content.read()
            resp.encoding = "utf-8"  # not in Content-Type, requests misdetects
            reader = DictReader(resp.iter_lines(decode_unicode=True), delimiter=";")
            for row in reader:
                name = self.normalize_channel_name(row["Kanava"])
                lcn = row["MP"]
                name, is_hd = self._check_hd(name)
                self.add_channel_mapping(name, is_hd, lcn)
        except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError):
            pass
