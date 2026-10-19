You've been out of storage for 83 days … Not enough storage. You can't save to Drive, back up to Photos, and use Gmail. Share 100 GB of storage with your family members for EGP 14.90 for 3 months EGP 59.99.
import pygame

import Full_Fruits
import Sliced_Fruits
import Timer
import Score
import Hearts
import Game_Over
from Hand_Tracker import init_blade, tick_blade, blade_current_pos


def run_fruit(screen):
    """نفس النافذة. يرجع 'menu' أو 'quit'."""
    clock = pygame.time.Clock()
    windowWidth, windowHeight = screen.get_size()
    Full_Fruits.FLOOR_Y = windowHeight

    pygame.display.set_caption("Fruit Ninja")
    pygame.mouse.set_visible(False)

    init_blade(windowWidth // 2, windowHeight // 2)

    bg_orig = pygame.image.load("Fruits_Photo/bg2.png")
    bg = pygame.transform.smoothscale(bg_orig, (windowWidth, windowHeight))

    hearts = [Hearts.FullHearts(i) for i in range(3)]
    fruits = []
    leftSlicedFruits = []
    rightSlicedFruits = []

    fullFruitsMapping = {
        "apple": Full_Fruits.Apples,
        "coconut": Full_Fruits.Coconuts,
        "pineapple": Full_Fruits.Pineapples,
        "orange": Full_Fruits.Oranges,
        "lemon": Full_Fruits.Lemons,
        "pear": Full_Fruits.Pears,
    }

    slicedFruitsMapping = {
        "apple": [Sliced_Fruits.SlicedLeftApples, Sliced_Fruits.SlicedRightApples],
        "coconut": [Sliced_Fruits.SlicedLeftCoconuts, Sliced_Fruits.SlicedRightCoconuts],
        "pineapple": [Sliced_Fruits.SlicedLeftPineapples, Sliced_Fruits.SlicedRightPineapples],
        "orange": [Sliced_Fruits.SlicedLeftOranges, Sliced_Fruits.SlicedRightOranges],
        "lemon": [Sliced_Fruits.SlicedLeftLemons, Sliced_Fruits.SlicedRightLemons],
        "pear": [Sliced_Fruits.SlicedLeftPears, Sliced_Fruits.SlicedRightPears],
    }

    score = Score.Score()
    timer = Timer.Timer()

    previousTime = 0
    gameState = Game_Over.GameOver(windowWidth, windowHeight)

    run = True
    while run:
        currentTime = pygame.time.get_ticks()
        elapsedTime = currentTime // 1000
        numOfFruits = 2 + (elapsedTime // 15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"

        screen.blit(bg, (0, 0))

        for heart in hearts:
            heart.draw(screen)

        tick_blade(windowWidth, windowHeight)
        mouse_currentPos = blade_current_pos()
        pygame.draw.circle(screen, (0, 0, 255), mouse_currentPos, 10)

        if currentTime - previousTime >= 2000:
            for i in range(numOfFruits):
                fruits.append(Full_Fruits.Fruits.randomFruitSelection(fullFruitsMapping))
            previousTime = currentTime

        for fruit in fruits:
            if fruit.hitboxType == "circular" and not fruit.isSliced:
                distance = (
                    (fruit.center[0] - mouse_currentPos[0]) ** 2
                    + (fruit.center[1] - mouse_currentPos[1]) ** 2
                ) ** 0.5
                if distance <= fruit.radius:
                    fruit.isSliced = True
                    fruitMapped = slicedFruitsMapping[fruit.type]
                    leftSlicedFruits.append(fruitMapped[0](fruit.x, fruit.y))
                    rightSlicedFruits.append(fruitMapped[1](fruit.x, fruit.y))
                    score.updateScore()

            elif fruit.hitboxType == "rectangular" and not fruit.isSliced:
                if fruit.rect.collidepoint(mouse_currentPos):
                    fruit.isSliced = True
                    fruitMapped = slicedFruitsMapping[fruit.type]
                    leftSlicedFruits.append(fruitMapped[0](fruit.x, fruit.y))
                    rightSlicedFruits.append(fruitMapped[1](fruit.x, fruit.y))
                    score.updateScore()

        if not gameState.gameOver:
            for fruit in fruits[:]:
                fruit.movement()
                if fruit.y >= windowHeight or fruit.isSliced:
                    fruits.remove(fruit)
                if (
                    fruit.y >= windowHeight
                    and not fruit.isSliced
                    and hearts
                    and fruit.velocityY > 0
                ):
                    hearts.pop()

            for lsf in leftSlicedFruits[:]:
                lsf.movementSliced()
                if lsf.leftY >= windowHeight:
                    leftSlicedFruits.remove(lsf)

            for rsf in rightSlicedFruits[:]:
                rsf.movementSliced()
                if rsf.rightY >= windowHeight:
                    rightSlicedFruits.remove(rsf)

            timer.updateTimer(elapsedTime)

        if len(hearts) == 0:
            gameState.gameOver = True

        for fruit in fruits:
            fruit.draw(screen)

        for lsf in leftSlicedFruits:
            lsf.drawSliced(screen)

        for rsf in rightSlicedFruits:
            rsf.drawSliced(screen)

        score.drawScore(screen, 20, 70)
        timer.drawTimer(screen)

        if gameState.gameOver:
            gameState.display(screen, windowWidth, windowHeight, score)

        pygame.display.update()
        clock.tick(60)

    return "menu"


if __name__ == "__main__":
    from Hand_Tracker import shutdown_hand_tracker

    pygame.init()
    wnd = pygame.display.set_mode((1024, 772))
    init_blade(512, 386)
    run_fruit(wnd)
    shutdown_hand_tracker()
    pygame.quit()