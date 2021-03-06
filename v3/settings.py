#*****Unless specified, all of the drawings are done by me with pixilart.com*****#


import pygame
import math
pygame.mixer.init()
###################################################
####################GAME SETUPS####################
###################################################
TITLE = '11HEAD SOCCER2'
WIDTH = 700
HEIGHT = 330
FPS = 200
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
BALL_r = 20
BALL_f = -0.3
###################################################
####################PLAYER SETUPS##################
###################################################
PLAYER_a = 0.5
PLAYER_f = -0.15
PLAYER_m = 100
PLAYER_r = 25
###################################################
####################AI SETUPS######################
###################################################
AI_a = 0.5
AI_f = -0.15
AI_m = 100
AI_r = 25

###################################################
####################SOUND SETUPS###################
###################################################
goalSound = pygame.mixer.Sound('sound/GOAL.wav')
lostSound = pygame.mixer.Sound('sound/lost.wav')
nextSound = pygame.mixer.Sound('sound/next.wav')
buttonSound = pygame.mixer.Sound('sound/button.wav')
upButton = pygame.mixer.Sound('sound/up.wav')
downButton = pygame.mixer.Sound('sound/down.wav')
###################################################
#https://freesound.org/people/volivieri/sounds/37159/
ballSound = pygame.mixer.Sound('sound/ballS.wav')
ballGroundSound = pygame.mixer.Sound('sound/ballground.wav')
###################################################
crowdSound = pygame.mixer.Sound('sound/crowd.wav')

crowdSound.set_volume(0.2)
goalSound.set_volume(0.2)
lostSound.set_volume(0.3)
nextSound.set_volume(0.3)
buttonSound.set_volume(0.5)
upButton.set_volume(0.3)
downButton.set_volume(0.3)
ballSound.set_volume(1)
ballGroundSound.set_volume(0.5)


###################################################
####################IMAGES SETUPS##################
###################################################
iGoal = pygame.image.load('images/goal.png')
iBall =pygame.image.load('images/ball.png')
iGP1=pygame.image.load('images/goalpost1.png')
iGP2=pygame.image.load('images/goalpost2.png')    
fieldImage = pygame.image.load('images/background.png')
scoreBoardImage =  pygame.image.load('images/scoreboard1.png')

######################
#Andrew Kim (CMU'2023)
woodImage = pygame.image.load('images/wood_art.jpg')
#UEFA for reference
uefaLogo =  pygame.image.load('images/UEFA.png')
stadiumImage = pygame.image.load('images/stadium1.png')
######################

################################################################################
#https://www.shutterstock.com/search/geometrical+people?image_type=illustration&page=2
AudImage1 = pygame.image.load('images/aud11.png')
AudImage2 = pygame.image.load('images/aud22.png')
AudImage3 = pygame.image.load('images/aud33.png')
AudImage4 = pygame.image.load('images/aud44.png')
################################################################################
ibannerImage = pygame.image.load('images/banner.png')
choiceBG = pygame.image.load('images/choiceBG.png')
LEFT = pygame.image.load('images/leftPressed.png')
RIGHT = pygame.image.load('images/rightPressed.png')
UP = pygame.image.load('images/upPressed.png')
goal1 = pygame.image.load('images/g1.png')
goal2 = pygame.image.load('images/g2.png')
goal3 = pygame.image.load('images/g3.png')
goal4 = pygame.image.load('images/g4.png')
goal5 = pygame.image.load('images/g5.png')
goalSPRITE = [goal1,goal2,goal3,goal4,goal5]
goalBG = pygame.image.load('images/goalBG.png')
playerUpPressed = pygame.image.load('images/playerUpPressed.png')
playerDownPressed = pygame.image.load('images/playerDownPressed.png')
aiUpPressed = pygame.image.load('images/aiUpPressed.png')
aiDownPressed = pygame.image.load('images/aiDownPressed.png')
nextPressed = pygame.image.load('images/nextPressed.png')
################################################################
#https://www.dreamstime.com/illustration/pixel-art-airplane.html
#while not completely used, referred to it for drawing
airplane = pygame.image.load('images/airplane.png')
################################################################
qMark = pygame.image.load('images/qMark.png')   
tournament = pygame.image.load('images/tournament.png')
tournamentSemi = pygame.image.load('images/tournamentSemi.png')
tournamentFinal = pygame.image.load('images/tournamentFinal.png')
iwinFlag = pygame.image.load('images/winFlag.png')
#############################################
#http://pixelartmaker.com/art/095fdd43110bb39
iTrophy = pygame.image.load('images/trophy.png')
#############################################
iChampion = pygame.image.load('images/champion.png')
backgroundSplash = pygame.image.load('images/backgroundSplash.png')
start1 = pygame.image.load('images/start1.png')
start2 = pygame.image.load('images/start2.png')
clickedlogo = pygame.image.load('images/iclickedLogo.png')
lost = pygame.image.load('images/lost.png')
restart = pygame.image.load('images/restart.png')
restartClicked = pygame.image.load('images/restartClicked.png')
quitImg = pygame.image.load('images/quit.png')
quitClickedImg = pygame.image.load('images/quitClicked.png')
#############################################
#https://thenounproject.com/term/mute/228608/
imuteImg = pygame.image.load('images/mute.png')
isoundOnImg = pygame.image.load('images/soundOn.png')
#############################################

pausedScreen = pygame.image.load('images/paused.png')
pausedResume = pygame.image.load('images/pausedResume.png')
pausedQuit = pygame.image.load('images/pausedQuit.png')

