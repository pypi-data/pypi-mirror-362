from evdev import InputDevice, list_devices, categorize, ecodes
from collections import deque
import time
import os

class Button:
    class CB_TYPE:
        WAS_CLICKED = "WAS_CLICKED"
        WAS_DOUBLE_CLICKED = "WAS_DOUBLE_CLICKED"
        WAS_HOLD = "WAS_HOLD"
        WAS_PRESSED = "WAS_PRESSED"
        WAS_RELEASED = "WAS_RELEASED"
    
    def __init__(self):
        # state
        self._pressed = False      # current pressed state
        self._released = True      # current released state
        self._holding = False      # current holding state
        
        # event
        self._clicked = False          # click event (short press)
        self._double_clicked = False   # double click event
        self._hold = False             # hold event
        
        # time record
        self._last_press_time = 0      # last press time
        self._last_click_time = 0      # last click time
        self._hold_time = 0.5          # hold time
        self._double_click_time = 0.3  # double click time
        
        # button index
        self._button_index = -1        # button index
        
        # callback function
        self._callbacks = {
            self.CB_TYPE.WAS_CLICKED: None,
            self.CB_TYPE.WAS_DOUBLE_CLICKED: None,
            self.CB_TYPE.WAS_HOLD: None,
            self.CB_TYPE.WAS_PRESSED: None,
            self.CB_TYPE.WAS_RELEASED: None
        }
    
    def update(self, is_pressed, button_index, current_button_index):
        """
        update button state
        Args:
            is_pressed: whether pressed
            button_index: current button index
            current_button_index: current active button index
        """
        # if not current button and other button is pressed, force set to released state
        if button_index != current_button_index and current_button_index != -1:
            if self._pressed:
                self._pressed = False
                self._released = True
                self._holding = False
                if self._callbacks[self.CB_TYPE.WAS_RELEASED]:
                    self._callbacks[self.CB_TYPE.WAS_RELEASED](True)
            return
        
        current_time = time.time()
        self._button_index = button_index
        
        # press event handle
        if is_pressed and not self._pressed:
            self._pressed = True
            self._released = False
            self._holding = True
            self._last_press_time = current_time
            # trigger press callback
            if self._callbacks[self.CB_TYPE.WAS_PRESSED]:
                self._callbacks[self.CB_TYPE.WAS_PRESSED](True)
        
        # release event handle
        elif not is_pressed and self._pressed:
            press_duration = current_time - self._last_press_time
            self._pressed = False
            self._released = True
            self._holding = False
            
            # short press check (click event)
            if press_duration < self._hold_time:
                self._clicked = True
                # check if double click
                if current_time - self._last_click_time < self._double_click_time:
                    self._double_clicked = True
                    if self._callbacks[self.CB_TYPE.WAS_DOUBLE_CLICKED]:
                        self._callbacks[self.CB_TYPE.WAS_DOUBLE_CLICKED](True)
                else:
                    # click callback
                    if self._callbacks[self.CB_TYPE.WAS_CLICKED]:
                        self._callbacks[self.CB_TYPE.WAS_CLICKED](True)
                self._last_click_time = current_time
            else:
                # hold event
                self._hold = True
                if self._callbacks[self.CB_TYPE.WAS_HOLD]:
                    self._callbacks[self.CB_TYPE.WAS_HOLD](True)
            
            # release callback
            if self._callbacks[self.CB_TYPE.WAS_RELEASED]:
                self._callbacks[self.CB_TYPE.WAS_RELEASED](True)
        
        # reset state (at the end of each update)
        if not is_pressed:
            self._clicked = False
            self._double_clicked = False
            self._hold = False
    
    def setCallback(self, type, cb):
        """set button callback function"""
        if type in self._callbacks:
            self._callbacks[type] = cb
    
    # status query method
    def isPressed(self):
        """current pressed state"""
        return self._pressed
    
    def isReleased(self):
        """current released state"""
        return self._released
    
    def isHolding(self):
        """current holding state"""
        return self._holding
    
    def wasClicked(self):
        """click event"""
        return self._clicked
    
    def wasDoubleClicked(self):
        """double click event"""
        return self._double_clicked
    
    def wasHold(self):
        """hold event"""
        return self._hold
    
    def wasPressed(self):
        """was pressed"""
        return self._pressed
    
    def wasReleased(self):
        """was released"""
        return self._released
    
    def wasSingleClicked(self):
        """click event (not double click)"""
        return self._clicked and not self._double_clicked

