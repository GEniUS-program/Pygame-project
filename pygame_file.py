import pygame
import sys
import json
import random


# Initialize PyGame
pygame.init()
pygame.mixer.init()

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
player_model = pygame.image.load('./data/images/player.png')
player_width = 50
player_height = 60
player_model = pygame.transform.scale(player_model, (player_width, player_height))
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
enemy_model = pygame.image.load('./data/images/enemy.png')
enemy_model = pygame.transform.rotate(enemy_model, 180)
enemy_width = 50
enemy_height = 50
enemy_model = pygame.transform.scale(enemy_model, (enemy_width, enemy_height))
enemy_speed = 2
enemies = []

# Spawn an enemy every enewy_spawn_time milliseconds
enemy_timer = 0
enemy_spawn_time = 2000 / difficulty_coef

# Upgrades
upgrades = {
    "Slower Enemies": {"cost": 1000, "purchased": False, "active": False},
    "Double Damage": {"cost": 1500, "purchased": False, "active": False},
    "Triple Bullets": {"cost": 3000, "purchased": False, "active": False},
    "Speed Boost": {"cost": 5000, "purchased": False, "active": False},
}

shoot_sound = pygame.mixer.Sound('./data/sounds/shoot.wav')
hit_sound = pygame.mixer.Sound('./data/sounds/hit.wav')
explosion_sound = pygame.mixer.Sound('./data/sounds/explosion.wav')
win_sound = pygame.mixer.Sound('./data/sounds/win.ogg')
lose_sound = pygame.mixer.Sound('./data/sounds/lose.wav')
got_hit_sound = pygame.mixer.Sound('./data/sounds/got_hit.wav')
music1 = pygame.mixer.Sound('./data/sounds/music1.mp3')
# Collision detection function

class Planet:
    def __init__(self, x, y, speed, planet):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(f'./data/images/planet0{planet}.png')
        size = random.randint(50, 100)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.image = pygame.transform.rotate(self.image, random.randint(-10, 10))

    def update(self):
        self.y += self.speed
        if self.y > screen_height:
            self.y = 0
            self.x = random.randint(0, screen_width)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

planets = []
for _ in range(10):
    planets.append(Planet(random.randint(0, screen_width), 0, random.sample([0.5, 0.6, 0.7, 0.8, 0.9, 1], 1)[0], random.randint(0, 9)))

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

def get_upgrades():
    global upgrades, player_damage, bullet_mult, enemy_speed, player_speed
    for upgrade, details in upgrades.items():
        if details["active"] == True:
            if upgrade == "Slower Enemies":
                enemy_speed /= 1.5
            elif upgrade == "Double Damage":
                player_damage *= 2
            elif upgrade == "Triple Bullets":
                bullet_mult *= 3
            elif upgrade == "Speed Boost":
                player_speed *= 2

def game_over(state=0):
    global music1, lose_sound, upgrades, game_state, max_score, wave, enemies_destroyed, score, lives, player_damage, bullet_mult, enemy_speed, player_speed, enemies, bullets, player_x, player_y, bullet_width, bullet_height, bullet_speed, enemy_width, enemy_height, enemy_speed, enemy_timer, enemy_spawn_time, enemies_count
    music1.stop()
    lose_sound.play()
    if score > max_score:
        max_score = score
    write_user_data()
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
    read_user_data()

    # Player settings
    player_speed = 5
    player_damage = 50

    # Bullet settings
    bullet_speed = 7
    bullet_mult = 1
    bullets = []

    # Enemy settings
    enemy_speed = 2
    enemies = []

    get_upgrades()

    # Spawn an enemy every enewy_spawn_time milliseconds
    enemy_timer = 0
    enemy_spawn_time = 2000 / difficulty_coef
    pygame.time.wait(2000)
    game_state = MAIN_MENU
    

