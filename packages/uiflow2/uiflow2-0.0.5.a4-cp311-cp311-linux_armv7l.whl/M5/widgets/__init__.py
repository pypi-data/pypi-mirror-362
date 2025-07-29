# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5
import time


def fillScreen(color):
    stash_color = M5.Lcd.getRawColor()
    M5.Lcd.setColor(color)
    M5.Lcd.fillScreen()
    M5.Lcd.setRawColor(stash_color)

def setRotation(r):
    M5.Lcd.setRotation(r)

def setBrightness(brightness):
    M5.Lcd.setBrightness(brightness)


def restart_draw(func):
    def wrapper(self, *args, **kwargs):
        if hasattr(self, 'compare_helper') and self.compare_helper(func.__name__, *args, **kwargs):
            return func(self, *args, **kwargs)
        
        self.erase_helper()
        result = func(self, *args, **kwargs)
        self.draw_helper()
        return result
    return wrapper


class FONTS:
    DejaVu9   = M5.m5gfxpy.DejaVu9   
    DejaVu12  = M5.m5gfxpy.DejaVu12  
    DejaVu18  = M5.m5gfxpy.DejaVu18  
    DejaVu24  = M5.m5gfxpy.DejaVu24  
    DejaVu40  = M5.m5gfxpy.DejaVu40  
    DejaVu56  = M5.m5gfxpy.DejaVu56  
    DejaVu72  = M5.m5gfxpy.DejaVu72  
    EFontCN14 = M5.m5gfxpy.efontCN_14
    EFontCN24 = M5.m5gfxpy.efontCN_24
    EFontJA14 = M5.m5gfxpy.efontJA_14
    EFontJA24 = M5.m5gfxpy.efontJA_24
    EFontKR14 = M5.m5gfxpy.efontKR_14
    EFontKR24 = M5.m5gfxpy.efontKR_24



