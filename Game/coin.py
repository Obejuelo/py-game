import pygame
from .config import *

class Coin(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((20, 30))
        self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

        self.vel_x = SPEED

    def update(self, *args):
        self.rect.left -= self.vel_x

    def stop(self):
        self.vel_x = 0
