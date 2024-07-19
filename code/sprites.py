import pygame.sprite

from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.ground = True


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)


class Gun(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        #player connection
        self.player = player
        self.distance = 140
        self.player_direction = pygame.math.Vector2(1, 0)

        #sprite setup
        super().__init__(groups)
        self.gun_surf = pygame.image.load(join('..', 'images', 'gun', 'gun.png')).convert_alpha()
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center=self.player.rect.center + self.player_direction * self.distance)

    def get_direction(self):
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.math.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_direction = (mouse_pos - player_pos).normalize()

    def update(self, _):
        self.get_direction()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance
