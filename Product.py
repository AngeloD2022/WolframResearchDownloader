

import requests
from Utilities import parse_response_hybrid
import WolframDownloadConfiguration
import const
import re

class Product:
    id: str
    version: str
    cfg: WolframDownloadConfiguration

    def __init__(self, id:str, selector:str):
        parsed = re.split(const.pattern, selector, re.MULTILINE)
        self.version = parsed[3]+".0"
        self.id = id
        self.cfg = self.get_remote_cfg()

    def get_remote_cfg(self):
        url = const.WR_CDN + self.version + "/" + self.id + "/catalog.json"
        response = requests.get(url)
        cfg = parse_response_hybrid(response.text)
        return WolframDownloadConfiguration.wolfram_download_configuration_from_dict(cfg)

    def get_meta(self):
        url = self.cfg.metafile
        response = requests.get(url)
        meta = parse_response_hybrid(response.text)
        return meta
