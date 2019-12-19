import requests
import json
import re
from .engine import Engine


class EngineUS(Engine):
    def __init__(self, zipcode):
        super().__init__(zipcode)

    def load_providers(self):
        page = requests.get(
            f"https://mobilelistings.tvguide.com/Listingsweb/ws/rest/serviceproviders/zipcode/{self.zipcode}?formattype=json"
        )
        for provider in json.loads(page.text):
            for device in provider["Devices"]:
                self.providers.append(
                    (
                        str(provider["Id"]) + "." + str(device["DeviceFlag"]),
                        provider["Name"],
                        device["DeviceName"],
                        provider["Type"],
                    )
                )

    def format_channel_name(self, channel):
        regex = re.compile(r"\(.+?\)")
        channel = regex.sub("", channel).lower()
        channel = channel.replace("&", "and")
        channel = channel.replace("the ", "")
        channel = channel.replace(" channel", "")

        pattern = re.compile(r"([^\s\w]|_)+")
        channel = pattern.sub("", channel).strip()
        return channel

    def load_channels(self):
        idx = self.provider[0]
        response = requests.get(
            f"http://mobilelistings.tvguide.com/Listingsweb/ws/rest/schedules/{idx}/start/0/duration/1?ChannelFields=Name,FullName,Number&formattype=json&disableChannels=music,ppv,24hr&ScheduleFields=ProgramId"
        )
        lineup = {}
        for channel in json.loads(response.text):
            full = self.format_channel_name(channel["Channel"]["FullName"])

            name = channel["Channel"]["Name"].lower()
            pattern = re.compile(r"([^\s\w]|_)+")
            name = pattern.sub("", name)
            num = channel["Channel"]["Number"]

            hd = False
            if " hdtv" in full or " hd" in full:
                hd = True
                full = full.replace(" hdtv", "")
                full = full.replace(" hd", "")

                if name.endswith("hd"):
                    name = name[:-2]
                elif name.endswith("d"):
                    name = name[:-1]
                name = name.strip()

            super().add_channel_mapping(name, hd, num)
            super().add_channel_mapping(full, hd, num)
