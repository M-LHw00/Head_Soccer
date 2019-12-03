import pygame
import game
import splash
import random
import copy
from settings import *

pygame.init()
pygame.mixer.init()
pygame.font.init()



splashScreen = splash.SplashScreen()
gamePlay = game.Game()



def gameIntro():
    running = True
    myFont = pygame.font.Font('husky stash.ttf',50)
    myFont1 = pygame.font.Font('husky stash.ttf',51)
    title1 = myFont.render('Head Soccer', False, (255, 208, 0))
    title2 = myFont.render('Champions League', False, (255, 207, 0))
    title11 = myFont1.render('Head Soccer', False, (196, 28, 33))
    title22 = myFont1.render('Champions League', False, (196, 28, 33))
    title123 = myFont.render('15112 TP Martin Lee', False, (255,255,255))
    spriteCounter = 0
    spriteCounter1 = 0
    spriteCounter2 = 0
    step1 = 170
    step2 = 120
    step3 = 120
    pygame.mixer.music.load('sound/crowd.wav')
    pygame.mixer.music.play(0)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gamePlay.screen.fill((48,79,254))

        if step1>700:
            spriteCounter1 = (1 + spriteCounter1) % len(zImageList)
            image1 = rImageList[spriteCounter1]
            gamePlay.screen.blit(image1,(step2-50,120))
            gamePlay.screen.blit(title2,(130,120))
            gamePlay.screen.blit(title22,(131,121))
            pygame.draw.rect(gamePlay.screen,(48,79,254),(step2,120,500,100))
            step2 += 10
        if step2 >=800:
            spriteCounter2 = (1 + spriteCounter2) % len(zImageList)
            image2 = nImageList[spriteCounter1]
            gamePlay.screen.blit(image2,(step3-50,200))
            gamePlay.screen.blit(title123,(130,200))
            pygame.draw.rect(gamePlay.screen,(48,79,254),(step3,200,500,100))
            step3 += 10
        if step3 > 1000:
            running = False
        else:
            spriteCounter = (1 + spriteCounter) % len(pImageList)
            gamePlay.screen.blit(logoImage,(-30,0))
            image = mImageList[spriteCounter]
            gamePlay.screen.blit(image,(step1-50,70))
            gamePlay.screen.blit(title1,(210,70))
            gamePlay.screen.blit(title11,(211,71))
            pygame.draw.rect(gamePlay.screen,(48,79,254),(step1,70,500,100))
            step1+=5
        pygame.display.update()

def splashScreen():
    running = True
    myFont = pygame.font.Font('husky stash.ttf',50)
    myFont1 = pygame.font.Font('husky stash.ttf',51)
    title1 = myFont.render('Head Soccer', False, (255, 208, 0))
    title11 = myFont1.render('Head Soccer', False, (196, 28, 33))
    title2 = myFont.render('Champions League', False, (255, 207, 0))
    title22 = myFont1.render('Champions League', False, (196, 28, 33))
    pygame.mixer.music.load('sound/champions.wav')
    pygame.mixer.music.play(-1)
    button = False
    while running:
        mouse = pygame.mouse.get_pos()
        mouseX = mouse[0]
        mouseY = mouse[1]
        gamePlay.screen.blit(backgroundSplash,(0,0))     
        gamePlay.screen.blit(title1,(210,50))
        gamePlay.screen.blit(title11,(211,51))
        gamePlay.screen.blit(title2,(130,100))
        gamePlay.screen.blit(title22,(131,101))
        gamePlay.screen.blit(logoSplash,(311,138))  
        gamePlay.screen.blit(start1,(0,0))
        if 270<mouseX<430 and 200<mouseY<250:
            button = True
            if button:
                gamePlay.screen.blit(start2,(0,1))
        else:
            button = False
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if 270<mouse[0]<430 and 200<mouse[1]<250 and event.type == pygame.MOUSEBUTTONDOWN:
                running = False
        pygame.display.update()

