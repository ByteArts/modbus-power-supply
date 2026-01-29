# Power Supply Control Console

## Overview
This project provides an interactive console program for controlling the Hanmatek HM310T power supply. The main functionality is encapsulated in the `PowerSupplyConsole` class, which manages the connection to the power supply and offers various commands for controlling it.

## Features
- Set and get output voltage and current.
- Enable and disable power output.
- Ramp voltage over a specified time.
- Configure over voltage, over current, and over power protection settings.
- Display current status and output values.

## Requirements
To run this project, you need to install the following dependencies:

- `pyHM310T`

You can install the required packages using the following command:

```
pip install -r requirements.txt
```

## Building the Executable

### Windows
To create a Windows executable, run the following batch script from the src folder:

```
scripts/build_exe.bat
```

### Unix-like Systems (Linux, macOS)
To create an executable for Unix-like systems, run the following shell script:

```
scripts/build_exe.sh
```

## Usage
After building the executable, you can run it from the command line. The program will prompt you for the serial port to connect to the power supply. You can use commands like `set_voltage`, `get_voltage`, `enable`, and `disable` to control the power supply.

## Contributing
Feel free to contribute to this project by submitting issues or pull requests. Your feedback and contributions are welcome!

## License
This project is licensed under the MIT License. See the LICENSE file for more details.