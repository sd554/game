"""
This is a simple interactive graphics and animation library for Python.
Original author: Andrew Merrill
Maintainer: Cel Skeggs
Help From: Aidan Smith
Version: 4.0.0 (last updated May 2016)

This code is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike license
see http://creativecommons.org/licenses/by-nc-sa/3.0/ for details
"""

import audio
import colors
import display
import events
import gmath
import image
import joysticks
import keyboard
import keys
import mouse
import sdl2
import timers

class World:
    pass


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class GameLibInfo:
    def __init__(self):
        self.world = None
        self.display = display.Display()
        self.joyinfo = joysticks.JoysticksInfo()
        self.keys = keyboard.Keys()
        self.fps = timers.GameClock()
        self.eventloop = events.EventLoop()

        self.graphicsInited = False

    def initGraphics(self):
        if not self.graphicsInited:
            assert sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING) == 0, "Could not init: %s" % sdl2.SDL_GetError()
            self.display.initialize()
            self.joyinfo.initialize()
            self.keys.initialize()
            events.handler(sdl2.SDL_QUIT, self.check_quit_event)
            events.handler(sdl2.SDL_KEYDOWN, self.check_quit_key)
            self.graphicsInited = True

    def check_quit_event(self, event, world):
        self.eventloop.stop()

    def check_quit_key(self, event, world):
        if event.key.keysym.scancode == sdl2.SDL_SCANCODE_ESCAPE:
            self.eventloop.stop()

    def startGame(self):
        self.world = World()
        self.fps.start()
        self.eventloop.start()

    def getWorld(self):
        return self.world

    # use animate for non-interactive animations
    def animate(self, drawFunction, timeLimit, repeat=False):
        def startAnimation(world):
            pass

        def timeExpired(world):
            if getElapsedTime() >= timeLimit:
                if repeat:
                    resetTime()
                else:
                    _GLI.eventloop.stop()

        def drawAnimationFrame(world):
            drawFunction(float(getElapsedTime()))

        self.runGraphics(startAnimation, timeExpired, drawAnimationFrame)

    # use runGraphics for interactive programs like games
    def runGraphics(self, startFunction, updateFunction, drawFunction):
        self.startGame()
        startFunction(self.world)

        def loopFunction():
            updateFunction(self.world)
            self.display.renderWithFunction(lambda: drawFunction(self.world))
            self.fps.tick()

        self.eventloop.runloop(self.world, loopFunction)


_GLI = GameLibInfo()


def makeGraphicsWindow(width, height, fullscreen=False):
    _GLI.initGraphics()
    setGraphicsMode(width, height, fullscreen)


def getScreenSize():
    _GLI.initGraphics()
    return _GLI.display.getScreenSize()


def getAllScreenSizes():
    _GLI.initGraphics()
    return _GLI.display.getAllScreenSizes()


def sizeString(text, size=30, bold=False, italic=False, font=None):
    font = _getFont(font, size, bold, italic)
    textimage = font.render(str(text), False, (1,1,1))
    return (textimage.get_width(), textimage.get_height())

# _GLI

animate = _GLI.animate
runGraphics = _GLI.runGraphics
getWorld = _GLI.getWorld

# audio

loadSound = audio.loadSound
playSound = audio.playSound
stopSound = audio.stopSound
loadMusic = audio.loadMusic
playMusic = audio.playMusic
stopMusic = audio.stopMusic

# colors

lookupColor = colors.lookupColor
getColorsList = colors.getColorsList

# display

setBackground = _GLI.display.setBackground
setForeground = _GLI.display.setForeground

setGraphicsMode = _GLI.display.setGraphicsMode
getWindowWidth = _GLI.display.getWindowWidth
getWindowHeight = _GLI.display.getWindowHeight
setWindowTitle = _GLI.display.setWindowTitle

saveScreen = _GLI.display.saveScreen
getScreenPixel = _GLI.display.getScreenPixel

drawPixel = _GLI.display.drawPixel
drawLine = _GLI.display.drawLine
drawCircle = _GLI.display.drawCircle
fillCircle = _GLI.display.fillCircle
drawEllipse = _GLI.display.drawEllipse
fillEllipse = _GLI.display.fillEllipse
drawRectangle = _GLI.display.drawRectangle
fillRectangle = _GLI.display.fillRectangle
drawPolygon = _GLI.display.drawPolygon
fillPolygon = _GLI.display.fillPolygon
sizeString = _GLI.display.sizeString
drawString = _GLI.display.drawString
drawImage = _GLI.display.drawImage
getFontList = _GLI.display.getFontList

# fps

getActualFrameRate = _GLI.fps.getActualFPS
displayFPS = _GLI.fps.displayFPS
getElapsedTime = _GLI.fps.getElapsedTime
resetTime = _GLI.fps.resetTime
setFrameRate = _GLI.fps.setTargetFPS

# gmath

polarToCartesian = gmath.polarToCartesian
cartesianToPolarAngle = gmath.cartesianToPolarAngle
pointInPolygon = gmath.pointInPolygon

# image

loadImage = image.loadImage
saveImage = image.saveImage
getImageWidth = image.getImageWidth
getImageHeight = image.getImageHeight
getImagePixel = image.getImagePixel
getImageRegion = image.getImageRegion
image.setDisplay(_GLI.display)

# joysticks

onGameControllerStick = _GLI.joyinfo.onGameControllerStick
onGameControllerDPad = _GLI.joyinfo.onGameControllerDPad
onGameControllerButtonPress = _GLI.joyinfo.onGameControllerButtonPress
onGameControllerButtonRelease = _GLI.joyinfo.onGameControllerButtonRelease

numGameControllers = _GLI.joyinfo.getJoystickCount
gameControllerSetDeadZone = _GLI.joyinfo.setDeadzone

gameControllerNumStickAxes = _GLI.joyinfo.getAxisCount
gameControllerGetStickAxesNames = _GLI.joyinfo.getAxisNames
gameControllerSetStickAxesNames = _GLI.joyinfo.setAxisNames
gameControllerStickAxis = _GLI.joyinfo.getAxis

gameControllerNumButtons = _GLI.joyinfo.getButtonCount
gameControllerButton = _GLI.joyinfo.getButton

gameControllerNumDPads = _GLI.joyinfo.getDPadCount
gameControllerDPadX = _GLI.joyinfo.getDPadX
gameControllerDPadY = _GLI.joyinfo.getDPadY

# keyboard

onKeyPress = keyboard.onKeyPress
onAnyKeyPress = keyboard.onAnyKeyPress
onKeyRelease = keyboard.onKeyRelease
onAnyKeyRelease = keyboard.onAnyKeyRelease

isKeyPressed = _GLI.keys.isKeyPressed

# keys

getKeyName = keys.getKeyName
getKeyCode = keys.getKeyCode
sameKeys = keys.sameKeys

# mouse

getMousePosition = mouse.getMousePosition
getMouseButton = mouse.getMouseButton
hideMouse = mouse.hideMouse
showMouse = mouse.showMouse
moveMouse = mouse.moveMouse

onMousePress = mouse.onMousePress
onMouseRelease = mouse.onMouseRelease
onWheelForward = mouse.onWheelForward
onWheelBackward = mouse.onWheelBackward
onMouseMotion = mouse.onMouseMotion

# timers

onTimer = timers.onTimer

# events

endGraphics = _GLI.eventloop.stop
