import sdl2, keys, events


class Keys:
    def __init__(self):
        self.keysPressedNow = {}

    def initialize(self):
        events.handler(sdl2.SDL_KEYDOWN, self.onPress)
        events.handler(sdl2.SDL_KEYUP, self.onRelease)

    def isKeyPressed(self, key):
        return self.keysPressedNow.get(keys.getKeyCode(key), False)

    def onPress(self, event, world):
        self.keysPressedNow[event.key.keysym.scancode] = True

    def onRelease(self, event, world):
        self.keysPressedNow[event.key.keysym.scancode] = False


def onKeyPress(listenerFunction, key):
    key = keys.getKeyCode(key)
    if key is None:
        raise Exception("that is not a valid key")

    def key_press_handler(event, world):
        if event.key.keysym.scancode == key:
            listenerFunction(world)

    events.handler(sdl2.SDL_KEYDOWN, key_press_handler)


def onAnyKeyPress(listenerFunction):
    def any_key_press_handler(event, world):
        listenerFunction(world, event.key.keysym.scancode)

    events.handler(sdl2.SDL_KEYDOWN, any_key_press_handler)


def onKeyRelease(listenerFunction, key):
    key = keys.getKeyCode(key)
    if key is None:
        raise Exception("that is not a valid key")

    def key_release_handler(event, world):
        if event.key.keysym.scancode == key:
            listenerFunction(world)

    events.handler(sdl2.SDL_KEYUP, key_release_handler)


def onAnyKeyRelease(listenerFunction):
    def any_key_release_handler(event, world):
        listenerFunction(world, event.key.keysym.scancode)

    events.handler(sdl2.SDL_KEYUP, any_key_release_handler)
