import pygame

from Config import *

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

def sys_text_object(text, color, size=FontSize.SMALL):
    """
    Returns text field as rectangle object
    :param text: text to be placed
    :param color: color of the text
    :param size: size of the text (small, medium, large)
    :return: text object and borders of text as rectangle
    """
    font_string = 'comicsansms'
    if size == FontSize.SMALL:
        text_surface = pygame.font.SysFont(font_string, 25).render(text, True, color)
    elif size == FontSize.MEDIUM:
        text_surface = pygame.font.SysFont(font_string, 50).render(text, True, color)
    elif size == FontSize.LARGE:
        text_surface = pygame.font.SysFont(font_string, 85).render(text, True, color)
    return text_surface, text_surface.get_rect()


def custom_text_object(text, color, size=FontSize.SMALL):
    """
    Returns text field as rectangle object
    :param text: text to be placed
    :param color: color of the text
    :param size: size of the text (small, medium, large)
    :return: text object and borders of text as rectangle
    """
    font_string = 'assets/fonts/font.ttf'
    if size == FontSize.SMALL:
        text_surface = pygame.font.Font(font_string, 25).render(text, True, color)
    elif size == FontSize.MEDIUM:
        text_surface = pygame.font.Font(font_string, 50).render(text, True, color)
    elif size == FontSize.LARGE:
        text_surface = pygame.font.Font(font_string, 85).render(text, True, color)
    return text_surface, text_surface.get_rect()

def message_to_screen(game_display, text, color, coords, size=FontSize.SMALL, sys_font=True):
    """
    Places text to screen
    :param game_display: handle to display
    :param text: text to place
    :param color: color of the text
    :param y_displace: vertical displacement of the text, positive/negative values
    :param size: size of the text (small, medium, large)
    :return: none
    """
    if sys_font:
        text_surf, text_rect = sys_text_object(text, color, size)
    else:
        text_surf, text_rect = custom_text_object(text, color, size)
    text_rect.center = coords
    game_display.blit(text_surf, text_rect)

def map_distances_to_colors(distances):
    colors = []
    for d in distances:
        if d:
            colors.append(yellow)
        else:
            colors.append(red)
    return colors