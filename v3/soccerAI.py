import pygame
import random
import game
import sprites 
import playerObject
from settings import *
import math

vec = pygame.math.Vector2

class AI(pygame.sprite.Sprite):
  # ,r,x,y,,speed,power,skill,color
    def __init__(self,game,player): #color changed to character later
        pygame.sprite.Sprite.__init__(self)
        self.r = AI_r
        self.mass = AI_m
        self.game = game
        self.image = pygame.Surface((AI_r*2,AI_r*2),pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.player = player
        self.playerL = charDict[self.player][0]
        self.playerFlippedL = charDict[self.player][1]
        self.power = charDict[self.player][2]
        self.speed = charDict[self.player][3]
        self.jumpMag = charDict[self.player][4]
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.pos = vec(3*WIDTH/4, HEIGHT/2)
        self.attackMode = None
        self.attackL = [0,1,2,3,4]
        self.defenseL = [0,1,2]
        self.attackModeOption = 0
        self.defenseModeOption = 0
        self.hasBall = False
        self.spriteCounter = 0

    def checkAttackMode(self):
        #Ball is on the player's half
        # print('ball pos',self.game.ball.pos.x,'my pos',self.pos.x)
        if self.game.ball.pos.x<=WIDTH//2:
            # AI is left to the ball and Player is closer to the ball
            if self.pos.x+self.r <= self.game.ball.pos.x-self.game.ball.r  and (self.distance(self.game.player.pos, self.game.ball.pos) <= self.distance(self.pos,self.game.ball.pos)):
                # print(self.pos.x+self.r, self.game.ball.pos.x-self.game.ball.r)
                self.attackMode = False
                self.defenseModeOption = self.defenseL[0]
            #AI is left to the ball and AI is closer to the ball
            elif self.pos.x+self.r <= self.game.ball.pos.x-self.game.ball.r and (self.distance(self.game.player.pos, self.game.ball.pos) >= self.distance(self.pos,self.game.ball.pos)):
                # print(self.pos.x+self.r, self.game.ball.pos.x-self.game.ball.r)
                self.attackMode = True
                self.attackModeOption = self.attackL[0]
            #AI is right to the ball and Player is closer to the ball
            elif self.pos.x-self.r >= self.game.ball.pos.x+self.game.ball.r and (self.distance(self.game.player.pos, self.game.ball.pos) <= self.distance(self.pos,self.game.ball.pos)):
                # print(self.pos.x-self.r, self.game.ball.pos.x+self.game.ball.r)
                self.attackMode = True
                self.attackModeOption = self.attackL[1]
            #AI is right to the ball and AI is closer to the ball
            elif (self.pos.x-self.r >= self.game.ball.pos.x+self.game.ball.r and (self.distance(self.game.player.pos, self.game.ball.pos) >= self.distance(self.pos,self.game.ball.pos))):
                # print(self.pos.x-self.r, self.game.ball.pos.x+self.game.ball.r)
                self.attackMode = True
                self.attackModeOption = self.attackL[2]
            else:
                # print('what?')
                # print(f'my position was {self.pos.x} and ball was {self.game.ball.pos.x}')
                self.chaseBall()
        #Ball is on the AI's half
        elif self.game.ball.pos.x > WIDTH//2:
            # AI is left to the ball and Player is closer to the ball
            if (self.distance(self.game.player.pos, self.game.ball.pos) <= self.distance(self.pos,self.game.ball.pos)
                and self.pos.x+self.r < self.game.ball.pos.x-self.game.ball.r):
                self.attackMode = False
                self.defenseModeOption = self.defenseL[2]
            # AI is left to the ball and AI is closer to the ball
            elif (self.distance(self.game.player.pos, self.game.ball.pos) >= self.distance(self.pos,self.game.ball.pos)
                and self.pos.x+self.r < self.game.ball.pos.x-self.game.ball.r):
                self.attackMode = False
                self.defenseModeOption = self.defenseL[1]
            # AI is right to the ball and Player is closer to the ball 
            elif (self.distance(self.game.player.pos, self.game.ball.pos) <= self.distance(self.pos,self.game.ball.pos)
                and self.pos.x-self.r > self.game.ball.pos.x+self.game.ball.r):
                self.attackMode = True
                self.attackModeOption = self.attackL[4]
            # AI is right to the ball and AI is closer to the ball
            elif (self.distance(self.game.player.pos, self.game.ball.pos) >= self.distance(self.pos,self.game.ball.pos)
                and self.pos.x-self.r > self.game.ball.pos.x+self.game.ball.r):
                self.attackMode = True
                self.attackModeOption = self.attackL[3]
            else:
                self.chaseBall()

    def checkBallPossession(self):
        # if the ball is very close to AI
        if self.distance(self.pos,self.game.ball.pos) <= self.r + self.game.ball.r+2: #if the ball is in front of AI
            self.hasBall = True
        else:
            self.hasBall = False

    def chaseBall(self):
        if self.game.ball.pos.x+self.game.ball.r+2 < self.pos.x-self.r:
            self.acc.x = -self.speed
            # print('chase ball to the Player')
        elif self.game.ball.pos.x-self.game.ball.r-2>self.pos.x+self.r:
            # print('chase ball to the AI')
            self.acc.x = +self.speed

    def distance(self,pos1,pos2):
        return ((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)**0.5

    def jump(self):
    #only jump when on platform
        # print(f"I jumped because I'm in attackmode: {self.attackMode} and {self.attackModeOption} and {self.defenseModeOption}")
        self.rect.y += 1
        onFloor = pygame.sprite.collide_rect(self, self.game.field)
        self.rect.y -= 1
        if onFloor:
            self.vel.y = self.jumpMag

    def update(self):
        self.acc.y = 2
        self.spriteCounter = (1 + self.spriteCounter) % len(self.playerL)
        self.checkAttackMode()
        self.checkBallPossession()

        #ATTACK MODE
        if self.attackMode:
            #Attack mode but doesn't have the ball --> aggressive
            if not self.hasBall:
                #Ball on player's half and
                #AI is left to the ball and AI is closer to the ball
                if self.attackModeOption == 0:
                    self.chaseBall()
                #AI is right to the ball and player is closer to the ball
                elif self.attackModeOption == 1:
                    self.chaseBall() # This will make the AI to possess the ball
                #AI is right to the ball and AI is closer to the ball
                elif self.attackModeOption == 2:
                    if self.pos.x+self.r<self.game.ball.pos.x-self.game.ball.r:
                        self.acc.x = self.speed

                    elif self.pos.x-self.r>=self.game.ball.pos.x + self.game.ball.r:
                        self.acc.x = -self.speed
                #Ball on AI's half and
                #AI is right to the ball and AI is closer to the ball
                elif self.attackModeOption == 3:
                    # if self.game.ball.pos.x+self.game.ball.r<self.pos.x-self.r:
                    if self.pos.x+self.r<self.game.ball.pos.x-self.game.ball.r:
                        self.acc.x = self.speed
                    elif self.pos.x-self.r>=self.game.ball.pos.x+self.game.ball.r:
                        self.acc.x = -self.speed

                #AI is right to the ball  and player is closer to the ball
                elif self.attackModeOption == 4:
                    # if self.game.ball.pos.x+self.game.ball.r<self.pos.x-self.r:
                    if self.pos.x+self.r<self.game.ball.pos.x-self.game.ball.r:
                        self.acc.x = self.speed
                    elif self.pos.x-self.r >= self.game.ball.pos.x-self.game.ball.r: 
                        self.acc.x = -self.speed
                if (abs(self.game.ball.pos.x-self.pos.x)<self.r+self.game.ball.r+10
                        and not math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.1)):
                    num = random.randint(1,1000)
                    if num <= 50:
                        self.jump()

            #Attack mode and has the ball --> very aggressive
            else:
                #AI is left to the ball and AI is closer to the ball
                if self.attackModeOption == 0:
                    if self.pos.x-self.r>self.game.ball.pos.x+self.game.ball.r and math.isclose(self.game.field.rect.top-self.pos.y,self.r,abs_tol=0.1):
                        self.acc.x = -self.speed
                    elif self.pos.x+self.r<=self.game.ball.pos.x-self.game.ball.r and math.isclose(self.game.field.rect.top-self.pos.y,self.r,abs_tol=0.1):
                        self.acc.x = +self.speed
                        if (abs(self.game.ball.pos.x-self.pos.x)<=self.r+self.game.ball.r+10
                        and math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.1)):
                            self.jump()
                #AI is right to the ball and player is closer to the ball
                elif self.attackModeOption == 1 :
                    self.acc.x = -self.speed
                #AI is right to the ball and AI is closer to the ball
                elif self.attackModeOption == 2:
                    self.acc.x = -self.speed
                #Ball on AI's half and
                #AI is right to the ball and AI is closer to the ball
                elif (self.attackModeOption == 3):
                    self.acc.x = -self.speed
                #AI is right to the ball  and player is closer to the ball
                elif self.attackModeOption == 4:
                    self.acc.x = -self.speed
                if (abs(self.game.ball.pos.x-self.pos.x)<self.r+self.game.ball.r+10
                        and not math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.1)):
                    num = random.randint(1,1000)
                    if num <= 50:
                        self.jump()
        #DEFENSE MODE
        else:
            #Ball on player's half and AI is left to the ball and Player is closer to the ball
            if self.defenseModeOption == 0:
                if not math.isclose(self.pos.x,(WIDTH-100),abs_tol=20):
                    self.acc.x = +self.speed
                    if (abs(self.game.ball.pos.x-self.pos.x)<=self.r+self.game.ball.r+10
                        and math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.01)):
                        self.jump()
            #Ball on AI's half and
            #AI is left to the ball and closer to the ball
            elif self.defenseModeOption == 1:
                if not math.isclose(self.pos.x,(WIDTH-50),abs_tol=20):
                    if self.pos.x-self.r>self.game.ball.pos.x+self.game.ball.r and math.isclose(self.game.field.rect.top-self.pos.y,self.r,abs_tol=0.1):
                        self.acc.x = -self.speed
                    else:
                        self.acc.x = +self.speed
                        if (abs(self.game.ball.pos.x-self.pos.x)<=self.r+self.game.ball.r+10
                            and  math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.01)):
                            self.jump()
            #Player is closer to the ball and AI is left to the ball
            elif self.defenseModeOption == 2:
                if not math.isclose(self.pos.x,(WIDTH-50),abs_tol=20):
                    if self.pos.x-self.r>self.game.ball.pos.x+self.game.ball.r and math.isclose(self.game.field.rect.top-self.pos.y,self.r,abs_tol=0.1):
                        self.acc.x = -self.speed
                    elif self.pos.x+self.r<self.game.ball.pos.x-self.game.ball.r:
                        self.acc.x = +self.speed
                        if (abs(self.game.ball.pos.x-self.pos.x)<=self.r+self.game.ball.r+10
                            and  math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.01)):
                            self.jump()
        self.acc.x += self.vel.x*AI_f
        self.vel += self.acc
        self.pos.x += 2*self.vel.x
        self.pos.y += self.vel.y
        if self.pos.x-self.r < 0:
            self.pos.x = self.r    
        elif self.pos.x+self.r > WIDTH:
            self.pos.x = WIDTH-self.r  
        self.rect.center = self.pos 


 

