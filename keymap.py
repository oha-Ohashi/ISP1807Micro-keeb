from key_object import MT, LT, VOL
from adafruit_hid.keyboard import Keycode as kc
keymap = [
    [
        LT(5,kc.TAB),kc.W,kc.B,kc.F,MT(kc.GUI,kc.BACKSPACE),  kc.M,kc.R,LT(5,kc.D),kc.Y,kc.P,
        kc.A,kc.O,kc.E,kc.U,kc.I,  kc.G,kc.T,kc.K,kc.N,kc.S,
        MT(kc.CONTROL,kc.Z),MT(kc.SHIFT,kc.X),MT(kc.ALT,kc.C),kc.V,LT(2,kc.TAB),  MT(kc.CONTROL,kc.ESCAPE),kc.H,kc.J,kc.L,MT(kc.GUI,kc.Q),
        '_','_','_',MT(kc.SHIFT,kc.F15),LT(1,kc.SPACE),  LT(3,kc.ENTER),LT(4,kc.F16),'_','_','_'
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
        ':','=','_','-','~',  [kc.CONTROL,kc.T],[kc.ALT,kc.HOME],[kc.ALT,kc.LEFT_ARROW],[kc.ALT,kc.RIGHT_ARROW],VOL('UP'),
        ';',' ',' ',' ',' ',  ' ','.',',',' ',VOL('DOWN'),
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
]# ここにコードを書いてね :-)
