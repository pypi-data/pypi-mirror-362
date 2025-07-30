from py_nvfan.nvidialib import *
from .config import VERSION, printAsciiArt, AppConfig, cl, pc, createConfigFile
from confz import FileSource
import argparse
import os
import time


def passArgs() -> None:
    printAsciiArt()
    # Configuração do parser
    parser = argparse.ArgumentParser(
        description=f"py-nvfan v{VERSION}: Automatic Fan Control for NVIDIA Graphics Cards Based on Temperature.",
    )

    # Argumentos
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=AppConfig.CONFIG_SOURCES.file,  # type: ignore
        required=False,
        help="Path to the config file (config.yaml)",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Version {VERSION}",
        help="Show the version and exit",
    )

    # Processamento dos argumentos
    args: argparse.Namespace = parser.parse_args()

    AppConfig.CONFIG_SOURCES = FileSource(file=args.config)

    # print(args.config)
    if not os.path.exists(args.config):
        cl.print("[bold red]Config file not found, creating...[/bold red]")
        createConfigFile(configFile=args.config)

    appConfig = AppConfig()
    pc(message="using config file", variable=args.config)
    pc(message="Temperatures", variable=appConfig.temps)
    pc(message="FanSpeeds", variable=appConfig.fanSpeeds)
    totalDevices = getTotalDevices()
    pc(message="Total devices", variable=totalDevices)
    checkingNumber: int = 0
    while True:
        with cl.status("Running...") as status:
            try:
                for i in range(totalDevices):
                    cl.print("-" * 40)
                    pc(message="Checking Number\t", variable=checkingNumber)
                    cl.print(
                        f"[bold yellow]Device[/bold yellow]\t\t: [{i}] - {getDeviceName(gpu_index=i)}"
                    )
                    currentTemp: int = getGpuTemperature(gpu_index=i)
                    pc(message="Temperature\t", variable=f"{currentTemp}°C")
                    newfanSpeed = getFanDuty(
                        currentTemp=currentTemp,
                        targetTemps=appConfig.temps,
                        targetDuties=appConfig.fanSpeeds,
                    )
                    fanCount = getFanCount(gpu_index=i)
                    pc(message="Fan Count\t", variable=fanCount)
                    currentFanSpeed: int = getFanSpeed(gpu_index=i)
                    pc(
                        message="Fan Speed\t",
                        variable=f"{currentFanSpeed}%",
                    )

                    if newfanSpeed != currentFanSpeed:
                        setFanSpeed(gpu_index=i, fan_speed=newfanSpeed)
                        # Add a small delay after changing fan speed
                        time.sleep(5)

                    checkingNumber += 1

                time.sleep(5)

            except KeyboardInterrupt:
                cl.print("[bold red]Exiting...[/bold red]")
                break


def main() -> None:
    passArgs()
