'''
Special thanks to the following:
http://blog.lukasperaza.com/getting-started-with-pygame/
https://github.com/kidscancode/pygame_tutorials
https://pygame.org
'''

import pygame
import pygame.gfxdraw
# from splash import SplashScreen
import time
import sprites
from settings import *

class Game(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.playerImageList = zImageList
        self.playerImageListFlipped = [pygame.transform.flip(image,True,False) for image in self.playerImageList]
        self.aiImageList = pImageList
        self.aiImageListFlipped = [pygame.transform.flip(image,True,False) for image in self.aiImageList]
        # self.backggroundImage = pygame
        self.score1 = 0
        self.score2 = 0
        self.myFont = pygame.font.SysFont('Light Pixel-7', 30)
        self.timer = 3
        self.scored = False

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

    def initializeSurface(self):
        fieldHeight = 40
        goalHeight = 100
        postHeight = 30
        self.player = sprites.Player(self)
        self.AI = sprites.AI(self, self.player)
        self.ball = sprites.Ball(self)
        self.field = sprites.Field(0, HEIGHT-fieldHeight, WIDTH, fieldHeight)
        self.gP1 = sprites.Goalpost(0, HEIGHT-fieldHeight-goalHeight, PLAYER_length*2,goalHeight)
        self.gP2 = sprites.Goalpost(WIDTH-PLAYER_length*2,HEIGHT-fieldHeight-goalHeight,PLAYER_length*2,goalHeight)
        # self.gPframe1 = sprites.Wall(0, HEIGHT-fieldHeight-goalHeight-postHeight, PLAYER_length*5,postHeight)
        # self.gPframe2 = sprites.Wall(WIDTH-PLAYER_length*5,HEIGHT-fieldHeight-goalHeight-postHeight,PLAYER_length*5,postHeight)
        self.wall1 = sprites.Wall(0, -10000, PLAYER_length*3+10,HEIGHT-140+10000)
        self.wall2 = sprites.Wall(WIDTH-PLAYER_length*3-10,-10000 , PLAYER_length*3+10,HEIGHT-140+10000)

    def new(self):
        self.initializeSurface()
        self.scoreSurface1 = self.myFont.render(f'{self.score1}', False, (0, 0, 0))
        self.scoreSurface2 = self.myFont.render(f'{self.score2}', False, (0, 0, 0))

        self.all_sprites = pygame.sprite.Group()
        self.initialSprites = pygame.sprite.Group()
        self.constantSprites = pygame.sprite.Group()
        self.wallSprites = pygame.sprite.Group()

        self.wallSprites.add(self.wall1, self.wall2)
        self.initialSprites.add(self.field,self.gP1,self.gP2,self.wall1,self.wall2)
        self.constantSprites.add(self.player,self.AI,self.ball)
        self.all_sprites.add(self.initialSprites)
        self.all_sprites.add(self.constantSprites)

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            # self.drawSetup()
            self.draw()

    def collided(self,pos1,pos2,dR):
        (cx1, cy1) = pos1
        (cx2, cy2) = pos2
        return ((cx1-cx2)**2+(cy1-cy2)**2)**(1/2) <= dR

    def distance(self,pos1,pos2):
        (cx1, cy1) = pos1
        (cx2, cy2) = pos2
        return ((cx1-cx2)**2+(cy1-cy2)**2)**(1/2)

    def update(self):
        self.constantSprites.update()
        overlap = 0.5*(self.ball.r+self.field.rect.top+1)

        playerOnGround = pygame.sprite.collide_rect(self.player,self.field)
        AIOnGround = pygame.sprite.collide_rect(self.AI,self.field)
        ballHitPlayer = self.collided(self.ball.pos,self.player.pos,abs(PLAYER_r+PLAYER_r))
        ballHitAI = self.collided(self.ball.pos,self.AI.pos,abs(AI_r+PLAYER_r))

        ballHitField = pygame.sprite.collide_rect(self.ball,self.field)
        # ballHitPost1 = pygame.sprite.collide_rect(self.ball,self.gPframe1)
        # ballHitPost2 = pygame.sprite.collide_rect(self.ball,self.gPframe2)

        if playerOnGround:
            self.player.pos.y = self.field.rect.top-PLAYER_r
            self.player.vel.y = 0

        if AIOnGround:
            self.AI.pos.y = self.field.rect.top - AI_r
            self.AI.vel.y = 0

        if self.playerScores(self.gP1):
            #stop
            self.score2 +=1

        elif self.playerScores(self.gP2):
            #stop
            self.score1 +=1

        if ballHitPlayer:
            self.collideWithPlayer()

        if ballHitAI:
            self.collideWithAI()

        if ballHitField:
            self.ball.angle = math.pi - self.ball.angle
            self.ball.speed *= ELASTICITY
            self.ball.pos.y = self.field.rect.top+1-self.ball.r

        if self.ballHitWall(self.wall1):
            self.ball.pos.x = self.ball.pos.x+5
            self.ball.angle = - self.ball.angle
            self.ball.speed *= ELASTICITY
        elif self.ballHitWall(self.wall2):
            self.ball.pos.x = self.ball.pos.x-5
            self.ball.angle = - self.ball.angle
            self.ball.speed *= ELASTICITY

    def collideWithPlayer(self):
        ballM, playerM = self.ball.mass, self.player.mass
        totalMass = ballM + playerM

        dx = self.ball.pos.x - self.player.pos.x
        dy = self.ball.pos.y - self.player.pos.y

        dist = self.distance((self.ball.pos.x,self.ball.pos.y),(self.player.pos.x,self.player.pos.y))

        if dist < self.ball.r+ self.player.r and not self.scored:
            interAngle = math.atan2(dy, dx) + 0.5 * math.pi

            vec1 = self.ball.angle, self.ball.speed*(ballM-playerM)/totalMass
            vec2 = interAngle, 2*self.player.vel.magnitude()*playerM/totalMass

            (self.ball.angle, self.ball.speed) = Game.addVectors(vec1, vec2)

            self.ball.speed *= 1.1
            overlap = 0.5*(self.ball.r + self.player.r - dist+2)

            self.ball.pos.x += math.sin(interAngle)*overlap
            self.ball.pos.y -= math.cos(interAngle)*overlap

    def collideWithAI(self):
        ballM, AIM = self.ball.mass, self.AI.mass
        totalMass = ballM + AIM

        dx = self.ball.pos.x - self.AI.pos.x
        dy = self.ball.pos.y - self.AI.pos.y

        dist = self.distance((self.ball.pos.x,self.ball.pos.y),(self.AI.pos.x,self.AI.pos.y))
        if dist < self.ball.r + self.AI.r and not self.scored:
            interAngle = math.atan2(dy, dx) + 0.5 * math.pi

            vec1 = self.ball.angle, self.ball.speed*(ballM-AIM)/totalMass
            vec2 = interAngle, 2*self.AI.vel.magnitude()*AIM/totalMass

            (self.ball.angle, self.ball.speed) = Game.addVectors(vec1, vec2)

            self.ball.speed *= 1.1
            overlap = 0.5*(self.ball.r + self.AI.r - dist+2)

            self.ball.pos.x += math.sin(interAngle)*overlap
            self.ball.pos.y -= math.cos(interAngle)*overlap

    def ballHitPost1(self):
        distX = self.ball.pos.x - self.gPframe1.rect.right
        distY = self.ball.pos.y - HEIGHT-151
        distance = (distX**2 + distY**2)**0.5
        if self.ball.r >= distance:
            return True
        return False

    def ballHitPost2(self):
        distX = self.ball.pos.x - self.gPframe2.rect.left
        distY = self.ball.pos.y - HEIGHT-151
        distance = (distX**2 + distY**2)**0.5
        if self.ball.r >= distance:
            return True
        return False

    def ballHitWall(self,wall):
        if pygame.sprite.collide_rect(self.ball,wall):
            return True
        return False

    def playerScores(self,goal):
        if pygame.sprite.collide_rect(self.ball,goal):
            self.scored =True
            return True
        return False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def drawPlayer(self):
        pygame.gfxdraw.aacircle(self.screen, int(self.player.pos.x), int(self.player.pos.y), PLAYER_r, (0, 0, 0, 0))
        if self.player.right == True:
            image = self.playerImageList[self.player.spriteCounter]
            self.screen.blit(image,(self.player.pos.x-self.player.r,self.player.pos.y-self.player.r))
        else:
            image = self.playerImageListFlipped[self.player.spriteCounter]
            self.screen.blit(image,(self.player.pos.x-self.player.r,self.player.pos.y-self.player.r))

    def drawAI(self):        
        pygame.gfxdraw.aacircle(self.screen, int(self.AI.pos.x), int(self.AI.pos.y), PLAYER_r, (0, 0, 0,0))
        if self.AI.acc.x<0:
            image = self.aiImageListFlipped[self.AI.spriteCounter]
            self.screen.blit(image,(self.AI.pos.x-self.AI.r,self.AI.pos.y-self.AI.r-5))
        else:
            image = self.aiImageList[self.AI.spriteCounter]
            self.screen.blit(image,(self.AI.pos.x-self.AI.r,self.AI.pos.y-self.AI.r-5))

    def drawBackground(self):
        self.screen.blit(fieldImage,(0,HEIGHT-80))
        self.screen.blit(woodImage,(0,0))
        self.screen.blit(woodImage,(WIDTH-70,0))
        self.screen.blit(gpImage1,(-100,HEIGHT//2-10))
        self.screen.blit(gpImage2,(WIDTH-WIDTH//9,HEIGHT//2-10))
        pygame.gfxdraw.aacircle(self.screen, int(self.ball.pos.x), int(self.ball.pos.y), BALL_r, (0, 0, 0,0))
        self.screen.blit(ballImage,(self.ball.pos.x-BALL_r,self.ball.pos.y-BALL_r))

    def draw(self):
        if self.scored:
            self.ball.speed= 0
            self.player.vel = 0
            self.AI.vel = 0
            self.timer +=1
            self.screen.blit(goalImage,(WIDTH//7,HEIGHT//4))
            pygame.display.update()
            if self.timer == 30:
                self.timer = 0
                self.scored = False
                self.new()
        self.screen.fill((255,255,255))
        self.all_sprites.draw(self.screen)

        self.drawBackground()
        self.screen.blit(self.scoreSurface1,(WIDTH//5,HEIGHT//6))
        self.screen.blit(self.scoreSurface2,(4*WIDTH//5,HEIGHT//6))
        self.drawPlayer()
        self.drawAI()
        pygame.display.flip()

    def activateScreen(self):
        pass

game = Game()


game.new()
# game.activateScreen(start)
while game.running:
    game.update()
    # game.activateScreen(go)

pygame.quit()