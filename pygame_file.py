import pygame
import sys
import json
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

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 128, 255)

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Game states
MAIN_MENU = 0
PLAYING = 1
UPGRADES = 2
game_state = MAIN_MENU

# Game logic
wave = 1
difficulty_coef = 1
lives = 5
enemies_count = 10
enemies_destroyed = 0
score = 0
max_score = 0

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
enemy_height = 50
enemy_speed = 2
enemies = []

# Spawn an enemy every enewy_spawn_time milliseconds
enemy_timer = 0
enemy_spawn_time = 2000 / difficulty_coef

# Upgrades
upgrades = {
    "Slower Enemies": {"cost": 1000, "active": False},
    "Double Damage": {"cost": 1500, "active": False},
    "Triple Bullets": {"cost": 3000, "active": False},
    "Speed Boost": {"cost": 5000, "active": False},
}

# Collision detection function


def check_collision(rect1, rect2):
    return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))


def read_user_data():
    global max_score
    with open('./data/user.json', 'r') as f:
        data = json.load(f)
    max_score = int(data['score'])


def write_user_data():
    global max_score
    with open('./data/user.json', 'w') as f:
        json.dump({'score': str(max_score)}, f)


def game_over(state=0):
    global game_state, max_score, wave, enemies_destroyed, score, lives, player_damage, bullet_mult, enemy_speed, player_speed, enemies, bullets, player_x, player_y, bullet_width, bullet_height, bullet_speed, enemy_width, enemy_height, enemy_speed, enemy_timer, enemy_spawn_time
    if score > max_score:
        max_score = score
    screen.fill(BLACK)
    if state == 0:
        game_over_text = font.render("Game Over", True, WHITE)
    else:
        game_over_text = font.render("Самоуничтожился", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(game_over_text, (screen_width //
                2 - 70, screen_height // 2 - 50))
    screen.blit(score_text, (screen_width // 2 - 50, screen_height // 2))
    pygame.display.flip()
    wave = 1
    difficulty_coef = 1
    lives = 5
    enemies_count = 10
    enemies_destroyed = 0
    score = 0
    max_score = 0

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
    enemy_height = 50
    enemy_speed = 2
    enemies = []

    # Spawn an enemy every enewy_spawn_time milliseconds
    enemy_timer = 0
    enemy_spawn_time = 2000 / difficulty_coef
    pygame.time.wait(2000)
    game_state = MAIN_MENU
    write_user_data()


def start_new_wave():
    global wave, difficulty_coef, lives, enemy_spawn_time, enemies_destroyed, enemies_count, enemy_speed
    wave += 1
    difficulty_coef += 0.2
    lives += 1
    enemies_count += 5
    enemies_destroyed = 0
    enemy_spawn_time = 2000 / difficulty_coef
    enemy_speed = 2 * difficulty_coef
    enemies.clear()
    bullets.clear()
    upgrade_player()


def upgrade_player():
    global player_speed, bullet_speed, bullet_mult
    player_speed += 1
    bullet_speed += 1
    bullet_mult += 1


def draw_main_menu():
    screen.fill(BLACK)
    title_text = font.render("Simple Shooter Game", True, WHITE)
    play_text = font.render("Play", True, WHITE)
    upgrade_text = font.render("Upgrade", True, WHITE)
    exit_text = font.render("Exit", True, WHITE)
    screen.blit(title_text, (screen_width // 2 -
                120, screen_height // 2 - 100))
    screen.blit(play_text, (screen_width // 2 - 30, screen_height // 2 - 30))
    screen.blit(upgrade_text, (screen_width // 2 - 60, screen_height // 2))
    screen.blit(exit_text, (screen_width // 2 - 30, screen_height // 2 + 30))
    pygame.display.flip()


def draw_upgrades_screen():
    screen.fill(BLACK)
    title_text = font.render("Upgrades", True, WHITE)
    screen.blit(title_text, (screen_width // 2 - 60, 50))
    y_offset = 100
    for upgrade, details in upgrades.items():
        cost = details["cost"]
        active = details["active"]
        upgrade_text = small_font.render(
            f"{upgrade} (Cost: {cost})", True, WHITE)
        status_text = small_font.render(
            "Active" if active else "Inactive", True, GREEN if active else RED)
        screen.blit(upgrade_text, (screen_width // 2 - 100, y_offset))
        screen.blit(status_text, (screen_width // 2 + 150, y_offset))
        y_offset += 30
    back_text = font.render("Back", True, WHITE)
    screen.blit(back_text, (screen_width // 2 - 30, screen_height - 50))
    pygame.display.flip()


def handle_main_menu_click(mouse_pos):
    x, y = mouse_pos
    if screen_width // 2 - 30 <= x <= screen_width // 2 + 30:
        if screen_height // 2 - 30 <= y <= screen_height // 2:
            # Play
            start_game()
        elif screen_height // 2 <= y <= screen_height // 2 + 30:
            # Upgrade
            global game_state
            game_state = UPGRADES
        elif screen_height // 2 + 30 <= y <= screen_height // 2 + 60:
            # Exit
            pygame.quit()
            sys.exit()


def handle_upgrades_screen_click(mouse_pos):
    global max_score, player_damage, bullet_mult, enemy_speed, player_speed
    x, y = mouse_pos
    y_offset = 100
    for upgrade, details in upgrades.items():
        if screen_width // 2 - 100 <= x <= screen_width // 2 + 100 and y_offset <= y <= y_offset + 20:
            if max_score >= details["cost"]:
                details["active"] = not details["active"]  # Toggle activation
                if details["active"]:
                    if upgrade == "Slower Enemies":
                        enemy_speed /= 1.5
                    elif upgrade == "Double Damage":
                        player_damage *= 2
                    elif upgrade == "Triple Bullets":
                        bullet_mult *= 3
                    elif upgrade == "Speed Boost":
                        player_speed *= 1.5  # Increase player speed
                else:
                    if upgrade == "Slower Enemies":
                        enemy_speed *= 1.5
                    elif upgrade == "Double Damage":
                        player_damage /= 2
                    elif upgrade == "Triple Bullets":
                        bullet_mult = 1
                    elif upgrade == "Speed Boost":
                        player_speed /= 1.5  # Reset player speed
            # break
    if screen_width // 2 - 30 <= x <= screen_width // 2 + 30 and screen_height - 70 <= y <= screen_height - 30:
        global game_state
        game_state = MAIN_MENU


def start_game():
    global game_state, wave, enemies_destroyed, score, lives
    game_state = PLAYING
    wave = 1
    enemies_destroyed = 0
    score = 0
    lives = 5
    bullets.clear()
    enemies.clear()


# Main game loop
while True:
    read_user_data()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_state == MAIN_MENU:
                handle_main_menu_click(mouse_pos)
            elif game_state == UPGRADES:
                handle_upgrades_screen_click(mouse_pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Spawn bullets side by side based on bullet_mult
                for i in range(bullet_mult):
                    bullet_x = player_x + \
                        (i - (bullet_mult - 1) / 2) * \
                        (bullet_width + 5)  # Adjust spacing
                    bullet_y = player_y
                    bullets.append([bullet_x, bullet_y])
            if event.key == pygame.K_u:
                upgrade_player()
            if event.key == pygame.K_ESCAPE and game_state == PLAYING:
                game_over(1)
                game_state = MAIN_MENU
    if game_state == MAIN_MENU:
        draw_main_menu()
    elif game_state == UPGRADES:
        draw_upgrades_screen()
    elif game_state == PLAYING:
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed

        # Spawn enemies
            # Update bullet positions
        for bullet in bullets:
            bullet[1] -= bullet_speed
        bullets = [bullet for bullet in bullets if bullet[1] > 0]

        # Update enemy positions and spawn new ones
        current_time = pygame.time.get_ticks()
        if current_time - enemy_timer > enemy_spawn_time:
            enemy_x = random.randint(0, screen_width - enemy_width)
            enemy_y = -enemy_height
            enemies.append([enemy_x, enemy_y, random.randint(
                50, 101) * difficulty_coef])  # Add enemy health
            enemy_timer = current_time

        for enemy in enemies:
            enemy[1] += enemy_speed

        # Check for collisions and apply damage
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if check_collision((bullet[0], bullet[1], bullet_width, bullet_height),
                                   (enemy[0], enemy[1], enemy_width, enemy_height)):
                    bullets.remove(bullet)
                    enemy[2] -= player_damage  # Reduce enemy health
                    if enemy[2] <= 0:  # If enemy health reaches zero
                        enemies.remove(enemy)
                        score += 10
                        enemies_destroyed += 1
                    break

        # Remove enemies that are off the screen
        for enemy in enemies[:]:
            if enemy[1] > screen_height:
                lives -= 1
                enemies.remove(enemy)
                if lives <= 0:
                    game_over()

        # Check if the required number of enemies are destroyed to start a new wave
        if enemies_destroyed >= enemies_count:
            start_new_wave()

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the player
        pygame.draw.rect(screen, (0, 128, 255), (player_x,
                         player_y, player_width, player_height))

        # Draw the bullets
        for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 255),
                             (bullet[0], bullet[1], bullet_width, bullet_height))

        # Draw the enemies
        for enemy in enemies:
            pygame.draw.rect(screen, (255, 0, 0),
                             (enemy[0], enemy[1], enemy_width, enemy_height))
            # Draw enemy health bar
            health_bar_width = enemy_width * \
                (enemy[2] / (100 * difficulty_coef))  # Scale health bar
            pygame.draw.rect(screen, (0, 255, 0),
                             (enemy[0], enemy[1] - 10, health_bar_width, 5))

        # Display wave, lives, and score
        font = pygame.font.Font(None, 36)
        wave_text = font.render('Wave: ' + str(wave), True, (255, 255, 255))
        lives_text = font.render('Lives: ' + str(lives), True, (255, 255, 255))
        score_text = font.render('Score: ' + str(score), True, (255, 255, 255))
        enemies_destroyed_text = font.render('Enemies Destroyed: ' + str(
            enemies_destroyed) + '/' + str(enemies_count), True, (255, 255, 255))
        screen.blit(wave_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(score_text, (10, 90))
        screen.blit(enemies_destroyed_text, (10, 130))

        # Update the display
        pygame.display.flip()
    # Cap the frame rate at 60 FPS
    clock.tick(60)
