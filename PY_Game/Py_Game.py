import pygame
import sys
import random

pygame.init()

# SCREEN DIMENSION:
WIDTH = 1250
HEIGHT = 720
# PLAYERS DETAILS:
PLAYER1_GREY = 50, 55, 77
PLAYER2_YELLOW = 255, 250, 150
player1_pos = 800, 670
player2_pos = 400, 695
player1_size = 50
player2_radius_size = 25
# ENEMY DETAILS:
ENEMY_PURPLE = 100, 25, 80
ENEMY_YELLOW = 255, 250, 150
enemy_size = 20
enemy_pos = [random.randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]
SPEED = 5
# OTHER DETAILS:
BACKGROUND = 155, 155, 155
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

SCORE = 0
myFont = pygame.font.SysFont("monospace", 35, bold=5, italic=5)
FONT_BLACK = 0, 0, 0

game_over = False
pygame.display.set_caption("BLOCK GAME")


def set_level(SCORE, SPEED):
    if SCORE < 20:
        SPEED = 10
    elif SCORE < 40:
        SPEED = 12
    elif SCORE < 60:
        SPEED = 15
    elif SCORE < 80:
        SPEED = 18
    else:
        SPEED = 20
    return SPEED



def GAME_SCORE(SCORE):
    text1 = ("SCORE:" + str(SCORE))
    label1 = myFont.render(text1, 1, FONT_BLACK)
    screen.blit(label1, (WIDTH - 300, 40))


def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 100 and delay < 0.20:
        x_pos = random.randint(0, WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, ENEMY_YELLOW, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
        pygame.draw.circle(screen, ENEMY_PURPLE, (enemy_pos[0], enemy_pos[1]), enemy_size)


def update_enemy_position(enemy_list, SCORE):
    for index, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and (enemy_pos[1] < HEIGHT):
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(index)
            SCORE += 1
    return SCORE


def collision_check(enemy_list):
    for enemy_pos in enemy_list:
        if detect_collision_player1(player1_pos, enemy_pos):
            return True
    return False


def detect_collision_player1(player1_pos, enemy_pos):
    p1_x = player1_pos[0]
    p1_y = player1_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]
    if (e_x >= p1_x and (e_x < p1_x + player1_size)) or (p1_x >= e_x and (p1_x < e_x + enemy_size)):
        # collision check on left and right position.
        if (e_y >= p1_y and (e_y < p1_y + player1_size)) or (p1_y >= e_y and (p1_y < e_y + enemy_size)):
            # collision check on up and down position.
            return True
    return False


while not game_over:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            x = player1_pos[0]
            y = player1_pos[1]

            if event.key == pygame.K_LEFT:
                x -= player1_size
            elif event.key == pygame.K_RIGHT:
                x += player1_size
            elif event.key == pygame.K_UP:
                y -= player1_size
            elif event.key == pygame.K_DOWN:
                y += player1_size
            player1_pos = [x, y]
            break
    screen.fill(BACKGROUND)

    # Calling all Functions
    drop_enemies(enemy_list)
    SCORE = update_enemy_position(enemy_list, SCORE)
    GAME_SCORE(SCORE)
    SPEED = set_level(SCORE, SPEED)
    if collision_check(enemy_list):
        game_over = True
        break
    draw_enemies(enemy_list)

    clock.tick(30)
    # Defining the player shape and color
    # pygame.draw.rect(Surface, Color, (Position WIDTH, Position HEIGHT, Player LENGTH, Player BREADTH
    # pygame.draw.circle(screen, PLAYER2_YELLOW, (player2_pos[0], player2_pos[1]), player2_radius_size)
    pygame.draw.rect(screen, PLAYER1_GREY, (player1_pos[0], player1_pos[1], player1_size, player1_size))
    pygame.display.update()


