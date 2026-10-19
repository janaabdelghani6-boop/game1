import pygame
import Full_Fruits
import Sliced_Fruits
import Timer
import Score
import Hearts
import Game_Over
import Blade
pygame.init()

windowWidth = 1024
windowHeight = 772
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Fruit Ninja")

pygame.mouse.set_visible(False) # input is hand only

bg = pygame.image.load('Fruits_Photo/bg2.png')
hearts = [Hearts.FullHearts(i) for i in range(3)] # creating 3 hearts (lives)
fruits = []
slicedFruits = []
bombs = []
fullFruitsMapping = {
    "bomb": Full_Fruits.Bombs,
    "apple": Full_Fruits.Apples,
    "coconut": Full_Fruits.Coconuts,
    "pineapple": Full_Fruits.Pineapples,
    "orange": Full_Fruits.Oranges,
    "lemon": Full_Fruits.Lemons,
    "pear": Full_Fruits.Pears
}
slicedFruitsMapping = {
    "apple": Sliced_Fruits.SlicedApples,
    "coconut": Sliced_Fruits.SlicedCoconuts,
    "pineapple": Sliced_Fruits.SlicedPineapples,
    "orange": Sliced_Fruits.SlicedOranges,
    "lemon": Sliced_Fruits.SlicedLemons,
    "pear": Sliced_Fruits.SlicedPears
}
Score.Score.loadHighScore()
blade = Blade.Blade(windowWidth, windowHeight)
score = Score.Score()
timer = Timer.Timer()
gameState = Game_Over.GameOver(windowWidth, windowHeight)
startTime = None
currentTime = None
previousTime = 0
timerStarted = False
bombAppeared = False
run = True

while run:
    pygame.time.delay(40)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if gameState.gameOver:
        for fruit in fruits:
            if fruit.type == "bomb":
                fruit.burningSound.stop()
        if gameState.playSound:
            gameState.sound.play()
            gameState.playSound = False

        for i in range(5, len(blade.bladePoints)):
            if gameState.restartRect.clipline(blade.bladePoints[i - 1], blade.bladePoints[i]):
                gameState.restartLoadingFlag = True
            else:
                gameState.restartLoadingFlag = False

            if gameState.exitRect.clipline(blade.bladePoints[i - 1], blade.bladePoints[i]):
                gameState.exitLoadingFlag = True
            else:
                gameState.exitLoadingFlag = False
            gameState.buttonTrigger()
            
        if gameState.restart:
            hearts.clear()
            fruits.clear()
            hearts = [Hearts.FullHearts(i) for i in range(3)]
            score = Score.Score()
            timer = Timer.Timer()
            startTime = pygame.time.get_ticks()
            gameState = Game_Over.GameOver(windowWidth, windowHeight)
                    
        if gameState.exit:
            run = False

    if timer.timeLeft == 0 and not gameState.gameOver: # to be checked each game state
        gameState.gameOver = True
        gameState.playSound = True
        buttonFlag = True
        gameState.gameOverType("time's up", windowWidth, windowHeight)

    window.blit(bg, (0, 0))
    blade.update(windowWidth, windowHeight)
    
    if not gameState.gameOver and len(bombs) == 0 and startTime:
        currentTime = pygame.time.get_ticks()
        elapsedTime = (currentTime - startTime) // 1000 # convert to seconds
        numOfFruits = 1 + (elapsedTime // 20) # add one fruit every 20 seconds
        timer.updateTimer(elapsedTime)

        if (currentTime - previousTime >= 2000):
            for i in range(numOfFruits):
                fruitInit, bombAppeared = Full_Fruits.Fruits.randomFruitSelection(fullFruitsMapping, bombAppeared)
                fruits.append(fruitInit)
            previousTime = currentTime

        for fruit in fruits[:]:
            for i in range(5, len(blade.bladePoints)):
                
                # detecting collision with circular fruit
                if fruit.hitboxType == "circular" and not(fruit.isSliced):
                    if  Blade.Blade.circularCollision(blade.bladePoints[i - 1], blade.bladePoints[i], fruit.center[0], fruit.center[1], fruit.radius):
                        if fruit.type != "bomb":
                            fruit.isSliced = True
                            blade.sound.play()
                            fruitMapped = slicedFruitsMapping[fruit.type]
                            slicedFruits.append(fruitMapped(fruit.x, fruit.y))
                            score.updateScore(currentTime, fruit.x, fruit.y)
                        else: # bomb got hit
                            bombs.append(fruit)
                            fruits.remove(fruit)
                            break

                # detecting collision with rectangular fruit
                elif fruit.hitboxType == "rectangular" and not(fruit.isSliced):
                    if fruit.rect.clipline(blade.bladePoints[i - 1], blade.bladePoints[i]):
                        fruit.isSliced = True
                        blade.sound.play()
                        fruitMapped = slicedFruitsMapping[fruit.type]
                        slicedFruits.append(fruitMapped(fruit.x, fruit.y))
                        score.updateScore(currentTime, fruit.x, fruit.y)

        for fruit in fruits[:]:
            fruit.movement()
            if fruit.y < windowHeight and fruit.velocityY < 0 and fruit.isSpawned:
                fruit.spawnSound.play()
                fruit.isSpawned = False
            if fruit.y >= windowHeight or fruit.isSliced:
                if fruit.type == "bomb":
                    fruit.burningSound.stop()
                fruits.remove(fruit)
            if fruit.y >= windowHeight and not fruit.isSliced and hearts and fruit.type != "bomb" and fruit.velocityY > 0:#or fruit.x >= windowWidth )
                hearts[0].sound.play() # the last heart remaining
                hearts.pop()

        for sf in slicedFruits[:]:
            sf.movementSliced()
            if (sf.endTime - sf.startTime) >= 1000:
                slicedFruits.remove(sf)

    for bomb in bombs[:]: # if bomb got hit
            bomb.burningSound.stop()
            bomb.explosion(window)
            if bomb.finished:
                bombs.remove(bomb)
                gameState.gameOver = True
                gameState.playSound = True
                buttonFlag = True
                gameState.gameOverType("lose", windowWidth, windowHeight)

    if len(hearts) == 0 and not gameState.gameOver: # to be checked each game state
        gameState.gameOver = True
        gameState.playSound = True
        buttonFlag = True
        gameState.gameOverType("lose", windowWidth, windowHeight)

    for heart in hearts:
        heart.draw(window)

    for fruit in fruits:
        fruit.draw(window)

    for sf in slicedFruits: 
        sf.drawSliced(window)

    score.drawScore(window, score.score, 130, 90)
    score.drawHighScore(window, 840, 40)
    if currentTime:
        score.drawCombo(window, currentTime)
    timer.drawTimer(window)

    if gameState.gameOver:
        gameState.display(window, windowWidth, windowHeight, score.score)
    
    blade.draw(window)

    pygame.display.update()

    if not timerStarted: # start timer when 1st frame ends
        startTime = pygame.time.get_ticks()
        timerStarted = True

Blade.Blade.terminate()
pygame.quit()