class TouchDriver:
    def __init__(self):
        self.device = None
        self.x = 0
        self.y = 0
        self.touch_down = False
        self._touch_callback = None
        self._touch_points = deque(maxlen=10)  # save 10 points
        self._touch_size = 0
        self._touch_id = 0
        self._current_button_index = -1  # current pressed button index
        
        # virtual button
        self.BtnA = Button()
        self.BtnB = Button()
        self.BtnC = Button()
        self._button_width = 320 // 3  # button width
    
    def init(self):
        try:
            # search touch device
            devices = [InputDevice(path) for path in list_devices()]
            for device in devices:
                # print(f"Found device: {device.path}, {device.name}, {device.phys}")
                self.device = device
                # set non-blocking mode
                os.set_blocking(self.device.fd, False)
                break
                
            if self.device:
                return True
        except Exception as e:
            print(f"Touch init error: {e}")
        return False
    
    def update(self):
        if not self.device:
            return
        
        try:
            events = []
            try:
                while True:
                    event = self.device.read_one()
                    if event is None:
                        break
                    events.append(event)
            except BlockingIOError:
                pass
            
            for event in events:
                if event.type == ecodes.EV_ABS:
                    if event.code == ecodes.ABS_X:
                        self.x = event.value
                    elif event.code == ecodes.ABS_Y:
                        self.y = event.value
                    elif event.code == ecodes.ABS_MT_TRACKING_ID:
                        if event.value == -1:  # touch end
                            self.touch_down = False
                        else:
                            self._touch_id = event.value
                    elif event.code == ecodes.ABS_MT_TOUCH_MAJOR:
                        self._touch_size = event.value
                        
                    if self.touch_down:
                        # add new touch point data
                        touch_data = (self.x, self.y, self._touch_size, self._touch_id)
                        self._touch_points.append(touch_data)
                        # update button state
                        self._update_buttons(self.x, self.y, True)
                        if self.y <= 240 and self._touch_callback:  # only trigger callback in non-button area
                            self._touch_callback(self.x, self.y, True)
                
                elif event.type == ecodes.EV_KEY:
                    if event.code == ecodes.BTN_TOUCH:
                        self.touch_down = event.value == 1
                        # update button state
                        self._update_buttons(self.x, self.y, self.touch_down)
                        if self.y <= 240 and self._touch_callback:  # only trigger callback in non-button area
                            self._touch_callback(self.x, self.y, self.touch_down)
        except Exception as e:
            print(f"Touch event loop error: {e}")
    
    def _update_buttons(self, x, y, is_pressed):
        # only process buttons when y > 240
        if y > 240:
            # determine which button based on x coordinate
            button_index = min(x // self._button_width, 2)
            
            # update current button state
            if is_pressed:
                self._current_button_index = button_index
            
            # update all button state
            buttons = [self.BtnA, self.BtnB, self.BtnC]
            for i, btn in enumerate(buttons):
                # only current pressed button will be set to pressed state
                is_button_pressed = is_pressed and i == button_index
                btn.update(is_button_pressed, i, self._current_button_index)
            
            # reset current button index when released
            if not is_pressed:
                self._current_button_index = -1
        else:
            # reset all button state when touch point is not in button area
            buttons = [self.BtnA, self.BtnB, self.BtnC]
            for i, btn in enumerate(buttons):
                btn.update(False, i, -1)
            self._current_button_index = -1
    
    def deinit(self):
        if self.device:
            self.device.close()
            self.device = None
    
    def set_callback(self, callback):
        """set touch callback: callback(x, y, is_pressed)"""
        self._touch_callback = callback 
        
    def getCount(self):
        """get count of touch points"""
        return len(self._touch_points)
    
    def getX(self):
        """get last touch x"""
        return self.x if self.touch_down else 0
    
    def getY(self):
        """get last touch y"""
        return self.y if self.touch_down else 0
    
    def getTouchPointRaw(self):
        """get last touch point data, return (x, y, size, id)"""
        if len(self._touch_points) > 0:
            return self._touch_points[-1]
        return (0, 0, 0, 0) 