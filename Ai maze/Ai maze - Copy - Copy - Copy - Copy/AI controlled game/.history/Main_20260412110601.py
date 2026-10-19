import pygame
import Full_Fruits
import Sliced_Fruits
import Timer
import Score
import Hearts
import Game_Over
from Hand_Tracker import (
    init_blade,
    tick_blade,
    blade_current_pos,
    shutdown_hand_tracker,
)

# import Mouse  # غلط: كان يخلّي اللعبة تعتمد على الماوس
# from Hand_Tracker import get_finger_position, shutdown_hand_tracker  # غلط: ناقص init_blade / tick_blade للشفرة فقط

# True = use webcam + hand when detected; falls back to mouse if hand is lost or camera fails  # غلط: التعليق كان يوصف fallback للماوس بينما الكود القديم كان يحرّك الماوس كل فريم
# USE_HAND_TRACKER = True  # غلط: مع mouse.mouseTracking() النقطة كانت تتبع الماوس حتى مع تفعيل الإيد

pygame.init()

windowWidth = 1024
windowHeight = 772
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Fruit Ninja")
pygame.mouse.set_visible(False)  # OS cursor off; input is hand only

init_blade(windowWidth // 2, windowHeight // 2)  # blade starts center until hand seen

bg = pygame.image.load('Fruits_Photo/bg2.png')
hearts = [Hearts.FullHearts(i) for i in range(3)] # creating 3 hearts (lives)
fruits = []
leftSlicedFruits = []
rightSlicedFruits = []

fullFruitsMapping = {
    "apple": Full_Fruits.Apples,
    "coconut": Full_Fruits.Coconuts,
    "pineapple": Full_Fruits.Pineapples,
    "orange": Full_Fruits.Oranges,
    "lemon": Full_Fruits.Lemons,
    "pear": Full_Fruits.Pears
}

slicedFruitsMapping = {
    "apple": [Sliced_Fruits.SlicedLeftApples, Sliced_Fruits.SlicedRightApples],
    "coconut": [Sliced_Fruits.SlicedLeftCoconuts, Sliced_Fruits.SlicedRightCoconuts],
    "pineapple": [Sliced_Fruits.SlicedLeftPineapples, Sliced_Fruits.SlicedRightPineapples],
    "orange": [Sliced_Fruits.SlicedLeftOranges, Sliced_Fruits.SlicedRightOranges],
    "lemon": [Sliced_Fruits.SlicedLeftLemons, Sliced_Fruits.SlicedRightLemons],
    "pear": [Sliced_Fruits.SlicedLeftPears, Sliced_Fruits.SlicedRightPears]
}
# mouse = Mouse.Mouse()  # غلط: كائن الماوس — شيلناه عشان التحكم بالإيد فقط
score = Score.Score()
timer = Timer.Timer()

previousTime = 0
gameState = Game_Over.GameOver(windowWidth, windowHeight)

run = True
while run:
    pygame.time.delay(100)
    currentTime = pygame.time.get_ticks()
    elapsedTime = currentTime // 1000 # convert to seconds
    numOfFruits = 2 + (elapsedTime // 15) # add one fruit every 15 seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # if timer.timeLeft == 0 or if lives == 0:
    #     run = False

    window.blit(bg, (0, 0))
    
    for heart in hearts:
        heart.draw(window)
    
    # mouse.mouseTracking()  # غلط: يحدّث الموضع من الماوس كل فريم فيطغى على الإيد
    # if USE_HAND_TRACKER:  # غلط: مع السطر فوق النقطة كانت ورا الماوس
    #     fx, fy = get_finger_position(windowWidth, windowHeight)
    #     if fx >= 0.0 and fy >= 0.0:
    #         new_pos = (int(fx), int(fy))
    #         mouse.dx = new_pos[0] - mouse.previousPos[0]
    #         mouse.dy = new_pos[1] - mouse.previousPos[1]
    #         mouse.speed = (mouse.dx ** 2 + mouse.dy ** 2) ** 0.5
    #         mouse.previousPos = new_pos
    #         mouse.currentPos = new_pos
    # mouse.draw(window)  # غلط: يرسم على موضع الماوس مش الإيد لو الإيد ضاعت

    tick_blade(windowWidth, windowHeight)
    mouse_currentPos = blade_current_pos()  # same role as old mouse.currentPos for hit tests
    pygame.draw.circle(window, (0, 0, 255), mouse_currentPos, 10)  # was mouse.draw(window)

    if (currentTime - previousTime >= 2000):
        for i in range(numOfFruits):
            fruits.append(Full_Fruits.Fruits.randomFruitSelection(fullFruitsMapping))
        previousTime = currentTime

    for fruit in fruits:
        # detecting collision with circular fruit
        if fruit.hitboxType == "circular" and not(fruit.isSliced):
            distance = ((fruit.center[0] - mouse_currentPos[0]) ** 2 + (fruit.center[1] - mouse_currentPos[1]) ** 2) ** 0.5 #, 
            if distance <= fruit.radius:
                fruit.isSliced = True
                fruitMapped = slicedFruitsMapping[fruit.type]
                leftSlicedFruits.append(fruitMapped[0](fruit.x, fruit.y))
                rightSlicedFruits.append(fruitMapped[1](fruit.x, fruit.y))
                score.updateScore()

        # detecting collision with rectangular fruit
        elif fruit.hitboxType == "rectangular" and not(fruit.isSliced):
            if fruit.rect.collidepoint(mouse_currentPos): # mouse.currentPos
                fruit.isSliced = True
                fruitMapped = slicedFruitsMapping[fruit.type]
                leftSlicedFruits.append(fruitMapped[0](fruit.x, fruit.y))
                rightSlicedFruits.append(fruitMapped[1](fruit.x, fruit.y))
                score.updateScore()

    if not gameState.gameOver:
        for fruit in fruits:
            fruit.movement()
            if fruit.y >= 772 or fruit.isSliced:
                fruits.remove(fruit)
            if fruit.y >= 772 and not fruit.isSliced and hearts and fruit.velocityY > 0: # 3rd condition will be deleted soon
                hearts.pop()

        for lsf in leftSlicedFruits:
            lsf.movementSliced()
            if lsf.leftY >= 772:
                leftSlicedFruits.remove(lsf)

        for rsf in rightSlicedFruits:
            rsf.movementSliced()
            if rsf.rightY >= 772:
                rightSlicedFruits.remove(rsf)

        timer.updateTimer(elapsedTime)

    if len(hearts) == 0:
        gameState.gameOver = True

    for fruit in fruits:
        fruit.draw(window)

    for lsf in leftSlicedFruits: 
        lsf.drawSliced(window)

    for rsf in rightSlicedFruits: 
        rsf.drawSliced(window)

    score.drawScore(window, 20, 70)
    timer.drawTimer(window)

    if gameState.gameOver:
        # gameState.display(window, windowWidth, windowHeight)  # غلط: ناقص score → TypeError في drawScore
        gameState.display(window, windowWidth, windowHeight, score)

    pygame.display.update()

shutdown_hand_tracker()
pygame.quit()
