import pygame
import sys
import random
import numpy as np
import pickle
import math

# ── Load trained model and scaler ──────────────────────────────
print("Loading BCI model...")
model  = pickle.load(open('data/model.pkl', 'rb'))
scaler = pickle.load(open('data/scaler.pkl', 'rb'))

print("Loading EEG features...")
X_features = np.load('data/X_features.npy')
print(f"Loaded {len(X_features)} EEG epochs for gameplay.")

LABEL_MAP     = {1: "IDLE", 2: "LEFT", 3: "RIGHT"}
ALT_LABEL_MAP = {0: "IDLE", 1: "LEFT", 2: "RIGHT"}

pygame.init()

# ── Layout: game area (600) + side panel (220) ──────────────────
GAME_W, GAME_H = 600, 500
PANEL_W        = 220
WIDTH          = GAME_W + PANEL_W
HEIGHT         = GAME_H

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NeuroGest BCI Game")
clock  = pygame.time.Clock()

background = pygame.image.load("Gamebackground.jpeg")
background = pygame.transform.scale(background, (GAME_W, GAME_H))

# ── Colors ──────────────────────────────────────────────────────
WHITE      = (220, 220, 220)
BLUE       = (30,  100, 200)
DARK       = (1,   15,  30)
RED        = (220, 50,  50)
YELLOW     = (255, 180, 0)
PURPLE     = (200, 100, 255)
CYAN       = (0,   255, 255)
NEON_GREEN = (57,  255, 20)
PANEL_BG   = (8,   12,  28)
PANEL_LINE = (30,  60,  120)
ORANGE     = (255, 140, 0)

font       = pygame.font.SysFont("Arial", 22, bold=True)
big_font   = pygame.font.SysFont("Arial", 46, bold=True)
small_font = pygame.font.SysFont("Arial", 16, bold=True)
tiny_font  = pygame.font.SysFont("Arial", 13)

# ── Brainwave history ────────────────────────────────────────────
WAVE_HISTORY       = 80
wave_data          = [0.0] * WAVE_HISTORY
confidence_history = [0.0] * WAVE_HISTORY

def draw_background():
    screen.blit(background, (0, 0))

def reset_game():
    return GAME_W // 2, GAME_H - 80, 0, [], [], 3

def create_obstacle():
    return [random.randint(50, GAME_W - 50), 0]

def create_coin():
    return [random.randint(50, GAME_W - 50), 0]

def get_bci_command(epoch_index):
    idx     = epoch_index % len(X_features)
    feature = X_features[idx].reshape(1, -1)
    feature = scaler.transform(feature)
    label   = model.predict(feature)[0]

    confidence = 0.0
    if hasattr(model, "predict_proba"):
        proba      = model.predict_proba(feature)[0]
        confidence = float(np.max(proba))
    elif hasattr(model, "decision_function"):
        dec = model.decision_function(feature)[0]
        if hasattr(dec, '__len__'):
            exp_dec    = np.exp(dec - np.max(dec))
            proba      = exp_dec / exp_dec.sum()
            confidence = float(np.max(proba))
        else:
            confidence = min(1.0, abs(float(dec)) / 3.0)

    command = LABEL_MAP.get(label, ALT_LABEL_MAP.get(label, "IDLE"))
    return command, label, confidence

