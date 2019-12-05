import pygame
from settings import *
import game
vec = pygame.math.Vector2
class Player(pygame.sprite.Sprite):
  # ,r,x,y,,speed,power,skill,color
    def __init__(self,game,player): #color changed to character later
        pygame.sprite.Sprite.__init__(self)
        self.r = PLAYER_r
        self.mass = PLAYER_m 
        self.game= game
        self.image = pygame.Surface((PLAYER_r*2,PLAYER_r*2), pygame.SRCALPHA)
        self.rect= self.image.get_rect()
        self.player = player
        self.playerL = charDict[self.player][0]
        self.playerFlippedL = charDict[self.player][1]
        self.power = charDict[self.player][2]
        self.speed = charDict[self.player][3]
        self.jumpMag = charDict[self.player][4]
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.pos = vec(WIDTH/4, HEIGHT/2)
        self.spriteCounter = 0   
        self.angle = 0
        self.right = True

    def update(self):
        self.acc = vec(0,2)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.pos.x+self.r < WIDTH:
            self.spriteCounter = (1 + self.spriteCounter) % len(self.playerL)
            self.acc.x = self.speed
            self.right = True
        elif keys[pygame.K_LEFT] and self.pos.x-self.r > 0:
            self.spriteCounter = (1 + self.spriteCounter) % len(self.playerL)
            self.acc.x = -self.speed
            self.right = False
        if keys[pygame.K_UP]:
            self.jump() 
        self.acc.x += self.vel.x*PLAYER_f
        self.vel += self.acc
        self.pos.x += 2*self.vel.x
        self.pos.y += self.vel.y
        if self.pos.x-self.r < 0:
            self.pos.x = self.r
        elif self.pos.x+self.r > WIDTH:
            self.pos.x = WIDTH-self.r
        self.rect.center = self.pos

    def getDistance(self,pos1,pos2):
      return ((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)**0.5

    def jump(self):
    #only jump when on platform
        self.pos.y += 1
        onFloor = pygame.sprite.collide_rect(self, self.game.field)
        self.pos.y -= 1
        if onFloor:
            self.vel.y = self.jumpMag
            self.isJumping = True
        self.isJumping = False

        


