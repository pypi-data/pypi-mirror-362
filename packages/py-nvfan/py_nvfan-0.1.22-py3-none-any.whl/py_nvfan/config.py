import os
from typing import Any
from confz import BaseConfig, FileSource
from rich.console import Console


# SeuUsuario ALL=(ALL) NOPASSWD: /usr/bin/nvidia-settings

# APP_NAME
APP_NAME = "py-nvfan"
# APP_VERSION
VERSION = "0.1.22"

cl = Console()


def createConfigFile(configFile: str) -> None:
    """
    Create the config file if it doesn't exist.
    """

    if not os.path.exists(configFile):
        dir_name = os.path.dirname(configFile)
        if dir_name:
            os.makedirs(
                name=dir_name,
                exist_ok=True,
            )
        with open(file=configFile, mode="w") as f:
            f.write(
                """#-----------------------------------------------------
# py-nvfan
# This is a configuration file for the fan control system.
#-----------------------------------------------------

# temps
# The target temperatures are the temperatures at which the fan should operate.
temps:
- 40
- 50
- 70
- 80
- 100

# targetDuties
# The duty cycle is the percentage of time the fan is on in a given period.
fanSpeeds:
- 30
- 50
- 70
- 80
- 100
                """
            )


def pc(message: str, variable: Any) -> None:
    cl.print(f"[bold yellow]{message}[/bold yellow]: {variable}")


def printAsciiArt() -> None:
    asciiArt = r"""
                               __             
 _ __  _   _       _ ____   __/ _| __ _ _ __  
| '_ \| | | |_____| '_ \ \ / / |_ / _` | '_ \ 
| |_) | |_| |_____| | | \ V /|  _| (_| | | | |
| .__/ \__, |     |_| |_|\_/ |_|  \__,_|_| |_|
|_|    |___/                
    """
    print(asciiArt)


class AppConfig(BaseConfig):
    CONFIG_SOURCES = FileSource(
        file=os.path.join(
            os.path.expanduser(path="~"), ".config", f"{APP_NAME}", "config.yaml"
        )
    )

    temps: list[int]
    fanSpeeds: list[int]
