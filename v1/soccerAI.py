import pygame
from settings import *
import math
vec = pygame.math.Vector2

class AI(pygame.sprite.Sprite):
  # ,r,x,y,,speed,power,skill,color
    def __init__(self, game, player): #color changed to character later
        pygame.sprite.Sprite.__init__(self)
        self.r = AI_r
        self.mass = AI_m
        self.game= game
        self.image = pygame.Surface((AI_r*2,AI_r*2),pygame.SRCALPHA)
        self.imageL = pogbaL
        self.rect= self.image.get_rect()
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.pos = vec(3*WIDTH/4, HEIGHT/2)
        self.length = PLAYER_length
        self.tanAI = math.atan2(self.vel.y,self.vel.x)
        self.attackMode = None
        self.hasBall = False
        self.spriteCounter = 0
      
    def checkAttackMode(self):
        if (self.distance(self.game.player.pos, self.game.ball.pos) >= self.distance(self.pos,self.game.ball.pos)):
            if self.pos.x < self.game.ball.pos.x:
                self.attackMode = False
            else:
                self.attackMode = True
        else:
            if self.game.ball.pos.x - self.game.wall1.rect.right <= 10:
                self.attackMode = True
            else:
                self.attackMode = False

    def checkBallPossession(self):
        if self.distance(self.pos,self.game.ball.pos) <= self.r + self.game.ball.r+2: #if the ball is in front of AI
            self.hasBall = True
        else:
            self.hasBall = False
    
    def ballReachingWall1(self):
        if self.game.ball.pos.x - self.game.wall1.rect.right<= 40+self.game.ball.r:
            return True
        else: return False

    def ballReachingWall2(self):
        if self.game.ball.pos.x - self.game.wall2.rect.left<= 40-self.game.ball.r:
            return True
        else: return False

    def wait(self):
        self.vel.x = 0

    def update(self):
        self.spriteCounter = (1 + self.spriteCounter) % len(self.imageL)

        print("AI's y position",self.pos.y)
        ballP = self.game.ball.pos
        playerP = self.game.player.pos
        ballPx = self.game.ball.pos.x
        playerPx = self.game.player.pos.x
        #If the ball is over the halfline towards the opponent's goal
        self.checkAttackMode()
        self.checkBallPossession()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            self.vel = 0
        if self.vel != 0:
            self.acc = vec(0,2)
        keys = pygame.key.get_pressed()
        #ATTACK MODE
        if self.attackMode:
            print('attack mode is true') 
            if self.hasBall == False: #AI doesn't have the ball
                if self.ballReachingWall1(): #coming towards AI
                    self.acc.x = AI_a
                if self.game.ball.pos.x<=self.pos.x and not self.ballReachingWall1():
                    self.acc.x = -AI_a
                elif self.game.ball.pos.x > self.pos.x and not self.ballReachingWall2():
                    self.acc.x = AI_a
                if self.pos.x < self.game.ball.pos.x:
                    self.attackMode = False
            else: # AI has the ball
                # if self.game.ball.pos.x < WIDTH//2: # ball is on the player's half
                if self.distance(self.pos,self.game.ball.pos)<=3+self.r+self.game.ball.r and self.game.ball.pos.x < self.pos.x: 
                    #ball is in front of AI
                    print('ball is in front of AI')
                    
                    self.acc.x = -AI_a
                    # if self.ball.pos.y :
                    #     self.jump()
                else:#ball is behind AI
                    if self.distance(self.game.ball.pos,self.pos)<=3+self.game.ball.r+self.r and self.game.ball.pos.x > self.pos.x:
                        print("ball is behind AI and is very close")
                        self.jump()
                    self.acc.x = AI_a
                if self.distance(self.game.ball.pos, self.game.player.pos)<=3+self.game.ball.r+self.game.player.r:# player is in the way
                    print('player is in the way')
                    if self.game.player.isJumping:
                        self.acc.x = -AI_a
                    else:
                        self.jump() 
                else:
                    self.acc.x = -AI_a
        else: #DEFENSE MODE
            print('defense mode is true') 

            if self.hasBall:
                self.attackMode = True
            else:
                if not math.isclose(self.pos.x,(WIDTH-PLAYER_length*3),abs_tol=20):
                    self.acc.x = AI_a
                else:
                    if self.game.ball.isJumping and math.isclose(self.game.ball.pos.y, 217, abs_tol = 5) :
                        self.jump()
                

        '''
        DefenseMode (ball is closer to the player)
        
        if self.hasBall:
            self.attackMode = True

        else (AI doesn't have the ball):
            pos = in front of the goal
            if the ball is in the air:
                try going for it

        '''

        if not self.game.scored:
            self.acc.x += self.vel.x*AI_f
            self.vel += self.acc
            self.pos.x += 2*self.vel.x
            self.pos.y += self.vel.y
            if self.pos.x-self.length < 0:
                self.pos.x = self.length    
            elif self.pos.x+self.length > WIDTH:
                self.pos.x = WIDTH-self.length  
        self.rect.center = self.pos 

    def almostEqual(d1, d2, epsilon=10**-1):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
        return (abs(d2 - d1) < epsilon)

    def distance(self,pos1,pos2):
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

    # def kick(self):
    #   AIPos = self.rect.center
    #   ballPos = self.game.ball.rect.center
    #   distance = self.getDistance(AIPos,ballPos)
    #   if distance <=70:
    #     self.game.ball.vel = 3*(2*AI_m*self.vel)/(AI_m+AI_m)

    def jump(self):
    #only jump when on platform
      self.rect.y += 1
      onFloor = pygame.sprite.collide_rect(self, self.game.field)
      self.rect.y -= 1
      if onFloor:
        self.vel.y = PLAYER_j

