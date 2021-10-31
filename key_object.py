import time

TAPPIG_TERM = 290
class MT():
    def __init__(self, modkc, kc):
        self.diff = 0
        self.modkc = modkc
        self.kc = kc
        self.executed = False

    def start(self):
        self.start_time = time.monotonic_ns() // 10**6

    def release(self, kbd):
        if not self.executed:
            kbd.press(self.kc)
            kbd.release(self.kc)
        else :
            kbd.release(self.modkc)
            self.executed = False

    def tick(self, kbd):
        self.diff = time.monotonic_ns() // 10**6 - self.start_time
        if not self.executed and self.diff > TAPPIG_TERM:
            kbd.press(self.modkc)
            self.executed = True
            print('MT executed')
        #print(self.diff)

class LT(MT):
    def __init__(self, layer, kc):
        self.diff = 0
        self.layer = layer
        self.kc = kc
        self.executed = False

    def release(self, kbd):
        if not self.executed:
            kbd.press(self.kc)
            kbd.release(self.kc)
        else :
            layer = 0
            self.executed = False

    def tick(self, layer):
        self.diff = time.monotonic_ns() // 10**6 - self.start_time
        if not self.executed and self.diff > TAPPIG_TERM:
            self.executed = True
            print('LT executed')
        #print(self.diff)

class VOL():
    def __init__(self, updown):
        if updown == 'UP':
            self.code = 0xE9
        else:
            self.code = 0xEA

    def press(self, cc):
        cc.press(self.code)
    def release(self, cc):
        cc.release()
