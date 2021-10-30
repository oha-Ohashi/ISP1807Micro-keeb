import board
import digitalio
import sys
import time
import keypad
import keymap, key_object
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.consumer_control import ConsumerControl
#from adafruit_hid.keyboard import Keycode as kc
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService

# Use default HID descriptor
hid = HIDService()
device_info = DeviceInfoService(
    software_revision=adafruit_ble.__version__, manufacturer="Adafruit Industries"
)
advertisement = ProvideServicesAdvertisement(hid)
advertisement.appearance = 961
scan_response = Advertisement()

ble = adafruit_ble.BLERadio()
if ble.connected:
    for c in ble.connections:
        c.disconnect()

print("advertising")
ble.start_advertising(advertisement, scan_response)

print(dir(board))
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
for i in range(1):
    led.value = False
    time.sleep(0.3)
    led.value = True
    time.sleep(0.3)

k = Keyboard(hid.devices)
cc = ConsumerControl(hid.devices)
kl = KeyboardLayoutUS(k)
km = keypad.KeyMatrix(
    column_pins=(board.D8,board.D7,board.D6,board.D5,board.D4, board.MOSI,board.MISO,board.SCK,board.AIN0,board.AIN1),
    row_pins=(board.AIN3,board.AIN2, board.D2, board.D3),
)
layer = 0
keymap = keymap.keymap
hold_list = []
LT_list = []
while True:
    while not ble.connected:
        pass
    print("Start typing:")
    while ble.connected:
        event = km.events.get()
        if event:
            code = keymap[layer][event.key_number]
            code_base = keymap[0][event.key_number]
            if event.pressed:
                led.value = False
                #print('layer:', layer)
                if type(code) == str:
                   kl.write(code)
                elif type(code) == int:
                    k.press(code)
                elif type(code) == list and type(code[0]) == int: # LCTL_T
                    k.press(code[0])
                    k.press(code[1])
                elif code.__class__.__name__ == 'VOL':
                    code.press(cc)
                elif code.__class__.__name__ == 'MT':
                    code.start()
                    hold_list.append(code)
                elif code.__class__.__name__ == 'LT':
                    layer = code.layer
                    code.start()
                    LT_list.append(code)
                    #LT_list.append(code_base)
            else:
                led.value = True
                if type(code) == str:
                    pass
                elif type(code) == int:
                    k.release(code)
                elif type(code) == list and type(code[0]) == int: # LCTL_T
                    k.release(code[1])
                    k.release(code[0])
                elif code.__class__.__name__ == 'VOL':
                    code.release(cc)
                elif code.__class__.__name__ == 'MT':
                    code.release(k)
                    hold_list.remove(code)
                if code_base.__class__.__name__ == 'LT' and layer == code_base.layer:
                    layer = 0
                    code_base.release(k)
                    #print(LT_list)
                    if code_base in LT_list:
                        LT_list.remove(code_base)


        for h in hold_list:
            h.tick(k)
        for lt in LT_list:
            lt.tick(layer)
        #time.sleep(0.01)
    ble.start_advertising(advertisement)
