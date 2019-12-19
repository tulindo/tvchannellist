import requests
import json
from .engine import Engine
from bs4 import BeautifulSoup


class EngineIT(Engine):
    def __init__(self, zipcode):
        super().__init__(zipcode)

    def load_providers(self):
        pass

    def format_channel_name(self, channel):
        return channel.strip().replace(" ", "").lower()

    def load_channels(self):

        page = requests.get("https://www.dtti.it/lcn")
        # page = requests.get("https://sites.google.com/site/litaliaindigitale/muxnazionali/listalcnnazionale")

        soup = BeautifulSoup(page.text, features="html.parser")
        for div in soup.find_all("div", {"class": "content-inner"}):
            for ul in div.findChildren("ul", recursive=True):
                for li in ul.findChildren("li"):
                    text = li.get_text().split(":")
                    if len(text) == 2 and text[0].isdigit():
                        lcn = int(text[0])
                        name = text[1]
                        if "(" in name:
                            name = name[: name.find("(")]
                        name = self.format_channel_name(name)
                        hd = False
                        if name[-2:] == "hd":
                            name = name[:-2]
                            hd = True
                        hd = lcn > 9 and (hd or (lcn > 500 and lcn < 510))

                        super().add_channel_mapping(name, hd, lcn)

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
