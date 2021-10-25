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
    column_pins=(board.D8,board.D7,board.D6,board.D5,board.D4, board.MOSI,board.MISO,board.SCK,board.AIN0,board.AIN1),
    row_pins=(board.AIN3,board.AIN2, board.D2, board.D3),
)
layer = 0
last_press = time.monotonic()
TAPPING_TERM = 0.2
keymap = [
    [
        ['LT',5,kc.TAB],kc.W,kc.B,kc.F,kc.BACKSPACE,  kc.M,kc.R,['LT',5,kc.D],kc.Y,kc.P,
        kc.A,kc.O,kc.E,kc.U,kc.I,  kc.G,kc.T,kc.K,kc.N,kc.S,
        ['MT',kc.CONTROL,kc.Z],['MT',kc.SHIFT,kc.X],['MT',kc.ALT,kc.C],kc.V,['LT',2,kc.TAB],  ['MT',kc.CONTROL,kc.ESCAPE],kc.H,kc.J,kc.L,['MT',kc.GUI,kc.Q],
        '_','_','_',['MT',kc.SHIFT,kc.F15],['LT',1,kc.SPACE],  ['LT',3,kc.ENTER],['LT',4,kc.F16],'_','_','_'
    ],
    [
        '!','@','#','$','%',  '^','+','-','*','/',
        '1','2','3','4','5',  '6','7','8','9','0',
        ' ',' ',' ',' ',' ',  ' ','.',',',' ',' ',
        ' ',' ',' ',' ',' ',  ' ',' ',' ',' ',' '
    ],
    [
        ' ',' ',' ',' ',' ',  ' ','.',',',' ',' ',
        kc.F1,kc.F2,kc.F3,kc.F4,kc.F5,  kc.F6,kc.F7,kc.F8,kc.F9,kc.F10,
        kc.F11,kc.F12,' ',' ',' ',      ' ',' ',' ',' ',' ',
        ' ',' ',' ',' ',' ',  ' ',' ',' ',' ',' '
    ],
    [
        ' ',' ','"','\'','`',  [kc.CONTROL,kc.W],' ',' ',' ',' ',
        ':','=','_','-','~',  [kc.CONTROL,kc.T],[kc.ALT,kc.HOME],[kc.ALT,kc.LEFT_ARROW],[kc.ALT,kc.RIGHT_ARROW],'V',
        ';',' ',' ',' ',' ',  ' ','.',',',' ','V',
        ' ',' ',' ',' ',' ',  ' ',' ',' ',' ',' '
    ],
    [
        '!','?','&','|','\\',  ' ',' ',' ',' ',' ',
        '(',')','[',']',' ',  ' ',' ',' ',' ',' ',
        '{','}','<','>',' ',  ' ','.',',',' ',' ',
        ' ',' ',' ',' ',' ',  ' ',' ',' ',' ',' '
    ],
    [
        ' ',kc.BACKSPACE,kc.UP_ARROW,kc.DELETE,kc.ENTER,            ' ',' ',' ',' ',' ',
        kc.HOME,kc.LEFT_ARROW,kc.DOWN_ARROW,kc.RIGHT_ARROW,kc.END,  ' ',' ',' ',' ',' ',
        ' ',' ',kc.PAGE_DOWN,kc.PAGE_UP,' ',  ' ','.',',',' ',' ',
        ' ',' ',' ',' ',' ',  ' ',' ',' ',' ',' '
    ]
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
                elif type(code[0]) == int: # LCTL_T
                    k.press(code[0])
                    k.press(code[1])
                elif code[0] == 'MT':  #MT
                    k.press(code[1])
                elif code[0] == 'LT':  # LT
                    layer = code[1]
            else:
                led.value = True
                span = time.monotonic() - last_press
                print(span)
                if type(code) == int:
                    k.release(code)
                elif type(code[0]) == int: # LCTL_T
                    k.release(code[1])
                    k.release(code[0])
                elif code[0] == 'MT':  # MT
                    k.release(code[1])
                    if span < TAPPING_TERM:
                        k.press(code[2])
                        k.release(code[2])
                if type(code_base) == list and code_base[0] == 'LT': # LT
                    layer = 0
                    if span < TAPPING_TERM:
                        k.press(code_base[2])
                        k.release(code_base[2])
    ble.start_advertising(advertisement)

