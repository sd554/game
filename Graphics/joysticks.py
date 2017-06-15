import sdl2, events

joystickLabels = {
    "Logitech Dual Action": [["X", "Y"], ["LeftX", "LeftY", "RightX", "RightY"]],
    "Logitech RumblePad 2 USB": [["X", "Y"], ["LeftX", "LeftY", "RightX", "RightY"]],
    "Logitech Cordless RumblePad 2": [["X", "Y"], ["LeftX", "LeftY", "RightX", "RightY"]],
    "Logitech Attack 3": [["X", "Y", "Throttle"]],

    "Logitech Logitech Dual Action": [["X", "Y"], ["LeftX", "LeftY", "RightX", "RightY"]],
    "Logitech Logitech RumblePad 2 USB": [["X", "Y"], ["LeftX", "LeftY", "RightX", "RightY"]],
    "Logitech Logitech Cordless RumblePad 2": [["X", "Y"], ["LeftX", "LeftY", "RightX", "RightY"]],
    "Logitech Logitech Attack 3": [["X", "Y", "Throttle"]],

    "Controller (Gamepad F310)": [["X", "Y"], ["LeftX", "LeftY", "Trigger", "RightY", "RightX"]],
    "Controller (Wireless Gamepad F710)": [["X", "Y"], ["LeftX", "LeftY", "Trigger", "RightY", "RightX"]],

    "Saitek Aviator Stick": [["X", "Y", "LeftThrottle", "Twist", "RightThrottle"]],
    "Saitek AV8R Joystick": [["X", "Y", "Twist", "LeftThrottle", "RightThrottle"]],
    "Saitek Pro Flight Throttle Quadrant": [["LeftThrottle", "CenterThrottle", "RightThrottle"]],

    "XBOX 360 For Windows (Controller)": [["X", "Y"], ["LeftX", "LeftY", "Trigger", "RightY", "RightX"]]
}

joystickLabelsUnknown = [["X", "Y"]]


class JoysticksInfo:
    def __init__(self):
        self.joysticks = []
        self.joystickLabels = []
        self.joystickDeadZone = 0.05

    def initialize(self):
        joystick_count = sdl2.SDL_NumJoysticks()
        if joystick_count < 0:
            print("failed to init Joysticks: %s" % sdl2.SDL_GetError())
            return
        for i in range(joystick_count):
            joystick = sdl2.SDL_JoystickOpen(i)
            assert joystick is not None, "failed to init Joystick %d: %s" % (i, sdl2.SDL_GetError())
            self.joysticks.append(joystick)
            self.joystickLabels.append({})
            stickname = sdl2.SDL_JoystickName(joystick)
            assert stickname is not None, "failed to find name of Joystick %d: %s" % (i, sdl2.SDL_GetError())
            if stickname in joystickLabels:
                print("recognized a", stickname)
                label_list = joystickLabels[stickname]
            else:
                print("unknown game controller:", stickname)
                label_list = joystickLabelsUnknown
            for labels in label_list:
                self.setAxisNames(labels, i)
            print("    with axes:", self.getAxisNames(i))

    def setDeadzone(self, deadzone):
        self.joystickDeadZone = deadzone

    def getJoystickCount(self):
        return len(self.joysticks)

    def getAxisCount(self, device=0):
        if 0 <= device < len(self.joysticks):
            return sdl2.SDL_JoystickNumAxes(self.joysticks[device])
        else:
            return 0

    def getDPadCount(self, device=0):
        if 0 <= device < len(self.joysticks):
            return sdl2.SDL_JoystickNumHats(self.joysticks[device])
        else:
            return 0

    def getButtonCount(self, device=0):
        if 0 <= device < len(self.joysticks):
            return sdl2.SDL_JoystickNumButtons(self.joysticks[device])
        else:
            return 0

    def getAxisNames(self, device=0):
        if 0 <= device < len(self.joysticks):
            label_dict = self.joystickLabels[device]
            axes = label_dict.keys()
            axes.sort(key=lambda axis: label_dict[axis])
            return axes
        return []

    def getAxis(self, axis, device=0):
        if 0 <= device < len(self.joysticks):
            joystick = self.joysticks[device]
            label_dict = self.joystickLabels[device]
            if axis in label_dict:
                axis = label_dict[axis]
            if 0 <= axis < sdl2.SDL_JoystickNumAxes(joystick):
                return self.convertRaw(sdl2.SDL_JoystickGetAxis(joystick, axis))
        return 0

    def setAxisNames(self, axis_list, device=0):
        if 0 <= device < len(self.joysticks):
            label_dict = self.joystickLabels[device]
            for i in range(len(axis_list)):
                label_dict[axis_list[i]] = i

    def getButton(self, button, device=0):
        if 0 <= device < len(self.joysticks):
            joystick = self.joysticks[device]
            button -= 1  # input is one-based, but SDL2 is zero-based
            if 0 <= button < sdl2.SDL_JoystickNumButtons(joystick):
                return bool(sdl2.SDL_JoystickGetButton(joystick, button))
        return False

    def getDPad(self, dpad=0, device=0):
        if 0 <= device < len(self.joysticks):
            joystick = self.joysticks[device]
            if dpad < sdl2.SDL_JoystickNumHats(joystick):
                raw_hat = sdl2.SDL_JoystickGetHat(joystick, dpad)
                return self.convertHat(raw_hat)
        return 0, 0

    def getDPadX(self, dpad=0, device=0):
        dx, dy = self.getDPad(dpad, device)
        return dx

    def getDPadY(self, dpad=0, device=0):
        dx, dy = self.getDPad(dpad, device)
        return dy

    def convertRaw(self, unscaled_value):
        value = unscaled_value / 32768.0
        if abs(value) < self.joystickDeadZone:
            return 0
        else:
            return value

    def convertHat(self, raw_index):
        dx, dy = 0, 0
        if raw_index & sdl2.SDL_HAT_LEFT:
            dx -= 1
        if raw_index & sdl2.SDL_HAT_RIGHT:
            dx += 1
        if raw_index & sdl2.SDL_HAT_DOWN:
            dy -= 1
        if raw_index & sdl2.SDL_HAT_UP:
            dy += 1
        return dx, dy

    def onGameControllerStick(self, listenerFunction):
        def joystick_motion_handler(event, world):
            listenerFunction(world, event.joy, event.axis, self.convertRaw(event.value))

        events.handler(sdl2.SDL_JOYAXISMOTION, joystick_motion_handler)

    def onGameControllerDPad(self, listenerFunction):
        def dpad_motion_handler(event, world):
            dx, dy = self.convertHat(event.value)
            listenerFunction(world, event.joy, event.hat, dx, dy)

        events.handler(sdl2.SDL_JOYHATMOTION, dpad_motion_handler)

    def onGameControllerButtonPress(self, listenerFunction):
        def joystick_button_press_handler(event, world):
            listenerFunction(world, event.joy, event.button + 1)

        events.handler(sdl2.SDL_JOYBUTTONDOWN, joystick_button_press_handler)

    def onGameControllerButtonRelease(self, listenerFunction):
        def joystick_button_release_handler(event, world):
            listenerFunction(world, event.joy, event.button + 1)

        events.handler(sdl2.SDL_JOYBUTTONUP, joystick_button_release_handler)
