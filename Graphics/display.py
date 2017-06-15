import sdl2, sdl2.sdlgfx, sdl2.sdlttf, colors, pygame_sysfont, image, ctypes, py3compat

DEFAULT_BACKGROUND = (255, 255, 255)
DEFAULT_FOREGROUND = (0, 0, 0)


class Display:
    def __init__(self):
        self.windowWidth, self.windowHeight = 0, 0
        self.background = DEFAULT_BACKGROUND
        self.foreground = DEFAULT_FOREGROUND
        self.window = None
        self.renderer = None
        self.fonts = {}

    def initialize(self):
        sdl2.SDL_SetHint(sdl2.SDL_HINT_RENDER_SCALE_QUALITY, b"linear")
        assert sdl2.sdlttf.TTF_Init() == 0, "Could not initialize TTF library: %s" % sdl2.SDL_GetError()

    # TODO: should title be added here?
    def setGraphicsMode(self, width, height, fullscreen=False, title="graphics.py"):
        self.windowWidth, self.windowHeight = width, height
        title = py3compat.to_bin(title)
        if fullscreen:
            self.window = sdl2.SDL_CreateWindow(title, sdl2.SDL_WINDOWPOS_UNDEFINED,
                                                sdl2.SDL_WINDOWPOS_UNDEFINED, 0, 0, sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP)
        else:
            self.window = sdl2.SDL_CreateWindow(title, sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED,
                                                width, height, sdl2.SDL_WINDOW_RESIZABLE)
        assert self.window is not None, "Could not create window: %s" % sdl2.SDL_GetError()
        self.renderer = sdl2.SDL_CreateRenderer(self.window, -1, 0)
        assert self.renderer is not None, "Could not create renderer: %s" % sdl2.SDL_GetError()
        if fullscreen:
            assert sdl2.SDL_RenderSetLogicalSize(self.renderer, width,
                                                 height) == 0, "Could not set logical size: %s" % sdl2.SDL_GetError()

    def getPixelFormat(self):
        return sdl2.SDL_GetWindowPixelFormat(self.window)

    def getWindowWidth(self):
        return self.windowWidth

    def getWindowHeight(self):
        return self.windowHeight

    def setWindowTitle(self, title):
        sdl2.SDL_SetWindowTitle(self.window, str(title))

    def drawPixel(self, x, y, color=None):
        color = color or self.foreground
        self.set_render_color(colors.lookupColor(color))
        assert sdl2.SDL_RenderDrawPoint(self.renderer, int(x), int(y)) == 0, \
            "Could not draw pixel: %s" % sdl2.SDL_GetError()

    def drawLine(self, x1, y1, x2, y2, color=None, thickness=1):
        color = color or self.foreground
        assert int(thickness) >= 1, "invalid thickness - gfx will fail"
        r, g, b, a = colors.lookupColor(color)
        assert sdl2.sdlgfx.thickLineRGBA(self.renderer, int(x1), int(y1), int(x2), int(y2), int(thickness), r, g, b,
                                         a) == 0, "Could not draw line: %s" % sdl2.SDL_GetError()

    def drawCircle(self, x, y, radius, color=None, thickness=1):
        color = color or self.foreground
        self.drawEllipse(x, y, 2*radius, 2*radius, color, thickness)

    def fillCircle(self, x, y, radius, color=None):
        color = color or self.foreground
        self.drawCircle(x, y, radius/2.0, color, 0)

    def drawEllipse(self, x, y, width, height, color=None, thickness=1):
        color = color or self.foreground
        thickness = int(thickness)
        r, g, b, a = colors.lookupColor(color)
        if thickness <= 0:
            assert sdl2.sdlgfx.filledEllipseRGBA(self.renderer, int(x), int(y), int(width), int(height), r, g, b, a) == 0, \
                "Could not fill ellipse: %s" % sdl2.SDL_GetError()
        else:
            # what on earth was pygame doing???
            for loop in range(thickness):
                assert sdl2.sdlgfx.ellipseRGBA(self.renderer, int(x), int(y), int(width / 2) - loop,
                                               int(height / 2) - loop, r, g, b, a) == 0, \
                    "Could not draw ellipse: %s" % sdl2.SDL_GetError()

    def fillEllipse(self, x, y, width, height, color=None):
        color = color or self.foreground
        self.drawEllipse(x, y, width, height, color, 0)

    def drawRectangle(self, x, y, width, height, color=None, thickness=1):
        color = color or self.foreground
        self.drawPolygon(((x, y), (x + width - 1, y), (x + width - 1, y + height - 1), (x, y + height - 1)), color,
                         thickness)

    def fillRectangle(self, x, y, width, height, color=None):
        color = color or self.foreground
        self.drawRectangle(x, y, width, height, color, 0)

    def drawPolygon(self, pointlist, color=None, thickness=1):
        color = color or self.foreground
        thickness = int(thickness)
        if thickness > 0:
            for i, (x1, y1) in enumerate(pointlist):
                x2, y2 = pointlist[(i + 1) % len(pointlist)]
                self.drawLine(x1, y1, x2, y2, color, thickness)
        else:
            r, g, b, a = colors.lookupColor(color)
            xlist, ylist = (sdl2.Sint16 * len(pointlist))(), (sdl2.Sint16 * len(pointlist))()
            for k, (x, y) in enumerate(pointlist):
                xlist[k], ylist[k] = int(x), int(y)
            xptr = ctypes.cast(xlist, ctypes.POINTER(sdl2.Sint16))
            yptr = ctypes.cast(ylist, ctypes.POINTER(sdl2.Sint16))
            assert sdl2.sdlgfx.filledPolygonRGBA(self.renderer, xptr, yptr, len(pointlist), int(r), int(g), int(b), int(a)) \
                   == 0, "Could not fill polygon: %s" % sdl2.SDL_GetError()

    def fillPolygon(self, pointlist, color=None):
        color = color or self.foreground
        self.drawPolygon(pointlist, color, 0)

    # internal only
    def getCachedFont(self, bold, font, italic, size):
        fontSignature = (font, size, bold, italic)
        if fontSignature not in self.fonts:
            fontpath, size, bold, italic = pygame_sysfont.lookup_sys(font, size, bold, italic)
            font = sdl2.sdlttf.TTF_OpenFont(py3compat.to_bin(fontpath), size)
            assert font is not None, "Could not open font: %s" % sdl2.SDL_GetError()
            style = sdl2.sdlttf.TTF_STYLE_NORMAL
            if bold:
                style |= sdl2.sdlttf.TTF_STYLE_BOLD
            if italic:
                style |= sdl2.sdlttf.TTF_STYLE_ITALIC
            sdl2.sdlttf.TTF_SetFontStyle(font, style)
            self.fonts[fontSignature] = font
        return self.fonts[fontSignature]

    def sizeString(self, text, size=30, bold=False, italic=False, font=None):
        font = self.getCachedFont(bold, font, italic, size)
        w = [-1]
        h = [-1]
        assert sdl2.sdlttf.TTF_SizeUTF8(font, str(text).encode("utf-8"), w, h) == 0, \
            "Could not find size of text: %s" % sdl2.SDL_GetError()
        assert w[0] != -1 and h[0] != -1
        return w[0], h[0]

    def convertColor(self, color):
        if color[3:]:
            return sdl2.SDL_Color(color[0], color[1], color[2], color[3])
        else:
            return sdl2.SDL_Color(color[0], color[1], color[2])

    def drawString(self, text, x, y, size=30, color=None, bold=False, italic=False, font=None):
        color = color or self.foreground
        color = self.convertColor(colors.lookupColor(color))
        font = self.getCachedFont(bold, font, italic, size)
        # TODO: do we want to change the quality?
        textimage = sdl2.sdlttf.TTF_RenderUTF8_Solid(font, str(text).encode("utf-8"), color)
        assert textimage is not None, "Could not render font: %s" % sdl2.SDL_GetError()
        try:
            texture = sdl2.SDL_CreateTextureFromSurface(self.renderer, textimage)
            assert texture is not None, "Could not convert surface: %s" % sdl2.SDL_GetError()
            try:
                target_rect = sdl2.SDL_Rect(int(x), int(y), textimage.contents.w, textimage.contents.h)
                assert sdl2.SDL_RenderCopy(self.renderer, texture, None, target_rect) == 0, \
                    "Could not render text: %s" % sdl2.SDL_GetError()
                return textimage.contents.w, textimage.contents.h
            finally:
                sdl2.SDL_DestroyTexture(texture)
        finally:
            sdl2.SDL_FreeSurface(textimage)

    def drawImage(self, image, x, y, rotate=0, scale=1, flipHorizontal=False, flipVertical=False):
        w, h = image.get_size()
        w *= scale
        h *= scale
        target_rect = sdl2.SDL_Rect(int(x), int(y), int(w), int(h))
        flags = sdl2.SDL_FLIP_NONE
        if flipHorizontal:
            flags |= sdl2.SDL_FLIP_HORIZONTAL
        if flipVertical:
            flags |= sdl2.SDL_FLIP_VERTICAL
        assert sdl2.SDL_RenderCopyEx(self.renderer, image.get_texture(self.renderer), None, target_rect, rotate, None,
                                     flags) == 0, "Could not render image: %s" % sdl2.SDL_GetError()

    def getFontList(self):
        return pygame_sysfont.get_fonts()

    def setBackground(self, background):
        self.background = colors.lookupColor(background)

    def setForeground(self, foreground):
        self.foreground = colors.lookupColor(foreground)

    def drawBackground(self):
        if isinstance(self.background, sdl2.SDL_Texture):
            # TODO: does this handle stretching right?
            assert sdl2.SDL_RenderCopy(self.renderer, self.background, None,
                                       None) == 0, "Could not render background: %s" % sdl2.SDL_GetError()
        elif self.background is not None:
            self.set_render_color(self.background)
            assert sdl2.SDL_RenderClear(self.renderer) == 0, "Could not set render color: %s" % sdl2.SDL_GetError()

    def set_render_color(self, color):
        r, g, b, a = colors.lookupColor(color)
        assert sdl2.SDL_SetRenderDrawColor(self.renderer, r, g, b, a) == 0, \
            "Could not set render color: %s" % sdl2.SDL_GetError()

    def getAllScreenSizes(self):
        display_index = self.get_display_index()
        mode_count = sdl2.SDL_GetNumDisplayModes(display_index)
        assert mode_count >= 0, "Could not get display modes: %s" % sdl2.SDL_GetError()
        modeinfo = sdl2.SDL_DisplayMode()
        modes = []
        for mode in range(mode_count):
            assert sdl2.SDL_GetDisplayMode(display_index, mode, modeinfo) == 0, "Could not get display mode %d: %s" % (
                mode, sdl2.SDL_GetError())
            modes.append((modeinfo.w, modeinfo.h))
        return modes

    def get_display_index(self):
        # we need a window because we don't know the correct display index
        if self.window is None:
            hidden_window = sdl2.SDL_CreateWindow("This window should not be visible", sdl2.SDL_WINDOWPOS_CENTERED,
                                                  sdl2.SDL_WINDOWPOS_CENTERED, 64, 64, sdl2.SDL_WINDOW_HIDDEN)
            assert hidden_window is not None, "Could not create window for screen size querying: %s" % sdl2.SDL_GetError()
            try:
                display_index = sdl2.SDL_GetWindowDisplayIndex(hidden_window)
            finally:
                sdl2.SDL_DestroyWindow(hidden_window)
        else:
            display_index = sdl2.SDL_GetWindowDisplayIndex(self.window)
        assert display_index >= 0, "Could not get default display index: %s" % sdl2.SDL_GetError()
        return display_index

    def getScreenSize(self):
        display_index = self.get_display_index()
        modeinfo = sdl2.SDL_DisplayMode()
        sdl2.SDL_GetCurrentDisplayMode(display_index, modeinfo)
        return modeinfo.w, modeinfo.h

    def getScreenPixel(self, x, y):
        if 0 <= x < self.windowWidth and 0 <= y < self.windowHeight:
            out = (sdl2.Uint8 * 7)()
            out[0] = out[1] = out[2] = 3
            out[3] = out[4] = out[5] = out[6] = 17
            assert sdl2.SDL_RenderReadPixels(self.renderer, sdl2.SDL_Rect(x, y, 1, 1), sdl2.SDL_PIXELFORMAT_RGB888, out,
                                             3) == 0, "Could not read screen pixel: %s" % sdl2.SDL_GetError()
            # makes sure that memory isn't corrupted
            # but we have to ignore the fourth byte because it might or might not be clobbered. it depends.
            assert out[4:7] == [17, 17, 17]
            return out[0], out[1], out[2]
        else:
            return None

    def saveScreen(self, filename):
        wp, hp = (ctypes.c_int)(), (ctypes.c_int)()
        assert sdl2.SDL_GetRendererOutputSize(self.renderer, ctypes.pointer(wp), ctypes.pointer(hp)) == 0, \
            "Could not get renderer size: %s" % sdl2.SDL_GetError()
        w, h = wp.value, hp.value
        render_target = sdl2.SDL_CreateRGBSurface(0, w, h, 32,
                                                  0x00ff0000, 0x0000ff00, 0x000000ff, 0xff000000)
        assert render_target is not None, "Could not create RGB surface for screenshot: %s" % sdl2.SDL_GetError()
        try:
            assert sdl2.SDL_RenderReadPixels(self.renderer, sdl2.SDL_Rect(0, 0, w, h),
                                             sdl2.SDL_PIXELFORMAT_ARGB8888,
                                             render_target.contents.pixels,
                                             render_target.contents.pitch) == 0, "Could not read screenshot: %s" % sdl2.SDL_GetError()
            image.saveImage(image.wrapSurface(render_target), filename)
        finally:
            sdl2.SDL_FreeSurface(render_target)

    def renderWithFunction(self, renderer):
        self.drawBackground()
        renderer()
        sdl2.SDL_RenderPresent(self.renderer)