winFlag = pygame.transform.scale(iwinFlag,(400,100))
bannerImage = pygame.transform.scale(ibannerImage,(560,50))
ballImage = pygame.transform.scale(iBall,(BALL_r*2,BALL_r*2))
goalImage = pygame.transform.scale(iGoal,(400,200))
gpImage1 =  pygame.transform.scale(iGP1,(int(WIDTH//4),int(WIDTH//4)))
gpImage2 =  pygame.transform.scale(iGP2,(int(WIDTH//4),int(WIDTH//4)))
logoImage =  pygame.transform.scale(uefaLogo,(int(WIDTH//4),int(WIDTH//4)))
clickedlogoImage =  pygame.transform.scale(clickedlogo,(int(WIDTH//4),int(WIDTH//4)))
audImage1 = pygame.transform.scale(AudImage1,(400,50))
audImage2 = pygame.transform.scale(AudImage2,(400,50))
audImage3 = pygame.transform.scale(AudImage3,(400,50))
audImage4 = pygame.transform.scale(AudImage4,(400,50))
trophy = pygame.transform.scale(iTrophy,(75,75))
champion = pygame.transform.scale(iChampion,(700,330))
muteImg = pygame.transform.scale(imuteImg,(44,44))
soundOnImg = pygame.transform.scale(isoundOnImg,(44,44))

#ZLATAN 
zlatan1=pygame.image.load('images/zlatan/zlatan11.png')   
zlatan2=pygame.image.load('images/zlatan/zlatan22.png')   
zlatan3=pygame.image.load('images/zlatan/zlatan33.png')   
zlatanL = [zlatan1,zlatan2,zlatan3]
zImageList = [pygame.transform.scale(image,(50,60)) for image in zlatanL]
zFlippedImageList = [pygame.transform.flip(image,True,False) for image in zImageList]

#SON
son1 = pygame.image.load('images/son/son1.png')
son2 = pygame.image.load('images/son/son2.png')
son3 = pygame.image.load('images/son/son3.png')
sonL = [son1,son2,son3]
sImageList = [pygame.transform.scale(image,(50,60)) for image in sonL]
sFlippedImageList = [pygame.transform.flip(image,True,False) for image in sImageList]

#POGBA
pogba1 = pygame.image.load('images/pogba/pogba1.png')
pogba2 = pygame.image.load('images/pogba/pogba2.png')
pogba3 = pygame.image.load('images/pogba/pogba3.png')
pogbaL = [pogba1,pogba2,pogba3]
pImageList = [pygame.transform.scale(image,(50,60)) for image in pogbaL]
pFlippedImageList = [pygame.transform.flip(image,True,False) for image in pImageList]

#HAZARD
hazard1 = pygame.image.load('images/hazard/hazard1.png')
hazard2 = pygame.image.load('images/hazard/hazard2.png')
hazard3 = pygame.image.load('images/hazard/hazard3.png')
hazardL = [hazard1,hazard2,hazard3]
hImageList = [pygame.transform.scale(image,(50,60)) for image in hazardL]
hFlippedImageList = [pygame.transform.flip(image,True,False) for image in hImageList]

#MESSI
messi1 = pygame.image.load('images/messi/messi1.png')
messi2 = pygame.image.load('images/messi/messi2.png')
messi3 = pygame.image.load('images/messi/messi3.png')
messiL = [messi1,messi2,messi3]
mImageList = [pygame.transform.scale(image,(50,60)) for image in messiL]
mFlippedImageList = [pygame.transform.flip(image,True,False) for image in mImageList]

#NEYMAR
neymar1 = pygame.image.load('images/neymar/neymar1.png')
neymar2 = pygame.image.load('images/neymar/neymar2.png')
neymar3 = pygame.image.load('images/neymar/neymar3.png')
neymarL = [neymar1,neymar2,neymar3]
nImageList = [pygame.transform.scale(image,(50,60)) for image in neymarL]
nFlippedImageList = [pygame.transform.flip(image,True,False) for image in nImageList]

#AGUERO
aguero1 = pygame.image.load('images/aguero/aguero1.png')
aguero2 = pygame.image.load('images/aguero/aguero2.png')
aguero3 = pygame.image.load('images/aguero/aguero3.png')
agueroL = [aguero1,aguero2,aguero3]
aImageList = [pygame.transform.scale(image,(50,60)) for image in agueroL]
aFlippedImageList = [pygame.transform.flip(image,True,False) for image in aImageList]

#RONALDO
ronaldo1 = pygame.image.load('images/ronaldo/ronaldo1.png')
ronaldo2 = pygame.image.load('images/ronaldo/ronaldo2.png')
ronaldo3 = pygame.image.load('images/ronaldo/ronaldo3.png')
ronaldoL = [ronaldo1,ronaldo2,ronaldo3]
rImageList = [pygame.transform.scale(image,(50,60)) for image in ronaldoL]
rFlippedImageList = [pygame.transform.flip(image,True,False) for image in rImageList]
                                            #powerFull = 10,speedFull = 0.8,jump = -25
charDict = {'Pogba':[pImageList,pFlippedImageList,9,0.5,-18],'Zlatan':[zImageList,zFlippedImageList,10,0.35,-20],
            'Son':[sImageList,sFlippedImageList,7,0.8,-15],'Hazard':[hImageList,hFlippedImageList,7,0.7,-15],
            'Messi':[mImageList,mFlippedImageList,7,0.7,-15],'Neymar':[nImageList,nFlippedImageList,7,0.7,-18]
            ,'Aguero':[aImageList,aFlippedImageList,9,0.5,-18],'Ronaldo':[rImageList,rFlippedImageList,10,0.8,-20]}

charChooseList = ['Pogba','Zlatan','Son','Hazard', 'Messi','Neymar','Aguero','Ronaldo','Random']
charList = ['Pogba','Zlatan','Son','Hazard', 'Messi','Neymar','Aguero','Ronaldo']