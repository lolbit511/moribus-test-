import numpy
import pygame # THIS IS THE ACTUAL FILE ON GITHUB (23/6/2021)
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *
import datetime

import time #######################################################################################new

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
        self.bgimage = pygame.image.load("background.png")
        self.bgimage = pygame.transform.scale(self.bgimage, (WIDTH, HEIGHT))
        self.bgY = 0
        self.bgX = 0

    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Ground.png")
        self.image = pygame.transform.scale(self.image, (WIDTH,50))
        self.rect = self.image.get_rect(center=(350, 350))



    def render(self):
        displaysurface.blit(self.image, (self.rect.x, self.rect.y))


class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("heart5.png")

    def render(self):
        displaysurface.blit(self.image, (10, 10))

# Moved health bar animations out so all other classes have easy access
health_ani = [pygame.image.load("heart0.png"), pygame.image.load("heart.png"),
                      pygame.image.load("heart2.png"), pygame.image.load("heart3.png"),
                      pygame.image.load("heart4.png"), pygame.image.load("heart5.png")]

class Player(pygame.sprite.Sprite):
    def __init__(self):

        super().__init__()
        self.image = pygame.image.load("playerWalk1.png")
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
        # Combat
        self.attacking = False
        self.attack_frame = 0
        self.attCD = 40

        self.experiance = 0
        self.mana = 0
        self.coin = 0

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
        self.run_ani_R = [pygame.transform.flip(pygame.image.load("player.png"),True,False), pygame.transform.flip(pygame.image.load("player.png"),True,False),
                     pygame.transform.flip(pygame.image.load("player.png"),True,False), pygame.transform.flip(pygame.image.load("player.png"),True,False),
                     pygame.transform.flip(pygame.image.load("playerWalk1.png"),True,False),pygame.transform.flip(pygame.image.load("playerWalk1.png"),True,False),
                     pygame.transform.flip(pygame.image.load("playerWalk1.png"),True,False), pygame.transform.flip(pygame.image.load("playerWalk1.png"),True,False)]

        self.run_ani_L = [pygame.image.load("player.png"), pygame.image.load("player.png"),
                     pygame.image.load("player.png"), pygame.image.load("player.png"),
                     pygame.image.load("playerWalk1.png"), pygame.image.load("playerWalk1.png"),
                     pygame.image.load("playerWalk1.png"), pygame.image.load("playerWalk1.png")]

        self.att_ani_R = [pygame.transform.flip(pygame.image.load("player.png"), True, False)]
        self.att_ani_R = self.att_ani_R + [pygame.transform.flip(pygame.image.load("sword.png"), True, False)] * self.attCD

        self.att_ani_R.append(pygame.image.load("player.png"))


        #print(self.att_ani_R)
        self.att_ani_L = [pygame.image.load("player.png")]
        self.att_ani_L = self.att_ani_L + [pygame.image.load("sword.png")] * self.attCD
        self.att_ani_L.append(pygame.transform.flip(pygame.image.load("player.png"), True, False))

        #print(self.att_ani_L)


    def player_hit(self): #new

        #print("entering player hit")
        if self.cooldown == False:

            self.cooldown = True  # Enable the cooldown
            pygame.time.set_timer(hit_cooldown, 1000)  # Resets cooldown in 1 second

            self.health = self.health - 1
            health.image = health_ani[self.health]

            if self.health <= 0:
                self.kill()
                pygame.display.update()

    def move(self):
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
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
        # Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
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
            self.vel.y = -18


class Item(pygame.sprite.Sprite):
    def __init__(self, itemtype):
        super().__init__()
        if itemtype == 1:
            self.image = pygame.image.load("heart.png")
        elif itemtype == 2:
            self.image = pygame.image.load("coin.png")
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
                health.image = health_ani[player.health] ################################################################################################################################################
                self.kill()
            if self.type == 2:
                # handler.money += 1
                player.coin += 1
                self.kill()


class PButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.vec = vec(620, 300)
        self.imgdisp = 0

    def render(self, num):
        if (num == 0):
            self.image = pygame.image.load("home_small.png")
        elif (num == 1):
            if cursor.wait == 0:
                self.image = pygame.image.load("pause_small.png")
            else:
                self.image = pygame.image.load("play_small.png")

        displaysurface.blit(self.image, self.vec)


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("cursor.png")
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






