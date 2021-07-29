import numpy
import pygame # THIS IS THE ACTUAL FILE ON GITHUB (23/6/2021)
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *
import datetime


import time #######################################################################################new


# freq, size, channel, buffsize
pygame.mixer.pre_init(44100, 16, 1, 512)
pygame.init()

#main variables
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.9
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
hit_cooldown = pygame.USEREVENT + 1
# defining font styles
headingfont = pygame.font.SysFont("Verdana", 40)
regularfont = pygame.font.SysFont('Corbel',25)
smallerfont = pygame.font.SysFont('Corbel',16)
# light shade of the button
color_light = (170,170,170)
color_dark = (100,100,100)
color_white = (255,255,255)




displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moribus")

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = pygame.image.load("images/background.png")
        self.bgimage = pygame.transform.scale(self.bgimage, (WIDTH, HEIGHT))
        self.bgY = 0
        self.bgX = 0

    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Ground.png")
        self.image = pygame.transform.scale(self.image, (WIDTH,50))
        self.rect = self.image.get_rect(center=(350, 330))



    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))


class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/heart5.png")
        self.image = pygame.transform.scale(self.image, (300, 130))

    def render(self):
        displaysurface.blit(self.image, (10, 10))

# Moved health bar animations out so all other classes have easy access
health_ani = [pygame.image.load("images/heart0.png"), pygame.image.load("images/heart1.png"),
                      pygame.image.load("images/heart2.png"), pygame.image.load("images/heart3.png"),
                      pygame.image.load("images/heart4.png"), pygame.image.load("images/heart5.png")]

