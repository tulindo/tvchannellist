"""The TV Channel Engine Unites States module."""
import json
import re
from requests.exceptions import RequestException
import requests

from ..engine import Engine


def _load_response(url):
    try:
        page = requests.get(url)
        if page.status_code == 200:
            return json.loads(page.text)
    except (RequestException, json.JSONDecodeError):
        return None
    return None


class EngineUS(Engine):
    """The Channel Engine class for United States."""

    def __init__(self, zipcode):
        """Init for response."""
        super().__init__(zipcode)
        self.provider = []

    def load_providers(self):
        """Load Provider list."""
        response = _load_response(
            "https://mobilelistings.tvguide.com/Listingsweb/ws/rest/serviceproviders/zipcode/"
            + f"{self.zipcode}?formattype=json"
        )
        if response:
            for provider in response:
                for device in provider["Devices"]:
                    self.providers.append(
                        (
                            str(provider["Id"]) + "." + str(device["DeviceFlag"]),
                            provider["Name"],
                            device["DeviceName"],
                            provider["Type"],
                        )
                    )

    def normalize_channel_name(self, channel):
        """Normalize channel name."""
        regex = re.compile(r"\(.+?\)")
        channel = regex.sub("", channel).lower()
        channel = channel.replace("&", "and")
        channel = channel.replace("the ", "")
        channel = channel.replace(" channel", "")

        pattern = re.compile(r"([^\s\w]|_)+")
        channel = pattern.sub("", channel).strip()
        return channel

    def load_channels(self):
        """Load channels from selected provider."""
        idx = self.provider[0]
        response = _load_response(
            f"http://mobilelistings.tvguide.com/Listingsweb/ws/rest/schedules/{idx}/"
            + "start/0/duration/1?ChannelFields=Name,FullName,Number&formattype=json&"
            + "disableChannels=music,ppv,24hr&ScheduleFields=ProgramId"
        )
        if response:
            for channel in response:
                full = self.normalize_channel_name(channel["Channel"]["FullName"])

                name = channel["Channel"]["Name"].lower()
                pattern = re.compile(r"([^\s\w]|_)+")
                name = pattern.sub("", name)
                num = int(channel["Channel"]["Number"])

                is_hd = False
                if " hdtv" in full or " hd" in full:
                    is_hd = True
                    full = full.replace(" hdtv", "")
                    full = full.replace(" hd", "")

                    if name.endswith("hd"):
                        name = name[:-2]
                    elif name.endswith("d"):
                        name = name[:-1]
                    name = name.strip()

                super().add_channel_mapping(name, is_hd, num)
                super().add_channel_mapping(full, is_hd, num)
