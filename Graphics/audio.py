import sdl2, sdl2.sdlmixer

class Audio:
    def __init__(self):
        pass

    def initialize(self):
        assert sdl2.sdlmixer.Mix_Init() == 0, "Could not initialize mixer library: %s" % sdl2.SDL_GetError()
        assert sdl2.sdlmixer.Mix_OpenAudio(22050, sdl2.AUDIO_S16SYS, 2, 4096) == 0, "Could not initialize sound device: %s" % sdl2.SDL_GetError()
        # TODO: do I need to do CloseAudio anywhere? Or is quitting sufficient?

    def loadSound(self, filename, volume):
        chunk = sdl2.sdlmixer.Mix_LoadWAV(filename)
        assert chunk is not None, "Could not load sound: %s" % sdl2.SDL_GetError()
        sdl2.sdlmixer.Mix_VolumeChunk(chunk, int(round(sdl2.sdlmixer.MIX_MAX_VOLUME * volume)))
        return chunk

    def playSound(self, sound, repeat=False):
        pass # TODO working here

loadSound = Audio.loadSound

def playSound(sound, repeat=False):
    if repeat:
        sound.play(-1)
    else:
        sound.play()


def stopSound(sound):
    sound.stop()


def loadMusic(filename, volume=1):
    pygame.mixer.music.load(filename)
    if volume != 1:
        pygame.mixer.music.set_volume(volume)


def playMusic(repeat=False):
    if repeat:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play()


def stopMusic():
    pygame.mixer.music.stop()
