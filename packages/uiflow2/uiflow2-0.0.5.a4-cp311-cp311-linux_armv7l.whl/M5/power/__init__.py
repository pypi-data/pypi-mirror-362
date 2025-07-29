import os
# from M5 import I2C, Pin
# from M5.driver import axp2102

class Power:
    def __init__(self):
        os.system("[ -d /sys/class/gpio/PI2 ] || echo 130 > /sys/class/gpio/export")
        os.system("[ -d /sys/class/gpio/PI3 ] || echo 131 > /sys/class/gpio/export")
        os.system("echo out > /sys/class/gpio/PI3/direction")
        os.system("echo out > /sys/class/gpio/PI2/direction")

    def __del__(self):
        os.system("echo 130 > /sys/class/gpio/unexport")
        os.system("echo 131 > /sys/class/gpio/unexport")

    def timerSleep(self, *args):
        """定时休眠函数
        
        重载方式:
        timerSleep(seconds: int) - 指定秒数后休眠
        timerSleep(minutes: int, hours: int) - 指定分钟和小时后休眠  
        timerSleep(minutes: int, hours: int, date: int, weekDay: int) - 指定具体时间休眠
        """
        if len(args) == 1:
            # 处理秒数休眠
            seconds = args[0]
            if isinstance(seconds, int) and 1 <= seconds <= 15300:
                # os.system(f"rtcwake -m mem -s {seconds}")
                os.system(f"sleep {seconds}")
                
        elif len(args) == 2:
            # 处理分钟和小时休眠
            minutes, hours = args
            if (isinstance(minutes, int) and isinstance(hours, int) and 
                0 <= minutes <= 59 and 0 <= hours <= 23):
                print("unsuppoert minutes hours")
                
        elif len(args) == 4:
            # 处理完整时间休眠
            minutes, hours, date, weekDay = args
            if (isinstance(minutes, int) and isinstance(hours, int) and
                isinstance(date, int) and isinstance(weekDay, int) and
                0 <= minutes <= 59 and 0 <= hours <= 23 and
                1 <= date <= 31 and 0 <= weekDay <= 6):
                print("unsuppoert minutes hours date weekDay")
                
        else:
            raise ValueError("error timesleep param")

    # 电源输出控制
    def setExtOutput(self, enable: bool, port: int = 0xFF): 
        value = 1 if enable else 0
        os.system(f"echo {value} > /sys/class/gpio/PI3/value")
    
    def getExtOutput(self) -> bool:
        with open("/sys/class/gpio/PI3/value", "r") as f:
            return f.read().strip() == "1"
    
    # USB 电源控制
    def setUsbOutput(self, enable: bool):
        value = 1 if enable else 0
        os.system(f"echo {value} > /sys/class/gpio/PI2/value")

    def getUsbOutput(self) -> bool:
        with open("/sys/class/gpio/PI2/value", "r") as f:
            return f.read().strip() == "1"
    
    # 电源管理
    def setLed(self, brightness=255):  # 通过AXP2101 PMU控制
        light = 50 + (int)(brightness/255 * 50)  # 将0-255映射到50-100
        os.system(f"echo {light} > /sys/class/backlight/axp2101_m5stack_bl/brightness")
    
    def powerOff(self):
        os.system("poweroff")
    
    def getBatteryLevel(self) -> int:
        if not os.path.exists("/sys/class/power_supply"):
            print("without battery in power_supply")
            return 0
        battery_dirs = os.listdir("/sys/class/power_supply")
        if not battery_dirs:
            print("without battery in power_supply")
            return 0
        for battery_dir in battery_dirs:
            capacity_path = f"/sys/class/power_supply/{battery_dir}/capacity"
            if os.path.exists(capacity_path):
                with open(capacity_path, "r") as f:
                    print(f"battery level: {f.read().strip()}%")
                    return int(f.read().strip())
        print("without battery in power_supply")
        return 0
        
    def setBatteryCharge(self, enable: bool):  # 电池充电控制
        if not os.path.exists("/sys/class/power_supply"):
            print("without battery in power_supply")
            return 0
        battery_dirs = os.listdir("/sys/class/power_supply")
        if not battery_dirs:
            print("without battery in power_supply")
            return 0
        for battery_dir in battery_dirs:
            capacity_path = f"/sys/class/power_supply/{battery_dir}/capacity"
            if os.path.exists(capacity_path):
                with open(capacity_path, "r") as f:
                    print(f"battery charge: {f.read().strip()}%")
                    return int(f.read().strip())
        print("without battery in power_supply")
        return 0
        
    def setChargeCurrent(self, max_mA: int):
        if not os.path.exists("/sys/class/power_supply"):
            print("without battery in power_supply")
            return 0
        # TODO

    def setChargeVoltage(self, max_mV: int):
        if not os.path.exists("/sys/class/power_supply"):
            print("without battery in power_supply")
            return 0
        # TODO

    def isCharging(self) -> bool:
        if not os.path.exists("/sys/class/power_supply"):
            print("without battery in power_supply")
            return 0
        # TODO

    def getBatteryVoltage(self) -> int:
        if not os.path.exists("/sys/class/power_supply"):
            print("without battery in power_supply")
            return 0
        # TODO

    def getBatteryCurrent(self) -> int:
        if not os.path.exists("/sys/class/power_supply"):
            print("without battery in power_supply")
            return 0
        # TODO
    
    # 振动电机控制（需硬件支持）
    def setVibration(self, level: int):
        print("unsupport vibration")
        return 0
    
    def deepSleep(self, seconds: int, enable: bool):
        print("linux unsupported deep sleep")
        return 0
    
    def lightSleep(self, seconds: int, enable: bool):
        print("linux unsupported light sleep")
        return 0

class PORT:
    MBUS = 0x01  # MBUS电源总线
    USB = 0x02   # USB端口
    CAN1 = 0x04  # CAN1接口
    CAN2 = 0x08  # CAN2接口
    RS485 = 0x10 # RS485接口
