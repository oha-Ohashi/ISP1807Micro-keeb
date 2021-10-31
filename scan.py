import board
import time
import digitalio

class Scan:
    ROW_SLEEP = 0.000
    DEBOUNCE = 0.000
    INTERVAL = 0.000
    def __init__(self, row_pins=[], col_pins=[], row2col=True):
        self.row_pins = []
        self.col_pins = []
        self.row2col = row2col

        for p in row_pins:
            pin = digitalio.DigitalInOut(p)
            pin.direction = digitalio.Direction.INPUT if row2col else digitalio.Direction.OUTPUT
            if row2col :
                pin.pull = digitalio.Pull.UP
            else:
                pin.value = True
            self.row_pins.append(pin)

        for p in col_pins:
            pin = digitalio.DigitalInOut(p)
            pin.direction = digitalio.Direction.OUTPUT if row2col else digitalio.Direction.INPUT
            if row2col :
                pin.value = True
            else:
                pin.pull = digitalio.Pull.UP
            self.col_pins.append(pin)

        self.col_length = len(self.col_pins);
        self.row_length = len(self.row_pins);
        self.values = [True for _ in range(self.col_length * self.row_length)]

    rap = 0
    def scan(self, pr):
        if self.row2col:
            for i in range(self.col_length):
                col = self.col_pins[i]
                col.value = False
                time.sleep(self.ROW_SLEEP)
                print("col is low")
                for j in range(self.row_length):
                    row = self.row_pins[j]
                    l = self.col_length*j+i
                    if row.value != self.values[l]:
                        time.sleep(self.DEBOUNCE)
                        if not row.value:
                            #print('press')
                            pr.action(l, True)
                        else:
                            #print('release')
                            pr.action(l, False)
                    self.values[l] = row.value
                col.value = True

        else:
            for j in range(self.row_length):
                row = self.row_pins[j]
                row.value = False
                time.sleep(self.ROW_SLEEP)
                for i in range(self.col_length):
                    col = self.col_pins[i]
                    l = self.col_length*j+i
                    if col.value != self.values[l]:
                        time.sleep(self.DEBOUNCE)
                        if not col.value:
                            #print('press')
                            pr.action(l, True)
                        else:
                            #print('release')
                            pr.action(l, False)
                    self.values[l] = col.value
                row.value = True
        time.sleep(self.INTERVAL)
        if self.rap > 1000:
            print(time.monotonic_ns() // 10**6)
            self.rap = 0
        self.rap += 1
