import pygame
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
        self.player = player
        self.playerL = charDict[self.player][0]
        self.playerFlippedL = charDict[self.player][1]
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.pos = vec(3*WIDTH/4, HEIGHT/2)
        self.tanAI = math.atan2(self.vel.y,self.vel.x)
        self.attackMode = None
        self.attackL = [0,1,2,3,4]
        self.defenseL = [0,1,2]
        self.attackModeOption = 0
        self.defenseModeOption = 0
        self.hasBall = False
        self.spriteCounter = 0

    def checkAttackMode(self):
        #Ball is on the player's half
        if self.game.ball.pos.x<=WIDTH//2:
            # AI is left to the ball and Player is closer to the ball
            if self.pos.x+self.r < self.game.ball.pos.x-self.game.ball.r  and (self.distance(self.game.player.pos, self.game.ball.pos) <= self.distance(self.pos,self.game.ball.pos)):
                self.attackMode = False
                self.defenseModeOption = self.defenseL[0]
            #AI is left to the ball and AI is closer to the ball
            elif self.pos.x+self.r < self.game.ball.pos.x-self.game.ball.r and (self.distance(self.game.player.pos, self.game.ball.pos) >= self.distance(self.pos,self.game.ball.pos)):
                self.attackMode = True
                self.attackModeOption = self.attackL[0]
            #AI is right to the ball and Player is closer to the ball    
            elif self.pos.x-self.r > self.game.ball.pos.x+self.game.ball.r and (self.distance(self.game.player.pos, self.game.ball.pos) <= self.distance(self.pos,self.game.ball.pos)):
                self.attackMode = True
                self.attackModeOption = self.attackL[1]
            #AI is right to the ball and AI is closer to the ball
            elif (self.pos.x-self.r > self.game.ball.pos.x+self.game.ball.r and (self.distance(self.game.player.pos, self.game.ball.pos) >= self.distance(self.pos,self.game.ball.pos))):
                self.attackMode = True
                self.attackModeOption = self.attackL[2]
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


    def checkBallPossession(self):
        # if the ball is very close to AI
        if self.distance(self.pos,self.game.ball.pos) <= self.r + self.game.ball.r+10: #if the ball is in front of AI
            self.hasBall = True
        else:
            self.hasBall = False
    
    # def ballReachingWall1(self):
    #     if self.game.ball.pos.x - self.wall1.rect.right<= 40+self.game.ball.r:
    #         return True
    #     else: return False

    # def ballReachingWall2(self):
    #     if self.game.ball.pos.x - self.wall2.rect.left<= 40-self.game.ball.r:
    #         return True
    #     else: return False

    def chaseBall(self):
        if self.game.ball.pos.x < self.pos.x:
            self.acc.x = -AI_a
        elif self.game.ball.pos.x>self.pos.x:
            self.acc.x = +AI_a

    def distance(self,pos1,pos2):
        return ((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)**0.5

    def jump(self):
    #only jump when on platform
        print(f"I jumped because I'm in attackmode: {self.attackMode} and {self.attackModeOption} and {self.defenseModeOption}")
        self.rect.y += 1
        onFloor = pygame.sprite.collide_rect(self, self.game.field)
        self.rect.y -= 1
        if onFloor:
            self.vel.y = PLAYER_j

    def update(self):
        self.acc = vec(0,2)
        self.spriteCounter = (1 + self.spriteCounter) % len(self.playerL)
        self.checkAttackMode()
        self.checkBallPossession()
        print('Attack mode is',self.attackMode)
        print('AI has the ball',self.hasBall)
        print(f'The attack option is {self.attackModeOption}')
        print(f'The defense option is {self.defenseModeOption}')

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
                        self.acc.x = AI_a
                    self.acc.x = -AI_a
                #Ball on AI's half and
                #AI is right to the ball and AI is closer to the ball
                elif self.attackModeOption == 3:
                    # if self.game.ball.pos.x+self.game.ball.r<self.pos.x-self.r:
                    if self.pos.x+self.r<self.game.ball.pos.x-self.game.ball.r:
                        self.acc.x = AI_a
                    self.acc.x = -AI_a
                    # else:
                    #     self.acc.x = +AI_a
                    #     print('3else')
                #AI is right to the ball  and player is closer to the ball
                elif self.attackModeOption == 4:
                    # if self.game.ball.pos.x+self.game.ball.r<self.pos.x-self.r:
                    if self.pos.x+self.r<self.game.ball.pos.x-self.game.ball.r:
                        self.acc.x = AI_a
                    self.acc.x = -AI_a
                if math.isclose(self.game.player.pos.x,self.game.ball.pos.x,abs_tol=0.5) and not math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.5):
                    self.jump()
            #Attack mode and has the ball --> very aggressive
            else:
                #AI is left to the ball and AI is closer to the ball
                if self.attackModeOption == 0:
                    # if self.pos.x+self.r < self.game.ball.pos.x-self.game.ball.r:
                    if self.pos.x-self.r>self.game.ball.pos.x+self.game.ball.r:
                        self.acc.x = -AI_a
                    self.acc.x = +AI_a
                    if (self.game.ball.pos.x-self.pos.x<self.r+self.game.ball.r+5
                        and not math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.2)):
                        self.jump()
                #AI is right to the ball and player is closer to the ball
                elif self.attackModeOption == 1 :
                    # if self.pos.x-self.r >self.game.ball.pos.x+self.game.ball.r:
                    if self.pos.x+self.r<self.game.ball.pos.x-self.game.ball.r:
                        self.acc.x = +AI_a
                        if (self.game.ball.pos.x-self.pos.x<self.r+self.game.ball.r+5
                        and not math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.2)):
                            self.jump()
                    self.acc.x = -AI_a
                #AI is right to the ball and AI is closer to the ball
                elif self.attackModeOption == 2:
                    # if self.pos.x-self.r > self.game.ball.pos.x + self.game.ball.r:
                    if self.pos.x+self.r<self.game.ball.pos.x-self.game.ball.r:
                        self.acc.x = +AI_a
                        if (self.game.ball.pos.x-self.pos.x<self.r+self.game.ball.r+5
                        and not math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.2)):
                            self.jump()
                    self.acc.x = -AI_a
                #Ball on AI's half and
                #AI is right to the ball and AI is closer to the ball
                elif (self.attackModeOption == 3):#math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.field.rect.top-self.game.ball.r,abs_tol=0.2)
                    # if self.game.ball.pos.x+self.game.ball.r<self.pos.x-self.r:
                    if self.pos.x+self.r<self.game.ball.pos.x-self.game.ball.r:
                        self.acc.x = +AI_a
                        if (self.game.ball.pos.x-self.pos.x<self.r+self.game.ball.r+5
                        and not math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.2)):
                            self.jump()
                    self.acc.x = -AI_a
                #AI is right to the ball  and player is closer to the ball
                elif self.attackModeOption == 4:
                    # if self.game.ball.pos.x+self.game.ball.r<self.pos.x-self.r:
                    if self.pos.x+self.r<self.game.ball.pos.x-self.game.ball.r:
                        self.acc.x = +AI_a
                        if (math.isclose(self.pos.x, self.game.ball.pos.x, abs_tol=self.r+self.game.ball.r+5)
                        and not math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.2)):
                            self.jump()
                    self.acc.x = -AI_a
                if (self.game.ball.pos.x-self.pos.x<self.r+self.game.ball.r+5
                        and not math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.2)):
                    self.jump()
        #DEFENSE MODE
        else:
            if not math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.2) and math.isclose(self.game.ball.angle,math.pi,abs_tol=0.5):
                #print("Defense TRUe")
                self.acc.x = +AI_a
            #Ball on player's half and AI is left to the ball and Player is closer to the ball
            elif self.defenseModeOption == 0:
                if not math.isclose(self.pos.x,(WIDTH-100),abs_tol=20):
                    self.acc.x = +AI_a
                if (math.isclose(self.pos.x, self.game.ball.pos.x, abs_tol=self.r+self.game.ball.r+5)
                    and math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.5)):
                    self.jump()
            #Ball on AI's half and
            #AI is left to the ball and closer to the ball
            elif self.defenseModeOption == 1:
                if not math.isclose(self.pos.x,(WIDTH-100),abs_tol=20):
                    # if self.game.ball.x-self.game.ball.r > self.pos.x+self.r:
                    if self.pos.x-self.r>self.game.ball.pos.x+self.game.ball.r:
                        self.acc.x = -AI_a
                    self.acc.x = +AI_a
                if (math.isclose(self.pos.x, self.game.ball.pos.x, abs_tol=self.r+self.game.ball.r+5)
                    and  math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.5)):
                    self.jump()
            #Player is closer to the ball and AI is left to the ball
            elif self.defenseModeOption == 2:
                if not math.isclose(self.pos.x,(WIDTH-100),abs_tol=20):
                    # if self.game.ball.x-self.game.ball.r > self.pos.x+self.r:
                    if self.pos.x-self.r>self.game.ball.pos.x+self.game.ball.r:
                        self.acc.x = -AI_a
                    self.acc.x = +AI_a
                if (math.isclose(self.pos.x, self.game.ball.pos.x, abs_tol=self.r+self.game.ball.r+5)
                    and  math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.5)):
                    self.jump()
            if math.isclose(self.game.player.pos.x,self.game.ball.pos.x,abs_tol=0.5) and not math.isclose(self.game.field.rect.top-self.game.ball.pos.y,self.game.ball.r,abs_tol=0.5):
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

 

