import sys
import random

import pygame

from player import Player
from obstacle import Obstacle
from model import ModelEnv, ModelTask, agent, Experiment

LEARN = True

pygame.init()

clock = pygame.time.Clock()

size = width, height = 700, 200
screen = pygame.display.set_mode(size)

black = 0, 0, 0
white = 255, 255, 255

player = Player()

obstacles = []

score = 0

font = pygame.font.SysFont('Arial', 25)


def flip_y(rect):
    return rect.move(0, height - rect.height - rect.top*2)


class World(object):

    def player(self):
        return player

    def distance(self, obstacle):
        return obstacle.x - player.x - player.width

    def all_distances(self):
        distances = map(lambda x: self.distance(x), obstacles)
        needed = 8 - len(distances)
        distances = distances + [1000 for x in range(needed)]
        return distances

    def reset(self):
        obstacles = []
        player.y = 0

    def collided(self):
        return any(map(
            lambda x: x.collide(player),
            obstacles
        ))

    def score(self):
        return score

w = World()

env = ModelEnv(w)
task = ModelTask(env)
experiment = Experiment(task, agent)

while 1:
    # delta is time since last frame (in seconds)
    delta = clock.tick(20) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # input phase
    player.start(delta)
    if LEARN:
        experiment.doInteractions(1)
    else:
        keys = pygame.key.get_pressed()
        player.input(keys, delta)

    # pre-action phase
    score += 2
    # print(score)

    ## random generate obstaces
    spawn_obstacle = random.random() * delta < 0.07/60
    if spawn_obstacle:
        obstacles.append(Obstacle(x=width))

    # action phase
    player.action(delta)
    for obstacle in obstacles:
        obstacle.action(delta)

    # post-action phase
    score += int(player.jumped)

    collide = any(map(
        lambda x: x.collide(player),
        obstacles
    ))
    if collide:
        # obstacles = []
        score -= 30

    # render phase
    screen.fill(black)
    screen.blit(player.surface, flip_y(player.rect))

    for obstacle in obstacles:
        screen.blit(obstacle.surface, flip_y(obstacle.rect))

    if score < 0:
        score = 0

    screen.blit(font.render('Score:' + str(score), True, (255, 0, 0)), (200, 100))

    pygame.display.flip()

    # print(player.jumped)
    obstacles = filter(lambda x: not x.gone, obstacles)

    if LEARN:
        agent.learn(1)
        # agent.reset()
