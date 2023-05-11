import pygame
import random

# Define some constants for the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BG_COLOR = (255, 255, 255)

# Define some constants for the player box
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_COLOR = (0, 0, 255)
PLAYER_SPEED = 10
PLAYER_START_X = (WINDOW_WIDTH - PLAYER_WIDTH) / 2
PLAYER_START_Y = WINDOW_HEIGHT - PLAYER_HEIGHT - 10

LANE_WIDTH = 160
LANE_COUNT = 10

# Define some constants for the other boxes
BOX_WIDTH = 50
BOX_HEIGHT = 50
NUM_BOX_COLORS = 5
BOX_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
BOX_SPEED_RANGE = (15, 25)
MAX_BOXES = 5

# Initialize Pygame and create the game window
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Define a class for the player box
class PlayerBox:
    def __init__(self):
        self.rect = pygame.Rect(PLAYER_START_X, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.color = PLAYER_COLOR
        self.speed = PLAYER_SPEED
        self.move_left_flag = False
        self.move_right_flag = False

    def update(self):
        if self.move_left_flag:
            self.rect.x -= self.speed
            if self.rect.x < 0:
                self.rect.x = 0
        elif self.move_right_flag:
            self.rect.x += self.speed
            if self.rect.x > WINDOW_WIDTH - PLAYER_WIDTH:
                self.rect.x = WINDOW_WIDTH - PLAYER_WIDTH

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)

# Define a class for the other boxes
class Box:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WINDOW_WIDTH - BOX_WIDTH), -BOX_HEIGHT, BOX_WIDTH, BOX_HEIGHT)
        self.color = random.choice(BOX_COLORS)
        self.speed = random.randint(*BOX_SPEED_RANGE)

    def move(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)

# Create the player box and a list of other boxes
player_box = PlayerBox()
boxes = []
lanes = [False] * LANE_COUNT
lanes[2] = True

# Define a function to handle user input
def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_box.move_left_flag = True
            elif event.key == pygame.K_RIGHT:
                player_box.move_right_flag = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_box.move_left_flag = False
            elif event.key == pygame.K_RIGHT:
                player_box.move_right_flag = False

# Define a function to add a new box to the list
def add_box():
    if len(boxes) < MAX_BOXES:
        boxes.append(Box())

# Define a function to draw the game screen
def draw_screen():
    window.fill(BG_COLOR)
    player_box.draw()
    for box in boxes:
        box.draw()
    pygame.display.flip()

# Define the main game loop
clock = pygame.time.Clock()
while True:
    handle_input()
    add_box()
    player_box.update()
    for box in boxes:
        box.move()
        if box.rect.colliderect(player_box.rect):
            print("Game over!")
            pygame.quit()
            exit()
    boxes = [box for box in boxes if box.rect.y < WINDOW_HEIGHT]
    draw_screen()
    clock.tick(30)
