import sdl2
import sdl2.ext

import time
import cairo
from sdl2 import render, rect, surface
from ctypes import byref
from math import pi, cos, sin

WIDTH = 300
HEIGHT = 400
RADIUS = 100


def draw(surface, scale):
    cr = cairo.Context(surface)
    cr.scale(scale, scale)

    cr.set_source_rgb(0.75, 0.45, 0.85)
    cr.rectangle(0, 0, WIDTH, HEIGHT)
    cr.fill()

    # Clock Face
    cr.set_line_width(2.0)

    center_x = WIDTH/2
    center_y = WIDTH/2 - 30

    cr.set_source_rgb(1.0, 1.0, 1.0)
    cr.arc(center_x, center_y, RADIUS, 0, 2 * pi)
    cr.stroke()

    for i in range(12):
        if i % 3 == 0:
            inset = 0.2 * RADIUS
        else:
            inset = 0.1 * RADIUS

        new_x = center_x + (RADIUS - inset) * cos(i * pi / 6)
        new_y = center_y + (RADIUS - inset) * sin(i * pi / 6)
        cr.move_to(new_x, new_y)

        new_x = center_x + RADIUS * cos(i * pi / 6)
        new_y = center_y + RADIUS * sin(i * pi / 6)

        cr.line_to(new_x, new_y)
        cr.stroke()

    # Hour

    cr.set_source_rgb(2, 0.0, 0.0)
    tm = time.localtime()
    hours = tm.tm_hour
    minutes = tm.tm_min
    seconds = tm.tm_sec

    cr.set_line_width(5.0)
    cr.move_to(center_x, center_y)
    new_x = center_x + RADIUS / 2 * sin(pi / 6 * hours + pi / 360 * minutes)
    new_y = center_y + RADIUS / 2 * -cos(pi / 6 * hours + pi / 360 * minutes)
    cr.line_to(new_x, new_y)
    cr.stroke()

    # Minutes
    cr.set_source_rgb(0, 3.0, 0.0)
    cr.set_line_width(4.0)
    cr.move_to(center_x, center_y)
    new_x = center_x + RADIUS * 0.7 * sin(pi / 30 * minutes)
    new_y = center_y + RADIUS * 0.7 * -cos(pi / 30 * minutes)
    cr.line_to(new_x, new_y)
    cr.stroke()

    # Seconds
    cr.set_source_rgb(0, 0.0, 4.0)
    cr.set_line_width(3.0)
    cr.move_to(center_x, center_y)
    new_x = center_x + RADIUS * 0.75 * sin(pi / 30 * seconds)
    new_y = center_y + RADIUS * 0.75 * -cos(pi / 30 * seconds)
    cr.line_to(new_x, new_y)
    cr.stroke()

    # show text
    cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL,
                        cairo.FONT_WEIGHT_NORMAL)

    cr.set_source_rgb(1.0, 1.0, 1.0)

    text = "%(hours)02d:%(minutes)02d:%(seconds)02d" % ({'hours': hours,
                                                         'minutes': minutes,
                                                         'seconds': seconds})

    cr.set_font_size(24)

    text_ext = cr.text_extents(text)
    cr.move_to(center_x - text_ext.width / 2, 260)
    cr.show_text(text)
    cr.stroke()


def run_sdl():
    sdl2.ext.init()
    window = sdl2.ext.Window("SDL Cairo Example", size=(
        WIDTH, 300), flags=sdl2.SDL_WINDOW_ALLOW_HIGHDPI)
    window.show()
    running = True

    renderer = render.SDL_CreateRenderer(window.window, -1, 0)
    render.SDL_RenderClear(renderer)

    port = rect.SDL_Rect()
    render.SDL_RenderGetViewport(renderer, byref(port))

    cairo_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, port.w, port.h)
    scale = port.w * 1.0 / WIDTH

    texture = render.SDL_CreateTexture(renderer,
                                       sdl2.pixels.SDL_PIXELFORMAT_ARGB32,
                                       render.SDL_TEXTUREACCESS_TARGET,
                                       port.w, port.h)

    while running:

        draw(cairo_surface, scale)
        buf = cairo_surface.get_data().tobytes()

        render.SDL_UpdateTexture(texture, port, buf, port.w * 4)

        render.SDL_RenderCopy(renderer, texture, port, port)
        render.SDL_RenderPresent(renderer)

        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break

        time.sleep(0.2)

    render.SDL_DestroyTexture(texture)


if __name__ == '__main__':
    run_sdl()
