import sys

import pygame
import colour
import random

sizeOfWindow = [2000, 1500]
pygame.init()
win = pygame.display.set_mode(sizeOfWindow)

countOfEnemy = 20
randomSpead = True
randomColor = True
infinity = True
backgroundColor = (0, 0, 0)
enemiesList = []
running = True
score = 0
player = None
wave = 1
defaultStepWave = 20
stepWave = defaultStepWave
defaultLastWaveScore = 1
lastWaveScore = defaultLastWaveScore
gameOver = False
generateEnemy = True
playAgainR = None
quitR = None

iForWave = 0
startingTime = False
endFlagStartingTime = False


class ManagementGame:
    @staticmethod
    def init():
        global playAgainR
        global quitR
        global player
        player = Rect(100, 100, 1000, 1300, "white", False, False, False, False, 8, 0, False, False)
        for num in range(countOfEnemy + 1):
            Rect
        playAgainR = Rect(300, 200, 1450, 1000, "white", False, False, False, False, 0, 5, False, False)
        quitR = Rect(300, 200, 250, 1000, "white", False, False, False, False, 0, 5, False, False)

    @staticmethod
    def gameOver():
        global gameOver
        gameOver = True
        pygame.display.update()
        global running
        running = False
        ManagementGame.claerEnemy()
        print('hi')
        global player

    @staticmethod
    def showTitle(score):
        global wave
        textScore = pygame.font.Font(None, 80)
        win.blit(textScore.render(f"Score: {score}", False, (255, 255, 255)), (0, 0))
        textScore = pygame.font.Font(None, 60)
        win.blit(textScore.render(f"wave: {wave}", False, (255, 0, 255)), (0, 60))
        if gameOver:
            ManagementGame.GameOverTitle()

    @staticmethod
    def GameOverTitle():
        global playAgainR
        global quitR
        global player
        global running
        global generateEnemy
        global gameOver
        global wave
        global lastWaveScore
        global score
        global defaultStepWave
        global defaultStepWave
        global stepWave
        text = pygame.font.Font(None, 250)
        text2 = pygame.font.Font(None, 100)
        win.blit(text.render(f"GAME OVER", False, (255, 0, 0)), (460, 650))
        win.blit(text2.render(f"final score: {score}", False, (255, 255, 255)), (720, 850))
        global playAgainR
        global quitR
        playAgainR.show()
        quitR.show()
        if (playAgainR.x < player.x < playAgainR.x + playAgainR.w) or (
                player.x < playAgainR.x < player.x + player.w) or (player.x == playAgainR.x):
            if (playAgainR.y < player.y < playAgainR.y + playAgainR.h) or (
                    player.y < playAgainR.y < player.y + player.h):
                running = True
                generateEnemy = True
                gameOver = False
                lastWaveScore = defaultLastWaveScore
                stepWave = defaultStepWave
                score = 0
                wave = 1

        if (quitR.x < player.x < quitR.x + quitR.w) or (player.x < quitR.x < player.x + player.w) or (
                player.x == quitR.x):
            if (quitR.y < player.y < quitR.y + quitR.h) or (player.y < quitR.y < player.y + player.h):
                pygame.quit()
                sys.exit()
        playAgainT = pygame.font.Font(None, 100)
        quitT = pygame.font.Font(None, 100)
        win.blit(playAgainT.render(f"again", False, (255, 255, 255)), (1510, 1060))
        win.blit(quitT.render(f"quit", False, (255, 255, 255)), (330, 1060))

    @staticmethod
    def claerEnemy():
        enemiesList.clear()
        player.x = 940
        player.y = 1100

    @staticmethod
    def manageWave():
        global lastWaveScore
        global stepWave
        global generateEnemy
        global wave
        global showTitleWave
        global startingTime
        global running
        global endFlagStartingTime
        global countOfEnemy
        if ((score - lastWaveScore) - stepWave) > 0:
            lastWaveScore = score
            wave += 1
            countOfEnemy += 2
            stepWave += countOfEnemy * 2
            startingTime = True
            running = False
            ManagementGame.claerEnemy()
        ManagementGame.checkTime(1000)
        if endFlagStartingTime and not gameOver:
            generateEnemy = True
            running = True
            endFlagStartingTime = False

        if startingTime:
            textWave = pygame.font.Font(None, 80)
            win.blit(textWave.render(f"Wave: {wave}", False, (255, 255, 255)), (450, 650))

    @staticmethod
    def checkTime(count):
        global iForWave
        global startingTime
        global endFlagStartingTime
        iForWave += 1
        if iForWave - count == 0:
            iForWave = 0
            startingTime = False
            endFlagStartingTime = True
            return True
        return False

    @staticmethod
    def intoWhile():
        ManagementGame.showTitle(score)
        ManagementGame.manageWave()
        keys = pygame.key.get_pressed()  # checking pressed keys
        if keys[pygame.K_UP]:
            player.moveY(False)
        if keys[pygame.K_DOWN]:
            player.moveY()
        if keys[pygame.K_LEFT]:
            player.moveX(False)
        if keys[pygame.K_RIGHT]:
            player.moveX()

        ManagementGame.checkPlayer()
        player.show()
        if running:
            if generateEnemy:
                if len(enemiesList) < countOfEnemy:
                    Rect()

            for item in enemiesList:
                item.moveY()
                item.check()
        pygame.display.update()
        win.fill(backgroundColor)

    @staticmethod
    def checkPlayer():
        global player
        if player.x + player.w > sizeOfWindow[0]:
            player.x = sizeOfWindow[0] - player.w
        if player.x < 0:
            player.x = 0
        if player.y < 0:
            player.y = 0
        if player.y + player.h > sizeOfWindow[1]:
            player.y = sizeOfWindow[1] - player.h


