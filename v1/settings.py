import pygame
import math
###################################################
####################GAME SETUPS####################
###################################################
TITLE = '11HEAD SOCCER2'
WIDTH = 700
HEIGHT = 330
FPS = 100
MARGIN = 50
GRAV = (math.pi ,0.7)

AIR_f = 0.6
AIR_m = 0.2
ELASTICITY = 0.65


###################################################
####################BALL SETUPS####################
###################################################
BALL_a = 0.1
BALL_m = 10
BALL_r = 15
BALL_f = -0.3
###################################################
####################PLAYER SETUPS##################
###################################################
PLAYER_a = 0.5
PLAYER_f = -0.15
PLAYER_length = 20
PLAYER_j = -15
PLAYER_m = 100
PLAYER_r = 25
###################################################
####################AI SETUPS######################
###################################################
AI_a = 0.5
AI_f = -0.15
AI_length = 20
AI_j = -15
AI_m = 100
AI_r = 25
#ZLATAN 
zlatan1=pygame.image.load('zlatan/zlatan1.png')   
zlatan2=pygame.image.load('zlatan/zlatan2.png')   
zlatan3=pygame.image.load('zlatan/zlatan3.png')   
zlatanL = [zlatan1,zlatan2,zlatan3]
zImageList = [pygame.transform.scale(image,(PLAYER_r*2,PLAYER_r*2)) for image in zlatanL]

#SON

#POGBA
pogba1 = pygame.image.load('pogba/pogba1.png')
pogba2 = pygame.image.load('pogba/pogba2.png')
pogba3 = pygame.image.load('pogba/pogba3.png')
pogbaL = [pogba1,pogba2,pogba3]
pImageList = [pygame.transform.scale(image,(50,60)) for image in pogbaL]
#HAZARD

#MESSI

#NEYMAR

#KDB

#RONALDIHNO

###################################################
####################IMAGES SETUPS##################
###################################################
iGoal = pygame.image.load('images/goal.png')
iBall =pygame.image.load('images/ball.png')
iGP1=pygame.image.load('images/goalpost1.png')
iGP2=pygame.image.load('images/goalpost2.png')    
fieldImage = pygame.image.load('images/background.png')
woodImage = pygame.image.load('images/wood_art.jpg')
ballImage = pygame.transform.scale(iBall,(BALL_r*2,BALL_r*2))
goalImage = pygame.transform.scale(iGoal,(400,200))
gpImage1 =  pygame.transform.scale(iGP1,(int(WIDTH//4),int(WIDTH//4)))
gpImage2 =  pygame.transform.scale(iGP2,(int(WIDTH//4),int(WIDTH//4)))