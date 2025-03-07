import pygame
import os
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Xotix Shooter Game")

GRAY = (255, 255, 0)
WHITE = (255, 255, 255)
ENEMY_COLOR = (255, 0, 0)

# Load player image and resize it
try:
    player_img = pygame.image.load(os.path.join("images", "pixel_demon.png"))
    print("Player image loaded successfully!")
except pygame.error as e:
    print("Error loading player image:", e)
    pygame.quit()
    exit()

try:
    bullet_img = pygame.image.load(os.path.join("images", "bullet.png"))  # Replace with your bullet PNG image
    print("Bullet image loaded successfully!")
except pygame.error as e:
    print("Error loading bullet image:", e)
    pygame.quit()
    exit()

# Resize the player image (adjust the size as needed)
player_img = pygame.transform.scale(player_img, (64, 64))  # Resize to 64x64 (or another suitable size)

# Player properties
player_x = WIDTH // 2 - 32  # Position the player in the center horizontally
player_y = HEIGHT - 80  # Position the player near the bottom of the screen
player_speed = 4

# Bullet properties
bullet_speed = 5
bullets = []  # List to store bullets

# Enemy properties
enemy_speed = 1
enemies = []  # List to store enemies

def draw_player(x, y):
    screen.blit(player_img, (x, y))  # Draw player at the specified position

# Bullet class for player bullets
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 1
        self.height = 2
        self.image = bullet_img  # Bullet image

    def move(self):
        self.y -= bullet_speed  # Move bullet up

    def draw(self):
        screen.blit(self.image, (self.x, self.y))  # Use image to draw the bullet

# Enemy class
class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 64)  # Random horizontal position
        self.y = random.randint(-100, -40)  # Spawn above the screen
        self.width = 40  # New width for bullet
        self.height = 50
        self.color = ENEMY_COLOR

    def move(self):
        self.y += enemy_speed  # Move the enemy down

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

# Collision detection between bullet and enemy
def check_collision(bullet, enemy):
    if bullet.x < enemy.x + enemy.width and bullet.x + bullet.width > enemy.x:
        if bullet.y < enemy.y + enemy.height and bullet.y + bullet.height > enemy.y:
            return True
    return False

# Create enemies periodically
def spawn_enemy():
    if random.randint(1, 100) < 2:  # Spawn enemies at random intervals
        enemies.append(Enemy())

# Game loop
running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Fire bullet
                print("Shooting bullet!")  # Debugging print
                bullets.append(Bullet(player_x + 32, player_y))  # Spawn a bullet near the player

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 64:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - 64:
        player_y += player_speed

    # Move and draw bullets
    for bullet in bullets[:]:
        bullet.move()
        bullet.draw()
        if bullet.y < 0:  # Remove bullets that go off-screen
            bullets.remove(bullet)

    # Move and draw enemies
    spawn_enemy()  # Randomly spawn new enemies
    for enemy in enemies[:]:
        enemy.move()
        enemy.draw()
        if enemy.y > HEIGHT:  # Remove enemies that go off-screen
            enemies.remove(enemy)

        # Check collision between each bullet and enemy
        for bullet in bullets[:]:
            if check_collision(bullet, enemy):
                bullets.remove(bullet)  # Remove bullet
                enemies.remove(enemy)  # Remove enemy
                break

    draw_player(player_x, player_y)

    pygame.display.update()

pygame.quit()