class Label:
    LEFT_ALIGNED = 0
    CENTER_ALIGNED = 1 
    RIGHT_ALIGNED = 2
    
    TOP_ALIGNED = 0
    MIDDLE_ALIGNED = 1
    BOTTOM_ALIGNED = 2
    
    def __init__(self, text, x, y, text_sz, text_c, bg_c, font, w=None, h=None, font_align=LEFT_ALIGNED, v_align=TOP_ALIGNED, auto_wrap=True):
        self._text = text
        self._x = x
        self._y = y
        self._text_sz = text_sz
        self._text_c = text_c
        self._bg_c = bg_c
        self._font = font
        self._width = w
        self._height = h
        self._align = font_align
        self._v_align = v_align
        self._auto_wrap = auto_wrap
        self.draw_helper()

    def draw_helper(self):
        stash_style = M5.Lcd.getTextStyle()
        M5.Lcd.setTextColor(self._text_c, self._bg_c)
        M5.Lcd.setTextSize(self._text_sz)

        # if width and height are specified, fill the background first
        if self._width is not None and self._height is not None:
            self._fill_background()
        
        # handle text display
        if self._auto_wrap and self._width is not None:
            self._draw_wrapped_text()
        else:
            self._draw_single_line_text()
            
        M5.Lcd.setTextStyle(stash_style)
    
    def _fill_background(self):
        if self._width is not None and self._height is not None:
            stash_color = M5.Lcd.getRawColor()
            M5.Lcd.setColor(self._bg_c)
            M5.Lcd.fillRect(self._x, self._y, self._width, self._height)
            M5.Lcd.setRawColor(stash_color)
    
    def _draw_single_line_text(self):
        text_to_draw = self._text
        
        if self._width is not None:
            text_width = M5.Lcd.textWidth(text_to_draw, self._font)
            if text_width > self._width:
                text_to_draw = self._truncate_text(text_to_draw)
        
        text_width = M5.Lcd.textWidth(text_to_draw, self._font)
        if self._width is not None:
            if self._align == self.CENTER_ALIGNED:
                x = self._x + (self._width - text_width) // 2
            elif self._align == self.RIGHT_ALIGNED:
                x = self._x + self._width - text_width
            else:
                x = self._x
        else:
            x = self._x
        
        font_height = M5.Lcd.fontHeight(self._font)
        if self._height is not None:
            if self._v_align == self.MIDDLE_ALIGNED:
                y = self._y + (self._height - font_height) // 2
            elif self._v_align == self.BOTTOM_ALIGNED:
                y = self._y + self._height - font_height
            else:
                y = self._y
        else:
            y = self._y
        
        M5.Lcd.drawString(text_to_draw, x, y, self._font)
    
    def _draw_wrapped_text(self):
        if not self._width:
            self._draw_single_line_text()
            return
            
        lines = []
        current_line = ""
        
        for char in self._text:
            test_line = current_line + char
            if M5.Lcd.textWidth(test_line, self._font) <= self._width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = char
                else:
                    lines.append(char)
                    current_line = ""
        
        if current_line:
            lines.append(current_line)
        
        font_height = M5.Lcd.fontHeight(self._font)
        if self._height is not None:
            max_lines = self._height // font_height
            lines = lines[:max_lines]
        
        total_text_height = len(lines) * font_height
        if self._height is not None and len(lines) > 0:
            if self._v_align == self.MIDDLE_ALIGNED:
                start_y = self._y + (self._height - total_text_height) // 2
            elif self._v_align == self.BOTTOM_ALIGNED:
                start_y = self._y + self._height - total_text_height
            else:
                start_y = self._y
        else:
            start_y = self._y
        
        for i, line in enumerate(lines):
            y = start_y + i * font_height
            
            text_width = M5.Lcd.textWidth(line, self._font)
            if self._align == self.CENTER_ALIGNED:
                x = self._x + (self._width - text_width) // 2
            elif self._align == self.RIGHT_ALIGNED:
                x = self._x + self._width - text_width
            else:
                x = self._x
            
            M5.Lcd.drawString(line, x, y, self._font)
    
    def _truncate_text(self, text):
        if not self._width:
            return text
            
        ellipsis = "..."
        ellipsis_width = M5.Lcd.textWidth(ellipsis, self._font)
        
        if M5.Lcd.textWidth(text, self._font) <= self._width:
            return text
        
        left, right = 0, len(text)
        best_text = ""
        
        while left <= right:
            mid = (left + right) // 2
            test_text = text[:mid] + ellipsis
            
            if M5.Lcd.textWidth(test_text, self._font) <= self._width:
                best_text = test_text
                left = mid + 1
            else:
                right = mid - 1
        
        return best_text if best_text else ellipsis
    def erase_helper(self):
        stash_color = M5.Lcd.getRawColor()
        M5.Lcd.setColor(self._bg_c)
        
        if self._width is not None and self._height is not None:
            M5.Lcd.fillRect(self._x, self._y, self._width, self._height)
        else:
            if self._auto_wrap and self._width is not None:
                erase_width = self._width
                erase_height = self._calculate_wrapped_text_height()
            else:
                erase_width = self._width if self._width is not None else M5.Lcd.textWidth(self._text, self._font)
                erase_height = M5.Lcd.fontHeight(self._font)
            
            erase_x = self._x
            if self._height is not None:
                if self._v_align == self.MIDDLE_ALIGNED:
                    erase_y = self._y + (self._height - erase_height) // 2
                elif self._v_align == self.BOTTOM_ALIGNED:
                    erase_y = self._y + self._height - erase_height
                else:
                    erase_y = self._y
            else:
                erase_y = self._y
            
            M5.Lcd.fillRect(erase_x, erase_y, erase_width, erase_height)
        
        M5.Lcd.setRawColor(stash_color)
    
    def _calculate_wrapped_text_height(self):
        if not self._width:
            return M5.Lcd.fontHeight(self._font)
        
        lines = []
        current_line = ""
        
        for char in self._text:
            test_line = current_line + char
            if M5.Lcd.textWidth(test_line, self._font) <= self._width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = char
                else:
                    lines.append(char)
                    current_line = ""
        
        if current_line:
            lines.append(current_line)
        
        font_height = M5.Lcd.fontHeight(self._font)
        if self._height is not None:
            max_lines = self._height // font_height
            lines = lines[:max_lines]
        
        return len(lines) * font_height
    
    def compare_helper(self, func_name, *args, **kwargs):
        try:
            if func_name == 'setText':
                return self._text == args[0]
            elif func_name == 'setColor':
                return self._text_c == args[0] and self._bg_c == args[1]
            elif func_name == 'setCursor':
                return self._x == args[0] and self._y == args[1]
            elif func_name == 'setSize':
                return self._text_sz == args[0]
            elif func_name == 'setFont':
                return self._font == args[0]
            elif func_name == 'setAlign':
                return self._align == args[0]
            elif func_name == 'setVerticalAlign':
                return self._v_align == args[0]
            elif func_name == 'setAutoWrap':
                return self._auto_wrap == args[0]
            elif func_name == 'setAreaSize':
                return self._width == args[0] and self._height == args[1]
            return False
        except (IndexError, TypeError):
            return False
    
    @restart_draw
    def setText(self, text):
        self._text = text

    @restart_draw
    def setColor(self, text_c, bg_c):
        self._text_c = text_c
        self._bg_c = bg_c
    
    @restart_draw
    def setCursor(self, x, y):
        self._x = x
        self._y = y
    
    @restart_draw
    def setSize(self, text_sz):
        self._text_sz = text_sz

    @restart_draw
    def setFont(self, font):
        self._font = font

    @restart_draw
    def setAlign(self, align):
        self._align = align

    @restart_draw
    def setVerticalAlign(self, v_align):
        self._v_align = v_align
    
    @restart_draw
    def setAutoWrap(self, auto_wrap):
        self._auto_wrap = auto_wrap
    
    @restart_draw
    def setAreaSize(self, w, h):
        self._width = w
        self._height = h

    def setVisible(self, visible):
        # self.stash_style = M5.Lcd.getTextStyle()
        if visible:
            self.draw_helper()
        else:
            self.erase_helper()
        # M5.Lcd.setTextStyle(self.stash_style)


