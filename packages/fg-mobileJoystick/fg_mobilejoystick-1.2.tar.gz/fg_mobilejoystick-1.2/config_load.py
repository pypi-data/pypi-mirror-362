import tomllib
import os

"""
Config_load.py
==============
Load the config
"""

DEFAULT_CFG = """\
# This is a TOML document
# For info about howto create/edit TOML
# See <https://toml.io/en/>

[socket]
rx.host = "localhost"
rx.port = 5503
tx.host = "localhost"
tx.port = 5504


[controls]
rudder_enabled = false


[debug]
debug = false

[web]
host = "0.0.0.0"
port = 5000
"""


config = os.path.expanduser("~/.config/mobileJoystick/config.toml")
configDir = os.path.expanduser("~/.config/mobileJoystick/")
for i in range(2):
    try:
        with open(config, "rb") as cfgFile:
            cfg = tomllib.load(cfgFile)
            break

    except FileNotFoundError:
        print(
            "No existing config file detected\n\
            Creating default one at ~/.config/mobileJoystick.config.toml"
        )

        os.mkdir(configDir)

        with open(config, "w+") as cfgFile:
            cfgFile.write(DEFAULT_CFG)

print(cfg)

RX_HOST = cfg["socket"]["rx"]["host"]
RX_PORT = cfg["socket"]["rx"]["port"]
TX_HOST = cfg["socket"]["tx"]["host"]
TX_PORT = cfg["socket"]["tx"]["port"]

RUDDER_ENABLED = cfg["controls"]["rudder_enabled"]

DEBUG = cfg["debug"]["debug"]

WEB_HOST = cfg["web"]["host"]
WEB_PORT = cfg["web"]["port"]
