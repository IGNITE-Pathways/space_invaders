import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Load Splash Screen
splash_screen = pygame.image.load('splash.png')
splash_screen = pygame.transform.scale(splash_screen, (screen_width, screen_height))

def show_splash_screen():
    screen.blit(splash_screen, (0, 0))
    pygame.display.update()
    pygame.time.delay(2000)  # Wait for 2 seconds

# Player
player_img = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_x_change = 0
player_speed = 3
player_lives = 5

# Enemy
enemy_imgs = ['enemy1.png', 'enemy2.png', 'enemy3.png']
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_bullet_img = pygame.image.load('enemy_bullet.png')
enemy_bullet_x = []
enemy_bullet_y = []
enemy_bullet_y_change = []
enemy_bullet_state = []
enemy_shoot_timer = []
num_of_enemies = 3

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load(random.choice(enemy_imgs)))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(random.randint(1, 2))  # Slowing down the enemy speed
    enemy_y_change.append(20)
    enemy_bullet_x.append(0)
    enemy_bullet_y.append(enemy_y[i])
    enemy_bullet_y_change.append(1)  # Slower enemy bullet speed
    enemy_bullet_state.append("ready")  # "ready" - you can't see the bullet on the screen, "fire" - the bullet is moving
    enemy_shoot_timer.append(random.randint(1000, 3000))  # Random shooting timer

# Bullet
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"  # "ready" - you can't see the bullet on the screen, "fire" - the bullet is moving

# Explosion
explosion_img = pygame.image.load('explosion.png')
explosion_x = 0
explosion_y = 0
explosion_counter = 0

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Timer
start_ticks = pygame.time.get_ticks()  # Start timer

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def show_lives(x, y):
    lives = font.render("Lives: " + str(player_lives), True, (255, 255, 255))
    screen.blit(lives, (x, y))

def show_timer(x, y):
    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000  # Convert to seconds
    timer = font.render("Time: " + str(elapsed_time), True, (255, 255, 255))
    screen.blit(timer, (x, y))
    return elapsed_time

def game_over_text(final_time):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    time_text = font.render("Final Time: " + str(final_time) + "s", True, (255, 255, 255))
    screen.blit(time_text, (280, 320))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 2, y + 20))

def fire_enemy_bullet(x, y, i):
    global enemy_bullet_state
    enemy_bullet_state[i] = "fire"
    screen.blit(enemy_bullet_img, (x + 16, y + 10))

def show_explosion(x, y):
    screen.blit(explosion_img, (x, y))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    return distance < 27

def is_player_hit(enemy_bullet_x, enemy_bullet_y, player_x, player_y):
    distance = math.sqrt(math.pow(enemy_bullet_x - player_x, 2) + math.pow(enemy_bullet_y - player_y, 2))
    return distance < 27

# Show splash screen before starting the game
show_splash_screen()

# Game Loop
running = True
game_over = False
player_hit_timer = 0
final_time = 0
while running:
    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            # If keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -player_speed
                if event.key == pygame.K_RIGHT:
                    player_x_change = player_speed
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bullet_x = player_x
                        fire_bullet(bullet_x, bullet_y)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0

    if not game_over:
        # Checking for boundaries of spaceship
        player_x += player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        # Enemy Movement
        for i in range(num_of_enemies):
            enemy_x[i] += enemy_x_change[i]
            if enemy_x[i] <= 0:
                enemy_x_change[i] = 2  # Adjusted speed
                enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] >= 736:
                enemy_x_change[i] = -2  # Adjusted speed
                enemy_y[i] += enemy_y_change[i]

            # Enemy Shooting
            if enemy_bullet_state[i] == "ready" and random.randint(0, 1000) < 2:  # Random chance to shoot
                enemy_bullet_x[i] = enemy_x[i]
                enemy_bullet_y[i] = enemy_y[i]
                fire_enemy_bullet(enemy_bullet_x[i], enemy_bullet_y[i], i)

            if enemy_bullet_state[i] == "fire":
                fire_enemy_bullet(enemy_bullet_x[i], enemy_bullet_y[i], i)
                enemy_bullet_y[i] += enemy_bullet_y_change[i]

            if enemy_bullet_y[i] > 600:
                enemy_bullet_state[i] = "ready"

            # Collision with bullet
            collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
            if collision:
                bullet_y = 480
                bullet_state = "ready"
                score_value += 1
                explosion_x, explosion_y = enemy_x[i], enemy_y[i]
                explosion_counter = 30  # Display explosion for a short duration
                enemy_x[i] = random.randint(0, 735)
                enemy_y[i] = random.randint(50, 150)

            # Collision with player
            player_hit = is_player_hit(enemy_bullet_x[i], enemy_bullet_y[i], player_x, player_y)
            if player_hit:
                if pygame.time.get_ticks() - player_hit_timer > 1000:  # Add delay after hit
                    player_lives -= 1
                    player_hit_timer = pygame.time.get_ticks()
                    enemy_bullet_state[i] = "ready"
                    if player_lives <= 0:
                        player_lives = 0
                        final_time = show_timer(screen_width - 150, 10)
                        for j in range(num_of_enemies):
                            enemy_y[j] = 2000
                        game_over = True
                        break

            enemy(enemy_x[i], enemy_y[i], i)

        # Bullet Movement
        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"

        player(player_x, player_y)
        show_score(text_x, text_y)
        show_lives(text_x, text_y + 40)  # Display lives below the score
        final_time = show_timer(screen_width - 150, 10)  # Display timer on the top-right

        # Display explosion for a short duration
        if explosion_counter > 0:
            show_explosion(explosion_x, explosion_y)
            explosion_counter -= 1

    if game_over:
        game_over_text(final_time)

    pygame.display.update()