class Title:
    def __init__(self, text, text_x, text_c, bg_c, font):
        self._text = text
        self._fg_color = text_c
        self._bg_color = bg_c
        self._font = font
        self._size_w = M5.Lcd.width()
        self._size_h = M5.Lcd.fontHeight(self._font)
        self._text_pos_x0 = text_x
        self.text_pos_y0 = 0
        self._text_size = 1.0
        self.draw_helper()

    def draw_helper(self):
        stash_style = M5.Lcd.getTextStyle()
        self.erase_helper()
        M5.Lcd.setTextColor(self._fg_color, self._bg_color)
        M5.Lcd.setTextSize(self._text_size)
        M5.Lcd.drawString(self._text, self._text_pos_x0, self.text_pos_y0, self._font)
        M5.Lcd.setTextStyle(stash_style)
    def erase_helper(self):
        stash_color = M5.Lcd.getRawColor()
        M5.Lcd.setColor(self._bg_color)
        M5.Lcd.fillRect(0, 0, self._size_w, self._size_h)
        M5.Lcd.setRawColor(stash_color)
    
    def compare_helper(self, func_name, *args, **kwargs):
        try:
            if func_name == 'setText':
                return self._text == args[0]
            elif func_name == 'setColor':
                return self._fg_color == args[0] and self._bg_color == args[1]
            elif func_name == 'setSize':
                return self._size_h == args[0]
            elif func_name == 'setTextCursor':
                return self._text_pos_x0 == args[0]
            return False
        except (IndexError, TypeError):
            return False
    
    @restart_draw
    def setText(self, text):
        self._text = text

    @restart_draw
    def setColor(self, text_c, bg_c):
        self._fg_color = text_c
        self._bg_color = bg_c

    @restart_draw
    def setSize(self, h):
        self._size_h = h

    @restart_draw
    def setTextCursor(self, text_x):
        self._text_pos_x0 = text_x

    def setVisible(self, visible):
        # self.stash_style = M5.Lcd.getTextStyle()
        if visible:
            self.draw_helper()
        else:
            self.erase_helper()
        # M5.Lcd.setTextStyle(self.stash_style)








class Image:
    def __init__(self, img, x, y, scale_x=1.0, scale_y=1.0):
        self._img_path = img
        self._pos_x0 = x
        self._pos_y0 = y
        self._scale_x = scale_x
        self._scale_y = scale_y
        self._size_w = 0
        self._size_h = 0
        # print(f"Image init with path: {self._img_path}, x: {self._pos_x0}, y: {self._pos_y0}, scale_x: {self._scale_x}, scale_y: {self._scale_y}")
        self.draw_helper()
    
    def draw_helper(self):
        try:
            # print(f"Drawing image from: {self._img_path}")
            M5.Lcd.drawFile(self._img_path, self._pos_x0, self._pos_y0, -1, -1, 0, 0, self._scale_x, self._scale_y)
        except Exception as e:
            print(f"Error drawing image: {e}")
    def erase_helper(self):
        M5.Lcd.fillRect(self._pos_x0, self._pos_y0, self._size_w, self._size_h)
    
    def compare_helper(self, func_name, *args, **kwargs):
        try:
            if func_name == 'setImage':
                return self._img_path == args[0]
            elif func_name == 'setPosition':
                return self._pos_x0 == args[0] and self._pos_y0 == args[1]
            elif func_name == 'setScale':
                return self._scale_x == args[0] and self._scale_y == args[1]
            elif func_name == 'setSize':
                return self._size_w == args[0] and self._size_h == args[1]
            return False
        except (IndexError, TypeError):
            return False
    
    @restart_draw
    def setImage(self, img):
        self._img_path = img
    
    @restart_draw
    def setPosition(self, x, y):
        self._pos_x0 = x
        self._pos_y0 = y
    
    @restart_draw
    def setScale(self, scale_x, scale_y):
        self._scale_x = scale_x
        self._scale_y = scale_y
    
    @restart_draw
    def setSize(self, w, h):
        self._size_w = w
        self._size_h = h
    
    def setVisible(self, visible):
        # self.stash_style = M5.Lcd.getTextStyle()
        if visible:
            self.draw_helper()
        else:
            self.erase_helper()
        # M5.Lcd.setTextStyle(self.stash_style)