class Player(pygame.sprite.Sprite):
    def __init__(self):

        super().__init__()
        self.start = False
        self.startdone = False

        self.image = pygame.image.load("images/player.png")
        #self.imageorg = self.image
        #cropped = pygame.Surface((80, 80))
        #cropped.blit(self.image, (-80, -80))
        #self.subsurface = pygame.Surface.subsurface(20, 2, 80, 98)
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()

        # Position and direction
        self.vx = 0
        self.pos = vec((340, 240))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.direction = "RIGHT"
        self.jumping = False
        # Movement
        self.jumping = False
        self.running = False
        self.move_frame = 0
        self.jumpheight = -13
        self.jump_timer = 250
        # Combat
        self.attacking = False
        self.attack_frame = 0
        self.attCD = 150

        self.experience = 0
        self.mana = 0
        self.coin = 0
        self.magic_cooldown = 1

        # Stage
        self.stage = 1
        # Health
        self.health = 5
        self.cooldown = False

        # ## Attacking Animations
        # self.att_ani_L = [pygame.image.load("player.png"), pygame.image.load("player.png"),
        #              pygame.transform.flip(pygame.image.load("sword_right.png"), True, False),
        #              pygame.transform.flip(pygame.image.load("sword_right.png"), True, False),
        #              pygame.transform.flip(pygame.image.load("sword_right.png"), True, False),
        #              pygame.transform.flip(pygame.image.load("sword_right.png"), True, False),
        #              pygame.image.load("player.png")]
        #
        # self.att_ani_R = [pygame.transform.flip(pygame.image.load("player.png"), True, False),
        #              pygame.transform.flip(pygame.image.load("player.png"), True, False),
        #              pygame.image.load("sword_right.png"), pygame.image.load("sword_right.png"),
        #              pygame.image.load("sword_right.png"), pygame.image.load("sword_right.png"),
        #              pygame.transform.flip(pygame.image.load("player.png"), True, False)]

        # Run animation for the RIGHT
        self.run_ani_R = [pygame.transform.flip(pygame.image.load("images/player.png"),True,False), pygame.transform.flip(pygame.image.load("images/player.png"),True,False),
                     pygame.transform.flip(pygame.image.load("images/player.png"),True,False), pygame.transform.flip(pygame.image.load("images/player.png"),True,False),
                     pygame.transform.flip(pygame.image.load("images/playerWalk1.png"),True,False),pygame.transform.flip(pygame.image.load("images/playerWalk1.png"),True,False),
                     pygame.transform.flip(pygame.image.load("images/playerWalk1.png"),True,False), pygame.transform.flip(pygame.image.load("images/playerWalk1.png"),True,False)]

        self.run_ani_L = [pygame.image.load("images/player.png"), pygame.image.load("images/player.png"),
                     pygame.image.load("images/player.png"), pygame.image.load("images/player.png"),
                     pygame.image.load("images/playerWalk1.png"), pygame.image.load("images/playerWalk1.png"),
                     pygame.image.load("images/playerWalk1.png"), pygame.image.load("images/playerWalk1.png")]

        self.att_ani_R = [pygame.transform.flip(pygame.image.load("images/player.png"), True, False)]
        self.att_ani_R = self.att_ani_R + [pygame.transform.flip(pygame.image.load("images/sword.png"), True, False)] * self.attCD

        self.att_ani_R.append(pygame.image.load("images/player.png"))


        #print(self.att_ani_R)
        self.att_ani_L = [pygame.image.load("images/player.png")]
        self.att_ani_L = self.att_ani_L + [pygame.image.load("images/sword.png")] * self.attCD
        self.att_ani_L.append(pygame.transform.flip(pygame.image.load("images/player.png"), True, False))

        #print(self.att_ani_L)


    def player_hit(self): #player
        if GO.GameEnded == False:

            #print("entering player hit")
            if self.cooldown == False:

                self.cooldown = True  # Enable the cooldown
                pygame.time.set_timer(hit_cooldown, 1000)  # Resets cooldown in 1 second

                self.health = self.health - 1
                health.image = health_ani[self.health]

                if self.health <= 0:
                    self.kill()
                    pygame.display.update()

    def move(self): #player
        if cursor.wait == 1: return
        self.acc = vec(0, 0.5)
        # Will set running to False if the player has slowed down to a certain extent
        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        # Returns the current key presses
        pressed_keys = pygame.key.get_pressed()

        # Accelerates the player in the direction of the key press
        if player.attacking == False:
            pass
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
                self.acc.x = -ACC


        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
                self.acc.x = ACC



        # Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        for SW in Swings:
            SW.rect.x += self.vel.x + 0.5 * self.acc.x
        self.pos += self.vel + 0.5 * self.acc  # Updates Position with new values

        # This causes character warping from one point of the screen to the other
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos  # Update rect with new pos


    def attack(self):
        if cursor.wait == 1: return
        # If attack frame has reached end of sequence, return to base frame
        if self.attack_frame > self.attCD-1:
            self.attack_frame = 0
            self.attacking = False

        # Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = self.att_ani_R[self.attack_frame]
        elif self.direction == "LEFT":
            self.image = self.att_ani_L[self.attack_frame]

        # Update the current attack frame
        self.attack_frame += 1
        # Updates position with new values
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x

        self.rect.center = self.pos  # Updates rect



    def update(self): #player
        if self.jumpheight == -18:
            self.jump_timer -= 1
        if self.jump_timer < 0:
            self.jumpheight = -13
            self.jump_timer = 250

        if cursor.wait == 1: return
        # Move the character to the next frame if conditions are met
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = self.run_ani_R[self.move_frame]
                self.direction = "RIGHT"

            elif self.vel.x < 0:
                self.image = self.run_ani_L[self.move_frame]
                self.direction = "LEFT"

            self.move_frame += 1
            if self.move_frame == 8:  # return to starting animation at loop 8
                self.move_frame = 0


            # Returns to base frame if standing still and incorrect frame is showing
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = self.run_ani_R[self.move_frame]
            elif self.direction == "LEFT":
                self.image = self.run_ani_L[self.move_frame]

                # Checks for collision with the Player
        if Enemies != None:
            hits = pygame.sprite.spritecollide(self, Enemies, False)

                    # Activates upon either of the two expressions being true
            #if hits and player.attacking == True:
             #   self.kill()
                # print("Enemy killed")

            # If collision has occured and player not attacking, call "hit" function
            if hits and player.attacking == False:
                self.player_hit()



    def jump(self):
        self.rect.x += 1


        # Check to see if payer is in contact with the ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)

        self.rect.x -= 1

        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = self.jumpheight


class Item(pygame.sprite.Sprite):
    def __init__(self, itemtype):
        super().__init__()
        if itemtype == 1:
            self.image = pygame.image.load("images/heart.png")
        elif itemtype == 2:
            self.image = pygame.image.load("images/coin.png")
            self.image = pygame.transform.scale(self.image, (30, 30))
        elif itemtype == 3:
            self.image = pygame.image.load("images/jump_potion.gif")
            self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.type = itemtype
        self.posx = 0
        self.posy = 0

    def render(self):
        self.rect.x = self.posx
        self.rect.y = self.posy
        displaysurface.blit(self.image, self.rect)

    def update(self): #item
        hits = pygame.sprite.spritecollide(self, Playergroup, False)
        # Code to be activated if item comes in contact with player
        if hits:
            if player.health < 5 and self.type == 1:
                player.health += 1
                health.image = health_ani[player.health]
                self.kill()
            if self.type == 2:
                # handler.money += 1
                player.coin += 1
                self.kill()
            if self.type == 3:
                print("jump boosted")
                player.jumpheight = -18
                self.kill()


class PButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.vec = vec(620, 300)
        self.imgdisp = 0

    def render(self, num):
        if (num == 2):
            self.image = pygame.image.load("images/home.png")
            self.vec = vec(560, 300)
        elif (num == 1):
            if cursor.wait == 0:
                self.image = pygame.image.load("images/pause.png")
            else:
                self.image = pygame.image.load("images/play.png")
        elif (num == 3):
            self.image = pygame.image.load("images/save.png")
            self.vec = vec(500, 300)
        elif (num == 4):
            self.image = pygame.image.load("images/load.png")
            self.vec = vec(440, 300)

        displaysurface.blit(self.image, self.vec)


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/cursor.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.wait = 0

    def pause(self):
        if self.wait == 1:
            self.wait = 0
        else:
            self.wait = 1

    def hover(self):
        if 620 <= mouse[0] <= 670 and 300 <= mouse[1] <= 345:
            pygame.mouse.set_visible(False)
            cursor.rect.center = pygame.mouse.get_pos()  # update position
            displaysurface.blit(cursor.image, cursor.rect)
        else:
            pygame.mouse.set_visible(True)




class Map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hide = False
        self.image = pygame.image.load("images/Map.png")

    def update(self):
        if self.hide == False and handler.world == 0:
            displaysurface.blit(self.image, (400, 100))


class MenuDisplay:
    def __init__(self):
        super().__init__()
        self.headingFont = pygame.font.SysFont('Verdana', 30)
        self.text = self.headingFont.render("PRESS SPACE TO START", True, (255, 255, 255))
        self.rect = self.text.get_rect()
        self.posx = 175
        self.posy = 100
        self.display = True
        self.clear = False
    def move_display(self):
        # Create the text to be displayed
        #self.text = self.headingFont.render(self.text, True, (157, 3, 252))
        if self.posx < 700:
            self.posx += 0
            displaysurface.blit(self.text, (self.posx, self.posy))
        else:
            self.display = False
            self.kill()



class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.headingFont = pygame.font.SysFont('Verdana', 60)
        self.text = self.headingFont.render(("Game Over"), True, (157, 3, 252))
        self.rect = self.text.get_rect()
        self.posx = 175
        self.posy = 100
        self.display = False
        self.GameEnded = False
        self.clear = False

    def GO_display(self):
        if player.health == 0:
            displaysurface.blit(self.text, (self.posx, self.posy))
            self.GameEnded = True


