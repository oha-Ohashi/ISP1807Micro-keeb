import board
import digitalio
import sys
import time
import keypad
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard import Keycode as kc
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
for i in range(5):
    led.value = False
    time.sleep(0.3)
    led.value = True
    time.sleep(0.3)
k = Keyboard(hid.devices)
kl = KeyboardLayoutUS(k)
km = keypad.KeyMatrix(
    row_pins=(board.D6, board.D5, board.D4),
    column_pins=(board.D9, board.D8, board.D7),
)
layer = 0
last_press = time.monotonic()
TAPPING_TERM = 0.2
keymap = [
    ['a','b',kc.BACKSPACE,
     'd','e','f',
     ['LT',1,kc.G], [kc.CONTROL,kc.H],[kc.SHIFT,kc.I]],
     ['x','y','z',
     'x','z','y',
     kc.G, kc.H,kc.I]
]
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
                last_press = time.monotonic()
                if type(code) == str:
                   kl.write(code)
                elif type(code) == int:
                    k.press(code)
                elif type(code[0]) == int: # MT
                    k.press(code[0])
                elif code[0] == 'LT':  # LT
                    layer = code[1]
            else:
                led.value = True
                span = time.monotonic() - last_press
                print(span)
                if type(code) == int:
                    k.release(code)
                elif type(code[0]) == int: # MT
                    k.release(code[0])
                    if span < TAPPING_TERM:
                        k.press(code[1])
                        k.release(code[1])
                if type(code_base) == list and code_base[0] == 'LT': # LT
                    layer = 0
                    if span < TAPPING_TERM:
                        k.press(code_base[2])
                        k.release(code_base[2])
    ble.start_advertising(advertisement)

