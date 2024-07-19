import pygame.time

from settings import *
from sprites import *
from player import Player
from groups import AllSprites

from random import randint
from pytmx.util_pygame import load_pygame


class Game:
    def __init__(self):
        #setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Gunslinger')
        self.clock = pygame.time.Clock()
        self.running = True
        self.load_images()

        #groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()

        self.setup()

        #gun timer
        self.can_shoot = True
        self.shoot_time = 0
        self.shoot_cooldown = 200

    def load_images(self):
        self.bullet_surf = pygame.image.load(join('..', 'images', 'gun', 'bullet.png')).convert_alpha()

    def input(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction * 50
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

    def gun_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time >= self.shoot_cooldown:
                self.can_shoot = True

    def setup(self):
        tilemap = load_pygame(join('..', 'data', 'maps', 'world.tmx'))

        for x, y, image in tilemap.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in tilemap.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in tilemap.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in tilemap.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)

    def run(self):
        while self.running:
            #dt
            dt = self.clock.tick() / 1000

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #update
            self.gun_timer()
            self.input()
            self.all_sprites.update(dt)

            #draw
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
