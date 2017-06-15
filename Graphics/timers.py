import sdl2, events


def onTimer(listenerFunction, interval):
    eventType = sdl2.SDL_RegisterEvents(1)
    assert eventType != 0xFFFFFFFF, "Out of timers!"

    def timer_handler(event, world):
        listenerFunction(world)

    def raw_callback(interval, param):
        event = sdl2.SDL_Event()
        event.type = eventType
        event.user = sdl2.SDL_UserEvent()
        assert sdl2.SDL_PushEvent(event) > 0, "Could not push event: %s" % sdl2.SDL_GetError()
        return interval

    events.handler(eventType, timer_handler)
    assert sdl2.SDL_AddTimer(interval, raw_callback, None) != 0, "Could not create timer: %s" % sdl2.SDL_GetError()


class GameClock:
    def __init__(self):
        self.startGameAt = None

        self.lastDisplayedAt = 0
        self.displayInterval = 0

        self.lastFrameAt = 0

        self.lastFPSAt = 0
        self.frameCount = 0
        self.actualFPS = 0

        self.targetFPS = 60

    def maybePrintFPS(self, time):
        if self.displayInterval > 0:
            if time > self.lastDisplayedAt + self.displayInterval:
                print(self.getActualFPS())
                self.lastDisplayedAt = time

    def updateFPS(self, time):
        self.frameCount += 1
        if self.frameCount >= 10:
            self.actualFPS = (1000.0 * self.frameCount) / (time - self.lastFPSAt)
            self.lastFPSAt = time
            self.frameCount = 0

    def tickDelay(self):
        time = sdl2.SDL_GetTicks()
        target_delay = 1000.0 / self.targetFPS
        target_time = self.lastFrameAt + target_delay
        real_delay = target_time - time
        if real_delay > 0:
            sdl2.SDL_Delay(int(real_delay))
            self.lastFrameAt = target_time
        else:
            # couldn't keep up!
            self.lastFrameAt = time

    def displayFPS(self, interval):
        self.displayInterval = interval * 1000
        self.lastDisplayedAt = sdl2.SDL_GetTicks()

    def getActualFPS(self):
        return self.actualFPS

    def start(self):
        self.frameCount = self.actualFPS = 0
        self.lastFPSAt = self.startGameAt = sdl2.SDL_GetTicks()

    def tick(self):
        time = sdl2.SDL_GetTicks()
        self.updateFPS(time)
        self.maybePrintFPS(time)
        self.tickDelay()

    def setTargetFPS(self, frameRate):
        self.targetFPS = frameRate

    def getElapsedTime(self):
        return sdl2.SDL_GetTicks() - self.startGameAt

    def resetTime(self):
        self.startGameAt = sdl2.SDL_GetTicks()
