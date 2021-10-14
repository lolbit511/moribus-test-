import parameters as p
import pygame
import numpy
import random
import MusicManager as mm
import runtime_parameters as r
import Bolt as bl
import Player as pl
import HealthBar as hb
import Item as it

class Enemy(pygame.sprite.Sprite): #enemy 1  enemy1
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Enemy.png").convert()

        self.pos = p.vec(0, 0)
        self.vel = p.vec(0, 0)
        self.image = pygame.transform.scale(self.image, (int(p.WIDTH*0.08), int(p.HEIGHT*0.20)))
        self.rect = self.image.get_rect()

        # Combat
        self.direction = random.randint(0, 1)  # 0 for Right, 1 for Left
        self.vel.x = random.randint(2, 6) / 2  # Randomised velocity of the generated enemy, enemy speed
        self.mana = random.randint(1, 3)  # Randomised mana amount obtained upon kill

        #self.attacking = False
        self.cooldown = False
        #self.attack_frame = 0

        # dummy variables (prevents crash)
        self.boltCD = 150
        self.fired = False

        # health
        self.maxHealth = 2  # default value
        self.health = self.maxHealth

        self.iframes = 15  # default value
        self.dmgCD = self.iframes

        self.cooldown = False
        self.hbWidth = 180
        self.hbHeight = 60
        self.bossHealth = hb.HealthBar(self.hbWidth, self.hbHeight)
        self.bossHealth.render(5, self.pos.x, self.pos.y, True)

        # spawn location



        # Sets the intial position of the enemy
        if self.direction == 0: # right
            self.pos.x = int(p.WIDTH*-0.01*(random.randint(8,28))) ########### left = below 0, right = above WIDTH ########### from 0 to 0.2 ##################################################################################
            self.pos.y = int(p.HEIGHT*0.64) # 100 is height of enemy image
        if self.direction == 1: # left
            self.pos.x = int(p.WIDTH*+0.01*(random.randint(8,28))+p.WIDTH)
            self.pos.y = int(p.HEIGHT*0.64)

    def move(self): # enemy
        if r.cursor.wait == 1: return

        # Causes the enemy to change directions upon reaching the end of screen
        if self.pos.x >= (p.WIDTH - int(p.WIDTH*0.08)):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0
        # Updates position with new values
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x

        self.rect.center = self.pos  # Updates rect

    # def player_hit(self): #enemy
    #
    #     if r.GO.GameEnded != True:
    #     # print("entering player hit")
    #         if self.cooldown == False:
    #             ####################################print("entered hit condition")
    #             self.cooldown = True  # Enable the cooldown
    #             pygame.time.set_timer(p.hit_cooldown, 1000)  # Resets cooldown in 1 second
    #
    #             ####################################print("hit")
    #             pygame.display.update()

    def update(self): # enemy 1
        self.bossHealth.image = p.health_ani[int(self.health)]
        self.bossHealth.image = pygame.transform.scale(self.bossHealth.image, (self.hbWidth,self.hbHeight))
        self.bossHealth.render(5,self.pos.x, self.pos.y -100, True)

    # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, r.Playergroup, False)
        s_hits = pygame.sprite.spritecollide(self, r.Swings, False)

        # Checks for collision with Fireballs
        f_hits = pygame.sprite.spritecollide(self, r.Fireballs, False)
        print(" ")
        print("health:", self.health)
        print("cooldown:", self.boltCD)

        print(" ")
        # Activates upon either of the two expressions being true
        if self.cooldown == True:
            self.dmgCD -= 1
        if self.dmgCD < 0:
            self.cooldown = False
            self.dmgCD = 25

            self.boltCD = 150

        if f_hits or s_hits and self.dmgCD == 25: # TODO: add iframes
            mm.mmanager.playsound(p.e3HitSound, 0.3)
            #player.health = player.health + 3 # added
            if hb.healthCount > 100:
                hb.healthCount = 100
            self.cooldown = True
            self.health -= 1
            if self.health < 0:
                mm.mmanager.playsound(p.e3DeathSound, 0.3)
                if pl.player.mana < 100: pl.player.mana += self.mana  # Release mana
                pl.player.experience += 1  # Release expeiriance

                rand_num = numpy.random.uniform(0, 100)
                item_no = 0
                if rand_num >= 0 and rand_num <= 5:  # 1 / 20 chance for an item (health) drop
                    item_no = 1
                elif rand_num > 5 and rand_num <= 15:
                    item_no = 2

                if item_no != 0:
                    # Add Item to Items group
                    item = it.Item(item_no)
                    r.Items.add(item)
                    # Sets the item location to the location of the killed enemy
                    item.posx = self.pos.x
                    item.posy = self.pos.y

                self.kill()
                r.handler.dead_enemy_count += 1

    def render(self):
        # Displayed the enemy on screen
        p.displaysurface.blit(self.image, (self.pos.x, self.pos.y))