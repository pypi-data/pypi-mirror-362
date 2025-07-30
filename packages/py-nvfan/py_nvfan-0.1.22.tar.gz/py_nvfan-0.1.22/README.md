<!-- markdownlint-disable -->

# py-nvfan 🚀

py-nvfan is a Python application designed to monitor and control NVIDIA GPU fan speeds on Linux systems. It provides a command-line interface to adjust fan profiles, monitor GPU temperatures, and automate cooling based on user-defined thresholds.

## Features 🔥

- Monitor NVIDIA GPU temperatures and fan speeds 🌡️
- Set custom fan speed profiles ⚙️
- Automatic fan control based on temperature 🤖
- Command-line interface for easy usage 💻
- Logging and status reporting 📊
- Works with both Xorg and Wayland 🖥️

## Requirements 📋

- Any recent Linux distribution 🐧
- Python 3.12+ 🐍
- NVIDIA GPU with supported drivers 🎮
- Linux x86_64 operating system 💾
- [xorg-xhost](https://www.x.org/archive/X11R7.7/doc/man/man1/xhost.1.xhtml) server access control program for X. 🔒
- [nvidia-smi](https://developer.nvidia.com/nvidia-system-management-interface) installed and available in **PATH** 🛠️
- [nvidia-settings](https://www.nvidia.com/en-us/) installed and available in **PATH** ⚙️
- [pip](https://pypi.org/project/pip/) for project management or use the **pip**. 📦

## Installation 🛠️

1. Create activate a python virtual environment:
   ```bash
   cd any-directory
   python -m venv .venv # if you use pip
   ```
2. Activate the python virtual environment:
   ```bash
   source .venv/bin/activate.fish # if you use fish
   source .venv/bin/activate # if you use bash or zsh
   ```
3. Install py-nvfan
   ```bash
   pip install py-nvfan
   ```

## Usage 🚀

Run the application from the command line:

```bash
sudo py-nvfan [OPTIONS]
```

## Options ⚙️

- `-c`, `--config <path>`: Path to the config file (default: config.yaml) 📄
- `-v`, `--version`: Show the version and exit ℹ️

### Examples 📖

Show the help:

```bash
sudo py-nvfan --help
```

Run with default configuration:

```bash
sudo py-nvfan
```

Specify a custom configuration file:

```bash
sudo py-nvfan --config /path/to/config.yaml
```

Show version information:

```bash
sudo py-nvfan --version
```

## Config File 📄

By default, **py-nvfan** will create the **_config.yaml_** file (configuration file) in the directory
**_/home/root/.config/py-nvfan/_**

If you want to use a different configuration file, use the --config option

For example:

```bash
sudo py-nvfan --config /path/to/another/dir/config.yaml
```

## Configuration File Structure ⚙️

The configuration file (typically named `config.yaml`) defines how py-nvfan manages GPU fan speeds based on temperature thresholds. Below is an example and explanation of its structure:

```yaml
# py-nvfan
# This is a configuration file for the fan control system.

# temps
# The target temperatures (in °C) at which the fan speed should change.
temps:
  - 40
  - 50
  - 70
  - 80
  - 100

# fanSpeeds
# The corresponding fan duty cycles (in %) for each temperature threshold.
fanSpeeds:
  - 30
  - 50
  - 70
  - 80
  - 100
```

- **temps**: List of temperature thresholds (in Celsius). When the GPU temperature reaches or exceeds a value in this list, the corresponding fan speed from `fanSpeeds` is applied. 🌡️
- **fanSpeeds**: List of fan duty cycles (percentages). Each value corresponds to the temperature at the same position in the `temps` list. ⚙️

The lists must have the same length, and values should be ordered from lowest to highest temperature. Adjust these values to fit your cooling preferences and hardware capabilities.

## Contributing 🤝

Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.

## License 📜

This project is licensed under the MIT License. See the LICENSE file for details.

## Disclaimer ⚠️

Use this tool at your own risk. Improper fan control may cause hardware damage. Always monitor your GPU temperatures and ensure adequate cooling.