class Color:
    colorRGB = None
    nameOfSomeColor = ['DarkGreen', 'Green', 'DarkCyan', 'DeepSkyBlue', 'DarkTurquoise', 'MediumSpringGreen', 'Lime',
                       'SpringGreen', 'Cyan', 'Aqua', 'MidnightBlue', 'DodgerBlue', 'LightSeaGreen', 'ForestGreen',
                       'SeaGreen', 'DarkSlateGray', 'DarkSlateGrey', 'LimeGreen', 'MediumSeaGreen', 'Turquoise',
                       'RoyalBlue', 'SteelBlue', 'DarkSlateBlue', 'MediumTurquoise']

    def __init__(self, color="white"):
        self.getRGB(color)

    def getRGB(self, color):
        c = list(colour.Color(color).get_rgb())
        c[0] = int(c[0] * 255)
        c[1] = int(c[1] * 255)
        c[2] = int(c[2] * 255)
        self.colorRGB = tuple(c)

    def getColor(self):
        return self.colorRGB

    def getRandomColor(self):
        self.getRGB(random.choice(self.nameOfSomeColor))


class Rect:
    x = None
    y = None
    w = None
    h = None
    color = None
    spead = None
    border = None
    randColor = None
    randSize = None
    randPositionX = None
    randSpead = None
    randBorder = None

    def __init__(self, w=0, h=0, x=0, y=0, color="white", randColor=True, randSize=True, randPositionX=True,
                 randSpead=True, spead=5,
                 border=5, append=True, randBorder=True):
        self.randColor = randColor
        self.x = x
        self.y = y
        self.spead = spead
        self.color = color
        self.border = border
        self.randSize = randSize
        self.w = w
        self.h = h
        self.randPositionX = randPositionX
        self.randSpead = randSpead
        self.randBorder = randBorder
        self.random()
        self.show()

        if append:
            enemiesList.append(self)

    def moveY(self, direction=True):
        if direction:
            self.y += self.spead
            self.show()
            self.destroyer()
        else:
            self.y -= self.spead
            self.show()
            self.destroyer()

    def random(self):
        if self.randColor:
            color = Color()
            color.getRandomColor()
            self.color = color.colorRGB
        if self.randSize:
            self.w = random.randint(30, 150)
            self.h = random.randint(30, 150)
        if self.randPositionX:
            self.x = random.randint(0, sizeOfWindow[0])
        if self.randSpead:
            self.spead = random.randint(1, 10)
        if self.randBorder:
            if random.randint(0, 1):
                self.border = random.randint(4, 15)
            else:
                self.border = 0

    def moveX(self, direction=True):
        if direction:
            self.x += self.spead
            self.show()
            self.destroyer()
        else:
            self.x -= self.spead
            self.show()
            self.destroyer()

    def show(self):
        pygame.draw.rect(win, self.color, ((self.x, self.y), (self.w, self.h)), self.border)

    def destroyer(self):
        if self.y > (sizeOfWindow[1] + 200):
            enemiesList.remove(self)
            global score
            score += 1

    def check(self):
        if (self.x < player.x < self.x + self.w) or (player.x < self.x < player.x + player.w) or (player.x == self.x):
            if (self.y < player.y < self.y + self.h) or (player.y < self.y < player.y + player.h):
                ManagementGame.gameOver()


ManagementGame.init()

while True:
    ManagementGame.intoWhile()
    events = pygame.event.get()
    for item in events:
        if item.type == pygame.QUIT:
            pygame.quit()
            pygame.sys.exit()
