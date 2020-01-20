"""The TV Channel Engine Finland module."""

from csv import DictReader
from enum import Enum
import re

from bs4 import BeautifulSoup
import requests

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

    def load_providers(self):
        """Load providers."""
        for provider in _Provider:
            self.providers.append(provider.value)

    def normalize_channel_name(self, channel):
        """Normalize channel name."""
        return re.sub(
            r"\W+", "", channel.replace(" channel", "").replace("&", "ja")
        ).lower()

    def load_channels(self):
        """Load channels."""
        if self.provider == _Provider.DIGITA.value:
            self._load_channels_digita()
        elif self.provider == _Provider.DNA_WELHO.value:
            self._load_channels_dna_welho()

    @staticmethod
    def _check_hd(name):
        is_hd = False
        if name[-2:] == "hd":
            name = name[:-2]
            is_hd = True
        return (name, is_hd)

    def _load_channels_digita(self):
        """Load Digita channels."""
        try:
            page = requests.get(
                "https://www.digita.fi/kuluttajille/tv/tv_ohjeet_ja_tietopankki/kanavajarjestys"
            )
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, features="html.parser")
        except requests.exceptions.RequestException:
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

    def _load_channels_dna_welho(self):
        """Load DNA Welho channels."""
        try:
            with requests.get("http://dvb.welho.fi/excel.php", stream=True) as resp:
                if resp.status_code == 200:
                    resp.encoding = "utf-8"  # not in Content-Type, requests misdetects
                    reader = DictReader(
                        resp.iter_lines(decode_unicode=True), delimiter=";"
                    )
                else:
                    return
                for row in reader:
                    name = self.normalize_channel_name(row["Kanava"])
                    lcn = row["MP"]
                    name, is_hd = self._check_hd(name)
                    self.add_channel_mapping(name, is_hd, lcn)
        except requests.exceptions.RequestException:
            pass