class StageDisplay(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.headingFont = pygame.font.SysFont('Verdana', 60)
        self.text = self.headingFont.render("STAGE: " + str(handler.stage), True, (157, 3, 252))
        self.rect = self.text.get_rect()
        self.posx = -100
        self.posy = 100
        self.display = False
        self.clear = False

    def stage_clear(self):
        self.text = headingfont.render("STAGE CLEAR!", True, color_dark)
        button.imgdisp = 0
        if self.posx < 720:
            self.posx += 10
            displaysurface.blit(self.text, (self.posx, self.posy))
        else:
            self.display = False
            self.posx = -100
            self.posy = 100

    def move_display(self):
        # Create the text to be displayed
        self.text = self.headingFont.render("STAGE: " + str(handler.stage), True, (157, 3, 252))
        if self.posx < 700:
            self.posx += 5
            displaysurface.blit(self.text, (self.posx, self.posy))
        else:
            self.display = False
            self.kill()


class StatusBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((90, 78))
        self.rect = self.surf.get_rect(center=(500, 10))

    def update_draw(self):
        # Create the text to be displayed
        text1 = smallerfont.render("STAGE: " + str(handler.stage), True, color_white)
        text2 = smallerfont.render("EXP: " + str(player.experience), True, color_white)
        text3 = smallerfont.render("MANA: " + str(player.mana), True, color_white)
        text4 = smallerfont.render("PURSE: " + str(player.coin), True, color_white)
        text5 = smallerfont.render("FPS: " + str(int(FPS_CLOCK.get_fps())), True, color_white)

        # Draw the text to the status bar
        displaysurface.blit(text1, (585, 7))
        displaysurface.blit(text2, (585, 22))
        displaysurface.blit(text3, (585, 37))
        displaysurface.blit(text4, (585, 52))
        displaysurface.blit(text5, (585, 67))

class EventHandler():
    def __init__(self):
        self.world = 0
        self.next_level_started = False
        self.stage = 1
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 1
        self.enemy_generation2 = pygame.USEREVENT + 3
        self.stage_enemies = []
        #self.stage_enemies.append(0)

        self.phase = 21
        for x in range(1, self.phase):
            self.stage_enemies.append(x) #formula for enemy generation
        print(self.stage_enemies)

    def next_stage(self):  # Code for when the next stage is clicked

        self.stage += 1
        self.enemy_count = 0
        self.dead_enemy_count = 0
        #print("Stage: " + str(self.stage))
        if self.world == 1:
            pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage))
        elif self.world == 2:
            pygame.time.set_timer(self.enemy_generation2, 1500 - (50 * self.stage))

    def update(self): #Event Handler
        #print("a:" , self.dead_enemy_count)
        #print("b:" , self.stage_enemies[self.stage - 1])
        if self.dead_enemy_count == self.stage_enemies[self.stage]:
            self.dead_enemy_count = 0
            stage_display.clear = True
            stage_display.stage_clear()
            print("stageClear ACTIVE")

    def home(self):
        # Reset Battle code
        pygame.time.set_timer(self.enemy_generation, 0)
        pygame.time.set_timer(self.enemy_generation2, 0)

        self.battle = False
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.stage = 1
        self.world = 0

        # Destroy any enemies or items lying around
        for group in Enemies, Items:
            for entity in group:
                entity.kill()

        # Bring back normal backgrounds
        Map.hide = False
        background.bgimage = pygame.image.load("images/Background.png")
        background.bgimage = pygame.transform.scale(background.bgimage, (WIDTH, HEIGHT))
        ground.image = pygame.image.load("images/Ground.png")
        ground.image = pygame.transform.scale(ground.image, (WIDTH,50))

    def saveG(self):
        f = open("guru99.txt", "w")
        # f=open("guru99.txt","a+")
        #for i in range(10):

        # everything that needs to be saved
        f.write(str(handler.stage) + "\n")
        f.write(str(player.experience) + "\n")
        f.write(str(player.mana) + "\n")
        f.write(str(player.coin) + "\n")
        f.write(str(player.health) +"\n")

        f.close()


    def loadG(self):
        #Open the file back and read the contents
        f=open("guru99.txt", "r")
        if f.mode == 'r':
            handler.stage = int(f.readline())
            player.experience = int(f.readline())
            player.mana = int(f.readline())
            player.coin = int(f.readline())
            player.health = int(f.readline())

        #or, readlines reads the individual line into a list
        #fl = f.readlines()
        #for x in fl:

            #print(x)


    def stage_handler(self):
        # Code for the Tkinter stage selection window
        self.root = Tk()
        self.root.geometry('295x270')
        width = 30
        button1 = Button(self.root, text="[Dungeon] Twilight Plains", width=width, height=2,
                         command=self.world1)
        button2 = Button(self.root, text="[Dungeon] Sabreclaw Wastelands", width=width, height=2,
                         command=self.world2)
        button3 = Button(self.root, text="[Town] Tarnstead Outlook", width=width, height=2,
                         command=self.world3)
        button4 = Button(self.root, text="[Dungeon] Iceborne Crypts", width=width, height=2,
                         command=self.world4)
        button5 = Button(self.root, text="[Dungeon] Mount Moru", width=width, height=2,
                         command=self.world5)

        button1.place(x=40, y=15)
        button2.place(x=40, y=65)
        button3.place(x=40, y=115)
        button4.place(x=40, y=165)
        button5.place(x=40, y=215)

        self.root.mainloop()

    def world1(self):
        self.root.destroy()
        self.world = 1
        pygame.time.set_timer(self.enemy_generation, 2000)

        Map.hide = True
        self.battle = True
        #mmanager.playsoundtrack(soundtrack[0], -1, 0.05)

    def world2(self):
        self.root.destroy()
        background.bgimage = pygame.image.load("images/wasteland.png")
        ground.image = pygame.image.load("images/Ground.png")

        pygame.time.set_timer(self.enemy_generation2, 2500)

        self.world = 2

        Map.hide = True
        self.battle = True
        #mmanager.playsoundtrack(soundtrack[1], -1, 0.05)

    def world3(self):

        self.world = 3
        self.battle = True
        # Empty for now

    def world4(self):

        self.battle = True
        # Empty for now

    def world5(self):

        self.battle = True
        # Empty for now



