import sys, pygame, random
from pygame import *
from pygame.locals import *
from pygame.sprite import *


class Mole(Sprite):

    def __init__(self, posx, posy, rad):
        Sprite.__init__(self)
        self.image = pygame.transform.scale(image.load('chocolatemilk.png'), (rad, rad))
        self.rect = self.image.get_rect(center=centerOfCircle(posx, posy))


FPS = 80
BOARDWIDTH = 4
BOARDHEIGHT = 4
RADIUS = 50
GAP = 10
WINDOWWIDTH = (BOARDWIDTH * 2 * RADIUS) + (GAP) + (GAP * BOARDWIDTH - 1)
WINDOWHEIGHT = (BOARDHEIGHT * 2 * RADIUS) + (GAP) + (GAP * BOARDHEIGHT - 1) + (RADIUS * 2)
assert BOARDWIDTH >= 4

RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (150, 0, 150)
BLUE = (50, 50, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def main():
    global DISPLAYSURF, FPSCLOCK, HIT
    HIT = 0
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Whack-a-mole')

    DISPLAYSURF.fill(BLUE)
    drawGame()
    drawTimerHit()
    pygame.display.update()
    increaseHitCount(HIT)
    while True:
        drawTimerHit()
        drawGame()

        molex, moley = random.randrange(BOARDWIDTH), random.randrange(BOARDHEIGHT)
        riseAnimation(molex, moley)
        drawTimerHit()
        fallAnimation(molex, moley)
        mole = Mole(molex, moley, RADIUS)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and mole.rect.collidepoint(mouse.get_pos()):
                HIT += 1
                increaseHitCount(HIT)
                break
        pygame.display.update()


def drawTimerHit():
    pygame.draw.rect(DISPLAYSURF, BLUE, (0, 0, 140, 75))
    pygame.draw.rect(DISPLAYSURF, BLACK, (5, 10, 140, 75), 5)
    numSeconds = int(pygame.time.get_ticks() / 1000)
    secFont = getScaledFont(75, 75, str(000), 'Comic Sans')
    text = secFont.render(str(numSeconds), 1, BLACK)
    text_rect = text.get_rect(center=(65, 50))
    DISPLAYSURF.blit(text, text_rect)



def drawGame():
    pygame.draw.rect(DISPLAYSURF, BLUE, (0, 75, BOARDWIDTH, BOARDHEIGHT - 75))
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            pygame.draw.circle(DISPLAYSURF, PURPLE, ((RADIUS + GAP) + (GAP * i) + (i * 2 * RADIUS), (RADIUS * 2) + (RADIUS + GAP) + (GAP * j) + (j * 2 * RADIUS)), RADIUS)


def increaseHitCount(hit):
    pygame.draw.rect(DISPLAYSURF, BLUE, (140, 0, 300, 100))
    pygame.draw.rect(DISPLAYSURF, BLACK, (140, 10, 305, 75), 5)
    font = getScaledFont(300, 100, 'Drinks: 000', 'Comic Sans')
    text = font.render('Drinks: ' + str(hit), 1, BLACK)
    text_rect = text.get_rect(center=(290, 50))
    DISPLAYSURF.blit(text, text_rect)


def riseAnimation(circx, circy):
    centx, centy = centerOfCircle(circx, circy)
    left = centx - int(RADIUS / 2)
    top = centy + int(RADIUS / 2)
    for height in range(RADIUS):
        if pygame.time.get_ticks() % 1000 == 0 :
            drawTimerHit()
        if MOUSEBUTTONDOWN and Mole(circx, circy, RADIUS).rect.collidepoint(mouse.get_pos()):
            increaseHitCount(HIT + 1)
            return 0
        drawGame()
        top -= 1
        moleSurf = pygame.Surface((RADIUS, height))
        moleSurf.blit(Mole(centx, centy, RADIUS).image, (0, 0))
        DISPLAYSURF.blit(moleSurf, (left, top))
        pygame.display.update()
        pygame.time.Clock().tick(FPS + int(pygame.time.get_ticks() / 1000))


def fallAnimation(circx, circy):
    centx, centy = centerOfCircle(circx, circy)
    left = centx - int(RADIUS / 2)
    top = centy - int(RADIUS / 2)
    for height in reversed(range(RADIUS)):
        if pygame.time.get_ticks() % 1000 == 0:
            drawTimerHit()
        if MOUSEBUTTONDOWN and Mole(circx, circy, RADIUS).rect.collidepoint(mouse.get_pos()):
            increaseHitCount(HIT + 1)
            return 0
        drawGame()
        top += 1
        moleSurf = pygame.Surface((RADIUS, height))
        moleSurf.blit(Mole(centx, centy, RADIUS).image, (0, 0))
        DISPLAYSURF.blit(moleSurf, (left, top))
        pygame.display.update()
        pygame.time.Clock().tick(FPS + int(pygame.time.get_ticks() / 1000))


def circleRect(circlex, circley):
    centx, centy = centerOfCircle(circlex, circley)
    left = centx - RADIUS
    top = centy - RADIUS
    return (left, top, RADIUS * 2, RADIUS * 2)


def centerOfCircle(circlex, circley):
    centx = 2 * (circlex + .5) * RADIUS + GAP * (circlex + 1)
    centy = 2 * (circley + .5) * RADIUS + RADIUS * 2 + GAP * (circley + 1)
    return centx, centy


def getCircleAtPixel(x, y):
    for circlex in range(BOARDWIDTH):
        for circley in range(BOARDHEIGHT):
            centx, centy = centerOfCircle(circlex, circley)
            boxCirc = pygame.Rect(centx - RADIUS, centy - RADIUS, 2 * RADIUS, 2 * RADIUS)
            if boxCirc.collidepoint(x, y):
                return circlex, circley
    return None, None


def getBoardPosish(num):
    circlex = int(num / 4)
    circley = num % 4
    return circlex, circley


def getScaledFont(max_w, max_h, text, font_name):
    font_size = 0
    font = pygame.font.SysFont(font_name, font_size)
    w, h = font.size(text)
    while w < max_w and h < max_h:
        font_size += 1
        font = pygame.font.SysFont(font_name, font_size)
        w, h = font.size(text)
    return pygame.font.SysFont(font_name, font_size - 1)


if __name__ == '__main__':
    main()
