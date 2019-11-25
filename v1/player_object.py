import pygame
from settings import *
vec = pygame.math.Vector2
class Player(pygame.sprite.Sprite):
  # ,r,x,y,,speed,power,skill,color
    def __init__(self, game): #color changed to character later
        pygame.sprite.Sprite.__init__(self)
        self.game= game
        self.image = pygame.Surface((PLAYER_r*2,PLAYER_r*2), pygame.SRCALPHA)
        self.rect= self.image.get_rect()
        self.imageL = zlatanL
        self.r = PLAYER_r
        self.mass = PLAYER_m 
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.pos = vec(WIDTH/4, HEIGHT/2)
        self.spriteCounter = 0   
        self.length = PLAYER_r #change later
        self.angle = 0
        self.power = 10 #change later
        self.right = True
        self.isJumping = False

    def update(self):
        self.acc = vec(0,2)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.pos.x+self.length < WIDTH:
            self.spriteCounter = (1 + self.spriteCounter) % len(self.imageL)
            self.acc.x = PLAYER_a
            self.right = True
        elif keys[pygame.K_LEFT] and self.pos.x-self.length > 0:
            self.spriteCounter = (1 + self.spriteCounter) % len(self.imageL)
            self.acc.x = -PLAYER_a
            self.right = False
        if keys[pygame.K_UP]:
            self.jump() 
        if keys[pygame.K_SPACE]:
            self.kick()
        if not self.game.scored:
            self.acc.x += self.vel.x*PLAYER_f
            self.vel += self.acc
            self.pos.x += 2*self.vel.x
            self.pos.y += self.vel.y
            if self.pos.x-self.length < 0:
                self.pos.x = self.length
            elif self.pos.x+self.length > WIDTH:
                self.pos.x = WIDTH-self.length
        self.rect.center = self.pos
      

    def getDistance(self,pos1,pos2):
      return ((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)**0.5

    # def touch(self):
    #   playerPos = self.rect.center
    #   ballPos = self.game.ball.rect.center
    #   distance = self.getDistance(playerPos,ballPos)
    #   if distance <=100:
    #     print('old',self.game.ball.vel)
    #     newVel = 2*(2*PLAYER_m*self.vel)/(PLAYER_m+BALL_m)
    #     print('new',newVel)
    #     self.game.ball.vel = newVel
    def kick(self):
      playerPos = self.pos
      ballPos = self.game.ball.pos
      distance = self.getDistance(playerPos,ballPos)
      if distance <=70:
        self.game.ball.speed = (BALL_m-PLAYER_m)/(BALL_m+PLAYER_m)*self.game.ball.speed + 2*PLAYER_m/(PLAYER_m+BALL_m)*self.vel.magnitude()*self.power

    def jump(self):
    #only jump when on platform
        self.pos.y += 1
        onFloor = pygame.sprite.collide_rect(self, self.game.field)
        self.pos.y -= 1
        if onFloor:
            self.vel.y = PLAYER_j
            self.isJumping = True
        self.isJumping = False

        


