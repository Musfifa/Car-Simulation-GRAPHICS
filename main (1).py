import pygame
import random

# Initialize
pygame.init()

# Screen
WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Car Simulation Project")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (70, 70, 70)
GREEN = (40, 170, 70)
BLUE = (50, 150, 255)
YELLOW = (255, 220, 0)
RED = (255, 60, 60)

# Font
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 22)

# ------------------- Game Variables -------------------
car_speed = 7
car_width = 80
car_height = 140

# Player car starting position
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - 170

# Road divider animation
line_y = 0

# Enemy cars list: each enemy = [x, y, speed]
enemy_cars = []

# Score
score = 0

# Game states
game_over = False
paused = False

# ------------------- Helper Functions -------------------
def reset_game():
    """Reset all game variables to initial state."""
    global car_x, car_y, line_y, enemy_cars, score, game_over, paused

    car_x = WIDTH // 2 - car_width // 2
    car_y = HEIGHT - 170
    line_y = 0
    score = 0
    game_over = False
    paused = False

    # Reset enemy cars
    enemy_cars.clear()
    for _ in range(5):
        x = random.randint(230, 690)          # within road boundaries
        y = random.randint(-600, -100)
        speed = random.randint(5, 10)
        enemy_cars.append([x, y, speed])

# Initialize game
reset_game()

# ------------------- Main Game Loop -------------------
running = True
while running:
    clock.tick(60)

    # ---- Event Handling ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard shortcuts for restart and pause (only when game is not over)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:          # Press R to restart (always works)
                reset_game()
            if not game_over and event.key == pygame.K_p:   # Press P to toggle pause (only during active game)
                paused = not paused

    # ---- Game Over screen ----
    if game_over:
        screen.fill(GREEN)
        # Draw road (just for background)
        pygame.draw.rect(screen, GRAY, (200, 0, 600, HEIGHT))
        pygame.draw.line(screen, WHITE, (200, 0), (200, HEIGHT), 5)
        pygame.draw.line(screen, WHITE, (800, 0), (800, HEIGHT), 5)

        # Display messages
        game_over_text = font.render("GAME OVER!", True, YELLOW)
        restart_text = small_font.render("Press R to Restart", True, WHITE)
        quit_text = small_font.render("Press ESC to Quit", True, WHITE)

        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 60))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2))
        screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 40))

        pygame.display.update()

        # Check for quit key during game over
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
        continue   # Skip the rest of the loop while game_over is True

    # ---- Paused screen ----
    if paused:
        screen.fill(GREEN)
        # Draw road (optional but keeps visuals)
        pygame.draw.rect(screen, GRAY, (200, 0, 600, HEIGHT))
        pygame.draw.line(screen, WHITE, (200, 0), (200, HEIGHT), 5)
        pygame.draw.line(screen, WHITE, (800, 0), (800, HEIGHT), 5)

        pause_text = font.render("PAUSED", True, YELLOW)
        resume_text = small_font.render("Press P to Resume", True, WHITE)
        screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 30))
        screen.blit(resume_text, (WIDTH//2 - resume_text.get_width()//2, HEIGHT//2 + 20))

        pygame.display.update()
        continue   # Don't update game logic when paused

    # ---- Active Game Logic (not game_over and not paused) ----
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x -= car_speed
    if keys[pygame.K_RIGHT]:
        car_x += car_speed

    # Road boundaries (keep car inside the road)
    min_x = 220
    max_x = 720
    if car_x < min_x:
        car_x = min_x
    if car_x > max_x:
        car_x = max_x

    # ---- Draw everything ----
    screen.fill(GREEN)
    # Road
    pygame.draw.rect(screen, GRAY, (200, 0, 600, HEIGHT))
    # Road side lines
    pygame.draw.line(screen, WHITE, (200, 0), (200, HEIGHT), 5)
    pygame.draw.line(screen, WHITE, (800, 0), (800, HEIGHT), 5)

    # Animated road divider lines
    line_y += 10
    if line_y >= 60:
        line_y = 0
    for i in range(0, HEIGHT, 60):
        pygame.draw.rect(screen, WHITE, (490, i + line_y, 20, 40))

    # Player car
    pygame.draw.rect(screen, BLUE, (car_x, car_y, car_width, car_height))
    pygame.draw.rect(screen, BLACK, (car_x + 15, car_y + 20, 50, 40))
    # Wheels
    pygame.draw.circle(screen, BLACK, (car_x + 10, car_y + 30), 10)
    pygame.draw.circle(screen, BLACK, (car_x + 70, car_y + 30), 10)
    pygame.draw.circle(screen, BLACK, (car_x + 10, car_y + 110), 10)
    pygame.draw.circle(screen, BLACK, (car_x + 70, car_y + 110), 10)

    # Enemy cars: update positions and draw
    for enemy in enemy_cars:
        enemy[1] += enemy[2]   # move downward

        # Draw enemy car
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], car_width, car_height))
        pygame.draw.rect(screen, BLACK, (enemy[0] + 15, enemy[1] + 20, 50, 40))

        # Reset enemy when off screen (bottom)
        if enemy[1] > HEIGHT:
            enemy[1] = random.randint(-400, -100)
            enemy[0] = random.randint(230, 690)
            enemy[2] = random.randint(5, 10)
            score += 1

        # Collision detection
        player_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        enemy_rect = pygame.Rect(enemy[0], enemy[1], car_width, car_height)
        if player_rect.colliderect(enemy_rect):
            game_over = True   # Switch to game over state instead of quitting
            # Break out of the loop to stop further collision checks
            break

    # ---- UI Text ----
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    instruction = font.render("LEFT / RIGHT Arrow Keys", True, WHITE)
    screen.blit(instruction, (250, 20))

    pause_hint = small_font.render("P = Pause  |  R = Restart", True, WHITE)
    screen.blit(pause_hint, (WIDTH - pause_hint.get_width() - 20, HEIGHT - 40))

    pygame.display.update()

pygame.quit()