import sys, pygame, time, random

#initialize pygame
pygame.init()

#variables
playerscore = 0
playershield = 10
stationhealth = 100
damage = 1
movement = 1

#for main loop
GamePlay = True

#size of screen in px
size = width, height = 1545, 900

#player laser and enemy laser speeds in [x, y] directions
speed = [0,-1]
enemyspeed = [0,1]

#colors in RGB
black = 0, 0, 0
white = 255, 255, 255
light_red = 236, 108, 91
red = 178, 34, 34
green = 0, 255, 0
gray = 170, 170, 170
dark_gray = 100, 100, 100
yellow = 255, 255, 102
blue = 0, 0, 255
purple = 255, 0, 255

#fonts
font = pygame.font.SysFont(None, 25)
font2 = pygame.font.Font(None, 100)
font3 = pygame.font.Font(None, 50)
font4 = pygame.font.SysFont('Corbel',35)
text = font4.render('quit' , True , white)

#display window
#has a set size
screen = pygame.display.set_mode(size)

#loading enemies
enemy = pygame.image.load("res/Alien-spaceship.png")
enemy = pygame.transform.scale(enemy, (100, 60))
enemies = []

#enemy spawn at random position at top of screen
for i in range(2):
    enemyrect = enemy.get_rect(topleft=(random.randint(10,width-110), 0))
    enemies.append(enemyrect)
    
#loading spaceship    
spaceship = pygame.image.load("res/Spaceship.png")
spaceship = pygame.transform.scale(spaceship, (100,100))
spaceshiprect = spaceship.get_rect(topleft=(width/2, height/2))

#loading lasers
las = pygame.image.load("res/Red-Laser.png")
las = pygame.transform.scale(las, (10,30))
lasrect = las.get_rect(topleft=(width/2, height/2))
lasers = []

#loading enemy lasers
enemylaser = pygame.image.load("res/Enemy-laser.png")
enemylaser = pygame.transform.scale(enemylaser, (10,20))
enemylaserrect = enemylaser.get_rect(topleft=(width/2, height/2))
enemylasers = []

#Enemy space station
#defeat to win
station = pygame.image.load("res/Space-Station.png")
stationrect = station.get_rect(center=(width/2, 0))
stationspeed = [0,0]
Station = []

#giant laser
biglas = pygame.image.load("res/Big-Laser.png")
biglasrect = biglas.get_rect(bottomright = (0, 0))
biglasers = []

#laser sound
laserblast = pygame.mixer.Sound("res/LaserBlast.mp3")
pygame.mixer.Sound.set_volume(laserblast, 0.2)

#explosion sound
explosion = pygame.mixer.Sound("res/explode-sound.wav")
pygame.mixer.Sound.set_volume(explosion, 0.5)

playerhitsound = pygame.mixer.Sound("res/Player-hit.wav")
pygame.mixer.Sound.set_volume(playerhitsound, 0.9)

#Delay between player lasers blasts
starttime=time.time()
timerdelay=0.2

#custom Events
ENEMYMOVE = pygame.USEREVENT+1
ENEMYSPAWN = pygame.USEREVENT+2
ENEMYATTACK = pygame.USEREVENT+3
STATIONMOVE = pygame.USEREVENT+4

#Event timers
#every set milliseconds gives an event
pygame.time.set_timer(ENEMYMOVE,20)
pygame.time.set_timer(ENEMYSPAWN, 1000)
pygame.time.set_timer(ENEMYATTACK, 2000)
pygame.time.set_timer(STATIONMOVE, 200)

