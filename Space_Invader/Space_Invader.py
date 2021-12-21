import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
WIDTH = 1200
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("bg4.jpg")

mixer.music.load("background2.wav")
mixer.music.play(-1)

# Title and logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Game initials
bg_colour = 0, 0, 0

# Player
playerImg = pygame.image.load("spaceship.png")
playerX = 1200/2
playerY = 500
playerX_change = 0
player_speed = 6

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_speed = []
enemyY_change = []
num_of_enemies = 12

for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_speed.append(4)
    enemyY_change.append(40)

# Bullet
# ready = You cant see the bullet on the screen
# fire = the bullet is currently moving
bulletImg = pygame.image.load("bullet2.png")
bulletX = 0
bulletY = 480
bulletX_speed = 0
bulletY_change = 5
bullet_state = "ready"

#SCORE
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

#GAME OVER TEXT

over_font = pygame.font.Font("freesansbold.ttf", 32)


def show_score(x, y):
    score =font.render("Score :" + str(score_value), True, (59,255,255))
    screen.blit(score,(x, y))


def game_over_text():
    over_text = font.render("GAME OVER, YOUR SCORE: " +str (score_value), True, (0,250,0))
    screen.blit(over_text, (200,250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX,2) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    screen.fill(bg_colour)
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Initializing the keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -player_speed
            if event.key == pygame.K_RIGHT:
                playerX_change = player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for the boundaries of spaceship
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= WIDTH - 64:
        playerX = WIDTH - 64

    # Enemy Movement
    for i in range(num_of_enemies):

        #GAME OVER
        if enemyY[i] > 420:
            for j in range (num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_speed[i]
        if enemyX[i] <= 0:
            enemyX_speed[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= WIDTH - 64:
            enemyX_speed[i] = -1
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion3.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
