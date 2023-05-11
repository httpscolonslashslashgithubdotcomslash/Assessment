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

# Define some constants for the other boxes
BOX_WIDTH = 50
BOX_HEIGHT = 50
NUM_BOX_COLORS = 5
BOX_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
BOX_SPEED_RANGE = (5, 15)

# Initialize Pygame and create the game window
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Define a class for the player box
class PlayerBox:

    def __init__(self):
        self.rect = pygame.Rect(PLAYER_START_X, PLAYER_START_Y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.color = PLAYER_COLOR
        self.speed = PLAYER_SPEED
        self.moving_left = False
        self.moving_right = False

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self):
        self.rect.x += self.speed
        if self.rect.x > WINDOW_WIDTH - PLAYER_WIDTH:
            self.rect.x = WINDOW_WIDTH - PLAYER_WIDTH

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)

    # Define a function to handle user input
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.moving_left = True
        if keys[pygame.K_RIGHT]:
            self.moving_right = True

    def update(self):
        if self.moving_left:
            self.move_left()
        if self.moving_right:
            self.move_right()
        self.moving_left = False
        self.moving_right = False



# Create the player box and a list of other boxes
player_box = PlayerBox()
boxes = []

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
    player_box.handle_input()
    for box in boxes:
        box.move()
        if box.rect.colliderect(player_box.rect):
            print("Game over!")
            pygame.quit()
            exit()
    boxes = [box for box in boxes if box.rect.y < WINDOW_HEIGHT]
    draw_screen()
    clock.tick(30)
