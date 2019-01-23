import pygame
import sys
import os
from .config import *
import random

from .platform import Platform
from .player import Player
from .wall import Wall
from . coin import Coin

class Game:

    def __init__(self):
        pygame.init()
        # Generate surface
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        # Add title to surface
        pygame.display.set_caption(TITLE)

        self.running = True

        self.clock = pygame.time.Clock()

        self.dir = os.path.dirname(__file__)
        self.dir_sounds = os.path.join(self.dir, 'sources/sounds')

        self.font = pygame.font.match_font(FONT)

    def start(self):
        self.new()

    def new(self):
        self.score = 0
        self.level = 0
        self.playing = True

        self.generate_elements()
        self.run()

    def generate_elements(self):
        self.platform = Platform()
        self.player = Player(100, self.platform.rect.top - 200)

        # Generate sprites group
        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

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

            self.level += 1
            self.generate_coins()

    def generate_coins(self):
        last_position = WIDTH + 100
        for c in range(0, MAX_COINS):
            pos_x = random.randrange(last_position + 180, last_position + 300)
            coin = Coin(pos_x, 150)
            last_position = coin.rect.right

            self.sprites.add(coin)
            self.coins.add(coin)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            self.player.jump()

        if key[pygame.K_r] and not self.playing:
            self.new()

    def draw(self):
        self.surface.fill(DARK)
        self.draw_text()
        self.sprites.draw(self.surface)
        pygame.display.flip()

    def update(self):
        if not self.playing:
            return

        #update display
        wall = self.player.collide_with(self.walls)
        if wall:
            if self.player.collide_bottom(wall):
                self.player.skid(wall)
            else:
                self.stop()
                sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, 'lose.wav'))
                sound.play()

        coin = self.player.collide_with(self.coins)
        if coin:
            self.score += 1
            coin.kill()

            sound = pygame.mixer.Sound(os.path.join(self.dir_sounds, 'coin.wav'))
            sound.play()

        self.sprites.update()
        self.player.validate_platform(self.platform)

        self.update_elements(self.walls)
        self.update_elements(self.coins)
        self.generate_walls()

    def update_elements(self, elements):
        for element in elements:
            if not element.rect.right > 0:
                element.kill()

    def stop(self):
        self.playing = False
        self.player.stop()
        self.stop_elements(self.walls)

    def stop_elements(self, elemenst):
        for element in elemenst:
            element.stop()

    def text_format(self):
        return 'Score: {}'.format(self.score)

    def level_format(self):
        return 'Level: {}'.format(self.level)

    def draw_text(self):
        self.display_text(self.text_format(), 30, WHITE, WIDTH // 2, 20)
        self.display_text(self.level_format(), 30, WHITE, 60, 20)

        if not self.playing:
            self.display_text('Perdiste', 60, WHITE, WIDTH // 2, HEIGHT // 2)
            self.display_text('Presiona "r" para reiniciar', 30, TEAL, WIDTH // 2, 100)

    def display_text(self, text, size, color, pos_x, pos_y):
        font = pygame.font.Font(self.font, size)

        text = font.render(text, True, color)
        rect = text.get_rect()
        rect.midtop = (pos_x, pos_y)

        self.surface.blit(text, rect)
