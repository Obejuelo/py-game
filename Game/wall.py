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

        self.rect_top = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, 1)

        self.vel_x = SPEED

    def update(self, *args):
        self.rect.left -= self.vel_x
        self.rect_top.x = self.rect.x

    def stop(self):
        self.vel_x = 0
