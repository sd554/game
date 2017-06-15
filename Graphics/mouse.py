import sdl2, events, ctypes


def getMousePosition():
	x, y = ctypes.c_int(0), ctypes.c_int(0)
	buttonstate = sdl2.mouse.SDL_GetMouseState(ctypes.byref(x), ctypes.byref(y))
	return (x.value, y.value)


def getMouseButton(button):
	buttonstate = sdl2.mouse.SDL_GetMouseState(None, None)
	if button=="left" and buttonstate & sdl2.mouse.SDL_BUTTON(sdl2.mouse.SDL_BUTTON_LEFT):
		return True
	elif button=="right" and buttonstate & sdl2.mouse.SDL_BUTTON(sdl2.mouse.SDL_BUTTON_RIGHT):
		return True
	elif button=="middle" and buttonstate & sdl2.mouse.SDL_BUTTON(sdl2.mouse.SDL_BUTTON_MIDDLE):
		return True
	return False
    #return pygame.mouse.get_pressed()[button - 1]


def hideMouse():
    sdl2.mouse.SDL_ShowCursor(False)


def showMouse():
    sdl2.mouse.SDL_ShowCursor(True)


def moveMouse(x, y):
	sdl2.mouse.SDL_WarpMouseInWindow(None,int(x),int(y))

def onMousePress(listenerFunction):
    def mouse_press_handler(event, world):
    	butt=event.button.button
    	if butt is sdl2.mouse.SDL_BUTTON_LEFT:
    		button="left"
    	elif butt is sdl2.mouse.SDL_BUTTON_RIGHT:
    		button="right"
    	elif butt is sdl2.mouse.SDL_BUTTON_MIDDLE:
    		button="middle"
    	else:
    		button=None
        listenerFunction(world, event.button.x, event.button.y, button)
    events.handler(sdl2.events.SDL_MOUSEBUTTONDOWN, mouse_press_handler)


def onMouseRelease(listenerFunction):
    def mouse_press_handler(event, world):
    	butt=event.button.button
    	if butt is sdl2.mouse.SDL_BUTTON_LEFT:
    		button="left"
    	elif butt is sdl2.mouse.SDL_BUTTON_RIGHT:
    		button="right"
    	elif butt is sdl2.mouse.SDL_BUTTON_MIDDLE:
    		button="middle"
    	else:
    		button=None
        listenerFunction(world, event.button.x, event.button.y, button)
    events.handler(sdl2.events.SDL_MOUSEBUTTONUP, mouse_press_handler)


def onWheelForward(listenerFunction): #TODO
    def wheel_forward_handler(event, world):
        if event.button == 4:
            listenerFunction(world, event.pos[0], event.pos[1])

    events.handler(pygame.MOUSEBUTTONDOWN, wheel_forward_handler)


def onWheelBackward(listenerFunction): #TODO
    def wheel_backward_handler(event, world):
        if event.button == 5:
            listenerFunction(world, event.pos[0], event.pos[1])

    events.handler(pygame.MOUSEBUTTONDOWN, wheel_backward_handler)


def onMouseMotion(listenerFunction): #TODO
    def mouse_motion_handler(event, world):
        dx, dy = event.rel
        if dx != 0 or dy != 0:
            listenerFunction(world, event.pos[0], event.pos[1], dx, dy, event.buttons[0] == 1,
                             event.buttons[1] == 1, event.buttons[2] == 1)

    events.handler(pygame.MOUSEMOTION, mouse_motion_handler)
