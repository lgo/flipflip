import pygame

import random

BASE_JUMP_ACCEL = 12.0
BASE_JUMP_DECCEL = 5.0

JUMP_ACCEL = BASE_JUMP_ACCEL
JUMP_DECCEL = BASE_JUMP_DECCEL


class Player(object):

    jump_speed = 50
    color = 255, 255, 255

    def __init__(self):
        self.y = 0
        self.x = 20

        self.dy = 0

        self.size = self.width, self.height = 20, 20

        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)

        self.rect = self.make_rect()

        self.jumping = True
        self.jumped = 0
        self.nojumpframes = 5

    def start(self, delta):
        self.delta = delta

    def jump(self):
        if self.y == 0:
            self.dy = JUMP_ACCEL
            self.jumping = True
            self.jumped = -3
        else:
            self.jumped -= 2
            self.dy += JUMP_DECCEL * 0.5 * self.delta * 9.8
            self.jumping = False
        # if self.jumped == 0:
        #     self.jumped = -0.3
        # else:
        #     self.jumped *= 1 + (7 * self.delta)

    def nojump(self):
        if self.y == 0 or self.nojumpframes > 5:
            self.jumped = 0
        self.nojumpframes += 1

    def input(self, keys, delta):
        if keys[pygame.K_w] or keys[pygame.K_SPACE]:
            self.jump()
        elif self.y == 0:
            self.jumped = 0

    def action(self, delta):
        self.rect = self.make_rect()

        # apply acceleration
        if not self.jumping:
            self.dy -= 9.8 * delta * JUMP_DECCEL
        else:
            self.dy -= 9.8 * delta * JUMP_DECCEL
            if self.dy < 0:
                self.dy = 0
            self.y += 65 * delta * (random.random() - 0.5)

        # apply velocity
        self.y += self.dy
        if self.y < 0:
            self.y = 0

        self.jumping = False

    def make_rect(self):
        return pygame.Rect(
            (self.x, self.y),
            self.size
        )
