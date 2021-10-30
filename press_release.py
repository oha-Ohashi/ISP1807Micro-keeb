
import board, digitalio, time
import keymap, key_object

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
#from adafruit_hid.keyboard import Keycode as kc
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import adafruit_ble

#keymap = keymap.keymap


class PressRelease():
    layer = 0
    keymap = keymap.keymap
    hold_list = []
    LT_list = []
    def __init__(self, hid):
        self.led = digitalio.DigitalInOut(board.LED)
        self.led.direction = digitalio.Direction.OUTPUT
        self.blink(3)

        self.k = Keyboard(hid.devices)
        self.kl = KeyboardLayoutUS(self.k)
        self.cc = ConsumerControl(hid.devices)

    def blink(self, count):
        for i in range(count):
            self.led.value = False
            time.sleep(0.3)
            self.led.value = True
            time.sleep(0.3)

    def action(self, key_number, pressed=True):
        code = self.keymap[self.layer][key_number]
        code_base = self.keymap[0][key_number]
        if pressed:
            self.led.value = False
            #print('layer:', layer)
            if type(code) == str:
               self.kl.write(code)
            elif type(code) == int:
                self.k.press(code)
            elif type(code) == list and type(code[0]) == int: # LCTL_T
                self.k.press(code[0])
                self.k.press(code[1])
            elif code.__class__.__name__ == 'VOL':
                code.press(self.cc)
            elif code.__class__.__name__ == 'MT':
                code.start()
                self.hold_list.append(code)
            elif code.__class__.__name__ == 'LT':
                self.layer = code.layer
                code.start()
                self.LT_list.append(code)
                #LT_list.append(code_base)
        else:
            self.led.value = True
            if type(code) == str:
                pass
            elif type(code) == int:
                self.k.release(code)
            elif type(code) == list and type(code[0]) == int: # LCTL_T
                self.k.release(code[1])
                self.k.release(code[0])
            elif code.__class__.__name__ == 'VOL':
                code.release(self.cc)
            elif code.__class__.__name__ == 'MT':
                code.release(self.k)
                if code in self.hold_list:
                    self.hold_list.remove(code)
            if code_base.__class__.__name__ == 'LT' and self.layer == code_base.layer:
                self.layer = 0
                code_base.release(self.k)
                #print(LT_list)
                if code_base in self.LT_list:
                    self.LT_list.remove(code_base)

    def listcheck(self):
        for h in self.hold_list:
            h.tick(self.k)
        for lt in self.LT_list:
            lt.tick(self.layer)