def chooseScreen():
    running = True
    spriteCounter1 = 0
    spriteCounter2 = 0
    p1Count = 0
    p2Count = 1
    fullList = copy.copy(charChooseList)
    button1 = False
    button2 = False
    button3 = False
    button4 = False
    button5 = False
    while running:
        gamePlay.screen.blit(choiceBG,(0,0))
        gamePlay.screen.blit(logoImage,(-30,0))
        player1 = charChooseList[(9+p1Count)%9]
        player2 = charChooseList[(9+p2Count)%9]
        mouse = pygame.mouse.get_pos()
        if player1=='Random' and player2=='Random':
            gamePlay.screen.blit(qMark,(147,115))
            gamePlay.screen.blit(qMark,(502,115))
        elif player1=='Random':
            gamePlay.screen.blit(qMark,(147,115))
            player2List = charDict[player2][1]
            image2 = player2List[spriteCounter2]
            gamePlay.screen.blit(image2,(502,115))
            pygame.draw.rect(gamePlay.screen,(198,40,40),(545,229,(charDict[player2][2]/10)*50+1,9))
            pygame.draw.rect(gamePlay.screen,(198,40,40),(545,263,(charDict[player2][3]/0.8)*50+1,9))
            pygame.draw.rect(gamePlay.screen,(198,40,40),(545,296,(charDict[player2][4]/-20)*50+1,9))
        elif player2 == 'Random':
            gamePlay.screen.blit(qMark,(502,115))
            player1List = charDict[player1][0]
            image1 = player1List[spriteCounter1]
            gamePlay.screen.blit(image1,(147,115))
            pygame.draw.rect(gamePlay.screen,(198,40,40),(190,230,(charDict[player1][2]/10)*50+1,9))
            pygame.draw.rect(gamePlay.screen,(198,40,40),(190,264,(charDict[player1][3]/0.8)*50+1,9))
            pygame.draw.rect(gamePlay.screen,(198,40,40),(190,297,(charDict[player1][4]/-20)*50+1,9))
        else:
            player1List = charDict[player1][0]
            player2List = charDict[player2][1]
            image1 = player1List[spriteCounter1]
            image2 = player2List[spriteCounter2]
            gamePlay.screen.blit(image1,(147,115))
            gamePlay.screen.blit(image2,(502,115))
            pygame.draw.rect(gamePlay.screen,(198,40,40),(190,230,(charDict[player1][2]/10)*50+1,9))
            pygame.draw.rect(gamePlay.screen,(198,40,40),(545,229,(charDict[player2][2]/10)*50+1,9))
            pygame.draw.rect(gamePlay.screen,(198,40,40),(190,264,(charDict[player1][3]/0.8)*50+1,9))
            pygame.draw.rect(gamePlay.screen,(198,40,40),(545,263,(charDict[player2][3]/0.8)*50+1,9))
            pygame.draw.rect(gamePlay.screen,(198,40,40),(190,297,(charDict[player1][4]/-20)*50+1,9))
            pygame.draw.rect(gamePlay.screen,(198,40,40),(545,296,(charDict[player2][4]/-20)*50+1,9))
        mouseX = mouse[0]
        mouseY = mouse[1]
        #playerUp
        if 146<mouseX<201 and 61<mouseY<89:
            button1 = True
            if button1:
                gamePlay.screen.blit(playerUpPressed,(0,1))
        else:
            button1 = False
        #playerDown
        if 146<mouseX<201 and 191<mouseY<219:
            button2 = True
            if button2:
                gamePlay.screen.blit(playerDownPressed,(0,1))
        else:
            button2 = False
        #opponentUp
        if 502<mouseX<555 and 61<mouseY<89:
            button3 = True
            if button3:
                gamePlay.screen.blit(aiUpPressed,(0,1))
        else:
            button3 = False
        #opponentDown
        if 502<mouseX<555 and 191<mouseY<219:
            button4 = True
            if button4:
                gamePlay.screen.blit(aiDownPressed,(0,1))
        else:
            button4 = False
        #next
        if 612<mouseX<700 and 283<mouseY<330:
            button5 = True
            if button5:
                gamePlay.screen.blit(nextPressed,(0,0))
            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False 
                if player1 == 'Random' and player2 == 'Random':
                    player1Num = random.randint(0,7)
                    player1 = charList[player1Num]
                    fullList.pop(player1Num)
                    player2 = fullList[random.randint(0,6)]
                elif player1 == 'Random':
                    fullList.remove(player2)
                    player1 = fullList[random.randint(0,6)]
                if player2 == 'Random':
                    fullList.remove(player1)
                    player2 = fullList[random.randint(0,6)]
                return player1,player2
        else:
            button5 = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if 146<mouseX<201 and 61<mouseY<89 and event.type == pygame.MOUSEBUTTONDOWN:
                if charChooseList[(9+p1Count+1)%9] == charChooseList[(9+p2Count)%9] and (player1 != 'Random' and player2!= 'Random'):
                    p1Count+=1
                elif charChooseList[(9+p1Count+1)%9] == charChooseList[(9+p2Count)%9] and player1== 'Random':
                    p1Count +=1
                p1Count +=1

            elif 146<mouseX<201 and 191<mouseY<219 and event.type == pygame.MOUSEBUTTONDOWN: 
                if charChooseList[(9+p1Count-1)%9] == charChooseList[(9+p2Count)%9] and (player1 != 'Random' and player2!= 'Random'):
                    p1Count-=1
                elif charChooseList[(9+p1Count-1)%9] == charChooseList[(9+p2Count)%9] and player1== 'Random':
                    p1Count -=1
                p1Count -=1

            elif 502<mouseX<555 and 61<mouseY<89 and event.type == pygame.MOUSEBUTTONDOWN:
                if charChooseList[(9+p1Count)%9] == charChooseList[(9+p2Count+1)%9] and (player1 != 'Random' and player2!= 'Random'):
                    p2Count+=1
                elif charChooseList[(9+p1Count)%9] == charChooseList[(9+p2Count+1)%9] and player2== 'Random':
                    p2Count +=1
                p2Count +=1


            elif 502<mouseX<555 and 191<mouseY<219 and event.type == pygame.MOUSEBUTTONDOWN:
                if charChooseList[(9+p1Count)%9] == charChooseList[(9+p2Count-1)%9] and (player1 != 'Random' and player2!= 'Random'):
                    p2Count -=1
                elif charChooseList[(9+p1Count)%9] == charChooseList[(9+p2Count-1)%9] and player2== 'Random':
                    p2Count -=1
                p2Count -=1

        spriteCounter1 = (1 + spriteCounter1) % len(player1List)
        spriteCounter2 = (1 + spriteCounter2) % len(player2List)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            gamePlay.screen.blit(RIGHT,(0,0))            
        if keys[pygame.K_LEFT]:
            gamePlay.screen.blit(LEFT,(0,0))
        if keys[pygame.K_UP]:
            gamePlay.screen.blit(UP,(0,0))
        pygame.display.update()

