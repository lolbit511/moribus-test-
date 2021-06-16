import pygame
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *

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
        # Stage
        self.stage = 1



    def move(self):
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
        # If attack frame has reached end of sequence, return to base frame
        if self.attack_frame > 4:
            self.attack_frame = 0
            self.attacking = False

        ## Attacking Animations

        att_ani_L= [pygame.image.load("player.png"),pygame.image.load("player.png"),pygame.transform.flip(pygame.image.load("sword_right.png"),True,False),pygame.transform.flip(pygame.image.load("sword_right.png"),True,False),
                     pygame.transform.flip(pygame.image.load("sword_right.png"),True,False),pygame.transform.flip(pygame.image.load("sword_right.png"),True,False),pygame.image.load("player.png")]

        att_ani_R = [pygame.transform.flip(pygame.image.load("player.png"),True,False),pygame.transform.flip(pygame.image.load("player.png"),True,False),pygame.image.load("sword_right.png"), pygame.image.load("sword_right.png"),
                     pygame.image.load("sword_right.png"), pygame.image.load("sword_right.png"),pygame.transform.flip(pygame.image.load("player.png"),True,False)]


        # Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = att_ani_R[self.attack_frame]
        elif self.direction == "LEFT":
            self.image = att_ani_L[self.attack_frame]

            # Update the current attack frame
        self.attack_frame += 1
        # Updates position with new values
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x

        self.rect.center = self.pos  # Updates rect


    def update(self): #
        ## Moving animations

        # Run animation for the RIGHT
        run_ani_R = [pygame.transform.flip(pygame.image.load("player.png"),True,False), pygame.transform.flip(pygame.image.load("player.png"),True,False),
                     pygame.transform.flip(pygame.image.load("player.png"),True,False), pygame.transform.flip(pygame.image.load("player.png"),True,False),
                     pygame.transform.flip(pygame.image.load("playerWalk1.png"),True,False),pygame.transform.flip(pygame.image.load("playerWalk1.png"),True,False),
                     pygame.transform.flip(pygame.image.load("playerWalk1.png"),True,False), pygame.transform.flip(pygame.image.load("playerWalk1.png"),True,False),
                     pygame.transform.flip(pygame.image.load("playerWalk2.png"), True, False),pygame.transform.flip(pygame.image.load("playerWalk2.png"), True, False),
                     pygame.transform.flip(pygame.image.load("playerWalk2.png"), True, False),pygame.transform.flip(pygame.image.load("playerWalk2.png"), True, False)]

        run_ani_L = [pygame.image.load("player.png"), pygame.image.load("player.png"),
                     pygame.image.load("player.png"), pygame.image.load("player.png"),
                     pygame.image.load("playerWalk1.png"), pygame.image.load("playerWalk1.png"),
                     pygame.image.load("playerWalk1.png"), pygame.image.load("playerWalk1.png"),
                     pygame.image.load("playerWalk2.png"), pygame.image.load("playerWalk2.png"),
                     pygame.image.load("playerWalk2.png"), pygame.image.load("playerWalk2.png")
                     ]


        # Move the character to the next frame if conditions are met
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = run_ani_R[self.move_frame]
                self.direction = "RIGHT"

            elif self.vel.x < 0:
                self.image = run_ani_L[self.move_frame]
                self.direction = "LEFT"

            self.move_frame += 1
            if self.move_frame == 8:  # return to starting animation at loop 8
                self.move_frame = 0


            # Returns to base frame if standing still and incorrect frame is showing
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = run_ani_R[self.move_frame]
            elif self.direction == "LEFT":
                self.image = run_ani_L[self.move_frame]


    def jump(self):
        self.rect.x += 1

        # Check to see if payer is in contact with the ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)

        self.rect.x -= 1

        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -10


class Castle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hide = False
        self.image = pygame.image.load("castle.png")

    def update(self):
        if self.hide == False:
            displaysurface.blit(self.image, (400, 80))




