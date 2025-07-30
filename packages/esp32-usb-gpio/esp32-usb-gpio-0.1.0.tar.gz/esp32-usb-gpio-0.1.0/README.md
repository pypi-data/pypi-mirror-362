# ESP32 USB GPIO Python Library

A Python library for controlling ESP32 GPIO pins via USB serial communication. This library provides a simple and intuitive interface to interact with ESP32 GPIO pins remotely through USB connection.

**Note**: This library requires compatible ESP32 firmware to be flashed on your ESP32 device. The corresponding ESP-IDF firmware code is available at: https://github.com/aakash4895/ESP32-USB-GPIO-ESPIDF

## Features

- **GPIO Pin Control**: Configure, set, reset, and toggle GPIO pins
- **Pin State Reading**: Read individual pin states and port states
- **Multiple GPIO Modes**: Support for input, output, open-drain configurations
- **Pull-up/Pull-down Resistors**: Configure internal pull resistors
- **Interrupt Support**: Configure GPIO interrupts (rising, falling, level-based)
- **Thread-safe Serial Communication**: Asynchronous serial data handling
- **Error Handling**: Comprehensive error reporting and exception handling

## Installation

### Option 1: Install from Source
Clone this repository and install:
```bash
git clone https://github.com/aakash4895/ESP32-USB-GPIO-PY.git
cd ESP32-USB-GPIO-PY
pip install .
```

### Option 2: Development Installation
For development, install in editable mode:
```bash
git clone https://github.com/aakash4895/ESP32-USB-GPIO-PY.git
cd ESP32-USB-GPIO-PY
pip install -e .
```

### Dependencies
The package automatically installs its dependencies:
- `pyserial`: For serial communication with ESP32

## Quick Start

```python
from esp32_usb_gpio.core import ESP32USBGPIO, GPIOPinMode, GPIOPinState

# Initialize connection to ESP32
gpio = ESP32USBGPIO('/dev/ttyUSB0')  # Replace with your port

# Setup GPIO pin 2 as output
gpio.setup(pin=2, mode=GPIOPinMode.OUTPUT)

# Set pin high
gpio.set(pin=2)

# Read pin state
state = gpio.pinState(pin=2)
print(f"Pin 2 state: {'HIGH' if state == GPIOPinState.HIGH else 'LOW'}")

# Toggle pin
gpio.toggle(pin=2)

# Reset pin to low
gpio.reset(pin=2)
```

## Package Information

- **Package Name**: esp32-usb-gpio
- **Version**: 0.1.0
- **Author**: Aakash Singh
- **License**: GPL-3.0
- **Python Compatibility**: Python 3.7+

## Core Classes and Enums

### GPIO Pin Modes (`GPIOPinMode`)
- `DISABLE`: Disable the pin
- `INPUT`: Configure as input pin
- `OUTPUT`: Configure as output pin
- `OUTPUT_OD`: Configure as open-drain output
- `INPUT_OUTPUT_OD`: Configure as input/output open-drain
- `INPUT_OUTPUT`: Configure as input/output

### GPIO Pin Pull Resistors
- `GPIOPinPullUp.ENABLE/DISABLE`: Enable/disable internal pull-up resistor
- `GPIOPinPullDown.ENABLE/DISABLE`: Enable/disable internal pull-down resistor

### GPIO Interrupts (`GPIOPinIntr`)
- `DISABLE`: Disable interrupts
- `RISING`: Trigger on rising edge
- `FALLING`: Trigger on falling edge
- `ANY`: Trigger on any edge
- `LOW_LEVEL`: Trigger on low level
- `HIGH_LEVEL`: Trigger on high level

### GPIO Pin States (`GPIOPinState`)
- `LOW`: Logic low (0V)
- `HIGH`: Logic high (3.3V)

## API Reference

### ESP32USBGPIO Class

#### Constructor
```python
ESP32USBGPIO(port)
```
- `port`: Serial port path (e.g., '/dev/ttyUSB0' on Linux, 'COM3' on Windows)

#### Methods

##### `setup(pin, mode, pull_up=DISABLE, pull_down=DISABLE, intr=DISABLE)`
Configure a GPIO pin with specified parameters.