class Line:
    def __init__(self, x0, y0, x1, y1, color):
        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1
        self._color = color
        self.draw_helper()
    def draw_helper(self):
        stash_color = M5.Lcd.getRawColor()
        M5.Lcd.setColor(self._color)
        M5.Lcd.drawLine(self._x0, self._y0, self._x1, self._y1)
        M5.Lcd.setRawColor(stash_color)
    def erase_helper(self):
        M5.Lcd.drawLine(self._x0, self._y0, self._x1, self._y1)
    
    def compare_helper(self, func_name, *args, **kwargs):
        try:
            if func_name == 'setColor':
                return self._color == args[0]
            elif func_name == 'setPoints':
                return (self._x0 == args[0] and self._y0 == args[1] and 
                        self._x1 == args[2] and self._y1 == args[3])
            return False
        except (IndexError, TypeError):
            return False
    
    @restart_draw
    def setColor(self, color):
        self._color = color
    
    @restart_draw
    def setPoints(self, x0, y0, x1, y1):
        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1
    
    def setVisible(self, visible):
        if visible:
            self.draw_helper()
        else:
            self.erase_helper()

class Circle:
    def __init__(self, x, y, r, color, fill_c):
        self._x = x
        self._y = y
        self._r = r
        self._color = color
        self._fill_c = fill_c
        self.draw_helper()
    def draw_helper(self):
        stash_color = M5.Lcd.getRawColor()
        M5.Lcd.setColor(self._fill_c)
        M5.Lcd.fillCircle(self._x, self._y, self._r)
        M5.Lcd.setColor(self._color)
        M5.Lcd.drawCircle(self._x, self._y, self._r)
        M5.Lcd.setRawColor(stash_color)
    def erase_helper(self):
        M5.Lcd.fillCircle(self._x, self._y, self._r)

    def compare_helper(self, func_name, *args, **kwargs):
        try:
            if func_name == 'setRadius':
                return self._r == args[0]
            elif func_name == 'setCursor':
                return self._x == args[0] and self._y == args[1]
            elif func_name == 'setColor':
                return self._color == args[0] and self._fill_c == args[1]
            return False
        except (IndexError, TypeError):
            return False

    @restart_draw
    def setRadius(self, r):
        self._r = r

    @restart_draw
    def setCursor(self, x, y):
        self._x = x
        self._y = y
    
    @restart_draw
    def setColor(self, color, fill_c):
        self._color = color
        self._fill_c = fill_c
    
    def setVisible(self, visible):
        if visible:
            self.draw_helper()
        else:
            self.erase_helper()





class Rectangle:
    def __init__(self, x, y, w, h, color, fill_c):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._color = color
        self._fill_c = fill_c
        self.draw_helper()
    def draw_helper(self):
        stash_color = M5.Lcd.getRawColor()
        M5.Lcd.setColor(self._fill_c)
        M5.Lcd.fillRect(self._x, self._y, self._w, self._h)
        M5.Lcd.setColor(self._color)
        M5.Lcd.drawRect(self._x, self._y, self._w, self._h)
        M5.Lcd.setRawColor(stash_color)
    def erase_helper(self):
        M5.Lcd.fillRect(self._x, self._y, self._w, self._h)
    
    def compare_helper(self, func_name, *args, **kwargs):
        try:
            if func_name == 'setSize':
                return self._w == args[0] and self._h == args[1]
            elif func_name == 'setColor':
                return self._color == args[0] and self._fill_c == args[1]
            elif func_name == 'setCursor':
                return self._x == args[0] and self._y == args[1]
            return False
        except (IndexError, TypeError):
            return False
    
    @restart_draw
    def setSize(self, w, h):
        self._w = w
        self._h = h

    @restart_draw
    def setColor(self, color, fill_c):
        self._color = color
        self._fill_c = fill_c
    
    @restart_draw
    def setCursor(self, x, y):
        self._x = x
        self._y = y

    def setVisible(self, visible):
        if visible:
            self.draw_helper()
        else:
            self.erase_helper()