# Updates laser position and handles collision
# return list of updated lasers
def laser_update(las, lasers, speed, targets, scoreincrement):
    global playerscore
    global playershield
    newlasers =[]
    for lasrect in lasers:
        laserhit=False
        lasrect = lasrect.move(speed)
        if lasrect.top <= 0 or lasrect.bottom >= height:
            if lasrect in lasers:
                lasers.remove(lasrect)
        else:
            for targetrect in targets:
                if pygame.Rect.colliderect(lasrect, targetrect):
                    if targetrect in targets:
                        targets.remove(targetrect)
                        laserhit = True
                    pygame.mixer.Sound.play(explosion)
                    if pygame.Rect.colliderect(lasrect, enemyrect):
                        if lasrect in lasers:
                            lasers.remove(lasrect)
                        if enemylaserrect in enemylasers:
                            enemylasers.remove(enemylaserrect)
                    playerscore += scoreincrement
                    if targetrect == spaceshiprect and laserhit == True:
                        playershield -= 1
                        pygame.mixer.Sound.stop(explosion)
                        pygame.mixer.Sound.stop(laserblast)
                        pygame.mixer.Sound.play(playerhitsound)
                        

            if laserhit==False:
                newlasers.append(lasrect)
                screen.blit(las, lasrect)
                
    return newlasers