def tournamentScreen(player,AI):
    running = True
    copyList = copy.copy(charList)
    copyList.remove(player)
    copyList.remove(AI)
    spriteCounter = 0
    player3 = copyList[random.randint(0,5)]
    copyList.remove(player3)
    player4 = copyList[random.randint(0,4)]
    copyList.remove(player4)
    player5 = copyList[random.randint(0,3)]
    copyList.remove(player5)
    player6 = copyList[random.randint(0,2)]
    copyList.remove(player6)
    player7 = copyList[random.randint(0,1)]
    copyList.remove(player7)
    player8 = copyList[0]
    player1List = charDict[player][0]
    player2List = charDict[AI][0]
    player3List = charDict[player3][0]
    player4List = charDict[player4][0]
    player5List = charDict[player5][1]
    player6List = charDict[player6][1]
    player7List = charDict[player7][1]
    player8List = charDict[player8][1]
    x1 = 60
    y11,y12,y13,y14 = 20, 95, 195, 270
    x2 = 590
    y21, y22, y23, y24 = 20, 95, 195 ,270
    button = False
    while running:
        mouse = pygame.mouse.get_pos()
        mouseX = mouse[0]
        mouseY = mouse[1]
        if 306<mouseX<406 and 194<mouseY<294:
            button = True
            print('??')
            if button:
                print('???')
                gamePlay.screen.blit(clickedlogoImage,(WIDTH//2-93,HEIGHT//2-16))
        else:
            button = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif 306<mouse[0]<406 and 194<mouse[1]<294 and event.type == pygame.MOUSEBUTTONDOWN:
                # gamePlay.screen.blit(nextPressed,(0,0))
                running = False 
                newPlayer2 = random.choice([player3, player4])
                newPlayer3 = random.choice([player5, player6])
                newPlayer4 = random.choice([player7, player8])
                return newPlayer2, newPlayer3, newPlayer4
        gamePlay.screen.blit(tournament,(0,0))
        gamePlay.screen.blit(logoImage,(WIDTH//2-93,HEIGHT//2-15))
        gamePlay.screen.blit(trophy,(WIDTH//2-40,HEIGHT//2-80))
        spriteCounter = (1 + spriteCounter) % len(player1List)
        image1 = player1List[spriteCounter]
        image2 = player2List[spriteCounter]
        image3 = player3List[spriteCounter]
        image4 = player4List[spriteCounter]
        image5 = player5List[spriteCounter]
        image6 = player6List[spriteCounter]
        image7 = player7List[spriteCounter]
        image8 = player8List[spriteCounter]
        gamePlay.screen.blit(image1,(x1,y11))
        gamePlay.screen.blit(image2,(x1,y12))
        gamePlay.screen.blit(image3,(x1,y13))
        gamePlay.screen.blit(image4,(x1,y14))
        gamePlay.screen.blit(image5,(x2,y21))
        gamePlay.screen.blit(image6,(x2,y22))
        gamePlay.screen.blit(image7,(x2,y23))
        gamePlay.screen.blit(image8,(x2,y24))

        pygame.display.update()

def secondTournamentScreen(player,AI,player3,player4):
    running = True
    spriteCounter = 0
    player1List = charDict[player][0]
    player2List = charDict[AI][0]
    player3List = charDict[player3][1]
    player4List = charDict[player4][1]
    x1 ,x2 = 200, 430
    y1, y2 = 50, 215
    button = False
    while running:
        mouse = pygame.mouse.get_pos()
        mouseX = mouse[0]
        mouseY = mouse[1]
        if 306<mouseX<406 and 194<mouseY<294:
            button = True
            print('??')
            if button:
                print('???')
                gamePlay.screen.blit(clickedlogoImage,(WIDTH//2-93,HEIGHT//2-16))
        else:
            button = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif 306<mouse[0]<406 and 194<mouse[1]<294 and event.type == pygame.MOUSEBUTTONDOWN:
                running = False 
                newPlayer = random.choice([player3, player4])
                return newPlayer
        gamePlay.screen.blit(tournamentSemi,(0,0))
        gamePlay.screen.blit(logoImage,(WIDTH//2-93,HEIGHT//2-15))
        gamePlay.screen.blit(trophy,(WIDTH//2-40,HEIGHT//2-80))
        spriteCounter = (1 + spriteCounter) % len(player1List)
        image1 = player1List[spriteCounter]
        image2 = player2List[spriteCounter]
        image3 = player3List[spriteCounter]
        image4 = player4List[spriteCounter]
    
        gamePlay.screen.blit(image1,(x1,y1))
        gamePlay.screen.blit(image2,(x1,y2))
        gamePlay.screen.blit(image3,(x2,y1))
        gamePlay.screen.blit(image4,(x2,y2))

        pygame.display.update()

def finals(player,AI):
    running = True
    spriteCounter = 0
    player1List = charDict[player][0]
    player2List = charDict[AI][1]
    x1 ,x2 = 147, 502
    y1 = 115
    button = False
    while running:
        mouse = pygame.mouse.get_pos()
        mouseX = mouse[0]
        mouseY = mouse[1]
        if 306<mouseX<406 and 194<mouseY<294:
            button = True
            print('??')
            if button:
                print('???')
                gamePlay.screen.blit(clickedlogoImage,(WIDTH//2-93,HEIGHT//2-16))
        else:
            button = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif 306<mouse[0]<406 and 194<mouse[1]<294 and event.type == pygame.MOUSEBUTTONDOWN:
                gamePlay.screen.blit(nextPressed,(0,0))
                running = False 
        gamePlay.screen.blit(tournamentFinal,(0,0))
        gamePlay.screen.blit(logoImage,(WIDTH//2-93,HEIGHT//2-15))
        gamePlay.screen.blit(trophy,(WIDTH//2-40,HEIGHT//2-80))
        spriteCounter = (1 + spriteCounter) % len(player1List)
        image1 = player1List[spriteCounter]
        image2 = player2List[spriteCounter]
        gamePlay.screen.blit(image1,(x1,y1))
        gamePlay.screen.blit(image2,(x2,y1))

        pygame.display.update()

def ending(player):
    running = True
    counter = 0
    player1FlippedList = charDict[player][1]
    spriteCounter = 0
    while running:
        counter +=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if counter == 700:
            running = False
        gamePlay.screen.blit(champion,(0,0))
        gamePlay.screen.blit(trophy,(WIDTH//2-50,HEIGHT//2-75))
        image1 = player1FlippedList[0]
        gamePlay.screen.blit(image1,(WIDTH//2+10,HEIGHT//2-50))

        pygame.display.update()

def mainGame():
    player1,firstAI = chooseScreen()
    semiAI, newP3, newP4 = tournamentScreen(player1,firstAI)
    pygame.mixer.music.load('sound/theme.wav')
    pygame.mixer.music.play(0)
    gamePlay.new(player1,firstAI)
    while gamePlay.running:
        gamePlay.update()
    pygame.mixer.music.stop()
    semiPlay = game.Game()
    if gamePlay.player1Win:
        finalAI = secondTournamentScreen(player1,semiAI,newP3,newP4)
        pygame.mixer.music.load('sound/theme.wav')
        pygame.mixer.music.play(0)
        semiPlay.new(player1, semiAI)
        while semiPlay.running:
            semiPlay.update()
    
    finalPlay = game.Game()
    if semiPlay.player1Win:
        finals(player1,finalAI)
        pygame.mixer.music.load('sound/theme.wav')
        pygame.mixer.music.play(0)
        finalPlay.new(player1, finalAI)
        while finalPlay.running:
            finalPlay.update()
    if finalPlay.player1Win:
        pygame.mixer.music.load('sound/champions_copy.wav')
        pygame.mixer.music.play(0)
        ending(player1)

    pygame.quit()

gameIntro()
splashScreen()
mainGame()

# import cProfile
# cProfile.run('gamePlay.update()')
