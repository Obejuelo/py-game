import pygame
from.config import *

class Wall(pygame.sprite.Sprite):

    def __init__(self, left, bottom):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((40, 80))
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.bottom = bottom

    def update(self, *args):
        self.rect.left -= 5