class EventHandler():
    def __init__(self):
        self.enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 1
        self.stage_enemies = []
        for x in range(1, 21):
            self.stage_enemies.append(int((x ** 2 / 2) + 1)) #formula for enemy generation

        def next_stage(self):  # Code for when the next stage is clicked
            self.stage += 1
            self.enemy_count = 0
            print("Stage: " + str(self.stage))
            pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage))

    # Code for when the next stage is clicked (reminder: ask question about this)




    def stage_handler(self):
        # Code for the Tkinter stage selection window
        self.root = Tk()
        self.root.geometry('200x170')

        button1 = Button(self.root, text="[Tutorial] Twilight Pathway", width=18, height=2,
                         command=self.world1)
        button2 = Button(self.root, text="[Town] Tilia Town", width=18, height=2,
                         command=self.world2)
        button3 = Button(self.root, text="[Dungeon] Shadowmancer's Hideout", width=18, height=2,
                         command=self.world3)
        button4 = Button(self.root, text="[Dungeon] Iceborne Crypts", width=18, height=2,
                         command=self.world4)
        button5 = Button(self.root, text="[Dungeon] Mount Moru", width=18, height=2,
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
        castle.hide = True
        self.battle = True

    def world2(self):
        self.battle = True
        # Empty for now

    def world3(self):
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
        self.attacking = False
        self.cooldown = False
        self.attack_frame = 0


        self.direction = random.randint(0, 1)  # 0 for Right, 1 for Left
        self.vel.x = random.randint(5, 18) / 2  # Randomized velocity of the generated enemy

        # Sets the intial position of the enemy
        if self.direction == 0:
            self.pos.x = 0
            self.pos.y = 350-120 # 100 is height of enemy image
        if self.direction == 1:
            self.pos.x = 700-100
            self.pos.y = 350-120

    def move(self): # enemy
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

    def player_hit(self):
        #print("entering player hit")
        if self.cooldown == False:
            ####################################print("entered hit condition")
            self.cooldown = True  # Enable the cooldown
            pygame.time.set_timer(hit_cooldown, 1000)  # Resets cooldown in 1 second

            ####################################print("hit")
            pygame.display.update()


    def update(self): #enemy
        # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, Playergroup, False)
        #print(player.attacking)
        #print(hits)
        # Activates upon either of the two expressions being true
        if hits and player.attacking == True:
            self.kill()
            #print("Enemy killed")

        # If collision has occured and player not attacking, call "hit" function
        elif hits and player.attacking == False:
            print("player died")
            print(self.rect)

            self.player_hit()


    def render(self):
        # Displayed the enemy on screen
        displaysurface.blit(self.image, (self.pos.x, self.pos.y))



background = Background()
ground = Ground()
ground_group = pygame.sprite.Group()
ground_group.add(ground)

player = Player()
Playergroup = pygame.sprite.Group()
Playergroup.add(player)


enemy = Enemy()
Enemies = pygame.sprite.Group()
Enemies.add(enemy)

castle = Castle()
handler = EventHandler()



def gravity_check(self):
    hits = pygame.sprite.spritecollide(player, ground_group, False)
    if self.vel.y > 0:
        if hits:
            lowest = hits[0]
            if self.pos.y < lowest.rect.bottom:
                self.pos.y = lowest.rect.top + 3
                self.vel.y = 0
                self.jumping = False

while True:

    gravity_check(player)

    for event in pygame.event.get():
        # Will run when the close window button is clicked ("X" at corner of the screen)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

            # For events that occur upon clicking the mouse (left click)
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

        if event.type == handler.enemy_generation:
            if handler.enemy_count < handler.stage_enemies[player.stage - 1]:
                enemy = Enemy()
                Enemies.add(enemy)
                handler.enemy_count += 1

                # Event handling for a range of different key presses
        if event.type == pygame.KEYDOWN:
            if 300 < player.rect.x < 600 and event.key == pygame.K_e:
                handler.stage_handler()
                print("castle range")
            if event.key == pygame.K_n:
                if handler.battle == True and len(Enemies) == 0:
                    handler.next_stage()
                    # Event handling for a range of different key presses
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_a:
                if player.attacking == False:
                    player.attack()
                    player.attacking = True
            if event.key == pygame.K_LEFT:
                player.move()
            if event.key == pygame.K_RIGHT:
                player.move()
        if event.type == hit_cooldown:
            enemy.cooldown = False
            pygame.time.set_timer(hit_cooldown, 0)
            #####################print("CD complete")

    background.render()
    ground.render()


    # Rendering Sprites
    castle.update()
    #enemy.update()
    #enemy.move()
    #enemy.render()

    for entity in Enemies:
        entity.update()
        entity.move()
        entity.render()

    player.image = pygame.transform.scale(player.image, (100, 100))################# had to add this to prevent a glitch where the player sprite will go to its full size when in the alternative walking frames
    displaysurface.blit(player.image, player.rect)

    # Player related functions
    player.update()
    if player.attacking == True:
        player.attack()
    player.move()
    print("player rect:",player.rect)


    pygame.display.update()
    FPS_CLOCK.tick(FPS)