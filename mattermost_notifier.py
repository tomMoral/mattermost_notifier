import os
import stat
import warnings
import configparser
from pathlib import Path

try:
    from matterhook import Webhook
except ImportError:
    raise ImportError(
        "Package matterhook is necessary to for mattermost_notifier. "
        "Please install it through pip install matterhook."
    )

CONFIG_FILE_NAME = 'matterhook.cfg'

# Global config file should be only accessible to current user as it stores
# sensitive information such as the Github token.
GLOBAL_CONFIG_FILE_MODE = stat.S_IFREG | stat.S_IRUSR | stat.S_IWUSR

# Default config
DEFAULT_CONFIG = {
    'api_key': None,
    'url': None
}


def get_global_config_file():
    "Return the global config file."

    config_file = os.environ.get('MATTERHOOK_CONFIG', None)
    if config_file is not None:
        config_file = Path(config_file)
        assert config_file.exists(), (
            f"BENCHOPT_CONFIG is set but file {config_file} does not exists.\n"
            f"It can be created with `touch {config_file.resolve()}`."
        )
    else:
        config_file = Path('.') / CONFIG_FILE_NAME
        if not config_file.exists():
            config_file = Path.home() / '.config' / CONFIG_FILE_NAME

    # check that the global config file is only accessible to current user as
    # it stores critical information such as the github token.
    if (config_file.exists()
            and config_file.stat().st_mode != GLOBAL_CONFIG_FILE_MODE):
        mode = oct(config_file.stat().st_mode)[5:]
        expected_mode = oct(GLOBAL_CONFIG_FILE_MODE)[5:]
        warnings.warn(
            f"BenchOpt config file {config_file} is with mode {mode}.\n"
            "As it stores sensitive information such as the github token,\n"
            f"it is advised to use mode {expected_mode} (user rw only)."
        )

    return config_file


def get_setting(name):
    config_file = get_global_config_file()

    # Get default value
    default_config = DEFAULT_CONFIG
    assert name in default_config, f"Unknown config key {name}"
    default_value = default_config[name]

    # Get config file
    config = configparser.ConfigParser()
    config.read(config_file)

    # Get the name of the environment variable associated to this setting
    env_var_name = f"MATTERHOOK_{name.upper()}"

    # Get setting with order: 1. env var / 2. config file / 3. default value
    value = config.get('matterhook', name, fallback=default_value)
    return os.environ.get(env_var_name, value)


def notify_mattermost(msg, channel=None, host='drago', url=None, api_key=None):

    if api_key is None:
        api_key = get_setting('api_key')
    assert api_key, (
        "No API key was provided for Mattermost. It can either be passed "
        "directly to the function, by env variable MATTERHOOK_API_KEY, or "
        "set in a config file.\nSee README.md for more info."
    )

    if url is None:
        url = get_setting('url')
    assert url, (
        "No URL was provided for Mattermost. It can either be passed "
        "directly to the function, by env variable MATTERHOOK_URL, or "
        "set in a config file.\nSee README.md for more info."
    )

    # mandatory parameters are url and your webhook API key
    mwh = Webhook(url, api_key)

    payload = {}
    payload['author_name'] = host
    payload['thumb_url'] = (
        'https://raw.githubusercontent.com/tomMoral/mattermost_notifier/'
        f'1356541d3cfff2745ffea55af54c9ff7ea6e18ae/icons/{host}.png'
    )
    payload['text'] = msg

    # send a message to the API_KEY's channel
    mwh.send(attachments=[payload], channel=channel)


if __name__ == '__main__':
    notify_mattermost(
        "Bitus!",
        channel='@thmoreau'
    )