def start_new_wave():
    global wave, difficulty_coef, lives, enemy_spawn_time, enemies_destroyed, enemies_count, enemy_speed
    win_sound.play()
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
    play_text = font.render("Играть", True, WHITE)
    upgrade_text = font.render("Улучшения", True, WHITE)
    exit_text = font.render("Выйти", True, WHITE)
    screen.blit(title_text, (screen_width // 2 -
                120, screen_height // 2 - 100))
    screen.blit(play_text, (screen_width // 2 - 30, screen_height // 2 - 30))
    screen.blit(upgrade_text, (screen_width // 2 - 60, screen_height // 2))
    screen.blit(exit_text, (screen_width // 2 - 30, screen_height // 2 + 30))
    pygame.display.flip()


def draw_upgrades_screen():
    screen.fill(BLACK)
    title_text = font.render("Улучшения", True, WHITE)
    screen.blit(title_text, (screen_width // 2 - 60, 50))
    y_offset = 100
    for upgrade, details in upgrades.items():
        cost = details["cost"]
        active = details["active"]
        upgrade_text = small_font.render(
            f"{upgrade} (Ограничение по очкам: {cost})", True, WHITE)
        status_text = small_font.render(
            "Активно" if active else "Не активно", True, GREEN if active else RED)
        screen.blit(upgrade_text, (screen_width // 2 - 200, y_offset))
        screen.blit(status_text, (screen_width // 2 + 200, y_offset))
        y_offset += 30
    back_text = font.render("Назад", True, WHITE)
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
            write_user_data()
            pygame.quit()
            sys.exit()


def handle_upgrades_screen_click(mouse_pos):
    global max_score, player_damage, bullet_mult, enemy_speed, player_speed
    x, y = mouse_pos
    y_offset = 100
    for upgrade, details in upgrades.items():
        if screen_width // 2 - 100 <= x <= screen_width // 2 + 100 and y_offset <= y <= y_offset + 20:
            if not details["purchased"] and max_score >= details["cost"]:
                details["purchased"] = True
                details["active"] = True  # Activate the upgrade by default
                apply_upgrade_effect(upgrade, True)
            elif details["purchased"]:
                # Toggle the upgrade's active state
                details["active"] = not details["active"]
                apply_upgrade_effect(upgrade, details["active"])
        y_offset += 30
    if screen_width // 2 - 30 <= x <= screen_width // 2 + 30 and screen_height - 70 <= y <= screen_height - 30:
        global game_state
        game_state = MAIN_MENU


def apply_upgrade_effect(upgrade, activate):
    global player_damage, bullet_mult, enemy_speed, player_speed
    if upgrade == "Медленнее враги (1.5x)":
        enemy_speed /= 1.5 if activate else 1.5
    elif upgrade == "Двойной урон (2х)":
        player_damage *= 2 if activate else 0.5
    elif upgrade == "Больше снарядов (3x)":
        if activate:
            bullet_mult *= 3
        else:
            bullet_mult = int(bullet_mult / 3)
    elif upgrade == "Улучшение скорости (2x)":
        if activate:
            player_speed *= 2
        else:
            player_speed /= 2


def start_game():
    global music1, game_state, wave, enemies_destroyed, score, lives, difficulty_coef
    music1.play()
    game_state = PLAYING
    difficulty_coef = 1
    wave = 1
    enemies_destroyed = 0
    score = 0
    lives = 5
    bullets.clear()
    enemies.clear()
    get_upgrades()

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
                shoot_sound.play()
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

        for bullet in bullets:
            bullet[1] -= bullet_speed
        bullets = [bullet for bullet in bullets if bullet[1] > 0]

        # Update enemy positions and spawn new ones
        current_time = pygame.time.get_ticks()
        if current_time - enemy_timer > enemy_spawn_time:
            enemy_x = random.randint(0, screen_width - enemy_width)
            enemy_y = -enemy_height
            health = random.randint(80, 101) * difficulty_coef
            temp = 0
            if 5 <= wave and random.randint(1, 20) == 1:
                temp = enemy_model
                enemy_model = pygame.transform.scale(enemy_model, (100, 100))
                health = 100 * 2 * difficulty_coef ** 2
            enemies.append([enemy_x, enemy_y, health, enemy_model])  # Add enemy health
            enemy_model = temp if temp != 0 else enemy_model 
            enemy_timer = current_time

        for enemy in enemies:
            enemy[1] += enemy_speed

        # Check for collisions and apply damage
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if check_collision((bullet[0], bullet[1], bullet_width, bullet_height),
                                   (enemy[0], enemy[1], enemy[3].get_width(), enemy[3].get_height())):
                    hit_sound.play()
                    bullets.remove(bullet)
                    enemy[2] -= player_damage  # Reduce enemy health
                    if enemy[2] <= 0:  # If enemy health reaches zero
                        explosion_sound.play()
                        enemies.remove(enemy)
                        add = 10
                        if enemy[3].get_width() == 100:
                            add *= (2 * difficulty_coef) // 1
                        score += add
                        enemies_destroyed += 1
                    break

        # Remove enemies that are off the screen
        for enemy in enemies[:]:
            if enemy[1] > screen_height:
                got_hit_sound.play()
                lives -= 1
                enemies.remove(enemy)
                if lives <= 0:
                    game_over()

        # Check if the required number of enemies are destroyed to start a new wave
        if enemies_destroyed >= enemies_count:
            start_new_wave()

        # Fill the screen with black
        screen.fill((0, 0, 0))

        #Update the planets
        for planet in planets:
            planet.update()

        # Draw planets
        for planet in planets:
            planet.draw(screen)

        # Draw the player
        screen.blit(player_model, (player_x, player_y))

        # Draw the bullets
        for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 255),
                             (bullet[0], bullet[1], bullet_width, bullet_height))

        prev_health = 100
        for enemy in enemies:
            screen.blit(enemy[3], (enemy[0], enemy[1]))
            # Draw enemy health bar
            health_bar_width = (enemy_width * (enemy[2] / (100 * difficulty_coef))) if enemy[3].get_width() != 100 else (enemy_width * (enemy[2] / (100 * 2 * difficulty_coef ** 2)))
            pygame.draw.rect(screen, (0, 255, 0),
                             (enemy[0], enemy[1] - 10, health_bar_width, 5))
            prev_health = enemy[2]

        # Display wave, lives, and score
        font = pygame.font.Font(None, 36)
        wave_text = font.render('Волна: ' + str(wave), True, (255, 255, 255))
        lives_text = font.render('Жизни: ' + str(lives), True, (255, 255, 255))
        score_text = font.render('Счёт: ' + str(score), True, (255, 255, 255))
        enemies_destroyed_text = font.render('Врагов уничтожено: ' + str(
            enemies_destroyed) + '/' + str(enemies_count), True, (255, 255, 255))
        screen.blit(wave_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(score_text, (10, 90))
        screen.blit(enemies_destroyed_text, (10, 130))

        # Update the display
        pygame.display.flip()
    # Cap the frame rate at 60 FPS
    clock.tick(60)
