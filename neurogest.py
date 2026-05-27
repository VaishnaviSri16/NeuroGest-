import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NeuroGest Game")
clock = pygame.time.Clock()

background = pygame.image.load("Gamebackground.jpg - copy.jpeg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

WHITE = (220, 220, 220)
BLUE = (30, 100, 200)
GREEN = (0, 200, 100)
DARK = (1, 15, 30)
RED = (220, 50, 50)
YELLOW = (255, 180, 0)
PURPLE = (200, 100, 255)

font = pygame.font.SysFont("Arial", 24, bold=True)
big_font = pygame.font.SysFont("Arial", 48, bold=True)
small_font = pygame.font.SysFont("Arial", 18, bold=True)

def reset_game():
    return WIDTH // 2, HEIGHT - 80, 0, [], [], 3

def create_obstacle():
    x = random.randint(50, WIDTH - 50)
    return [x, 0]

def create_coin():
    x = random.randint(50, WIDTH - 50)
    return [x, 0]

def draw_start_screen():
    screen.blit(background, (0, 0))
    
    # Title with shadow effect
    shadow = big_font.render("NeuroGest", True, (0, 0, 0))
    title = big_font.render("NeuroGest", True, (100, 200, 255))
    screen.blit(shadow, (WIDTH//2 - title.get_width()//2 + 3, 53))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
    
    # Decorative lines
    pygame.draw.line(screen, (100, 200, 255), (150, 105), (450, 105), 2)
    
    # Subtitle
    sub = font.render("~ Press ENTER to Begin ~", True, YELLOW)
    screen.blit(sub, (WIDTH//2 - sub.get_width()//2, 120))
    
    # Controls box
    pygame.draw.rect(screen, (10, 10, 40), (70, 160, 460, 230), border_radius=25)
    pygame.draw.rect(screen, (100, 200, 255), (70, 160, 460, 230), 2, border_radius=25)
    
    ctrl = font.render("Controls", True, (100, 200, 255))
    screen.blit(ctrl, (WIDTH//2 - ctrl.get_width()//2, 172))
    
    pygame.draw.line(screen, (100, 200, 255), (150, 200), (450, 200), 1)
    
    info1 = small_font.render("UP Arrow = Move Forward", True, WHITE)
    info2 = small_font.render("LEFT Arrow = Move Left", True, WHITE)
    info3 = small_font.render("RIGHT Arrow = Move Right", True, WHITE)
    info4 = small_font.render("Collect YELLOW coins!  Avoid RED blocks!", True, YELLOW)
    info5 = small_font.render("You have 3 lives!", True, RED)
    
    screen.blit(info1, (WIDTH//2 - info1.get_width()//2, 210))
    screen.blit(info2, (WIDTH//2 - info2.get_width()//2, 235))
    screen.blit(info3, (WIDTH//2 - info3.get_width()//2, 260))
    screen.blit(info4, (WIDTH//2 - info4.get_width()//2, 300))
    screen.blit(info5, (WIDTH//2 - info5.get_width()//2, 335))
    
    pygame.display.flip()

def draw_gameover_screen(score):
    screen.blit(background, (0, 0))
    over = big_font.render("GAME OVER", True, RED)
    sc = font.render(f"Your Score: {score}", True, YELLOW)
    restart = font.render("Press ENTER to Play Again", True, YELLOW)
    pygame.draw.rect(screen, DARK, (100, 120, 400, 250))
    screen.blit(over, (WIDTH//2 - over.get_width()//2, 150))
    screen.blit(sc, (WIDTH//2 - sc.get_width()//2, 250))
    screen.blit(restart, (WIDTH//2 - restart.get_width()//2, 310))
    pygame.display.flip()

def draw_lives(lives):
    for i in range(lives):
        pygame.draw.circle(screen, RED, (20 + i * 30, 40), 10)

STATE = "start"
player_x, player_y, score, obstacles, coins, lives = reset_game()
SPEED = 5
command = "IDLE"
obstacle_speed = 3
invincible = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if STATE == "start" or STATE == "gameover":
                    player_x, player_y, score, obstacles, coins, lives = reset_game()
                    obstacle_speed = 3
                    invincible = 0
                    STATE = "playing"

    if STATE == "start":
        draw_start_screen()

    elif STATE == "playing":
        keys = pygame.key.get_pressed()

        moving_forward = keys[pygame.K_UP]
        moving_left = keys[pygame.K_LEFT]
        moving_right = keys[pygame.K_RIGHT]

        if moving_forward and moving_left:
            player_x -= SPEED
            player_y -= SPEED
            command = "LEFT + FORWARD"
        elif moving_forward and moving_right:
            player_x += SPEED
            player_y -= SPEED
            command = "RIGHT + FORWARD"
        elif moving_forward:
            player_y -= SPEED
            command = "FORWARD"
        elif moving_left:
            player_x -= SPEED
            command = "LEFT"
        elif moving_right:
            player_x += SPEED
            command = "RIGHT"
        else:
            command = "IDLE"
            if player_y < HEIGHT - 80:
             player_y += 3

        player_x = max(20, min(WIDTH - 20, player_x))
        player_y = max(20, min(HEIGHT - 20, player_y))

        score += 1
        obstacle_speed = 3 + score // 500

        if random.randint(1, 120) == 1:
            obstacles.append(create_obstacle())

        if random.randint(1, 45) == 1:
            coins.append(create_coin())

        for obs in obstacles:
            obs[1] += obstacle_speed

        for coin in coins:
            coin[1] += 3

        obstacles = [obs for obs in obstacles if obs[1] < HEIGHT]
        coins = [coin for coin in coins if coin[1] < HEIGHT]

        player_rect = pygame.Rect(player_x - 20, player_y - 20, 40, 40)

        if invincible > 0:
            invincible -= 1

        new_obstacles = []
        for obs in obstacles:
            obs_rect = pygame.Rect(obs[0] - 20, obs[1] - 20, 40, 40)
            if player_rect.colliderect(obs_rect) and invincible == 0:
                lives -= 1
                invincible = 60
                if lives <= 0:
                    STATE = "gameover"
            else:
                new_obstacles.append(obs)
        obstacles = new_obstacles

        new_coins = []
        for coin in coins:
            coin_rect = pygame.Rect(coin[0] - 15, coin[1] - 15, 30, 30)
            if player_rect.colliderect(coin_rect):
                score += 50
            else:
                new_coins.append(coin)
        coins = new_coins

        screen.blit(background, (0, 0))

        if invincible > 0 and invincible % 10 < 5:
            pygame.draw.rect(screen, WHITE, (player_x - 20, player_y - 20, 40, 40))
        else:
            pygame.draw.rect(screen, BLUE, (player_x - 20, player_y - 20, 40, 40))

        for obs in obstacles:
            pygame.draw.rect(screen, RED, (obs[0] - 20, obs[1] - 20, 40, 40))

        for coin in coins:
            pygame.draw.circle(screen, YELLOW, (coin[0], coin[1]), 15)

        score_text = font.render(f"Score: {score}", True, WHITE)
        command_text = small_font.render(f"Command: {command}", True, PURPLE)
        screen.blit(score_text, (10, 10))
        screen.blit(command_text, (WIDTH - 220, 10))
        draw_lives(lives)

        pygame.display.flip()
        clock.tick(60)

    elif STATE == "gameover":
        draw_gameover_screen(score)