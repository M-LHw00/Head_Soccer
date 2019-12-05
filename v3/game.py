import pygame
import pygame.gfxdraw
import time
import sprites
import soccerAI
import playerObject
from settings import *
vec = pygame.math.Vector2

class Game(object):
    def __init__(self):
        pygame.mixer.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.score1 = 0
        self.score2 = 0
        self.myFont = pygame.font.SysFont('Light Pixel-7', 70)
        self.myFont1 = pygame.font.SysFont('Pixeled', 70)
        self.spriteCounter = 0
        self.bannerCounter = 0
        self.angle = 0
        self.player1Win = False
        self.player2Win = False
        self.musicPause = False
        self.paused = False
        self.forceQuit = False
        self.musicOn = True
        self.pauseQuit = False

    def initializeSurface(self,p1,p2):
        fieldHeight = 40
        goalHeight = 100
        postHeight = 30
        self.player = playerObject.Player(self,p1)
        self.AI = soccerAI.AI(self,p2)
        self.playerChar = self.player.player
        self.aiPlayerChar = self.AI.player
        self.playerImageList = self.player.playerL
        self.playerImageListFlipped = self.player.playerFlippedL
        self.aiImageList = self.AI.playerL
        self.aiImageListFlipped = self.AI.playerFlippedL
        self.ball = sprites.Ball(self)
        self.field = sprites.Field(0, HEIGHT-fieldHeight, WIDTH, fieldHeight)
        self.gP1 = sprites.Goalpost(0, HEIGHT-fieldHeight-goalHeight, PLAYER_r*2,goalHeight)
        self.gP2 = sprites.Goalpost(WIDTH-PLAYER_r*2,HEIGHT-fieldHeight-goalHeight,PLAYER_r*2,goalHeight)
        self.wall1 = sprites.Wall(0, 0, PLAYER_r*3,HEIGHT-140)
        self.wall2 = sprites.Wall(WIDTH-PLAYER_r*3,0 , PLAYER_r*3+10,HEIGHT-140)
        self.banner = sprites.Banner(70,199,560,50)
        self.scoreBoard = sprites.ScoreBoard(WIDTH*2//6,0,WIDTH//3,HEIGHT//4)
        self.sky = sprites.Wall(0,-200,WIDTH,200)

    #https://github.com/kidscancode/pygame_tutorials
    def new(self,player1,player2):
        self.initializeSurface(player1,player2)
        self.scoreSurface1 = self.myFont1.render(f'{self.score1}', False, (255, 255, 0))
        self.scoreSurface2 = self.myFont1.render(f'{self.score2}', False, (255, 255, 0))

        self.all_sprites = pygame.sprite.Group()
        self.initialSprites = pygame.sprite.Group()
        self.constantSprites = pygame.sprite.Group()
        self.wallSprites = pygame.sprite.Group()
        self.wallSprites.add(self.wall1, self.wall2)

        self.initialSprites.add(self.field,self.gP1,self.gP2,self.wall1,self.wall2,self.scoreBoard,self.banner)
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
            self.draw()

    def pauseMusic(self):
        pygame.mixer.music.pause()
        self.musicPause = True
    
    def unpauseMusic(self):
        pygame.mixer.music.unpause()
        self.musicPause = False

    #referenced from http://archive.petercollingridge.co.uk/book/export/html/6
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

    def collided(self,pos1,pos2,dR):
        (cx1, cy1) = pos1
        (cx2, cy2) = pos2
        return ((cx1-cx2)**2+(cy1-cy2)**2)**(1/2) <= dR

    def distance(self,pos1,pos2):
        (cx1, cy1) = pos1
        (cx2, cy2) = pos2
        return ((cx1-cx2)**2+(cy1-cy2)**2)**(1/2)

    #referenced from http://archive.petercollingridge.co.uk/book/export/html/6
    def collideWithPlayer(self):
        ballM, playerM = self.ball.mass, self.player.mass
        totalMass = ballM + playerM

        dx = self.ball.pos.x - self.player.pos.x
        dy = self.ball.pos.y - self.player.pos.y

        dist = self.distance((self.ball.pos.x,self.ball.pos.y),(self.player.pos.x,self.player.pos.y))

        if dist < self.ball.r+ self.player.r:
            interAngle = math.atan2(dy, dx) + math.pi/2

            vec1 = (self.ball.angle, self.ball.speed*(ballM-playerM)/totalMass)
            vec2 = (interAngle, 2*self.player.vel.magnitude()*playerM/totalMass)

            (self.ball.angle, self.ball.speed) = Game.addVectors(vec1, vec2)

            self.ball.speed *= 0.9
            overlap = 0.5*(self.ball.r + self.player.r - dist+2)

            self.ball.pos.x += math.sin(interAngle)*overlap
            self.ball.pos.y -= math.cos(interAngle)*overlap

    #referenced from http://archive.petercollingridge.co.uk/book/export/html/6
    def collideWithAI(self):
        ballM, AIM = self.ball.mass, self.AI.mass
        totalMass = ballM + AIM

        dx = self.ball.pos.x - self.AI.pos.x
        dy = self.ball.pos.y - self.AI.pos.y

        dist = self.distance((self.ball.pos.x,self.ball.pos.y),(self.AI.pos.x,self.AI.pos.y))
        if dist < self.ball.r + self.AI.r:
            interAngle = math.atan2(dy, dx) + math.pi/2

            vec1 = self.ball.angle, self.ball.speed*(ballM-AIM)/totalMass
            vec2 = interAngle, 2*self.AI.vel.magnitude()*AIM/totalMass

            (self.ball.angle, self.ball.speed) = Game.addVectors(vec1, vec2)

            self.ball.speed *= 0.9
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

    def ballHitField(self):
        if self.field.rect.top < (self.ball.pos.y+self.ball.r):
            return True
        return False
    
    def ballHitSky(self):
        if self.sky.rect.bottom > (self.ball.pos.y-self.ball.r):
            return True
        return False
    
    def pause(self):
        self.paused = True
        self.pauseMusic()
        button1 = False
        button2 = False
        button3 = False
        while self.paused:
            mouse = pygame.mouse.get_pos()
            mouseX = mouse[0]
            mouseY = mouse[1]
            self.screen.blit(pausedScreen,(0,0))
            if 311<mouseX<408 and 216<mouseY<258:
                button1 = True
                if button1:
                    self.screen.blit(pausedQuit,(0,1))
            else:
                button1 = False

            if 310<mouseX<408 and 150<mouseY<196:
                button2 = True
                if button2:
                    self.screen.blit(pausedResume,(0,1))
            else:
                button2 = False
            if self.musicOn:
                self.screen.blit(soundOnImg, (529,73))
            else:
                self.screen.blit(muteImg,(529,73))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if 310<mouseX<408 and 150<mouseY<196 and event.type == pygame.MOUSEBUTTONDOWN:
                    self.paused = False
                    self.unpauseMusic()
                if 310<mouseX<408 and 216<mouseY<258 and event.type == pygame.MOUSEBUTTONDOWN:
                    self.pauseQuit = True
                    pygame.quit()
                    quit()
                if 529<mouseX<573 and 73<mouseY<117 and event.type == pygame.MOUSEBUTTONDOWN:
                    if self.musicOn:
                        self.musicOn = False
                        self.screen.blit(muteImg,(529,73))
                        pygame.mixer.music.stop()
                    else:
                        self.musicPause = False
                        pygame.mixer.music.load('sound/theme.wav')
                        pygame.mixer.music.set_volume(0.2)
                        pygame.mixer.music.play(-1)
                        self.pauseMusic()
                        self.musicOn = True
            pygame.display.update()

    def update(self):
        self.angle += (math.pi-self.ball.angle)*180/math.pi
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.pause()
        elif keys[pygame.K_1]:
            self.score1 = 5
        elif keys[pygame.K_2]:
            self.score2 = 5


        self.constantSprites.update()
        self.playerScores()
        self.spriteCounter +=1
        self.bannerCounter+=1
        overlap = 0.5*(self.ball.r+self.field.rect.top+1)
        playerOnGround = pygame.sprite.collide_rect(self.player,self.field)
        AIOnGround = pygame.sprite.collide_rect(self.AI,self.field)
        ballHitPlayer = self.collided(self.ball.pos,self.player.pos,abs(BALL_r+PLAYER_r))
        ballHitAI = self.collided(self.ball.pos,self.AI.pos,abs(BALL_r+AI_r))
        if self.score2 == 5 and self.playing:
            self.player2Wins()
            self.playing = False
            self.running = False
        if self.score1 == 5 and self.playing:
            self.player1Wins()
            self.running = False
            self.playing = False
        if playerOnGround:
            self.player.pos.y = self.field.rect.top-PLAYER_r
            self.player.vel.y = 0

        if AIOnGround:
            self.AI.pos.y = self.field.rect.top - AI_r
            self.AI.vel.y = 0

        if ballHitPlayer:
            ballSound.play()
            self.collideWithPlayer()

        if ballHitAI:
            ballSound.play()
            self.collideWithAI()

        if self.ballHitField():
            self.ball.pos.y = self.field.rect.top-self.ball.r
            self.ball.angle = math.pi - self.ball.angle
            self.ball.speed *= ELASTICITY

        if self.ballHitSky():
            self.ball.pos.y = self.sky.rect.bottom + self.ball.r
            self.ball.angle = math.pi - self.ball.angle
            self.ball.speed *= ELASTICITY

        if self.ballHitWall(self.wall1):
            ballGroundSound.play()
            self.ball.pos.x += 5
            self.ball.angle = - self.ball.angle
            self.ball.speed *= ELASTICITY
            ballGroundSound.fadeout(500)

        elif self.ballHitWall(self.wall2):
            ballGroundSound.play()
            self.ball.pos.x -= 5
            self.ball.angle = - self.ball.angle
            self.ball.speed *= ELASTICITY
            ballGroundSound.fadeout(500)


    def goalHandling(self,player):
        running = True
        self.pauseMusic()
        goal = self.myFont.render('GOAL!!!!', False, (196, 28, 33))
        spriteCounter = 0
        goalCounter = 0
        step1 = 170
        step2 = 530
        goalSound.play()
        jumpCount = 10
        x1 = step1
        y1 = 200
        x2 = step2
        y2 = 200 
        while running:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and player == self.aiPlayerChar:
                self.score2+=1
                pygame.mixer.fadeout(2000)
                self.unpauseMusic()
                self.new(self.playerChar,self.aiPlayerChar)
                running = False

            elif keys[pygame.K_SPACE] and player == self.playerChar:
                self.score1+=1       
                pygame.mixer.fadeout(2000)
                self.unpauseMusic()
                self.new(self.playerChar,self.aiPlayerChar)
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.screen.blit(goalBG,(0,0))
            goalCounter = (1+goalCounter)%len(goalSPRITE)
            gImage = goalSPRITE[goalCounter]
            self.screen.blit(gImage,(0,0))
            if player == self.aiPlayerChar and step1<700:
                spriteCounter = (1 + spriteCounter) % len(self.aiImageList)
                image = self.aiImageList[spriteCounter]
                self.screen.blit(image,(step1,y1))
                if step1 == 420:
                    if jumpCount >= -10:
                        y1 -= (jumpCount * abs(jumpCount)) * 0.2
                        jumpCount -= 1
                    else: 
                        step1+=10
                else:
                    step1+=10
            elif player == self.aiPlayerChar and step1>=700:
                self.score2+=1
                pygame.mixer.fadeout(2000)
                self.unpauseMusic()
                self.new(self.playerChar,self.aiPlayerChar)
                running = False

            elif player == self.playerChar and step2>=0:
                spriteCounter = (1 + spriteCounter) % len(self.playerImageList)
                image = self.playerImageListFlipped[spriteCounter]
                self.screen.blit(image,(step2,y2))
                if step2 == 280:
                    if jumpCount >= -10:
                        y2 -= (jumpCount * abs(jumpCount)) * 0.2
                        jumpCount -= 1
                    else: 
                        step2-=10
                else:
                    step2-=10
            elif player == self.playerChar and step2<0:
                self.score1+=1       
                pygame.mixer.fadeout(2000)
                self.unpauseMusic()
                self.new(self.playerChar,self.aiPlayerChar)
                running = False           
            pygame.display.update()

    def player1Wins(self):
        running = True
        goalSound.play()
        goalSound.fadeout(5000)
        airplaneCounter = WIDTH
        self.ball.pos = vec(-999,-999)
        while running:
            self.spriteCounter +=1
            self.bannerCounter +=1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.drawWinBackground()
            if self.spriteCounter%4 == 0:
                self.screen.blit(audImage1,(WIDTH//6+20,5))
                self.screen.blit(audImage2,(WIDTH//6+20,50))
                self.screen.blit(audImage3,(WIDTH//6+20,105))
                self.screen.blit(audImage4,(WIDTH//6+20,150))
            elif self.spriteCounter%4 == 1:
                self.screen.blit(audImage1,(WIDTH//6+15,5))
                self.screen.blit(audImage2,(WIDTH//6+15,50))
                self.screen.blit(audImage3,(WIDTH//6+15,105))
                self.screen.blit(audImage4,(WIDTH//6+15,150))
            elif self.spriteCounter%4 == 2:
                self.screen.blit(audImage1,(WIDTH//6+20,0))
                self.screen.blit(audImage2,(WIDTH//6+20,55))
                self.screen.blit(audImage3,(WIDTH//6+20,100))
                self.screen.blit(audImage4,(WIDTH//6+20,155))
            elif self.spriteCounter%4 == 3:
                self.screen.blit(audImage1,(WIDTH//6+20,10))
                self.screen.blit(audImage2,(WIDTH//6+20,50))
                self.screen.blit(audImage3,(WIDTH//6+20,110))
                self.screen.blit(audImage4,(WIDTH//6+20,150))
            self.screen.blit(airplane,(airplaneCounter,70))
            self.screen.blit(winFlag,(airplaneCounter+150,50))
            airplaneCounter -= 10
            if airplaneCounter <-200:
                running = False
                self.running = False
                self.playing = False
                goalSound.stop()
                self.player1Win = True
            pygame.display.update()

    def player2Wins(self):
        pygame.mixer.music.stop()
        self.running = False
        self.playing = False
        self.player1Win = False

    def playerScores(self):
        if pygame.sprite.collide_rect(self.ball, self.gP1):
            self.ball.pos = vec(-999,-999)
            self.goalHandling(self.aiPlayerChar)
        elif pygame.sprite.collide_rect(self.ball, self.gP2):
            self.ball.pos = vec(-999,-999)
            self.goalHandling(self.playerChar)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    if self.pauseQuit:
                        self.playing = False
                        self.forceQuit = True
                self.running = False

    def drawWinBackground(self):
        self.screen.blit(fieldImage,(0,HEIGHT-80))
        self.screen.blit(woodImage,(0,0))
        self.screen.blit(woodImage,(WIDTH-70,0))
        self.screen.blit(stadiumImage,(70,0))
        self.screen.blit(bannerImage,(70-self.bannerCounter,199))
        self.screen.blit(bannerImage, (630-self.bannerCounter,199))
        if self.bannerCounter == 560:
            self.bannerCounter = 0
            self.screen.blit(bannerImage,(70-self.bannerCounter,199))
            self.screen.blit(bannerImage, (630-self.bannerCounter,199))
        self.screen.blit(gpImage1,(-100,HEIGHT//2-10))
        self.screen.blit(gpImage2,(WIDTH-WIDTH//9,HEIGHT//2-10))
            
    def drawAudience(self):
        self.screen.blit(stadiumImage,(70,0))
        self.screen.blit(bannerImage,(70-self.bannerCounter,199))
        self.screen.blit(bannerImage, (630-self.bannerCounter,199))
        if self.bannerCounter == 560:
            self.bannerCounter = 0
            self.screen.blit(bannerImage,(70-self.bannerCounter,199))
            self.screen.blit(bannerImage, (630-self.bannerCounter,199))
        if self.spriteCounter//10%2 == 0:
            self.screen.blit(audImage1,(WIDTH//6+20,5))
            self.screen.blit(audImage2,(WIDTH//6+20,50))
            self.screen.blit(audImage3,(WIDTH//6+20,105))
            self.screen.blit(audImage4,(WIDTH//6+20,150))
        elif self.spriteCounter//10%2 == 1:
            self.screen.blit(audImage1,(WIDTH//6+20,0))
            self.screen.blit(audImage2,(WIDTH//6+20,55))
            self.screen.blit(audImage3,(WIDTH//6+20,100))
            self.screen.blit(audImage4,(WIDTH//6+20,155))
        
    def drawPlayer(self):
        pygame.gfxdraw.aacircle(self.screen, int(self.player.pos.x), int(self.player.pos.y), PLAYER_r, (0, 0, 0,0))
        if self.player.right == True:
            image = self.playerImageList[self.player.spriteCounter]
            self.screen.blit(image,(self.player.pos.x-self.player.r,self.player.pos.y-self.player.r-5))
        else:
            image = self.playerImageListFlipped[self.player.spriteCounter]
            self.screen.blit(image,(self.player.pos.x-self.player.r,self.player.pos.y-self.player.r-5))

    def drawAI(self):        
        pygame.gfxdraw.aacircle(self.screen, int(self.AI.pos.x), int(self.AI.pos.y), PLAYER_r, (0, 0, 0,0))
        if self.AI.vel.x<=0:
            image = self.aiImageListFlipped[self.AI.spriteCounter]
            self.screen.blit(image,(self.AI.pos.x-self.AI.r,self.AI.pos.y-self.AI.r-5))
        else:
            image = self.aiImageList[self.AI.spriteCounter]
            self.screen.blit(image,(self.AI.pos.x-self.AI.r,self.AI.pos.y-self.AI.r-5))

    def drawBackground(self):
        self.screen.blit(fieldImage,(0,HEIGHT-80))
        self.screen.blit(woodImage,(0,0))
        self.screen.blit(woodImage,(WIDTH-70,0))
        self.drawAudience()
        self.screen.blit(gpImage1,(-100,HEIGHT//2-10))
        self.screen.blit(gpImage2,(WIDTH-WIDTH//9,HEIGHT//2-10))
        pygame.gfxdraw.aacircle(self.screen, int(self.ball.pos.x), int(self.ball.pos.y), BALL_r, (0, 0, 0,0))
        self.screen.blit(scoreBoardImage,(WIDTH*2//6,0))
        rotatedImage, newRect = self.rotCenter()
        self.screen.blit(rotatedImage, (self.ball.pos.x-newRect.center[0], self.ball.pos.y-newRect.center[1]))
        
    #https://www.youtube.com/watch?v=g7KoOUu4v7Q
    def rotCenter(self):
        rotated = pygame.transform.rotate(ballImage, self.angle)
        newRect = rotated.get_rect()
        return rotated,newRect

    def draw(self):
        self.all_sprites.draw(self.screen)
        self.drawBackground()
        self.screen.blit(self.scoreSurface1,(4*WIDTH//10+8,HEIGHT//15))
        self.screen.blit(self.scoreSurface2,(6*WIDTH//10-35,HEIGHT//15))
        self.drawPlayer()
        self.drawAI()
        pygame.display.flip()