#main loop
while GamePlay == True:
    
    mouse = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
        #If mouse is pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            if width/2-40 <= mouse[0] <= width/2+55 and height/2+65 <= mouse[1] <= height/2+110:
                pygame.quit()
                sys.exit()
                
        #Event ENEMYMOVE, look above for more code    
        if event.type == ENEMYMOVE:
            newenemies = []
            for enemyrect in enemies:
                if enemyrect.bottom<=height:
                    enemyrect = enemyrect.move([0, 1])
                    newenemies.append(enemyrect)
            enemies = newenemies
        
        #Event ENEMYSPAWN, look above for more code
        if event.type == ENEMYSPAWN:
            enemyrect = enemy.get_rect(topleft=(random.randint(10,width-110), 0))
            enemies.append(enemyrect)
            
        #Event ENEMYATTACK, look above for more code    
        if event.type == ENEMYATTACK:
            for enemyrect in enemies:
                enemylaserrect = enemylaser.get_rect(midtop = enemyrect.midtop)
                enemylasers.append(enemylaserrect)
            if playerscore >= 150:
                biglasrect = biglas.get_rect(midtop = stationrect.midbottom)
        
        #Event STATIONMOVE, look above for more code
        if event.type == STATIONMOVE:
            newStation = []
            if stationrect.bottom<=height:
                stationrect = stationrect.move(stationspeed)
                newStation.append(stationrect)
            Station = newStation
            
    #key controls --- 
    #forward (w)
    #backward (s)
    #left (a)
    #right (d)
    #shoot laser (space)
    #quit game (esc)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and spaceshiprect.left>0:
        spaceshiprect.x -= movement
    if keys[pygame.K_d] and spaceshiprect.right<width:
        spaceshiprect.x += movement
    if keys[pygame.K_w] and spaceshiprect.top>0:
        spaceshiprect.y -= movement
    if keys[pygame.K_s] and spaceshiprect.bottom<height:
        spaceshiprect.y += movement
    if time.time()>starttime+timerdelay:
        if keys[pygame.K_SPACE]:
            lasrect = las.get_rect(midtop = spaceshiprect.midtop)
            lasers.append(lasrect)
            starttime=time.time()
            pygame.mixer.Sound.play(laserblast)
    if keys[pygame.K_ESCAPE]:
        pygame.display.quit()
        sys.exit()
    
    #redraw screen
    screen.fill(black)
    
    #update and display lasers
    lasers = laser_update(las, lasers, speed, enemies, 1)
    enemylasers = laser_update(enemylaser, enemylasers, enemyspeed, [spaceshiprect], -5)
    
    #display big laser
    newbiglasers = []
    biglasrect.move([0,1])
    newbiglasers.append(biglasrect)
    biglasers = newbiglasers
    if pygame.Rect.colliderect(biglasrect, spaceshiprect):
        playershield -= damage
    screen.blit(biglas, biglasrect)
    
    #display spaceship
    screen.blit(spaceship, spaceshiprect)
    
    #area of rectangle for laser
    pygame.draw.rect(screen, purple, biglasrect, width = 1)
    
    #display enemies
    for enemyrect in enemies:
        screen.blit(enemy, enemyrect)
        
    
    
        
    
    #display scores
    scoretext = font.render("Score: "+str(playerscore), True, white)
    screen.blit(scoretext,(50, 50))
    
    #display shield amount
    shieldtext = font.render("Shield remaining: "+str(playershield), True, white)
    screen.blit(shieldtext, (width-250, 50))
    
    #display game over and restart if the aliens break shield and hit player
    if playershield < 0:
        movement = 0
        if playershield < -1000:
            pygame.display.quit()
            sys.exit()
        gameover = font2.render("GAME OVER", True, red)
        deathmessage = font3.render("The aliens broke through your shield", True, yellow)
        quit = font3.render("Quit", True, green)
        gameoverrect = gameover.get_rect(center = (width/2, height/2))
        deathmessagerect = deathmessage.get_rect(center=(width/2, height/2+45))
        quitrect = quit.get_rect(center = (width/2, height/2+90))
        screen.blit(gameover, gameoverrect)
        screen.blit(deathmessage, deathmessagerect)
        
        #Change color of button when mouse is hovering
        if width/2-40 <= mouse[0] <= width/2+55 and height/2+65 <= mouse[1] <= height/2+110:
            pygame.draw.rect(screen,gray,[width/2-40,height/2+70,90,40])
        
        else:
            pygame.draw.rect(screen,dark_gray,[width/2-40,height/2+70,90,40])
            
        #restart text
        screen.blit(quit, quitrect)
        
    #display Game Over and restart if the station passed through you    
    if stationrect.bottom >= height:
        movement = 0
        gameover = font2.render("GAME OVER", True, red)
        deathmessage = font3.render("You let the station pass through", True, yellow)
        quit = font3.render("Quit", True, green)
        gameoverect = gameover.get_rect(center = (width/2, height/2))
        deathmessagerect = deathmessage.get_rect(center=(width/2, height/2+45))
        quitrect = quit.get_rect(center = (width/2, height/2+90))
        screen.blit(gameover, gameoverrect)
        screen.blit(deathmessage, deathmessagerect)
        
        #Change color of button when mouse is hovering
        if width/2-40 <= mouse[0] <= width/2+55 and height/2+65 <= mouse[1] <= height/2+110:
            pygame.draw.rect(screen,gray,[width/2-40,height/2+70,90,40])
        
        else:
            pygame.draw.rect(screen,dark_gray,[width/2-40,height/2+70,90,40])
            
        #restart text
        screen.blit(quit, quitrect)
        
    #stop enemy spawning 
    #set station speed   
    if playerscore >= 150:
        pygame.time.set_timer(ENEMYSPAWN, 0)
        stationspeed = [0,1]
        for enemyrect in enemies:
            if enemyrect in enemies:
                enemies.remove(enemyrect)
        
        #display space station
        Station = [stationrect]
        screen.blit(station, stationrect)
        
        #health bar for space station
        pygame.draw.rect(screen, light_red, [stationrect.x+273, stationrect.y+132, stationhealth, 20])
        for lasrect in lasers:
            if pygame.Rect.colliderect(lasrect, stationrect):
                stationhealth -= 1
                pygame.draw.rect(screen, light_red, [stationrect.x+270, stationrect.y+132, stationhealth, 20])
                lasers.remove(lasrect)
        
        #Win if station health is gone
        if stationhealth <= 0:
            stationspeed = [0,0]
            damage = 0
            winner = font2.render("You Won!", True, yellow)
            quit = font3.render("Quit", True, green)
            winnerrect = winner.get_rect(center = (width/2, height/2))
            quitrect = quit.get_rect(center = (width/2, height/2+90))

            if width/2-40 <= mouse[0] <= width/2+55 and height/2+65 <= mouse[1] <= height/2+110:
                pygame.draw.rect(screen,gray,[width/2-40,height/2+70,90,40])
        
            else:
                pygame.draw.rect(screen,dark_gray,[width/2-40,height/2+70,90,40])

            #restart text
            screen.blit(quit, quitrect)
            screen.blit(winner, winnerrect)

    
    pygame.display.flip()
