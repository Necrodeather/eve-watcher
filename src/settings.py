import configparser
from functools import lru_cache
from typing import Any

config_parser = configparser.ConfigParser()


class Config:
    upper_left_position: str
    lower_right_position: str
    alert_sound: str


@lru_cache
def read_config_file() -> Config:
    file = config_parser.read('./config.ini')
    if not file:
        raise FileNotFoundError('File is not created!')
    config = Config()
    config.upper_left_position = config_parser.get(
        'Settings', 'upper_left_position'
    )
    config.lower_right_position = config_parser.get(
        'Settings', 'lower_right_position'
    )
    config.alert_sound = config_parser.get('Settings', 'alert_sound')
    return config


def create_config_file() -> None:
    config_parser.add_section('Settings')
    config_parser.set('Settings', 'upper_left_position', '')
    config_parser.set('Settings', 'lower_right_position', '')
    config_parser.set(
        'Settings', 'alert_sound', r'C:\Windows\Media\Alarm10.wav'
    )
    with open('config.ini', 'w') as config_file:
        config_parser.write(config_file)


def set_config_file(params: list[Any]) -> None:
    for item in params:
        config_parser.set('Settings', item[0], item[1])
    with open('config.ini', 'w') as config_file:
        config_parser.write(config_file)
