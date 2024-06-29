from configparser import ConfigParser
from dataclasses import dataclass


@dataclass
class Config:
    cache: bool = False
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 4096
    temperature: float = 0.0
    base_system: str = "I will provide a prompt with this structure -> {message: string, samples: int, fields: [field1,field2]} and you will generate a json with an array of size samples of objects with the specified fields and fill them with mock data, and the context from the field name and the message which specifies the data context."
    key: str = ""


def get_config_from_file(config: ConfigParser) -> Config:
    res = Config()

    if "CONFIG" in config:
        for key in config["CONFIG"]:
            setattr(res, key, config["CONFIG"][key])
    else:
        raise KeyError("No config section found in config.ini")

    return res


def set_config_key(key: str, config: Config) -> Config:
    config.key = key
    return config
