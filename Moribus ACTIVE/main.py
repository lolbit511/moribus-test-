import contextlib
with contextlib.redirect_stdout(None):
    import pygame # THIS IS THE ACTUAL FILE ON GITHUB (17/12/2021)


from pygame.locals import *
from tkinter import *
import datetime

import parameters as p
import Player as pl
import HealthBar as hb
import EventHandler as e
import MusicManager as mm
import runtime_parameters as r
import Fireball as fb
import Enemy as e1
import Enemy2 as e2
import Boss1 as b1
import swing as s
import StageDisplay as sd

pl.player.image = pygame.image.load("images/empty.png")

while True:
    #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" + str(p.WIDTH))

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!" + str(p.ACC))


    p.WIDTH, p.HEIGHT = pygame.display.get_surface().get_size()
    p.HEIGHT = int(p.WIDTH/2)
    #p.WIDTH = p.WIDTH*2

    if p.WIDTH < 500:
        p.displaysurface = pygame.display.set_mode((500, 250), pygame.RESIZABLE)
    elif p.WIDTH > 1390:
        p.displaysurface = pygame.display.set_mode((1390, 695), pygame.RESIZABLE)
    else:
        p.displaysurface = pygame.display.set_mode((p.WIDTH, p.HEIGHT), pygame.RESIZABLE)


    #print(player.experience)



    a = datetime.datetime.now()
    #print(Enemies)
    e.gravity_check(pl.player)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        # Will run when the close window button is clicked ("X" at corner of the screen)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

            # For events that occur upon clicking the mouse (left click)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if int(p.WIDTH-int(p.WIDTH*0.05)) <= mouse[0] <= int(p.WIDTH) and int(p.HEIGHT-int(p.HEIGHT*0.1)) <= mouse[1] <= p.HEIGHT:
                r.cursor.pause()
                mm.mmanager.playsound(p.bsound, 0.2)
            elif int(p.WIDTH-int(p.WIDTH*0.1)) <= mouse[0] <= int(p.WIDTH) and int(p.HEIGHT-int(p.HEIGHT*0.1)) <= mouse[1] <= p.HEIGHT:
                r.handler.home()
                mm.mmanager.playsound(p.bsound, 0.2)
            elif int(p.WIDTH-int(p.WIDTH*0.15)) <= mouse[0] <= int(p.WIDTH) and int(p.HEIGHT-int(p.HEIGHT*0.1)) <= mouse[1] <= p.HEIGHT:
                r.handler.saveG()
                mm.mmanager.playsound(p.bsound, 0.2)
            elif int(p.WIDTH-int(p.WIDTH*0.2)) <= mouse[0] <= int(p.WIDTH) and int(p.HEIGHT-int(p.HEIGHT*0.1)) <= mouse[1] <= p.HEIGHT:
                r.handler.loadG()
                mm.mmanager.playsound(p.bsound, 0.2)


            elif 0 <= mouse[0] <= p.WIDTH and 0 <= mouse[1] <= p.HEIGHT and event.button == 1: # attacking
                #player.attack()
                #player.attacking = True
                #print("attack")
                #print("swung")
                if pl.player.attacking == False:
                    pl.player.attacking = True
                    SW = s.swing()
                    r.Swings.add(SW)
            elif 0 <= mouse[0] <= p.WIDTH and 0 <= mouse[1] <= p.HEIGHT and pl.player.magic_cooldown == 1 and event.button == 3:
                print("fired")
                if pl.player.mana >= 6:
                    pl.player.mana -= 6
                    # player.attacking = True
                    fireball = fb.FireBall()
                    r.Fireballs.add(fireball)
                    mm.mmanager.playsound(p.fsound, 0.3) # sound

        if event.type == r.handler.enemy_generation:
            #print(handler.stage)
            while r.handler.enemy_count < r.handler.stage_enemies[r.handler.stage - 1]:
                #print("a:", handler.enemy_count)
                #print("b:", handler.stage_enemies[player.stage - 1])
                enemy = e1.Enemy()
                r.Enemies.add(enemy)
                r.handler.enemy_count += 1
                r.handler.next_level_started = False

        if event.type == r.handler.enemy_generation2:
            if r.handler.enemy_count < r.handler.stage_enemies[r.handler.stage - 1]:
                enemy = e2.Enemy2()
                r.Enemies.add(enemy)
                enemy = b1.Boss1()
                r.Enemies.add(enemy)
                r.handler.enemy_count += 1
                r.handler.next_level_started = False

        if event.type == r.handler.enemy_generation3:
            if r.handler.enemy_count < r.handler.stage_enemies[r.handler.stage - 1]:
                enemy = e2.Enemy2()
                r.Enemies.add(enemy)
                enemy = b1.Boss1()
                r.Enemies.add(enemy)
                #enemy = Boss1()
                # Enemies.add(enemy)
                r.handler.enemy_count += 1
                r.handler.next_level_started = False


                # Event handling for a range of different key presses
        # Event handling for a range of different key presses

        # if event.type == pygame.KEYDOWN and r.cursor.wait == 0 and event.key == pygame.K_y:  ################################################################################################################################################################################################################################################
        #     pl.player.sheildUp = True
        #     print("shieldUp TRUE")
        # else:
        #     pl.player.sheildUp = False
        #     print("shieldUp FALSE")

        if event.type == pygame.KEYDOWN and r.cursor.wait == 0: #int(WIDTH * 0.4), int(HEIGHT * 0.53)
            if int(p.WIDTH * 0.4) < pl.player.rect.x < int(p.WIDTH * 0.6) and event.key == pygame.K_e and r.handler.world == 0:
                r.handler.stage_handler()
                #print("castle range")
            if event.key == pygame.K_n:
                if r.Enemies != None  and not (r.handler.next_level_started):
                    if r.handler.battle == True and len(r.Enemies) == 0:
                        r.handler.next_level_started = True
                        r.handler.next_stage()
                        print("test")
                        stage_display = sd.StageDisplay()
                        stage_display.display = True


                    # Event handling for a range of different key presses
            if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                pl.player.jump()
            if event.key == pygame.K_SPACE and pl.player.startdone == False:
                pl.player.start = True



            if event.key == pygame.K_LEFT:
                pl.player.move()
            if event.key == pygame.K_RIGHT:
                pl.player.move()
        if event.type == p.hit_cooldown:
            pl.player.cooldown = False
            pygame.time.set_timer(p.hit_cooldown, 0)
            #####################print("CD complete")


    # attackCD = attackCD - 1
    # if attackCD <1:
    #     attackCD = 1
    #
    # if attackCD > 2:
    #     player.attacking = True


    # Rendering Sprites
    r.background.render() ######################################
    r.ground.render()
    r.Map.update()
    r.Pause.render(1)
    r.Home.render(2)
    r.savebutton.render(3)
    r.loadbutton.render(4)
    r.cursor.hover()

    if hb.healthCount > 0:
        pl.player.rect.x = 0
        #displaysurface.blit(player.image, player.rect)
        pl.player.image = pygame.transform.scale(pl.player.image, (pl.player.xRatio, pl.player.yRatio))
        p.displaysurface.blit(pl.player.image, pl.player.rect)

    hb.health.render(hb.healthCount)  # updates healthbar image


    if r.cursor.wait == 0:
        if r.Enemies != None:
            for entity in r.Enemies:
                #print(entity.boltCD)
                entity.update()
                entity.move()
                entity.render()

                if entity.boltCD > 0 and entity.fired == True:
                    entity.boltCD -= 1
                else:
                    entity.boltCD = 150
                    entity.fired = False



    #################


    # Player related functions

        if pl.player.attacking == True:
            pl.player.attack()
            #print("attacked")

        for i in r.Items:
            i.render()
            i.update()

        for SW in r.Swings:
            SW.attack()
        for ball in r.Fireballs:
            ball.fire()
        for bolt in r.Bolts:
            bolt.fire()


        if pl.player.startdone == False:
            if pl.player.start == True :
                pl.player.image = pygame.transform.scale(pl.player.image, (pl.player.xRatio, pl.player.yRatio)) ############################################################################################
                pl.player.start = False
                r.menu_display.display = False
                pl.player.startdone = True
        else:
            pl.player.update()
            pl.player.move()


    #print("player rect:",player.rect)


    # Render stage display
    if r.stage_display.display == True:
        r.stage_display.move_display()
    if r.stage_display.clear == True:
        r.stage_display.stage_clear()

    # Render Starting screen
    if r.menu_display.display == True:
        r.menu_display.move_display()
    if r.menu_display.clear == True:
        r.menu_display.stage_clear()

    #print(stage_display.clear)
    # Status bar update and render

    r.GO.GO_display()

    p.displaysurface.blit(r.status_bar.surf, (p.WIDTH-r.status_bar.statusWidth, 0))
    r.status_bar.update_draw()
    r.handler.update()




    hb.health.image = pygame.transform.scale(hb.health.image, (int(p.WIDTH*0.35), int(p.HEIGHT*0.2))) #####################################################################################################################################################################
    r.background.bgimage = pygame.transform.scale(r.background.bgimage, (p.WIDTH, p.HEIGHT))



    pygame.display.update()
    p.FPS_CLOCK.tick(p.FPS)


    b = datetime.datetime.now()
    #print(GO.GameEnded)

    #print(player.jump_timer)