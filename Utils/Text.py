import pygame.font
from pygame import draw


def draw_text(font: pygame.font.Font, surface: pygame.Surface, text: str,
              color: tuple, x: int, y: int):
    """
    Draws text.
    :param font: The font_medium used.
    :param surface: The surface to write on (pygame surface)
    :param text: The text.
    :param color: The color
    :param x: X of the center of the rectangle containing the text
    :param y: Y of the center of the rectangle containing the text
    :return:
    """
    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


def draw_centered_text(font: pygame.font.Font, surface: pygame.Surface, text: str,
                       color: tuple, rect: pygame.Rect):
    """
    Draws text.
    :param font: The font_medium used.
    :param surface: The surface to write on (pygame surface)
    :param text: The text.
    :param color: The color
    :param rect: The rect
    :return:
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = rect.center
    surface.blit(text_surface, text_rect)


def draw_number_with_circle_background(font: pygame.font.Font, surface: pygame.Surface, number: str,
                                       bg_color: tuple, fg_color: tuple, x: int, y: int):
    """
    Draws a number with a circle background.
    :param font: The font used.
    :param surface: The surface to write on (pygame surface)
    :param number: The number.
    :param bg_color: The color of the background
    :param fg_color: The color of the number
    :param x: X of the center of the rectangle containing the text
    :param y: Y of the center of the rectangle containing the text
    :return:
    """
    draw.circle(surface, bg_color, (x + font.size(number)[0] * .5, y + font.size(number)[1] * .5), 10)
    draw_text(font, surface, str(number), fg_color, x, y)
