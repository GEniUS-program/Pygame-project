import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Shooter Game")

# Set the frame rate
clock = pygame.time.Clock()

# Game logic
wave = 1
difficulty_coef = 1  # increment each wave
lives = 5  # +1 on wave passed; -1 for enemy skipped
score = 0

# Player settings
player_width = 50
player_height = 60
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5
player_damage = 50

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullet_mult = 1
bullets = []

# Enemy settings
enemy_width = 50
enemy_height = 60
enemy_speed = 2
enemies = []

# Spawn an enemy every 2 seconds
enemy_timer = 0
enemy_health = random.randint(50, 101) * difficulty_coef
enemy_spawn_time = 2000 / difficulty_coef

# Collision detection function
def check_collision(rect1, rect2):
    return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))

def game_over():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    score_text = font.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

def start_new_wave():
    global wave, difficulty_coef, lives, enemy_spawn_time, enemy_health
    wave += 1
    difficulty_coef += 0.5
    lives += 1
    enemy_spawn_time = 2000 / difficulty_coef
    enemy_health = random.randint(50, 101) * difficulty_coef
    enemies.clear()
    bullets.clear()

def upgrade_player():
    global player_speed, bullet_speed, bullet_mult
    player_speed += 1
    bullet_speed += 1
    bullet_mult += 1

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for i in range(bullet_mult):
                    # Create a bullet at the current player position
                    bullet_x = player_x + player_width // 2 - bullet_width // 2
                    bullet_y = player_y + i * 5
                    bullets.append([bullet_x, bullet_y])
            if event.key == pygame.K_u:
                upgrade_player()

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # Update bullet positions
    for bullet in bullets:
        bullet[1] -= bullet_speed
    bullets = [bullet for bullet in bullets if bullet[1] > 0]

    # Update enemy positions and spawn new ones
    current_time = pygame.time.get_ticks()
    if current_time - enemy_timer > enemy_spawn_time:
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = -enemy_height
        enemies.append([enemy_x, enemy_y])
        enemy_timer = current_time

    for enemy in enemies:
        enemy[1] += enemy_speed

    # Check for collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if check_collision((bullet[0], bullet[1], bullet_width, bullet_height),
                               (enemy[0], enemy[1], enemy_width, enemy_height)):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break

    # Remove enemies that are off the screen
    lives -= len(enemies) - len([enemy for enemy in enemies if enemy[1] < screen_height])
    
    if lives <= 0:
        game_over()

    enemies = [enemy for enemy in enemies if enemy[1] < screen_height]

    # Check if all enemies are defeated to start a new wave
    if not enemies and current_time - enemy_timer > enemy_spawn_time * 2:
        start_new_wave()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the player
    pygame.draw.rect(screen, (0, 128, 255), (player_x, player_y, player_width, player_height))

    # Draw the bullets
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 255), (bullet[0], bullet[1], bullet_width, bullet_height))

    # Draw the enemies
    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), (enemy[0], enemy[1], enemy_width, enemy_height))

    # Display wave, lives, and score
    font = pygame.font.Font(None, 36)
    wave_text = font.render('Wave: ' + str(wave), True, (255, 255, 255))
    lives_text = font.render('Lives: ' + str(lives), True, (255, 255, 255))
    score_text = font.render('Score: ' + str(score), True, (255, 255, 255))
    screen.blit(wave_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    screen.blit(score_text, (10, 90))

    # Update the display
    pygame.display.flip()

 
    clock.tick(60)