class Button:
    def __init__(self, event=None, x=0, y=0, w=0, h=0, color=0, fill_c=0):
        self._event = event
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._color = color
        self._fill_c = fill_c
        self.draw_helper()
    def draw_helper(self):
        M5.Lcd.drawRect(self._x, self._y, self._w, self._h)
        M5.Lcd.setColor(self._color)
        M5.Lcd.fillRect(self._x, self._y, self._w, self._h)
    def erase_helper(self):
        M5.Lcd.fillRect(self._x, self._y, self._w, self._h)

    def compare_helper(self, func_name, *args, **kwargs):
        try:
            if func_name == 'setColor':
                return self._color == args[0] and self._fill_c == args[1]
            elif func_name == 'setEvent':
                return self._event == args[0]
            elif func_name == 'setPosition':
                return self._x == args[0] and self._y == args[1]
            elif func_name == 'setSize':
                return self._w == args[0] and self._h == args[1]
            return False
        except (IndexError, TypeError):
            return False

    @restart_draw
    def setColor(self, color, fill_c):
        self._color = color
        self._fill_c = fill_c
    
    @restart_draw
    def setEvent(self, event):
        self._event = event
    
    @restart_draw
    def setPosition(self, x, y):
        self._x = x
        self._y = y
    
    @restart_draw
    def setSize(self, w, h):
        self._w = w
        self._h = h


class Triangle:
    def __init__(self, x0, y0, x1, y1, x2, y2, color, fill_c):
        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._color = color
        self._fill_c = fill_c
        self.draw_helper()
    def draw_helper(self):
        stash_color = M5.Lcd.getRawColor()
        M5.Lcd.setColor(self._fill_c)
        M5.Lcd.fillTriangle(self._x0, self._y0, self._x1, self._y1, self._x2, self._y2)
        M5.Lcd.setColor(self._color)
        M5.Lcd.drawTriangle(self._x0, self._y0, self._x1, self._y1, self._x2, self._y2)
        M5.Lcd.setRawColor(stash_color)
    def erase_helper(self):
        M5.Lcd.fillTriangle(self._x0, self._y0, self._x1, self._y1, self._x2, self._y2)
    
    def compare_helper(self, func_name, *args, **kwargs):
        try:
            if func_name == 'setColor':
                return self._color == args[0] and self._fill_c == args[1]
            elif func_name == 'setPoints':
                return (self._x0 == args[0] and self._y0 == args[1] and 
                        self._x1 == args[2] and self._y1 == args[3] and 
                        self._x2 == args[4] and self._y2 == args[5])
            return False
        except (IndexError, TypeError):
            return False
    
    @restart_draw
    def setColor(self, color, fill_c):
        self._color = color
        self._fill_c = fill_c
    
    @restart_draw
    def setPoints(self, x0, y0, x1, y1, x2, y2):
        self._x0 = x0
        self._y0 = y0
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

    def setVisible(self, visible):
        if visible:
            self.draw_helper()
        else:
            self.erase_helper()






class Qrcode:
    def __init__(self, text, x, y, w, version):
        self._text = text
        self._x = x
        self._y = y
        self._w = w
        self._version = version
        self.draw_helper()
    def draw_helper(self):
        M5.Lcd.qrcode(self._text, self._x, self._y, self._w, self._version)
    def erase_helper(self):
        M5.Lcd.fillRect(self._x, self._y, self._w, self._w)
    
    def compare_helper(self, func_name, *args, **kwargs):
        try:
            if func_name == 'setText':
                return self._text == args[0]
            elif func_name == 'setSize':
                return self._w == args[0]
            elif func_name == 'setVersion':
                return self._version == args[0]
            elif func_name == 'setCursor':
                return self._x == args[0] and self._y == args[1]
            return False
        except (IndexError, TypeError):
            return False
    
    @restart_draw
    def setText(self, text):
        self._text = text

    @restart_draw
    def setSize(self, w):
        self._w = w
    
    @restart_draw
    def setVersion(self, version):
        self._version = version
    
    @restart_draw
    def setCursor(self, x, y):
        self._x = x
        self._y = y

    def setVisible(self, visible):
        if visible:
            self.draw_helper()
        else:
            self.erase_helper()











































