class Castle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hide = False
        self.image = pygame.image.load("castle.png")

    def update(self):
        if self.hide == False:
            displaysurface.blit(self.image, (400, 80))


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
        text2 = smallerfont.render("EXP: " + str(player.experiance), True, color_white)
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
        self.stage = 1
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 1
        self.stage_enemies = []
        #self.stage_enemies.append(0)
        for x in range(1, 21):
            self.stage_enemies.append(x) #formula for enemy generation
        print(self.stage_enemies)

    def next_stage(self):  # Code for when the next stage is clicked
        button.imgdisp = 1
        self.stage += 1
        print("Stage: " + str(self.stage))
        self.enemy_count = 0
        self.dead_enemy_count = 0
        print("Stage: " + str(self.stage))
        pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage))

    def update(self): #Event Handler
        #print("a:" , self.dead_enemy_count)
        #print("b:" , self.stage_enemies[self.stage - 1])
        if self.dead_enemy_count == self.stage_enemies[self.stage - 1]:
            self.dead_enemy_count = 0
            stage_display.clear = True
            stage_display.stage_clear()
            print("stageClear ACTIVE")

    def home(self):
        # Reset Battle code
        pygame.time.set_timer(self.enemy_generation, 0)
        self.battle = False
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.stage = 1

        # Destroy any enemies or items lying around
        for group in Enemies, Items:
            for entity in group:
                entity.kill()

        # Bring back normal backgrounds
        castle.hide = False
        background.bgimage = pygame.image.load("Background.png")
        background.bgimage = pygame.transform.scale(background.bgimage, (WIDTH, HEIGHT))
        ground.image = pygame.image.load("Ground.png")
        ground.image = pygame.transform.scale(ground.image, (WIDTH,50))

    # Code for when the next stage is clicked (reminder: ask question about this)




    def stage_handler(self):
        # Code for the Tkinter stage selection window
        self.root = Tk()
        self.root.geometry('295x270')
        width = 30
        button1 = Button(self.root, text="[Tutorial] Twilight Pathway", width=width, height=2,
                         command=self.world1)
        button2 = Button(self.root, text="[Town] Tilia Town", width=width, height=2,
                         command=self.world2)
        button3 = Button(self.root, text="[Dungeon] Shadowmancer's Hideout", width=width, height=2,
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
        pygame.time.set_timer(self.enemy_generation, 2000)
        button.imgdisp = 1
        castle.hide = True
        self.battle = True

    def world2(self):
        button.imgdisp = 1
        self.battle = True
        # Empty for now

    def world3(self):
        button.imgdisp = 1
        self.battle = True
        # Empty for now

    def world4(self):
        button.imgdisp = 1
        self.battle = True
        # Empty for now

    def world5(self):
        button.imgdisp = 1
        self.battle = True
        # Empty for now



class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")

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
        #print(player.attacking)
        #print(hits)
        # Activates upon either of the two expressions being true
        if hits and player.attacking == True:
            if player.mana < 100: player.mana += self.mana  # Release mana
            player.experiance += 1  # Release expeiriance
            self.kill()
            handler.dead_enemy_count += 1
            #print(handler.dead_enemy_count)

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

        #If collision has occured and player not attacking, call "hit" function
        elif hits and player.attacking == False:
            self.player_hit()
            #print("player died")
            #print(self.rect)

    def render(self):
        # Displayed the enemy on screen
        displaysurface.blit(self.image, (self.pos.x, self.pos.y))

attackCD = 1 ###############################################

background = Background()
ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)

Items = pygame.sprite.Group()
button = PButton()
cursor = Cursor()

player = Player()
Playergroup = pygame.sprite.Group()
Playergroup.add(player)

health = HealthBar()

#enemy = Enemy()
Enemies = pygame.sprite.Group()
#Enemies = []
#Enemies.add(enemy)

castle = Castle()
handler = EventHandler()
stage_display = StageDisplay()


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
    #print(player.experiance)


    #player.health = 6 # cheat code 1

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
                if button.imgdisp == 1:
                    cursor.pause()
                elif button.imgdisp == 0:
                    handler.home()

        if event.type == handler.enemy_generation:
            #print(handler.stage)
            while handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                #print("a:", handler.enemy_count)
                #print("b:", handler.stage_enemies[player.stage - 1])
                enemy = Enemy()
                Enemies.add(enemy)
                handler.enemy_count += 1

                # Event handling for a range of different key presses
        # Event handling for a range of different key presses
        if event.type == pygame.KEYDOWN and cursor.wait == 0:
            if 300 < player.rect.x < 600 and event.key == pygame.K_e:
                handler.stage_handler()
                #print("castle range")
            if event.key == pygame.K_n:
                if Enemies != None:
                    if handler.battle == True and len(Enemies) == 0:
                        handler.next_stage()
                        print("test")
                        stage_display = StageDisplay()
                        stage_display.display = True

                    # Event handling for a range of different key presses
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_a: #and attackCD < 2:  new
                # attackCD = 40

                player.attack()
                player.attacking = True

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
    castle.update()
    button.render(button.imgdisp)
    cursor.hover()

    if player.health > 0:
        #displaysurface.blit(player.image, player.rect)
        player.image = pygame.transform.scale(player.image, (100, 100))
        displaysurface.blit(player.image, player.rect)

    health.render()

    if Enemies != None: ##################################### check if array is empty ###################################################################################################################################################
        for entity in Enemies:
            entity.update()
            entity.move()
            entity.render()


    ################# had to add this to prevent a glitch where the player sprite will go to its full size when in the alternative walking frames


    # Player related functions

    if player.attacking == True:
        player.attack()
        #print("attacked")

    for i in Items:
        i.render()
        i.update()

    player.move()
    player.update()
    #print("player rect:",player.rect)


    # Render stage display ######################################
    if stage_display.display == True:
        stage_display.move_display()
    if stage_display.clear == True:
        stage_display.stage_clear()

    #print(stage_display.clear)
    # Status bar update and render
    displaysurface.blit(status_bar.surf, (580, 5))
    status_bar.update_draw()
    handler.update()

    pygame.display.update()
    FPS_CLOCK.tick(FPS)


    b = datetime.datetime.now()
    #print(b - a)