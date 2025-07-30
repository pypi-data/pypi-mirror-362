from serial import Serial
from enum import IntEnum, StrEnum
import threading
from dataclasses import dataclass


class GPIOPinMode(IntEnum):
    DISABLE = 0
    INPUT = 1
    OUTPUT = 2
    OUTPUT_OD = 6
    INPUT_OUTPUT_OD = 7
    INPUT_OUTPUT = 3

class GPIOPinPullUp(IntEnum):
    DISABLE = 0
    ENABLE = 1

class GPIOPinPullDown(IntEnum):
    DISABLE = 0
    ENABLE = 1

class GPIOPinIntr(IntEnum):
    DISABLE = 0
    RISING = 1
    FALLING = 2
    ANY = 3
    LOW_LEVEL = 4
    HIGH_LEVEL = 5

class GPIOPinState(IntEnum):
    LOW = 0
    HIGH = 1

class GPIOCmd(StrEnum):
    GPIO_SETUP = "INIT"
    GPIO_SET = "SET"
    GPIO_RESET = "RESET"
    GPIO_TOGGLE = "TOGGLE"
    GPIO_GET = "GET"

class GPIOCmdResponse(StrEnum):
    GPIO_OK = "OK"
    GPIO_ERROR = "ERROR"
    GPIO_STATE = "STATE"
    GPIO_INTR = "INTR"
    GPIO_INTR_CLEAR = "INTR_CLEAR"
    GPIO_INTR_GET = "INTR_GET"
    GPIO_IN = "IN_GPIO_LEVEL"

class ESP32USBGPIO:

    @dataclass
    class gpioPortState:
        cnt:int = 0
        state:int = 0
    
    @dataclass
    class gpioPinState:
        pin:int = 0
        state:int = 0
        error:int = 0

    _gpioPortState: gpioPortState = gpioPortState()
    _gpioPinState: gpioPinState = gpioPinState()

    responseRecv = False

    def __init__(self, port):
        self.port = port
        self.baudrate = 115200
        self.serial = Serial(port, self.baudrate)
        self.serialThread = threading.Thread(target=self._read_serial, daemon=True)
        self.serialThread.start()

    def _read_serial(self):
        while True:
            try:
                if self.serial.in_waiting > 0:
                    data = self.serial.readline().decode().strip()
                    data = data.split(':')
                    match data[0]:
                        case GPIOCmdResponse.GPIO_IN:
                            self._gpioPortState.cnt = int(data[1])
                            self._gpioPortState.state = int(data[2], 0)
                        case GPIOCmdResponse.GPIO_STATE:
                            self._gpioPinState.pin = int(data[1])
                            self._gpioPinState.state = GPIOPinState(int(data[2]))
                        case GPIOCmdResponse.GPIO_OK:
                            self._gpioPinState.pin = int(data[1])
                        case GPIOCmdResponse.GPIO_ERROR:
                            self._gpioPinState.pin = int(data[1])
                            self._gpioPinState.error = int(data[2])

                    if data[0] is not GPIOCmdResponse.GPIO_IN:
                        self.responseRecv = True
            except Exception as e:
                print(f"Error reading serial data: {e}")

    def _sendCommand(self, cmd: str):
        self.responseRecv = False
        self.serial.write(cmd.encode())
        while not self.responseRecv:
            pass

    def setup(self, pin:int, mode:GPIOPinMode, pull_up:GPIOPinPullUp=GPIOPinPullUp.DISABLE, pull_down:GPIOPinPullDown=GPIOPinPullDown.DISABLE, intr:GPIOPinIntr=GPIOPinIntr.DISABLE):
        self._sendCommand(f"{GPIOCmd.GPIO_SETUP};{pin};{mode};{pull_up};{pull_down};{intr}")
        if self._gpioPinState.pin == pin:
            self.responseRecv = False
            if self._gpioPinState.error != 0:
                raise Exception(f"Error setting up pin {pin}: {hex(self._gpioPinState.error)}")
        
    def set(self, pin:int):
        self._sendCommand(f"{GPIOCmd.GPIO_SET};{pin}")
        if self._gpioPinState.pin == pin:
            self.responseRecv = False
            if self._gpioPinState.error != 0:
                raise Exception(f"Error setting pin {pin}: {hex(self._gpioPinState.error)}")

    def reset(self, pin:int):
        self._sendCommand(f"{GPIOCmd.GPIO_RESET};{pin}")
        if self._gpioPinState.pin == pin:
            self.responseRecv = False
            if self._gpioPinState.error != 0:
                raise Exception(f"Error resetting pin {pin}: {hex(self._gpioPinState.error)}")

    def toggle(self, pin:int):
        self._sendCommand(f"{GPIOCmd.GPIO_TOGGLE};{pin}")
        if self._gpioPinState.pin == pin:
            self.responseRecv = False
            if self._gpioPinState.error != 0:
                raise Exception(f"Error toggling pin {pin}: {hex(self._gpioPinState.error)}")
    
    def pinState(self, pin:int) -> GPIOPinState:
        self._sendCommand(f"{GPIOCmd.GPIO_GET};{pin}")
        if self._gpioPinState.pin == pin:
            self.responseRecv = False
            if self._gpioPinState.error != 0:
                raise Exception(f"Error reading pin {pin}: {hex(self._gpioPinState.error)}")
            return GPIOPinState(self._gpioPinState.state)

    def portState(self) -> list[int]:
        return [self._gpioPortState.cnt, self._gpioPortState.state]