# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = wolfram_download_configuration_from_dict(json.loads(json_string))

from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Remote:
    type: str
    flags: int
    url: str

    def __init__(self, type: str, flags: int, url: str) -> None:
        self.type = type
        self.flags = flags
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> 'Remote':
        assert isinstance(obj, dict)
        type = from_str(obj.get("type"))
        flags = from_int(obj.get("flags"))
        url = from_str(obj.get("url"))
        return Remote(type, flags, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_str(self.type)
        result["flags"] = from_int(self.flags)
        result["url"] = from_str(self.url)
        return result


class Config:
    remote: Remote

    def __init__(self, remote: Remote) -> None:
        self.remote = remote

    @staticmethod
    def from_dict(obj: Any) -> 'Config':
        assert isinstance(obj, dict)
        remote = Remote.from_dict(obj.get("remote"))
        return Config(remote)

    def to_dict(self) -> dict:
        result: dict = {}
        result["remote"] = to_class(Remote, self.remote)
        return result


class WolframDownloadConfiguration:
    config: Config
    id: str
    metafile: str

    def __init__(self, config: Config, id: str, metafile: str) -> None:
        self.config = config
        self.id = id
        self.metafile = metafile

    @staticmethod
    def from_dict(obj: Any) -> 'WolframDownloadConfiguration':
        assert isinstance(obj, dict)
        config = Config.from_dict(obj.get("config"))
        id = from_str(obj.get("id"))
        metafile = from_str(obj.get("metafile"))
        return WolframDownloadConfiguration(config, id, metafile)

    def to_dict(self) -> dict:
        result: dict = {}
        result["config"] = to_class(Config, self.config)
        result["id"] = from_str(self.id)
        result["metafile"] = from_str(self.metafile)
        return result


def wolfram_download_configuration_from_dict(s: Any) -> WolframDownloadConfiguration:
    return WolframDownloadConfiguration.from_dict(s)


def wolfram_download_configuration_to_dict(x: WolframDownloadConfiguration) -> Any:
    return to_class(WolframDownloadConfiguration, x)
