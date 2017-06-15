import sdl2

keyList = [
    (sdl2.SDL_SCANCODE_UP, ['up', 'up arrow']),
    (sdl2.SDL_SCANCODE_DOWN, ['down', 'down arrow']),
    (sdl2.SDL_SCANCODE_RIGHT, ['right', 'right arrow']),
    (sdl2.SDL_SCANCODE_LEFT, ['left', 'left arrow']),
    (sdl2.SDL_SCANCODE_BACKSPACE, ['backspace']),
    (sdl2.SDL_SCANCODE_SPACE, ['space', ' ']),
    (sdl2.SDL_SCANCODE_RETURN, ['enter', 'return']),
    (sdl2.SDL_SCANCODE_TAB, ['tab']),

    (sdl2.SDL_SCANCODE_A, ['a']),
    (sdl2.SDL_SCANCODE_B, ['b']),
    (sdl2.SDL_SCANCODE_C, ['c']),
    (sdl2.SDL_SCANCODE_D, ['d']),
    (sdl2.SDL_SCANCODE_E, ['e']),
    (sdl2.SDL_SCANCODE_F, ['f']),
    (sdl2.SDL_SCANCODE_G, ['g']),
    (sdl2.SDL_SCANCODE_H, ['h']),
    (sdl2.SDL_SCANCODE_I, ['i']),
    (sdl2.SDL_SCANCODE_J, ['j']),
    (sdl2.SDL_SCANCODE_K, ['k']),
    (sdl2.SDL_SCANCODE_L, ['l']),
    (sdl2.SDL_SCANCODE_M, ['m']),
    (sdl2.SDL_SCANCODE_N, ['n']),
    (sdl2.SDL_SCANCODE_O, ['o']),
    (sdl2.SDL_SCANCODE_P, ['p']),
    (sdl2.SDL_SCANCODE_Q, ['q']),
    (sdl2.SDL_SCANCODE_R, ['r']),
    (sdl2.SDL_SCANCODE_S, ['s']),
    (sdl2.SDL_SCANCODE_T, ['t']),
    (sdl2.SDL_SCANCODE_U, ['u']),
    (sdl2.SDL_SCANCODE_V, ['v']),
    (sdl2.SDL_SCANCODE_W, ['w']),
    (sdl2.SDL_SCANCODE_X, ['x']),
    (sdl2.SDL_SCANCODE_Y, ['y']),
    (sdl2.SDL_SCANCODE_Z, ['z']),
    (sdl2.SDL_SCANCODE_0, ['0']),
    (sdl2.SDL_SCANCODE_1, ['1']),
    (sdl2.SDL_SCANCODE_2, ['2']),
    (sdl2.SDL_SCANCODE_3, ['3']),
    (sdl2.SDL_SCANCODE_4, ['4']),
    (sdl2.SDL_SCANCODE_5, ['5']),
    (sdl2.SDL_SCANCODE_6, ['6']),
    (sdl2.SDL_SCANCODE_7, ['7']),
    (sdl2.SDL_SCANCODE_8, ['8']),
    (sdl2.SDL_SCANCODE_9, ['9']),

    (sdl2.SDL_SCANCODE_GRAVE, ['`', 'backquote', 'grave', 'grave accent']),
    (sdl2.SDL_SCANCODE_MINUS, ['-', 'minus', 'dash', 'hyphen']),
    (sdl2.SDL_SCANCODE_EQUALS, ['=', 'equals']),
    (sdl2.SDL_SCANCODE_LEFTBRACKET, ['[', 'left bracket']),
    (sdl2.SDL_SCANCODE_RIGHTBRACKET, [']', 'right bracket']),
    (sdl2.SDL_SCANCODE_BACKSLASH, ['backslash', '\\']),
    (sdl2.SDL_SCANCODE_SEMICOLON, [';', 'semicolon']),
    (sdl2.SDL_SCANCODE_APOSTROPHE, ['quote', '\'']),
    (sdl2.SDL_SCANCODE_COMMA, [',', 'comma']),
    (sdl2.SDL_SCANCODE_PERIOD, ['.', 'period']),
    (sdl2.SDL_SCANCODE_SLASH, ['/', 'slash', 'divide']),

    (sdl2.SDL_SCANCODE_DELETE, ['delete']),
    (sdl2.SDL_SCANCODE_INSERT, ['insert']),
    (sdl2.SDL_SCANCODE_HOME, ['home']),
    (sdl2.SDL_SCANCODE_END, ['end']),
    (sdl2.SDL_SCANCODE_PAGEUP, ['page up']),
    (sdl2.SDL_SCANCODE_PAGEDOWN, ['page down']),
    (sdl2.SDL_SCANCODE_CLEAR, ['clear']),
    (sdl2.SDL_SCANCODE_PAUSE, ['pause']),

    (sdl2.SDL_SCANCODE_F1, ['F1']),
    (sdl2.SDL_SCANCODE_F2, ['F2']),
    (sdl2.SDL_SCANCODE_F3, ['F3']),
    (sdl2.SDL_SCANCODE_F4, ['F4']),
    (sdl2.SDL_SCANCODE_F5, ['F5']),
    (sdl2.SDL_SCANCODE_F6, ['F6']),
    (sdl2.SDL_SCANCODE_F7, ['F7']),
    (sdl2.SDL_SCANCODE_F8, ['F8']),
    (sdl2.SDL_SCANCODE_F9, ['F9']),
    (sdl2.SDL_SCANCODE_F10, ['F10']),
    (sdl2.SDL_SCANCODE_F11, ['F11']),
    (sdl2.SDL_SCANCODE_F12, ['F12']),
    (sdl2.SDL_SCANCODE_F13, ['F13']),
    (sdl2.SDL_SCANCODE_F14, ['F14']),
    (sdl2.SDL_SCANCODE_F15, ['F15']),

    (sdl2.SDL_SCANCODE_RSHIFT, ['right shift']),
    (sdl2.SDL_SCANCODE_LSHIFT, ['left shift']),
    (sdl2.SDL_SCANCODE_RCTRL, ['right ctrl']),
    (sdl2.SDL_SCANCODE_LCTRL, ['left ctrl']),
    (sdl2.SDL_SCANCODE_RALT, ['right alt', 'right option']),
    (sdl2.SDL_SCANCODE_LALT, ['left alt', 'left option']),
    (sdl2.SDL_SCANCODE_RGUI, ['right command', 'right windows']),  # apparently GUI <- META & SUPER?
    (sdl2.SDL_SCANCODE_LGUI, ['left command', 'left windows']),

    (sdl2.SDL_SCANCODE_NUMLOCKCLEAR, ['numlock']),
    (sdl2.SDL_SCANCODE_CAPSLOCK, ['capslock']),
    (sdl2.SDL_SCANCODE_SCROLLLOCK, ['scrollock']),
    (sdl2.SDL_SCANCODE_MODE, ['mode']),
    (sdl2.SDL_SCANCODE_HELP, ['help']),
    (sdl2.SDL_SCANCODE_PRINTSCREEN, ['print', 'print screen', 'prtsc']),
    (sdl2.SDL_SCANCODE_SYSREQ, ['sysrq']),
    (sdl2.SDL_SCANCODE_PAUSE, ['break']),
    (sdl2.SDL_SCANCODE_MENU, ['menu']),
    (sdl2.SDL_SCANCODE_POWER, ['power']),
    (sdl2.SDL_SCANCODE_CURRENCYUNIT, ['euro']),  # I'm not sure if this is correct but it's what pygame_sdl2 does

    (sdl2.SDL_SCANCODE_KP_0, ['keypad 0']),
    (sdl2.SDL_SCANCODE_KP_1, ['keypad 1']),
    (sdl2.SDL_SCANCODE_KP_2, ['keypad 2']),
    (sdl2.SDL_SCANCODE_KP_3, ['keypad 3']),
    (sdl2.SDL_SCANCODE_KP_4, ['keypad 4']),
    (sdl2.SDL_SCANCODE_KP_5, ['keypad 5']),
    (sdl2.SDL_SCANCODE_KP_6, ['keypad 6']),
    (sdl2.SDL_SCANCODE_KP_7, ['keypad 7']),
    (sdl2.SDL_SCANCODE_KP_8, ['keypad 8']),
    (sdl2.SDL_SCANCODE_KP_9, ['keypad 9']),
    (sdl2.SDL_SCANCODE_KP_PERIOD, ['keypad period']),
    (sdl2.SDL_SCANCODE_KP_DIVIDE, ['keypad divide']),
    (sdl2.SDL_SCANCODE_KP_MULTIPLY, ['keypad multiply']),
    (sdl2.SDL_SCANCODE_KP_MINUS, ['keypad minus']),
    (sdl2.SDL_SCANCODE_KP_PLUS, ['keypad plus']),
    (sdl2.SDL_SCANCODE_KP_EQUALS, ['keypad equals']),
    (sdl2.SDL_SCANCODE_KP_ENTER, ['keypad enter'])
]

key2nameDict = {}
name2keyDict = {}
for code, nameList in keyList:
    key2nameDict[code] = nameList[0].lower()
    for name in nameList:
        name2keyDict[name.lower()] = code


def getKeyName(key):
    return key2nameDict.get(key, None)


def getKeyCode(key):
    if key is None:
        return None
    if key in key2nameDict:
        return key
    return name2keyDict.get(key.lower(), None)


def sameKeys(key1, key2):
    code1 = getKeyCode(key1)
    code2 = getKeyCode(key2)
    if code1 is None:
        raise Exception("unknown key name: " + key1)
    if code2 is None:
        raise Exception("unknown key name: " + key2)
    return code1 == code2


if __name__ == "__main__":
    with open("keys.html", "w") as web:
        web.write('<html><head><title>Python Keys</title></head>\n<body><center>\n<h1>Key Names</h1>\n<table>\n')
        for code, nameList in keyList:
            web.write('<tr>')
            for name in nameList:
                web.write('<td>' + name + '</td>')
            web.write('</tr>')
        web.write('</table></center></body></html>')
