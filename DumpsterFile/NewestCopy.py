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


class Ball:
    def __init__(self, screen, initial_position, initial_velocity, radius=20, color=(255, 0, 0)):
        self.screen = screen
        self.position = initial_position
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
        final_position = [self.position[0], self.position[1] + (k1p + 2*k2p + 2*k3p + k4p) * delta_t / 6]

        return final_position, final_velocity
    
    def update(self, delta_t):
        self.position, self.velocity = self.rk4(delta_t)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)

#Code by Paul Panzer (December 7th, 2017) Array of coordinates between two points
#URL: https://stackoverflow.com/questions/47704008/fastest-way-to-get-all-the-points-between-two-x-y-coordinates-in-python
def connect(ends):
    d0, d1 = np.abs(np.diff(ends, axis=0))[0]
    if d0 > d1: 
        return np.c_[np.linspace(ends[0, 0], ends[1, 0], d0+1, dtype=np.int32),
                     np.round(np.linspace(ends[0, 1], ends[1, 1], d0+1))
                     .astype(np.int32)]
    else:
        return np.c_[np.round(np.linspace(ends[0, 0], ends[1, 0], d1+1))
                     .astype(np.int32),
                     np.linspace(ends[0, 1], ends[1, 1], d1+1, dtype=np.int32)]


class Triangle:
    def __init__(self, screen, pos, color):
        # pos format [[x,y],[x2,y2],[x3,y3]]
        self.screen = screen
        self.pos = pos  # order will top vertice, right vertice, left vertice
        self.color = color
        rp = np.array([pos[0], pos[1]])
        lp = np.array([pos[0], pos[2]])
        self.rightedge = connect(rp)
        self.leftedge = connect(lp)
        # the angle from the center of the ball that will hit the edges of the triangle
        self.langle = math.atan2((pos[0][0] - pos[1][0]), -(pos[0][1] - pos[1][1]))
        self.rangle = math.atan2(-(pos[0][0] - pos[2][0]), (pos[0][1] - pos[2][1]))
        # find

    def draw(self):
        pygame.draw.polygon(screen, self.color, self.pos)  # position needs to be a list of 3 coords [[x,y],[x2,y2],[x3,y3]]


class BigBall:
    def __init__(self, screen, pos, color, radius):
        self.screen = screen
        self.pos = np.array(pos)
        self.radius = radius
        self.color = color

    def set_pos(self, pos):
        self.pos = np.array(pos)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.pos[0]), int(self.pos[1])), self.radius)


def Collision_detection(activeballs, bigball, triangle):
    for ball in activeballs:

        # Wall collision
        if (ball.position[0] - ball.radius) <= 0:
            # Left wall
            ball.position[0] = ball.radius
            ball.velocity[0] *= -COR
        elif (ball.position[0] + ball.radius) >= screen_width:
            # Right wall
            ball.position[0] = screen_width - ball.radius
            ball.velocity[0] *= -COR

        # Object collision
        # Check if the ball is on the left side of the screen
        elif ball.position[0] <= win_width // 2:
            # Check collision with triangle
            disx = ball.position[0] - triangle.pos[0][0]
            disy = ball.position[1] - triangle.pos[0][1]
            distance = math.sqrt(disx**2 + disy**2)

            if distance <= ball.radius:
                # Ball has collided with triangle
                angle = math.atan2(disy, disx)
                overlap = ball.radius - distance
                ball.position[0] -= overlap * math.cos(angle)
                ball.position[1] -= overlap * math.sin(angle)

                # Calculate new velocities
                normal = np.array([math.cos(angle), math.sin(angle)])
                tangent = np.array([-normal[1], normal[0]])

                v1n = np.dot(np.array(ball.velocity), np.array(normal))
                v1t = np.dot(ball.velocity, tangent)

                m1 = mass  # Ball mass
                m2 = float('inf')  # Assuming the triangle is fixed

                v1n_final = (v1n * (m1 - m2) + 2 * m2 * 0) / (m1 + m2)  # Using coefficient of restitution for collision
                v1n_final *= COR

                ball.velocity = v1n_final * normal + v1t * tangent

        else:
            # Ball collision with big ball
            disx = ball.position[0] - triangle.pos[0][0]
            disy = ball.position[1] - triangle.pos[0][1]
            distance = math.sqrt(disx**2 + disy**2)
            if distance < (ball.radius + bigball.radius):
                angle = math.atan2(disy, disx)
                overlap = (ball.radius + bigball.radius) - distance
                ball.position[0] -= overlap * math.cos(angle)
                ball.position[1] -= overlap * math.sin(angle)

                # Calculate new velocities
                normal = np.array([math.cos(angle), math.sin(angle)])
                tangent = np.array([-normal[1], normal[0]])

                v1n = np.dot(ball.velocity, normal)
                v1t = np.dot(ball.velocity, tangent)

                m1 = mass  # Ball mass
                m2 = mass  # Assuming big ball has the same mass as the small ball

                v1n_final = (v1n * (m1 - m2) + 2 * m2 * 0) / (m1 + m2)  # Using coefficient of restitution for collision
                v1n_final *= COR

                ball.velocity = v1n_final * normal + v1t * tangent

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
initial_position = [screen_width // 2, 0]
initial_velocity = 0

ball = Ball(screen, initial_position, initial_velocity)
bigball = BigBall(screen, [600, 330], BLUE, 60)
tripoints = np.array([[200,260],[250,380],[150,380]])
triangle = Triangle(screen, tripoints, GREEN)
is_ball_dropped = False
clock = pygame.time.Clock()
active = [ball]

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
    Collision_detection(active,bigball,triangle)
    screen.fill((255, 255, 255))
    ball.draw()
    bigball.draw()
    triangle.draw()
    pygame.display.flip()
    clock.tick(60)