class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Enemy.png")

        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.image = pygame.transform.scale(self.image, (80, 100))
        self.rect = self.image.get_rect()

        # Combat
        self.direction = random.randint(0, 1)  # 0 for Right, 1 for Left
        self.vel.x = random.randint(2, 6) / 2  # Randomised velocity of the generated enemy
        self.mana = random.randint(1, 3)  # Randomised mana amount obtained upon kill

        #self.attacking = False
        self.cooldown = False
        #self.attack_frame = 0

        # dummy variables (prevents crash)
        self.boltCD = 150
        self.fired = False


        # Sets the intial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 350-120 # 100 is height of enemy image
        if self.direction == 1:
            self.pos.x = 700-100
            self.pos.y = 350-120

    def move(self): # enemy
        if cursor.wait == 1: return

        # Causes the enemy to change directions upon reaching the end of screen
        if self.pos.x >= (WIDTH - 20):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0
        # Updates position with new values
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x

        self.rect.center = self.pos  # Updates rect

    def player_hit(self): #enemy
        if GO.GameEnded != True:
        # print("entering player hit")
            if self.cooldown == False:
                ####################################print("entered hit condition")
                self.cooldown = True  # Enable the cooldown
                pygame.time.set_timer(hit_cooldown, 1000)  # Resets cooldown in 1 second

                ####################################print("hit")
                pygame.display.update()

    def update(self): #enemy
        if cursor.wait == 1: return
        rand_num = numpy.random.uniform(0, 50)
        # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, Playergroup, False)
        s_hits = pygame.sprite.spritecollide(self, Swings, False)

        # Checks for collision with Fireballs
        f_hits = pygame.sprite.spritecollide(self, Fireballs, False)


        # Activates upon either of the two expressions being true
        if player.attacking == True and f_hits or s_hits:
            if player.mana < 100: player.mana += self.mana  # Release mana
            player.experience += 1  # Release expeiriance
            self.kill()
            handler.dead_enemy_count += 1
            #print(handler.dead_enemy_count)

            item_no = 0
            if rand_num >= 0 and rand_num <= 5:  # 1 / 20 chance for an item (health) drop
                item_no = 1
            elif rand_num > 5 and rand_num <= 15:
                item_no = 2
            elif rand_num > 15 and rand_num < 50:
                item_no = 3

            if item_no != 0:
                # Add Item to Items group
                item = Item(item_no)
                Items.add(item)
                # Sets the item location to the location of the killed enemy
                item.posx = self.pos.x
                item.posy = self.pos.y

        #If collision has occured and player not attacking, call "hit" function
        elif hits and player.attacking == False:
            self.player_hit()
            #print("player died")
            #print(self.rect)

    def render(self):
        # Displayed the enemy on screen
        displaysurface.blit(self.image, (self.pos.x, self.pos.y))


class Bolt(pygame.sprite.Sprite):
    def __init__(self, x, y, d):
        super().__init__()
        self.image = pygame.image.load("images/sabreclaw.png")
        self.rect = self.image.get_rect()
        self.rect.x = x + 15
        self.rect.y = y + 20
        self.direction = d

    def fire(self):
        # Runs while the fireball is still within the screen w/ extra margind
        if -10 < self.rect.x < 710:
            if self.direction == 0:
                self.image = pygame.image.load("images/sabreclaw.png")
                displaysurface.blit(self.image, self.rect)
            else:
                self.image = pygame.transform.flip(pygame.image.load("images/sabreclaw.png"), True, False)
                displaysurface.blit(self.image, self.rect)

            if self.direction == 0:
                self.rect.move_ip(12, 0)
            else:
                self.rect.move_ip(-12, 0)
        else:
            self.kill()

        # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, Playergroup, False)
        if hits:
            player.player_hit()
            self.kill()