def draw_panel(command, confidence, epoch_index, score):
    pygame.draw.rect(screen, PANEL_BG, (GAME_W, 0, PANEL_W, HEIGHT))
    pygame.draw.line(screen, CYAN, (GAME_W, 0), (GAME_W, HEIGHT), 2)

    y = 15
    title = small_font.render("BRAIN MONITOR", True, CYAN)
    screen.blit(title, (GAME_W + PANEL_W//2 - title.get_width()//2, y))
    y += 25
    pygame.draw.line(screen, PANEL_LINE, (GAME_W+10, y), (GAME_W+PANEL_W-10, y), 1)
    y += 10

    # Command
    cmd_color = {"LEFT": ORANGE, "RIGHT": NEON_GREEN, "IDLE": PURPLE, "FORWARD": CYAN}.get(command, WHITE)
    lbl = tiny_font.render("COMMAND", True, (150,150,180))
    screen.blit(lbl, (GAME_W+10, y)); y += 16
    arrow = {"LEFT": "◀  LEFT", "RIGHT": "RIGHT  ▶", "IDLE": "●  IDLE", "FORWARD": "▲  FWD"}.get(command, command)
    cmd_text = font.render(arrow, True, cmd_color)
    screen.blit(cmd_text, (GAME_W + PANEL_W//2 - cmd_text.get_width()//2, y)); y += 34

    pygame.draw.line(screen, PANEL_LINE, (GAME_W+10, y), (GAME_W+PANEL_W-10, y), 1); y += 10

    # Confidence bar
    lbl2 = tiny_font.render("MODEL CONFIDENCE", True, (150,150,180))
    screen.blit(lbl2, (GAME_W+10, y)); y += 16
    bar_w  = PANEL_W - 20
    bar_h  = 18
    bar_x  = GAME_W + 10
    filled = int(bar_w * confidence)
    bar_col = NEON_GREEN if confidence > 0.7 else (YELLOW if confidence > 0.4 else RED)
    pygame.draw.rect(screen, (30,30,60),  (bar_x, y, bar_w, bar_h), border_radius=5)
    if filled > 0:
        pygame.draw.rect(screen, bar_col, (bar_x, y, filled, bar_h), border_radius=5)
    pygame.draw.rect(screen, PANEL_LINE,  (bar_x, y, bar_w, bar_h), 1, border_radius=5)
    pct = tiny_font.render(f"{confidence*100:.1f}%", True, WHITE)
    screen.blit(pct, (bar_x + bar_w//2 - pct.get_width()//2, y+2)); y += 30

    pygame.draw.line(screen, PANEL_LINE, (GAME_W+10, y), (GAME_W+PANEL_W-10, y), 1); y += 10

    # Live EEG graph
    lbl3 = tiny_font.render("LIVE EEG SIGNAL", True, (150,150,180))
    screen.blit(lbl3, (GAME_W+10, y)); y += 16
    graph_w = PANEL_W - 20
    graph_h = 70
    gx, gy  = GAME_W+10, y
    pygame.draw.rect(screen, (10,15,35), (gx, gy, graph_w, graph_h))
    pygame.draw.rect(screen, PANEL_LINE, (gx, gy, graph_w, graph_h), 1)
    mid_y = gy + graph_h//2
    pygame.draw.line(screen, (30,50,80), (gx, mid_y), (gx+graph_w, mid_y), 1)
    if len(wave_data) > 1:
        pts = []
        for i, val in enumerate(wave_data):
            px = gx + int(i * graph_w / len(wave_data))
            py = mid_y - int(val * (graph_h//2 - 5))
            py = max(gy+2, min(gy+graph_h-2, py))
            pts.append((px, py))
        if len(pts) > 1:
            pygame.draw.lines(screen, NEON_GREEN, False, pts, 2)
    y += graph_h + 10

    pygame.draw.line(screen, PANEL_LINE, (GAME_W+10, y), (GAME_W+PANEL_W-10, y), 1); y += 10

    # Confidence trend
    lbl4 = tiny_font.render("CONFIDENCE TREND", True, (150,150,180))
    screen.blit(lbl4, (GAME_W+10, y)); y += 16
    th = 50
    tx, ty = GAME_W+10, y
    pygame.draw.rect(screen, (10,15,35), (tx, ty, graph_w, th))
    pygame.draw.rect(screen, PANEL_LINE, (tx, ty, graph_w, th), 1)
    if len(confidence_history) > 1:
        pts2 = []
        for i, val in enumerate(confidence_history):
            px = tx + int(i * graph_w / len(confidence_history))
            py = ty + th - int(val * (th-4)) - 2
            py = max(ty+2, min(ty+th-2, py))
            pts2.append((px, py))
        if len(pts2) > 1:
            pygame.draw.lines(screen, CYAN, False, pts2, 2)
    y += th + 10

    pygame.draw.line(screen, PANEL_LINE, (GAME_W+10, y), (GAME_W+PANEL_W-10, y), 1); y += 10

    # Stats
    for txt, val in [("Epoch", epoch_index), ("Score", score), ("Total", len(X_features))]:
        t = tiny_font.render(f"{txt} : {val}", True, (180,180,200))
        screen.blit(t, (GAME_W+10, y)); y += 18

    y += 6
    # Pulsing dot
    pulse = int(math.sin(pygame.time.get_ticks() * 0.005) * 127 + 128)
    pygame.draw.circle(screen, (0, pulse, 0), (GAME_W+15, y+6), 6)
    sig = tiny_font.render("EEG SIGNAL ACTIVE", True, NEON_GREEN)
    screen.blit(sig, (GAME_W+28, y))

def draw_start_screen():
    draw_background()
    dark = pygame.Surface((GAME_W, GAME_H), pygame.SRCALPHA)
    dark.fill((0,0,0,120))
    screen.blit(dark, (0,0))
    shadow = big_font.render("NeuroGest", True, (0,0,0))
    title  = big_font.render("NeuroGest", True, (100,200,255))
    screen.blit(shadow, (GAME_W//2 - title.get_width()//2 + 3, 53))
    screen.blit(title,  (GAME_W//2 - title.get_width()//2, 50))
    pygame.draw.line(screen, (100,200,255), (150,105), (450,105), 2)
    sub = font.render("~ Press ENTER to Begin ~", True, YELLOW)
    screen.blit(sub, (GAME_W//2 - sub.get_width()//2, 120))
    pygame.draw.rect(screen, (10,10,40),    (70,160,460,230), border_radius=25)
    pygame.draw.rect(screen, (100,200,255), (70,160,460,230), 2, border_radius=25)
    ctrl = font.render("BCI Controlled Mode", True, (100,200,255))
    screen.blit(ctrl, (GAME_W//2 - ctrl.get_width()//2, 172))
    pygame.draw.line(screen, (100,200,255), (150,200), (450,200), 1)
    for i, (txt, col) in enumerate([
        ("Game controlled by EEG Brain Signals!", CYAN),
        ("SVM Model predicts: LEFT / RIGHT / IDLE", WHITE),
        ("Collect YELLOW coins!  Avoid RED blocks!", YELLOW),
        ("You have 3 lives!", RED)
    ]):
        t = small_font.render(txt, True, col)
        screen.blit(t, (GAME_W//2 - t.get_width()//2, 210 + i*30))
    draw_panel("IDLE", 0.0, 0, 0)
    pygame.display.flip()

def draw_gameover_screen(score):
    draw_background()
    dark = pygame.Surface((GAME_W, GAME_H), pygame.SRCALPHA)
    dark.fill((0,0,0,120))
    screen.blit(dark, (0,0))
    over    = big_font.render("GAME OVER", True, RED)
    sc      = font.render(f"Your Score: {score}", True, YELLOW)
    restart = font.render("Press ENTER to Play Again", True, YELLOW)
    pygame.draw.rect(screen, DARK, (100,120,400,250))
    screen.blit(over,    (GAME_W//2 - over.get_width()//2, 150))
    screen.blit(sc,      (GAME_W//2 - sc.get_width()//2, 250))
    screen.blit(restart, (GAME_W//2 - restart.get_width()//2, 310))
    draw_panel("IDLE", 0.0, 0, score)
    pygame.display.flip()

def draw_lives(lives):
    for i in range(lives):
        pygame.draw.circle(screen, RED, (20 + i*30, 40), 10)

# ── Game state ───────────────────────────────────────────────────
STATE    = "start"
player_x, player_y, score, obstacles, coins, lives = reset_game()
SPEED          = 8
command        = "IDLE"
confidence     = 0.0
obstacle_speed = 3
invincible     = 0
epoch_index    = 0
frame_counter  = 0
FRAMES_PER_EPOCH = 30
wave_tick        = 0

print("Game ready! Press ENTER in the game window to start.")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if STATE in ("start", "gameover"):
                    player_x, player_y, score, obstacles, coins, lives = reset_game()
                    obstacle_speed = 3
                    invincible = epoch_index = frame_counter = 0
                    STATE = "playing"
            if event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

    if STATE == "start":
        draw_start_screen()

    elif STATE == "playing":
        frame_counter += 1
        wave_tick     += 1

        if frame_counter >= FRAMES_PER_EPOCH:
            command, raw_label, confidence = get_bci_command(epoch_index)
            epoch_index  += 1
            frame_counter = 0
            print(f"Epoch {epoch_index} | Label: {raw_label} | Cmd: {command} | Conf: {confidence*100:.1f}%")

        # Update wave
        norm_val  = math.sin(wave_tick * 0.3) * 0.5 + math.sin(wave_tick * 0.7) * 0.3
        norm_val += random.uniform(-0.1, 0.1)
        norm_val  = max(-1.0, min(1.0, norm_val))
        wave_data.append(norm_val)
        if len(wave_data) > WAVE_HISTORY: wave_data.pop(0)
        confidence_history.append(confidence)
        if len(confidence_history) > WAVE_HISTORY: confidence_history.pop(0)

        # Move player
        if   command == "LEFT":    player_x -= SPEED
        elif command == "RIGHT":   player_x += SPEED
        elif command == "FORWARD": player_y -= SPEED
        else:
            if player_y < GAME_H - 80: player_y += 2

        player_x = max(20, min(GAME_W-20, player_x))
        player_y = max(20, min(GAME_H-20, player_y))

        score         += 1
        obstacle_speed = 3 + score // 500

        if random.randint(1, 120) == 1: obstacles.append(create_obstacle())
        if random.randint(1, 20)  == 1: coins.append(create_coin())

        for o in obstacles: o[1] += obstacle_speed
        for c in coins:     c[1] += 3

        obstacles = [o for o in obstacles if o[1] < GAME_H]
        coins     = [c for c in coins     if c[1] < GAME_H]

        player_rect = pygame.Rect(player_x-20, player_y-20, 40, 40)
        if invincible > 0: invincible -= 1

        new_obs = []
        for o in obstacles:
            if pygame.Rect(o[0]-20, o[1]-20, 40, 40).colliderect(player_rect) and invincible == 0:
                lives -= 1; invincible = 60
                if lives <= 0: STATE = "gameover"
            else:
                new_obs.append(o)
        obstacles = new_obs

        new_coins = []
        for c in coins:
            if pygame.Rect(c[0]-15, c[1]-15, 30, 30).colliderect(player_rect):
                score += 100
            else:
                new_coins.append(c)
        coins = new_coins

        # Draw
        draw_background()
        for o in obstacles:
            pygame.draw.rect(screen, RED, (o[0]-20, o[1]-20, 40, 40))
        for c in coins:
            pygame.draw.circle(screen, YELLOW, (c[0], c[1]), 15)

        if invincible > 0 and invincible % 10 < 5:
            pygame.draw.rect(screen, WHITE, (player_x-20, player_y-20, 40, 40))
        else:
            pygame.draw.rect(screen, (0,60,180), (player_x-23, player_y-23, 46, 46), border_radius=8)
            pygame.draw.rect(screen, BLUE,       (player_x-20, player_y-20, 40, 40), border_radius=6)
            pygame.draw.rect(screen, CYAN,       (player_x-20, player_y-20, 40, 40), 2, border_radius=6)

        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        draw_lives(lives)
        draw_panel(command, confidence, epoch_index, score)

        pygame.display.flip()
        clock.tick(60)

    elif STATE == "gameover":
        draw_gameover_screen(score)