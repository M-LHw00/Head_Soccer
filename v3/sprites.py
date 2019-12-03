import pygame
import pygame.gfxdraw
import math
import playerObject
from settings import *
import game
import random
vec = pygame.math.Vector2


class Ball(pygame.sprite.Sprite):
  def __init__(self,game):
    pygame.sprite.Sprite.__init__(self)
    self.game = game
    self.image = pygame.Surface((BALL_r*2,BALL_r*2),pygame.SRCALPHA)
    self.rect= self.image.get_rect()
    
    self.pos = vec(random.randint(WIDTH/4,3*WIDTH/4),110)
    self.mass = BALL_m
    self.speed = 0
    # self.vel = vec(0,0)
    self.r = BALL_r
    self.length = self.r
    self.angle = 0
    self.drag = 0.999
    self.isJumping = False
    

  @staticmethod
  def addVectors(v1, v2):
    angle1, length1 = v1
    angle2, length2 = v2
    resultantVecX  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    resultantVecY  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle =  math.pi/2 - math.atan2(resultantVecY, resultantVecX)
    length  = math.hypot(resultantVecX, resultantVecY)
    resultantVec = (angle, length)
    return resultantVec
  
  def move(self):
      (self.angle, self.speed) = Ball.addVectors((self.angle, self.speed), GRAV)
      self.pos.x += math.sin(self.angle) * self.speed*0.9
      self.pos.y -= math.cos(self.angle) * self.speed*0.9
      self.speed *= self.drag
      self.rect.center = self.pos

  def update(self):
      if self.pos.y+self.r < self.game.field.rect.top:
        self.isJumping = True
      else:
        self.isJumping = False
      self.move()
  
class ScoreBoard(pygame.sprite.Sprite):
  def __init__(self,x,y,width,height):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((width,height))
    self.rect = self.image.get_rect()
    self.image.fill((0,255,255))
    self.rect.x = x
    self.rect.y = y


  
class Field(pygame.sprite.Sprite):
  def __init__(self,x,y,width,height):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((width,height))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y 

class Goalpost(pygame.sprite.Sprite):
  def __init__(self,x,y,w,h):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((w,h))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y 

class Banner(pygame.sprite.Sprite):
  def __init__(self,x,y,w,h):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((w,h))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y 

class Wall(pygame.sprite.Sprite):
  def __init__(self,x,y,w,h):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.Surface((w,h))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y 