class Enemy2(pygame.sprite.Sprite): #second enemy, enemy 2
    def __init__(self):
        super().__init__()
        self.pos = vec(0, 0)
        self.vel = vec(0, 0)
        self.wait = 0
        self.wait_status = False
        self.turning = 0
        self.boltCD = 150
        self.fired = False

        self.direction = random.randint(0, 1)  # 0 for Right, 1 for Left
        self.vel.x = random.randint(2, 6) / 3  # Randomized velocity of the generated enemyd
        self.mana = random.randint(2, 3)  # Randomized mana amount obtained upon


        if self.direction == 0:
            self.image = pygame.image.load("images/enemy2.png")
        elif self.direction == 1:
            self.image = pygame.image.load("images/enemy2_L.png")

        self.image = pygame.transform.scale(self.image, (105, 105))
        self.rect = self.image.get_rect()

        # Sets the initial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 250
        if self.direction == 1:
            self.pos.x = 700
            self.pos.y = 250

    def move(self):
        if cursor.wait == 1: return

        # Causes the enemy to change directions upon reaching the end of screen
        if self.pos.x >= (WIDTH - 50):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0
        # Updates position with new values
        if self.wait > 50:
            self.wait_status = True
        elif int(self.wait) <= 0:
            self.wait_status = False

        if self.wait_status == True:
            rand_num = numpy.random.uniform(0, 50)
            if int(rand_num) == 25 and self.boltCD > 0 and self.fired == False:
                self.fired = True
                bolt = Bolt(self.pos.x, self.pos.y, self.direction)
                Bolts.add(bolt)
            self.wait -= 1

        if (self.direction_check()):
            self.turn()
            self.wait = 90
            self.turning = 1

        if self.wait_status == True:
            self.wait -= 1

        elif self.direction == 0:
            self.pos.x += self.vel.x
            self.wait += self.vel.x
        elif self.direction == 1:
            self.pos.x -= self.vel.x
            self.wait += self.vel.x

        self.rect.topleft = self.pos  # Updates rect




    def update(self):

        # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, Playergroup, False)
        s_hits = pygame.sprite.spritecollide(self, Swings, False)

        # Checks for collision with Fireballs
        f_hits = pygame.sprite.spritecollide(self, Fireballs, False)

        # Activates upon either of the two expressions being true
        if player.attacking == True and f_hits or s_hits:
            self.kill()
            handler.dead_enemy_count += 1

            if player.mana < 100: player.mana += self.mana  # Release mana
            player.experience += 1  # Release expeiriance

            rand_num = numpy.random.uniform(0, 100)
            item_no = 0
            if rand_num >= 0 and rand_num <= 5:  # 1 / 20 chance for an item (health) drop
                item_no = 1
            elif rand_num > 5 and rand_num <= 15:
                item_no = 2

            if item_no != 0:
                # Add Item to Items group
                item = Item(item_no)
                Items.add(item)
                # Sets the item location to the location of the killed enemy
                item.posx = self.pos.x
                item.posy = self.pos.y

    def render(self):
        # Displays the enemy on screen
        displaysurface.blit(self.image, self.rect)

    def direction_check(self):
        if (player.pos.x - self.pos.x < 0 and self.direction == 0):
            return 1
        elif (player.pos.x - self.pos.x > 0 and self.direction == 1):
            return 1
        else:
            return 0

    def turn(self): # self.wait is not decreasing fast enough
        if self.wait > 0:
            self.wait -= 1

        elif int(self.wait) <= 0:
            self.turning = 0
        print("turning")
        if (self.direction):
            self.direction = 0
            self.image = pygame.image.load("images/enemy2.png")

            self.image = pygame.transform.scale(self.image, (105, 105))
        else:
            self.direction = 1
            self.image = pygame.image.load("images/enemy2_L.png")

            self.image = pygame.transform.scale(self.image, (105, 105))



class FireBall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = player.direction



        if self.direction == "RIGHT":
            self.image = pygame.image.load("images/fireball1_L.png")
            self.image = pygame.transform.scale(self.image, (15, 15))
        else:
            self.image = pygame.image.load("images/fireball1_R.png")
            self.image = pygame.transform.scale(self.image, (15, 15))
        self.rect = self.image.get_rect(center=player.pos)
        self.rect.x = player.pos.x
        self.rect.y = player.pos.y - 40

    def fire(self): #movement of the fireball
        player.magic_cooldown = 0
        # Runs while the fireball is still within the screen w/ extra margin
        if -10 < self.rect.x < 710:
            if self.direction == "RIGHT":
                self.image = pygame.image.load("images/fireball1_L.png")
                displaysurface.blit(self.image, self.rect)
            else:
                self.image = pygame.image.load("images/fireball1_R.png")
                displaysurface.blit(self.image, self.rect)

            if self.direction == "RIGHT":
                self.rect.move_ip(1, 0)
            else:
                self.rect.move_ip(-1, 0)
        else:
            self.kill()
            player.magic_cooldown = 1
            player.attacking = False


