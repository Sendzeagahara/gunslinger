from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_group):
        super().__init__(groups)
        self.image = pygame.image.load(join('..', 'images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-40, 0)

        #movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 500
        self.collision_sprites = collision_group

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, delta_time):
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.rect.center = self.hitbox_rect.center
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * delta_time
        self.rect.center = self.hitbox_rect.center
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                        self.rect.center = self.hitbox_rect.center
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom
                        self.rect.center = self.hitbox_rect.center
                elif direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                        self.rect.center = self.hitbox_rect.center
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                        self.rect.center = self.hitbox_rect.center

    def update(self, delta_time):
        self.input()
        self.move(delta_time)
