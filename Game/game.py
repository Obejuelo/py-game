import pygame
import sys
from .config import *
import random

from .platform import Platform
from .player import Player
from .wall import Wall

class Game:

    def __init__(self):
        pygame.init()
        # Generate surface
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        # Add title to surface
        pygame.display.set_caption(TITLE)

        self.running = True

        self.clock = pygame.time.Clock()

    def start(self):
        self.new()

    def new(self):
        self.generate_elements()
        self.run()

    def generate_elements(self):
        self.platform = Platform()
        self.player = Player(100, self.platform.rect.top - 200)

        # Generate sprites group
        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()

        self.sprites.add(self.platform)
        self.sprites.add(self.player)

        self.generate_walls()

    def generate_walls(self):
        last_position = WIDTH + 100
        if not len(self.walls) > 0:
            for w in range(0, 10):
                left = random.randrange(last_position + 200, last_position + 400)
                wall = Wall(left, self.platform.rect.top)

                last_position = wall.rect.right
                self.sprites.add(wall)
                self.walls.add(wall)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            self.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            self.player.jump()

    def draw(self):
        self.surface.fill(DARK)
        self.sprites.draw(self.surface)

    def update(self):
        #update display
        pygame.display.flip()
        self.sprites.update()
        self.player.validate_platform(self.platform)

    def stop(self):
        pass
