"""The TV Channel Engine Italy module."""
from bs4 import BeautifulSoup

from ..engine import Engine


class EngineIT(Engine):
    """The Channel Engine class for Italy."""

    def __init__(self, zipcode=None):
        """Init for data."""
        super().__init__(zipcode)
        self.requires_provider = False

    async def load_providers(self, session):
        """No provider defined."""

    def normalize_channel_name(self, channel):
        """Normalize channel name."""
        return channel.strip().replace(" ", "").lower()

    async def load_channels(self, session):
        """Load channels."""
        text = await Engine.get_response("https://www.dtti.it/lcn", session)
        if text:
            soup = BeautifulSoup(text, features="html.parser")
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