class swing(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = player.direction
        self.swoop_ani_R = [pygame.transform.scale(pygame.transform.flip(pygame.image.load("images/swing1.png"), True, False), (105, 105)),
                            pygame.transform.scale(pygame.transform.flip(pygame.image.load("images/swing2.png"), True, False), (105, 105)),
                            pygame.transform.scale(pygame.transform.flip(pygame.image.load("images/swing3.png"), True, False), (105, 105))]
        self.swoop_ani_L = [pygame.transform.scale(pygame.image.load("images/swing1.png"),(105, 105)),
                            pygame.transform.scale(pygame.image.load("images/swing2.png"),(105, 105)),
                            pygame.transform.scale(pygame.image.load("images/swing3.png"),(105, 105))]

        if self.direction == "RIGHT":
            self.image = pygame.transform.flip(pygame.image.load("images/swing1.png"), True, False)
            self.image = pygame.transform.scale(self.image, (105, 105))
        else:
            self.image = pygame.image.load("images/swing1.png")
            self.image = pygame.transform.scale(self.image, (105, 105))
        self.rect = self.image.get_rect(center=player.pos)

        if self.direction == "RIGHT":
            self.rect.x = player.pos.x + 20
        else:
            self.rect.x = player.pos.x - 80
        self.rect.y = player.pos.y - 70

    def attack(self):
        #print(abs(player.rect.x - self.rect.x))

        self.rect.y = player.pos.y - 70

        if abs(player.rect.x - self.rect.x) < 100:
            #print("passed")
            if self.direction == "RIGHT":
                #self.image = pygame.transform.flip(pygame.image.load("images/swing.png"), True, False)
                #self.image = pygame.transform.scale(self.image, (105, 105))

                self.image = self.swoop_ani_R[(abs(player.rect.x - self.rect.x) // 30)-1]
                #print((abs(player.rect.x - self.rect.x) // 30)-1)
                displaysurface.blit(self.image, self.rect)
            else:
                #self.image = pygame.image.load("images/swing.png")
                #self.image = pygame.transform.scale(self.image, (105, 105))
                #self.image = self.swoop_ani_L[abs(player.rect.x - self.rect.x) // 30]

                self.image = self.swoop_ani_L[(abs(player.rect.x - self.rect.x) // 30) - 1]
                #print((abs(player.rect.x - self.rect.x) // 30) - 1)
                displaysurface.blit(self.image, self.rect)

            if self.direction == "RIGHT":
                self.rect.move_ip(1.5, 0)
            else:
                self.rect.move_ip(-1.5, 0)
            if player.direction != self.direction:
                self.kill()
        else:
            self.kill()
            player.attacking = False



attackCD = 1

background = Background()
ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)

Items = pygame.sprite.Group()
Pause = PButton()
Home = PButton()
savebutton = PButton()
loadbutton = PButton()

cursor = Cursor()
Fireballs = pygame.sprite.Group()
Bolts = pygame.sprite.Group()
Swings = pygame.sprite.Group()

player = Player()
Playergroup = pygame.sprite.Group()
Playergroup.add(player)

health = HealthBar()

#enemy = Enemy()
Enemies = pygame.sprite.Group()

#Enemies = []
#Enemies.add(enemy)

Map = Map()
handler = EventHandler()
stage_display = StageDisplay()
menu_display = MenuDisplay()
GO = GameOver()

# Music and Sound
#soundtrack = ["Twilight_Plains_music", "Sabreclaw_wastelands_music"]
#swordtrack = [pygame.mixer.Sound("sword1.wav"), pygame.mixer.Sound("sword2.wav")]
#fsound = pygame.mixer.Sound("fireball_sound.wav")
#hit = pygame.mixer.Sound("enemy_hit.wav")


player.image = pygame.image.load("images/empty.png")

def gravity_check(self):
    hits = pygame.sprite.spritecollide(player, ground_group, False)
    if self.vel.y > 0:
        if hits:
            lowest = hits[0]
            if self.pos.y < lowest.rect.bottom:
                self.pos.y = lowest.rect.top + 3
                self.vel.y = 0
                self.jumping = False

status_bar = StatusBar()

while True:

    #print(player.experience)

    #player.health = 5  # cheat code 1
    #player.mana = 12  # cheat code 2
    #nEventHandler.phase = 100  # cheat code 3

    a = datetime.datetime.now()
    #print(Enemies)
    gravity_check(player)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        # Will run when the close window button is clicked ("X" at corner of the screen)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

            # For events that occur upon clicking the mouse (left click)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 620 <= mouse[0] <= 670 and 300 <= mouse[1] <= 345:
                cursor.pause()
            if 560 <= mouse[0] <= 610 and 300 <= mouse[1] <= 345:
                handler.home()
            if 500 <= mouse[0] <= 550 and 300 <= mouse[1] <= 345:
                handler.saveG()
            if 440 <= mouse[0] <= 490 and 300 <= mouse[1] <= 345:
                handler.loadG()


            elif 0 <= mouse[0] <= 700 and 0 <= mouse[1] <= 300 and event.button == 1: # attacking
                #player.attack()
                #player.attacking = True
                #print("attack")
                #print("swung")
                if player.attacking == False:
                    player.attacking = True
                    SW = swing()
                    Swings.add(SW)
            elif 0 <= mouse[0] <= 700 and 0 <= mouse[1] <= 300 and player.magic_cooldown == 1 and event.button == 3:
                print("fired")
                if player.mana >= 6:
                    player.mana -= 6
                    player.attacking = True
                    fireball = FireBall()
                    Fireballs.add(fireball)

        if event.type == handler.enemy_generation:
            #print(handler.stage)
            while handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                #print("a:", handler.enemy_count)
                #print("b:", handler.stage_enemies[player.stage - 1])
                enemy = Enemy()
                Enemies.add(enemy)
                handler.enemy_count += 1
                handler.next_level_started = False

        if event.type == handler.enemy_generation2:
            if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                enemy = Enemy2()
                Enemies.add(enemy)
                handler.enemy_count += 1
                handler.next_level_started = False


                # Event handling for a range of different key presses
        # Event handling for a range of different key presses
        if event.type == pygame.KEYDOWN and cursor.wait == 0:
            if 300 < player.rect.x < 600 and event.key == pygame.K_e and handler.world == 0:
                handler.stage_handler()
                #print("castle range")
            if event.key == pygame.K_n:
                if Enemies != None  and not (handler.next_level_started):
                    if handler.battle == True and len(Enemies) == 0:
                        handler.next_level_started = True
                        handler.next_stage()
                        print("test")
                        stage_display = StageDisplay()
                        stage_display.display = True


                    # Event handling for a range of different key presses
            if event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_SPACE and player.startdone == False:
                player.start = True



            if event.key == pygame.K_LEFT:
                player.move()
            if event.key == pygame.K_RIGHT:
                player.move()
        if event.type == hit_cooldown:
            player.cooldown = False
            pygame.time.set_timer(hit_cooldown, 0)
            #####################print("CD complete")


    # attackCD = attackCD - 1
    # if attackCD <1:
    #     attackCD = 1
    #
    # if attackCD > 2:
    #     player.attacking = True


    # Rendering Sprites
    background.render()
    ground.render()
    Map.update()
    Pause.render(1)
    Home.render(2)
    savebutton.render(3)
    loadbutton.render(4)
    cursor.hover()

    if player.health > 0:
        #displaysurface.blit(player.image, player.rect)
        player.image = pygame.transform.scale(player.image, (100, 100))
        displaysurface.blit(player.image, player.rect)

    health.render()

    if Enemies != None:
        for entity in Enemies:
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

    if player.attacking == True:
        player.attack()
        #print("attacked")

    for i in Items:
        i.render()
        i.update()

    for SW in Swings:
        SW.attack()
    for ball in Fireballs:
        ball.fire()
    for bolt in Bolts:
        bolt.fire()


    if player.startdone == False:
        if player.start == True :
            player.image = pygame.transform.scale(player.image, (80, 80))
            player.start = False
            menu_display.display = False
            player.startdone = True
    else:
        player.update()
        player.move()


    #print("player rect:",player.rect)


    # Render stage display
    if stage_display.display == True:
        stage_display.move_display()
    if stage_display.clear == True:
        stage_display.stage_clear()

    # Render Starting screen
    if menu_display.display == True:
        menu_display.move_display()
    if menu_display.clear == True:
        menu_display.stage_clear()

    #print(stage_display.clear)
    # Status bar update and render

    GO.GO_display()

    displaysurface.blit(status_bar.surf, (580, 5))
    status_bar.update_draw()
    handler.update()




    health.image = pygame.transform.scale(health.image, (280, 90)) #####################################################################################################################################################################
    background.bgimage = pygame.transform.scale(background.bgimage, (WIDTH, HEIGHT))


    pygame.display.update()
    FPS_CLOCK.tick(FPS)


    b = datetime.datetime.now()
    #print(GO.GameEnded)
    #print(player.jump_timer)