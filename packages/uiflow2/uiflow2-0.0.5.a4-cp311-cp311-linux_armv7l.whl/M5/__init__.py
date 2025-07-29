import platform
import time
import sys, os

from M5 import micropython_middle_layer
from M5 import hardware
from M5 import color_conv

from M5.micropython_middle_layer import BOARD, getBoard
globals()['BOARD'] = BOARD
globals()['getBoard'] = getBoard

sys.modules['micropython'] = micropython_middle_layer
sys.modules['machine'] = hardware
sys.modules["M5.unit.pahub"] = micropython_middle_layer
sys.modules['ustruct'] = micropython_middle_layer
sys.modules['utime'] = micropython_middle_layer
sys.modules['m5utils'] = micropython_middle_layer
sys.modules['color_conv'] = color_conv

from M5 import driver
from M5 import utility
from M5 import power
from M5 import umqtt
from M5 import requests2
from M5 import modbus
from M5 import unit
from M5 import module

sys.modules['hardware'] = hardware
sys.modules['unit'] = unit
sys.modules['driver'] = driver
sys.modules['utility'] = utility
sys.modules['umqtt'] = umqtt
sys.modules['requests2'] = requests2
sys.modules['modbus'] = modbus
sys.modules['module'] = module

Display = None
Lcd = None
Widgets = None
Touch = None
BtnA = None
BtnB = None
BtnC = None
Speaker = None
uiflow_run_enable = False
i2c0 = None
Power = None

if platform.system() == "Linux" and platform.machine() == "armv7l":
    import m5gfxpy
    from M5 import widgets
    from M5.touch import TouchDriver
    from M5.hardware import Speaker, I2C, Pin

    fb_device = '/dev/fb0'
    try:
        with open('/proc/fb', 'r') as f:
            for line in f:
                num, name = line.strip().split()
                if 'ili9342c' in name.lower():
                    fb_device = f'/dev/fb{num}'
                    break
    except:
        pass

    Lcd = m5gfxpy.m5lgxfpy(320, 240, fb_device)
    Lcd.setRotation(1)
    Widgets = widgets
    Touch = TouchDriver()
    BtnA = Touch.BtnA
    BtnB = Touch.BtnB
    BtnC = Touch.BtnC
    Speaker = Speaker()
    i2c0 = I2C(1, scl=Pin(11), sda=Pin(83), freq=100000)
    Power = power.Power()
    Power.setExtOutput(True) # 默认打开5V输出
    uiflow_run_enable = True

sys.path.append(os.path.join(os.path.dirname(__file__), 'widgets_ext'))


def begin():
    if uiflow_run_enable:
        try:
            with open('/sys/class/graphics/fbcon/cursor_blink', 'w') as f:
                f.write('0')
        except:
            pass
        Lcd.init()
        Touch.init()

def update():
    if uiflow_run_enable and Touch:
        Touch.update()
    time.sleep(0)