**Parameters:**
- `pin` (int): GPIO pin number
- `mode` (GPIOPinMode): Pin mode configuration
- `pull_up` (GPIOPinPullUp): Pull-up resistor setting (optional)
- `pull_down` (GPIOPinPullDown): Pull-down resistor setting (optional)
- `intr` (GPIOPinIntr): Interrupt configuration (optional)

**Example:**
```python
# Setup pin 4 as input with pull-up resistor
gpio.setup(pin=4, mode=GPIOPinMode.INPUT, pull_up=GPIOPinPullUp.ENABLE)
```

##### `set(pin)`
Set a GPIO pin to HIGH state.

**Parameters:**
- `pin` (int): GPIO pin number

##### `reset(pin)`
Set a GPIO pin to LOW state.

**Parameters:**
- `pin` (int): GPIO pin number

##### `toggle(pin)`
Toggle the current state of a GPIO pin.

**Parameters:**
- `pin` (int): GPIO pin number

##### `pinState(pin)`
Read the current state of a specific GPIO pin.

**Parameters:**
- `pin` (int): GPIO pin number

**Returns:**
- `GPIOPinState`: Current pin state (HIGH or LOW)

##### `portState()`
Get the current state of all GPIO pins.

**Returns:**
- `list[int]`: [count, state] where state contains bit-packed pin states

## Communication Protocol

The library communicates with the ESP32 using a custom serial protocol:

### Commands Sent to ESP32:
- `INIT;pin;mode;pull_up;pull_down;intr` - Initialize pin
- `SET;pin` - Set pin high
- `RESET;pin` - Set pin low
- `TOGGLE;pin` - Toggle pin state
- `GET;pin` - Read pin state

### Responses from ESP32:
- `OK:pin` - Command executed successfully
- `ERROR:pin:error_code` - Command failed with error code
- `STATE:pin:state` - Pin state response
- `IN_GPIO_LEVEL:count:state` - Port state update

## Error Handling

The library includes comprehensive error handling:

```python
try:
    gpio.setup(pin=99, mode=GPIOPinMode.OUTPUT)  # Invalid pin
except Exception as e:
    print(f"Setup failed: {e}")
```

## Thread Safety

The library uses a background thread for serial communication, making it safe to use in multi-threaded applications. Serial data is continuously monitored and processed asynchronously.

## Hardware Requirements

- ESP32 development board with USB connection
- **ESP32 Firmware**: Compatible ESP32 firmware that implements the GPIO command protocol
  - **Required**: Flash the ESP-IDF firmware from https://github.com/aakash4895/ESP32-USB-GPIO-ESPIDF
  - This firmware handles the serial communication protocol and GPIO operations
- USB cable for connection to host computer

## Setup Instructions

1. **Flash ESP32 Firmware**:
   ```bash
   git clone https://github.com/aakash4895/ESP32-USB-GPIO-ESPIDF.git
   cd ESP32-USB-GPIO-ESPIDF
   # Follow the ESP-IDF setup and flashing instructions in that repository
   ```

2. **Install Python Library**:
   ```bash
   git clone https://github.com/aakash4895/ESP32-USB-GPIO-PY.git
   cd ESP32-USB-GPIO-PY
   pip install .
   ```

3. **Connect and Test**:
   ```python
   from esp32_usb_gpio.core import ESP32USBGPIO, GPIOPinMode
   gpio = ESP32USBGPIO('/dev/ttyUSB0')  # Your ESP32 port
   gpio.setup(pin=2, mode=GPIOPinMode.OUTPUT)
   gpio.set(pin=2)
   ```

## Supported Platforms

- Linux
- Windows
- macOS

## Dependencies

- `pyserial`: For serial communication
- `threading`: For asynchronous data handling (built-in)
- `dataclasses`: For data structure definitions (built-in)
- `enum`: For enumeration definitions (built-in)

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Troubleshooting

### Common Issues:

1. **Serial Port Access**: Ensure you have proper permissions to access the serial port
   ```bash
   sudo usermod -a -G dialout $USER  # Linux
   ```

2. **Port Not Found**: Verify the correct serial port path for your system
   ```bash
   ls /dev/tty*  # Linux/macOS
   ```

3. **Connection Issues**: Check that the ESP32 is properly connected and running compatible firmware

4. **Timeout Errors**: Ensure the ESP32 firmware is responding to commands correctly