"""The TV Channel Engine Italy module."""
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests

from ..engine import Engine


class EngineIT(Engine):
    """The Channel Engine class for Italy."""

    def __init__(self, zipcode=None):
        """Init for data."""
        super().__init__(zipcode)
        self.requires_provider = False

    def load_providers(self):
        """No provider defined."""

    def normalize_channel_name(self, channel):
        """Normalize channel name."""
        return channel.strip().replace(" ", "").lower()

    def load_channels(self):
        """Load channels."""
        try:
            page = requests.get("https://www.dtti.it/lcn")
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, features="html.parser")
        except RequestException:
            return
        if soup is None:
            return
        for tag_div in soup.find_all("div", {"class": "content-inner"}):
            for tag_ul in tag_div.findChildren("ul", recursive=True):
                for tag_li in tag_ul.findChildren("li"):
                    text = tag_li.get_text().split(":")
                    if len(text) == 2 and text[0].isdigit():
                        lcn = int(text[0])
                        name = text[1]
                        if "(" in name:
                            name = name[: name.find("(")]
                        name = self.normalize_channel_name(name)
                        is_hd = False
                        if name[-2:] == "hd":
                            name = name[:-2]
                            is_hd = True

                        is_hd = lcn > 9 and (is_hd or (500 < lcn < 510))

                        super().add_channel_mapping(name, is_hd, lcn)
