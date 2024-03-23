import pygame
import sys
import math
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
TABLE_WIDTH, TABLE_HEIGHT = 700, 500
TABLE_COLOR = (0, 128, 0)
TABLE_POS = (50, 50)
BALL_RADIUS = 15
NUM_BALLS = 6
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BALL_COLORS = [WHITE, BLACK, RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]
FPS = 60

# Physics constants
FRICTION = 0.99
SPEED_THRESHOLD = 0.5
POCKET_RADIUS = 30
COR = 0.7  # Coefficient of restitution

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Billiards")

# Ball class
class Ball:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.velocity = [0, 0]

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), BALL_RADIUS)

    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.velocity[0] *= FRICTION
        self.velocity[1] *= FRICTION

        # Apply speed limit
        speed_limit = 20  # Adjust as needed
        speed = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        if speed > speed_limit:
            factor = speed_limit / speed
            self.velocity[0] *= factor
            self.velocity[1] *= factor


        # Bounce off walls
        if self.x - BALL_RADIUS < TABLE_POS[0]:
            self.x = TABLE_POS[0] + BALL_RADIUS
            self.velocity[0] *= -COR
        elif self.x + BALL_RADIUS > TABLE_POS[0] + TABLE_WIDTH:
            self.x = TABLE_POS[0] + TABLE_WIDTH - BALL_RADIUS
            self.velocity[0] *= -COR

        if self.y - BALL_RADIUS < TABLE_POS[1]:
            self.y = TABLE_POS[1] + BALL_RADIUS
            self.velocity[1] *= -COR
        elif self.y + BALL_RADIUS > TABLE_POS[1] + TABLE_HEIGHT:
            self.y = TABLE_POS[1] + TABLE_HEIGHT - BALL_RADIUS
            self.velocity[1] *= -COR

        # Stop ball if velocity is very small
        if abs(self.velocity[0]) < SPEED_THRESHOLD:
            self.velocity[0] = 0
        if abs(self.velocity[1]) < SPEED_THRESHOLD:
            self.velocity[1] = 0

    def pocketed(self):
        return self.x < TABLE_POS[0] or self.x > TABLE_POS[0] + TABLE_WIDTH or self.y < TABLE_POS[1] or self.y > TABLE_POS[1] + TABLE_HEIGHT

# Handle collisions function
def handle_collisions(balls):
    for i in range(NUM_BALLS):
        for j in range(i + 1, NUM_BALLS):
            dx = balls[j].x - balls[i].x
            dy = balls[j].y - balls[i].y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < 2 * BALL_RADIUS:
                angle = math.atan2(dy, dx)
                overlap = 2 * BALL_RADIUS - distance
                balls[i].x -= overlap * math.cos(angle)
                balls[i].y -= overlap * math.sin(angle)
                balls[j].x += overlap * math.cos(angle)
                balls[j].y += overlap * math.sin(angle)
                dvx = balls[j].velocity[0] - balls[i].velocity[0]
                dvy = balls[j].velocity[1] - balls[i].velocity[1]
                dot_product = dx * dvx + dy * dvy
                balls[i].velocity[0] += overlap * dot_product * dx / distance**2 * COR
                balls[i].velocity[1] += overlap * dot_product * dy / distance**2 * COR
                balls[j].velocity[0] -= overlap * dot_product * dx / distance**2 * COR
                balls[j].velocity[1] -= overlap * dot_product * dy / distance**2 * COR

# Arrange balls
start_x = TABLE_POS[0] + TABLE_WIDTH // 2
start_y = TABLE_POS[1] + TABLE_HEIGHT // 2
cue_ball = Ball(start_x, start_y, WHITE)
balls = [cue_ball]
for i in range(1, NUM_BALLS):
    x = random.randint(TABLE_POS[0] + 2 * BALL_RADIUS, TABLE_POS[0] + TABLE_WIDTH - 2 * BALL_RADIUS)
    y = random.randint(TABLE_POS[1] + 2 * BALL_RADIUS, TABLE_POS[1] + TABLE_HEIGHT - 2 * BALL_RADIUS)
    while any(math.sqrt((ball.x - x)**2 + (ball.y - y)**2) < 4 * BALL_RADIUS for ball in balls):
        x = random.randint(TABLE_POS[0] + 2 * BALL_RADIUS, TABLE_POS[0] + TABLE_WIDTH - 2 * BALL_RADIUS)
        y = random.randint(TABLE_POS[1] + 2 * BALL_RADIUS, TABLE_POS[1] + TABLE_HEIGHT - 2 * BALL_RADIUS)
    balls.append(Ball(x, y, BALL_COLORS[i]))

# Aiming cue stick
aiming = False
aim_line_length = 100
aim_line_angle = 0

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not aiming:
            cue_start = pygame.mouse.get_pos()
            aiming = True
        elif event.type == pygame.MOUSEBUTTONUP and aiming:
            cue_end = pygame.mouse.get_pos()
            cue_dir = pygame.math.Vector2(cue_end) - pygame.math.Vector2(cue_start)
            cue_dir.normalize_ip()
            cue_ball.velocity = [-cue_dir.x * 6, -cue_dir.y * 6]
            aiming = False

    # Update balls
    for ball in balls:
        ball.move()

    # Handle collisions
    handle_collisions(balls)

    # Handle pocketing
    for ball in balls:
        if ball.pocketed():
            balls.remove(ball)

    # Draw everything
    screen.fill(TABLE_COLOR)  # Table background
    pygame.draw.rect(screen, BLACK, (TABLE_POS[0], TABLE_POS[1], TABLE_WIDTH, TABLE_HEIGHT), 2)  # Table border
    for ball in balls:
        ball.draw()
    if aiming:
        cue_end = pygame.mouse.get_pos()
        pygame.draw.line(screen, WHITE, cue_start, cue_end, 2)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit pygame
pygame.quit()
sys.exit()
