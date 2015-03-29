import pygame


class Obstacle(object):

    move_speed = 400

    color = 255, 0, 255

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

        self.size = self.width, self.height = 10, 10

        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)

        self.rect = self.make_rect()
        self.gone = False

    def input(self, keys):
        pass

    def action(self, delta):
        self.rect = self.make_rect()

        self.x -= self.move_speed * delta
        self.gone = self.x < 0

    def collide(self, player):
        return self.rect.colliderect(player.rect)

    def make_rect(self):
        return pygame.Rect(
            (self.x, self.y),
            self.size
        )
