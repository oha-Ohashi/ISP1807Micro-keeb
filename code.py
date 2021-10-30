import board
import digitalio
import sys
import time
import keymap, key_object
import scan
import press_release

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


col_pins = [board.D8,board.D7,board.D6,board.D5,board.D4, board.MOSI,board.MISO,board.SCK,board.AIN0,board.AIN1]
row_pins = [board.AIN3,board.AIN2, board.D2, board.D3]
km = scan.Scan(row_pins, col_pins, row2col=False)
pr = press_release.PressRelease(hid)



while True:
    while not ble.connected:
        pass
    print("Start typing:")
    pr.blink(3)
    while ble.connected:
        km.scan(pr)
        pr.listcheck()

    ble.start_advertising(advertisement)



