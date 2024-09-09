import pygame


def draw_rect_alpha(surface, color, rect, corner_radius=10):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), border_radius=corner_radius)
    surface.blit(shape_surf, rect)
