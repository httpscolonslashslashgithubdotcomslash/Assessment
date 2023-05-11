import pygame
import random

# Define game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

LANE_WIDTH = 160
LANE_COUNT = 10

BOX_WIDTH = 40
BOX_HEIGHT = 40

BOX_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Box Racer")

# Set up the clock
clock = pygame.time.Clock()

# Define the Box class
class Box(pygame.sprite.Sprite):
    def __init__(self, lane):
        super().__init__()
        self.image = pygame.Surface((BOX_WIDTH, BOX_HEIGHT))
        self.image.fill(random.choice(BOX_COLORS))
        self.rect = self.image.get_rect()
        self.rect.x = lane * LANE_WIDTH + (LANE_WIDTH - BOX_WIDTH) / 2
        self.rect.y = -BOX_HEIGHT
        self.speed = random.randint(10, 20)

    def update(self):
        self.rect.y += self.speed

# Set up the sprite groups
all_sprites = pygame.sprite.Group()
box_sprites = pygame.sprite.Group()

# Add the player's box
player_box = Box(2)
all_sprites.add(player_box)

# Set up the lanes
lanes = [False] * LANE_COUNT
lanes[2] = True

# Set up the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the player's box
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_box.rect.x > 0:
        player_box.rect.x -= LANE_WIDTH
        lanes[player_box.rect.x // LANE_WIDTH] = True
        lanes[(player_box.rect.x + BOX_WIDTH) // LANE_WIDTH] = False
    elif keys[pygame.K_RIGHT] and player_box.rect.x < (LANE_COUNT - 1) * LANE_WIDTH:
        player_box.rect.x += LANE_WIDTH
        lanes[player_box.rect.x // LANE_WIDTH] = True
        lanes[(player_box.rect.x + BOX_WIDTH) // LANE_WIDTH] = False

    # Add new boxes at the top of the screen
    if random.random() < 0.02:
        for lane in range(LANE_COUNT):
            if not lanes[lane]:
                box = Box(lane)
                all_sprites.add(box)
                box_sprites.add(box)
                lanes[lane] = True
                break

    # Update the boxes
    for box in box_sprites:
        box.update()
        if box.rect.y > SCREEN_HEIGHT:
            lanes[box.rect.x // LANE_WIDTH] = False
            box.kill()

    # Check for collisions
    if pygame.sprite.spritecollide(player_box, box_sprites, False):
        running = False

    # Draw the screen
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

    # Wait for the next frame
    clock.tick(FPS)

# Clean up Pygame
pygame.quit()
