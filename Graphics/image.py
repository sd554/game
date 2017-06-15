import sdl2, sdl2.sdlimage, colors, sdl2.sdlgfx, ctypes

_disp = None


# TODO: make sure everything gets freed properly, in general
class Image:
    def __init__(self, surface):
        self.surface = surface
        so = surface[0]
        self.w = so.w
        self.h = so.h
        self.renderer = None
        self.texture = None

    def get_texture(self, renderer):
        # TODO: optimize this for the case of multiple renderers
        if renderer != self.renderer:
            assert renderer is not None
            if self.texture is not None:
                sdl2.SDL_DestroyTexture(self.texture)
                self.texture = None
            self.texture = sdl2.SDL_CreateTextureFromSurface(renderer, self.surface)
            assert self.texture is not None, "Could not prepare image for rendering: %s" % sdl2.SDL_GetError()
        else:
            assert self.texture is not None
        return self.texture

    def free(self):
        # TODO: make sure this happens
        sdl2.SDL_DestroyTexture(self.texture)
        self.texture = None
        self.renderer = None
        sdl2.SDL_FreeSurface(self.surface)
        self.surface = None

    def get_size(self):
        return self.w, self.h


def loadImage(filename, transparentColor=None, rotate=0, scale=1, flipHorizontal=False, flipVertical=False):
    freeable_images = []
    image_out = None
    try:
        image = sdl2.sdlimage.IMG_Load(filename.encode())
        if image is None:
            raise IOError("Could not load image: %s" % sdl2.sdlimage.IMG_GetError())
        freeable_images.append(image)

        # pf = _disp.getPixelFormat()
        # TODO: do we still need to convert the surface? I don't think so...
        #image = sdl2.SDL_ConvertSurface(image_base, pf, 0)
        #assert image is not None, "Could not convert image: %s" % sdl2.SDL_GetError()
        #freeable_images.append(image)

        # TODO: do something differently if transparentColor is None versus False?
        if transparentColor is not None and transparentColor is not False:
            r, g, b = colors.lookupColor(transparentColor)
            pix = sdl2.SDL_MapRGB(r, g, b)
            assert sdl2.SDL_SetColorKey(image, True, pix) == 0, "Could not set color key: %s" % sdl2.SDL_GetError()

        if rotate != 0 or scale != 1 or flipHorizontal or flipVertical:
            hscale = -scale if flipHorizontal else scale
            vscale = -scale if flipVertical else scale
            image = sdl2.sdlgfx.rotozoomSurfaceXY(image, rotate, hscale, vscale, sdl2.sdlgfx.SMOOTHING_ON)
            assert image is not None, "Could not transform image: %s" % sdl2.SDL_GetError()
            freeable_images.append(image)
        image_out = image
    finally:
        for freeable in freeable_images:
            if freeable is not image_out and freeable is not None:
                sdl2.SDL_FreeSurface(freeable)
    return Image(image_out)


def getImageWidth(image):
    return image.get_size()[0]


def getImageHeight(image):
    return image.get_size()[1]


def getImagePixel(image, x, y):
    assert isinstance(image, Image)
    surf = image.surface
    assert sdl2.SDL_LockSurface(surf) == 0, "Could not lock surface: %s" % sdl2.SDL_GetError()
    try:
        bpp = surf.format.BytesPerPixel
        ptr = ctypes.cast(surf.pixels + y * surf.pitch + x * bpp, ctypes.POINTER(sdl2.Uint8))
        if bpp == 1:
            pix = ptr[0]
        elif bpp == 2:
            if sdl2.SDL_BYTEORDER == sdl2.SDL_LIL_ENDIAN:
                pix = ptr[0] | (ptr[1] << 8)
            else:
                pix = ptr[1] | (ptr[0] << 8)
        elif bpp == 3:
            if sdl2.SDL_BYTEORDER == sdl2.SDL_LIL_ENDIAN:
                pix = ptr[0] | (ptr[1] << 8) | (ptr[2] << 16)
            else:
                pix = ptr[2] | (ptr[1] << 8) | (ptr[0] << 16)
        else:
            assert bpp == 4, "invalid BytesPerPixel from builtin surface..."
            if sdl2.SDL_BYTEORDER == sdl2.SDL_LIL_ENDIAN:
                pix = ptr[0] | (ptr[1] << 8) | (ptr[2] << 16) | (ptr[3] << 24)
            else:
                pix = ptr[3] | (ptr[2] << 8) | (ptr[1] << 16) | (ptr[0] << 24)
    finally:
        sdl2.SDL_UnlockSurface(surf)
    out = (sdl2.Uint8 * 5)()
    out[0] = out[1] = out[2] = out[3] = out[4] = 17
    sdl2.SDL_GetRGBA(pix, surf.format, out + 0, out + 1, out + 2, out + 3)
    assert out[4] == 17
    return out[0], out[1], out[2], out[3]


def getImageRegion(image, x, y, width, height):
    x, y, width, height = int(x), int(y), int(width), int(height)
    f = image.format
    bipp = f.BitsPerPixel
    p = image.pixels + f.BytesPerPixel * x + image.pitch * y
    return sdl2.SDL_CreateRGBSurfaceFrom(p, width, height, bipp, image.pitch, f.Rmask, f.Gmask, f.Bmask, f.Amask)


def saveImage(image, filename):
    assert isinstance(image, Image)
    # Always saves images in BMP or PNG, unlike pygame.
    if filename.lower().endswith(".bmp"):
        assert sdl2.SDL_SaveBMP(image.surface, filename.encode()) == 0, "Could not save image: %s" % sdl2.SDL_GetError()
    elif filename.lower().endswith(".png"):
        assert sdl2.sdlimage.IMG_SavePNG(image.surface, filename.encode()) == 0, "Could not save image: %s" % sdl2.SDL_GetError()
    else:
        raise IOError("Can only save images in BMP or PNG format.")


def setDisplay(display):
    global _disp
    _disp = display


def wrapSurface(surface):
    return Image(surface)
