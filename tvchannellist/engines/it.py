"""The TV Channel Engine Italy module."""
from bs4 import BeautifulSoup
import requests

from ..engine import Engine


class EngineIT(Engine):
    """The Channel Engine class for Italy."""

    def __init__(self, zipcode=None):
        """Init for data."""
        super().__init__(zipcode)

    def load_providers(self):
        """No provider defined."""

    def normalize_channel_name(self, channel):
        """Normalize channel name."""
        return channel.strip().replace(" ", "").lower()

    def load_channels(self):
        """Load channels."""
        page = requests.get("https://www.dtti.it/lcn")

        soup = BeautifulSoup(page.text, features="html.parser")
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

    #   for div in soup.find_all("div", { "class" : "sites-canvas-main"}):
    #     for table in div.findChildren("table", recursive=True):
    #       for tr in table.findChildren("tr", recursive=True):
    #         td = tr.find_all("td")
    #         if len(td) == 5:
    #           numero = td[0].get_text().strip()
    #           nome = td[2].get_text().strip().replace(" ","").lower()
    #           if numero.isdigit() and len(nome) != 0 and nome != "emittente locale":
    #             numero = int(numero)
    #             hd = False
    #             if nome[-2:] == "hd":
    #               nome = nome[:-2]
    #               hd = True
    #             if (nome[-3:]) == "tgr":
    #               nome = nome[:-3]
    #             hd = numero > 9 and ( hd or (numero > 500 and numero < 510))
    #             if nome not in lookup or (preferhd == hd and lookup[nome][1] != hd):
    #                 lookup[nome] = [numero, hd]
