import pygame
import random
import math
from pygame import mixer

# initialize the pygame before creating any game then only it works otherwise it wint work
pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))  # 800=width and 600= width

# caption and background
background = pygame.image.load('background.png')  # the image extension should be png while creating dont forget

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)  # to play in loop

# TITLE AND ICON ON WINDOW
pygame.display.set_caption("Space Invadors")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)  # till here we laernt how to give name and logo

# player
playerImg = pygame.image.load('spaceship.png')
playerX = 370  # this and next step will decide where the space ship would lie in the screen at present it is at middle
playerY = 480  # change values and observe the changes
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))  # this instruction  and  next instruction decides that where we have to put enemy
    enemyY.append(random.randint(50, 150))  # beacause we are using random it appears in different positions
    enemyX_change.append(0.8)
    enemyY_change.append(10)

# BULLET
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"  # ready - you cannot see the bullet #fire- the bullet is currently moving

# Font
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf',64)


def show_score(x,y):
    score = font.render("score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text( ):
    over_text =over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200,250))

def player(x, y):
    screen.blit(playerImg, (x, y))  # blit means draw


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # RBG RED BLUE GREEN (EVERY COLOUR IN THE WORLD ACHIEVED BY MIXING THESE IN DIFFERET PROPORTIONS
    screen.fill((0, 0, 0))  # here we are setting the screen colour
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:  # IF WE PRESSING CONTINUOUSLY WITH OUT RLEASING
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:  # IF WE RELEASE THE KEY AFTER PRESSING
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # checking boundaries of spaceship so it doesnt goout of boundaries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736



    # enemy movement
    for i in range(num_of_enemies):

        # GAME OVER
        if enemyY[i] > 200:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
           enemyX_change[i] = 0.6
           enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
           enemyX_change[i] = -0.6
           enemyY[i] += enemyY_change[i]
        # COLLISION
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # BULLET MOVEMENT
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()  # after adding the colour we are updating the window
