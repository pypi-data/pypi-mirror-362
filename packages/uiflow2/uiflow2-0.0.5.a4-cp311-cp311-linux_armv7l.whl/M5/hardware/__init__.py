"""M5 hardware module"""

from .pin import Pin
from .i2c import I2C
from .uart import UART
from .speaker import Speaker
from .rtc import RTC
from .spi import SPI

__all__ = ['Pin', 'I2C', 'UART', 'Speaker', 'RTC', 'SPI']