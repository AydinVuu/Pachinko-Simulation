import pygame
import sys
import numpy as np
import math

pygame.init()
win_width = 640
win_height = 640
screen = pygame.display.set_mode((win_width, win_height))  # Top left corner is (0,0)
pygame.display.set_caption('Ball Fall')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Constants
gravity = -9.8
dt = 0.05
mass = 1
radius = 1
# Elasticity of all objects
COR = 0.7

# randomize for different types of balls
# change mass constant to a gravity multiplier
# radius multiplier as well
# have one normal ball with default gravity and radius
# random ball spawns use lab 6
# when balls below line, check for x coord to assign points
# if we goated add spin

# clock
clock = pygame.time.Clock()

def connect(points):
    edges = []
    for i in range(len(points) - 1):
        edges.append([points[i], points[i + 1]])
    edges.append([points[-1], points[0]])  # Closing the loop
    return edges

class Ball:
    def __init__(self, screen, initial_position, initial_velocity, radius=20, color=(255, 0, 0)):
        self.screen = screen
        self.position = list(initial_position)
        self.velocity = initial_velocity
        self.radius = radius
        self.color = color

    def acceleration(self):
        return gravity

    def rk4(self, delta_t):
        k1v = self.acceleration()
        k1p = self.velocity
        k2v = self.acceleration()
        k2p = self.velocity + k1v * delta_t / 2
        k3v = self.acceleration()
        k3p = self.velocity + k2v * delta_t / 2
        k4v = self.acceleration()
        k4p = self.velocity + k3v * delta_t

        final_velocity = self.velocity + (k1v + 2*k2v + 2*k3v + k4v) * delta_t / 6
        final_position = (self.position[0], self.position[1] + (k1p + 2*k2p + 2*k3p + k4p) * delta_t / 6)

        return final_position, final_velocity

    def update(self, delta_t):
        self.position, self.velocity = self.rk4(delta_t)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)


class Triangle:
    def __init__(self, pos):
        # pos format [[x,y],[x2,y2],[x3,y3]]
        self.pos = np.array(pos)  # order will top vertice, right vertice, left vertice
        self.rightedge = connect([pos[0], pos[1]])
        self.leftedge = connect([pos[0], pos[2]])
        # the angle from the center of the ball that will hit the edges of the triangle
        self.rangle = math.atan2((pos[0][0] - pos[1][0]), -(pos[0][1] - pos[1][1]))
        self.langle = math.atan2((pos[0][0] - pos[2][0]), -(pos[0][1] - pos[2][1]))
        # find

    def draw(self):
        pygame.draw.t(screen, self.color, self.pos, self.radius)  # position needs to be a list of 3 coords [[x,y],[x2,y2],[x3,y3]]


class BigBall:
    def __init__(self, pos, color, radius):
        self.pos = np.array(pos)
        self.radius = radius
        self.color = color

    def set_pos(self, pos):
        self.pos = np.array(pos)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)


def Collision_detection(activeballs, bigball, triangle):
    pass
    # Add collision detection logic here


def make_ball(active, Total):
    x = 320  # set to random in a range
    y = 620
    pos = np.array([x, y])
    active.append(Ball(pos, mass, WHITE, radius))
    Total.append(Ball(pos, mass, WHITE, radius))


screen_width = 800
screen_height = 600
gravity = 9.8
left_boundary = 100
right_boundary = 700

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ball Falling")

delta_t = 0.05
initial_position = (screen_width // 2, 0)
initial_velocity = 0

ball = Ball(screen, initial_position, initial_velocity)
is_ball_dropped = False
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                is_ball_dropped = True
            elif event.key == pygame.K_a and not is_ball_dropped:
                if ball.position[0] - 10 >= left_boundary:
                    ball.position[0] -= 10
            elif event.key == pygame.K_d and not is_ball_dropped:
                if ball.position[0] + 10 <= right_boundary:
                    ball.position[0] += 10

    if is_ball_dropped:
        ball.update(delta_t)

    screen.fill((255, 255, 255))
    ball.draw()
    pygame.display.flip()
    clock.tick(60)
