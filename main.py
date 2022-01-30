import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
SCREEN_X = 800
SCREEN_Y = 600
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

MIDDLE_X = int(SCREEN_X / 2)
MIDDLE_Y = int(SCREEN_Y / 2)

#INSERT FILE PATH
jack = pygame.image.load("./jack.png")
jack = pygame.transform.scale(jack, (48, 48))
jackX = int(SCREEN_X / 2)
jackY = int(SCREEN_Y - 96)
screen.blit(jack, (jackX, jackY))
jackHealth = 100

enemies = []

lizzard_a = pygame.image.load("./lizzard.png")
lizzard_a = pygame.transform.scale(lizzard_a, (48, 48))
lizzardX = int(SCREEN_X / 2)
lizzardY = int(96)

running = True
while running:
        
    if event.type == KEYDOWN:
        if()
    
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            running = False
            
    
    
    #SKY
    screen.fill((135, 206, 235))

    #GRASS
    pygame.draw.rect(screen, (0, 154, 23), pygame.Rect(0, MIDDLE_X, SCREEN_ ))

    
    screen.blit(jack, (jackX, jackY))
    jackX += 1 
    
    pygame.display.update()
    pygame.time.wait(35)