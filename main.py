from multiprocessing.connection import wait
from tkinter import Y
import turtle
import pygame
from pygame import mixer
import random
import cv2 as cv
import mediapipe as mp

def jack_health(jackX, jackY, enemies, jackHealth):
    hitboxXMin = jackX
    hitboxXMax = jackX + 48
    hitboxYMin = jackY
    hitboxYMax = jackY + 48
    
    enemiesXMin = enemies['x']
    enemiesXMax = enemies['x'] + 48
    enemiesYMin = enemies['y']
    enemiesYMax = enemies['y'] + 48
    hit = False
    if ((enemiesXMax > hitboxXMin and enemiesXMax < hitboxXMax) or (enemiesXMin > hitboxXMin and enemiesXMin < hitboxXMax)) and (enemiesYMax>hitboxYMin and enemiesYMin<hitboxYMax):
        hit = True
        #print('hit')
        jackHealth-=10
    return jackHealth, hit
    
        
    
def fist_hit(fistX, fistY, enemies):
    hitboxXMin = fistX
    hitboxXMax = fistX + 100
    hitboxYMin = fistY
    hitboxYMax = fistY + 100
    
    enemiesXMin = enemies['x']
    enemiesXMax = enemies['x'] + 48
    enemiesYMin = enemies['y']
    enemiesYMax = enemies['y'] + 48
    hit = False
    if ((enemiesXMax > hitboxXMin and enemiesXMax < hitboxXMax) or (enemiesXMin > hitboxXMin and enemiesXMin < hitboxXMax)) and enemiesYMax>hitboxYMin:
        hit = True
        lizardHitSound.play()
    return hit


def lizzard_spawn(rand, enemies):
    num = random.randint(0, 100)
    
    if num < rand:
        
        lizzardX = random.randint(0, SCREEN_X)
        lizzardY = -96
        lizzard = {'lizzard':pygame.image.load("./lizzard.png"), 'x':lizzardX, 'y':lizzardY}
        lizzard['lizzard'] = pygame.transform.scale(lizzard['lizzard'], (48, 48))
        screen.blit(lizzard['lizzard'], (lizzard['x'], lizzard['y']))
        enemies.append(lizzard)
    return enemies



# Intialize the pygame
pygame.init()
pygame.mixer.init()

# create the screen
SCREEN_X = 800
SCREEN_Y = 600
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

MIDDLE_X = int(SCREEN_X / 2)
MIDDLE_Y = int(SCREEN_Y / 2)

jack = pygame.image.load("./jack.png")
jack = pygame.transform.flip(jack, True, False)
jack = pygame.transform.scale(jack, (48, 48))
jackX = int(SCREEN_X / 2)
jackY = int(SCREEN_Y - 200)
screen.blit(jack, (jackX, jackY))
jackHealth = 100

beanstalk = pygame.image.load("./beanstalk.png")
beanstalkY = MIDDLE_Y - 1000

fist = pygame.image.load("./fist.png")
fist = pygame.transform.scale(fist, (100, 100))

enemies = []

lizardHitSound = pygame.mixer.Sound("./death.ogg")
lizzard_a = pygame.image.load("./lizzard.png")
lizzard_a = pygame.transform.scale(lizzard_a, (48, 48))
lizzardX = int(SCREEN_X / 2)
lizzardY = int(-96)

###HAND TRACKING###
capture = cv.VideoCapture(0)
capture.set(cv.CAP_PROP_FRAME_WIDTH, 800)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, 600)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
######
running = True
jackMovingLeft = False
jackMovingRight = False

#Text init
BLUE = (255, 255, 255)
font = pygame.font.SysFont('freesansbold.tff', 72)
text = font.render(f"Health: {str(jackHealth)}", True, BLUE)

handX = 0
handY = 0

score = 0

height = 0

firstRun = True

story1 = pygame.image.load("./backStory1.png")
story2 = pygame.image.load("./backStory2.png")
story3 = pygame.image.load("./backStory3.png")


while running:
    
    '''
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_a):
                jackMovingLeft = True
            if(event.key == pygame.K_d):
                jackMovingRight = True
    
    if(jackMovingLeft):
        jackX -=1 
        
    if(jackMovingRight):
        jackX +=1 
    '''     

    if(firstRun):
        cutsceneX = 0
        cutsceneY = 0
        screen.blit(story1, (cutsceneX, cutsceneY))
        for event in pygame.event.get():
            if(event.type !)




    


    ###HAND TRACKING###

    success, img = capture.read()
    
    img = cv.flip(img, 1)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    results = hands.process(imgRGB)
    
    if results.multi_hand_landmarks:
        for handLm in results.multi_hand_landmarks:
            
            for id, lm in enumerate(handLm.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                if id == 9:
                    handX = cx
                    handY = cy
            
            mpDraw.draw_landmarks(img, handLm, mpHands.HAND_CONNECTIONS)


    cv.imshow("Hand Tracking", img)

    if(cv.waitKey(1) & 0xFF == ord('q')):
        break
    #############



    #SKY
    screen.fill((135, 206, 235))

    #GRASS
    pygame.draw.rect(screen, (0, 154, 23), pygame.Rect(0, MIDDLE_Y + height, SCREEN_X, SCREEN_Y))

    screen.blit(beanstalk, (MIDDLE_X - 150, beanstalkY + height))

    
    screen.blit(jack, (jackX, jackY))
    screen.blit(fist, (handX, handY))
    
    
    level = 1 + score*.1
    
    text = font.render(f"Health: {str(jackHealth)}", True, BLUE)
    
    enemies = lizzard_spawn(10, enemies)
    inds = []
    for ind, enemie in enumerate(enemies):
        speedX = random.randint(1, 50)*level
        speedY = random.randint(1, 50)*level
        rand = random.randint(0, 1)
        if rand:
            num = -1
        else:
            num = 1
        enemie['x'] += num*10*.5*level
        enemie['y'] += 10*level*.5
        jackHealth, hit_jack = jack_health(jackX, jackY, enemie, jackHealth)
        hit_fist = fist_hit(handX, handY, enemie)
        
        score += int(hit_fist)
        
        if hit_fist or hit_jack:
            inds.append(ind)
        screen.blit(enemie['lizzard'], (enemie['x'], enemie['y']))
    for i in range(len(inds)-1, -1, -1):
        enemies.pop(inds[i])
        
    for i in range(len(enemies)-1, -1, -1):
        if enemies[i]['y']>SCREEN_X:
            enemies.pop(i)
            
    screen.blit(text, (20, 20))
    pygame.display.update()
    height += 0.5*level
    firstRun = False

    if(height == 1020):
        screen.fill((0, 0, 0))
        win = font.render("YOU WIN ", True, (255, 0, 0))
        pygame.time.wait(5000)
        break

    pygame.time.wait(35)
    
    win = False
    
    if height >= 1050:
        win = True
        break
    
if win:
    screen.fill((0, 0, 0))
    win = font.render("YOU WIN ", True, (255, 0, 0))
    screen.blit(win, (int(SCREEN_X/2), int(SCREEN_Y/2)))
    pygame.display.update()
    pygame.time.wait(100000)

    
capture.release()
cv.destroyAllWindows()