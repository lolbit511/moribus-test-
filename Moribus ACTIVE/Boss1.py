import parameters as p
import pygame
import numpy
import random
import MusicManager as mm
import runtime_parameters as r
import Player as pl
import Bolt as bl
import EventHandler as e
import HealthBar as hb
import Item as it

class Boss1(pygame.sprite.Sprite): #boss, first boss boss 1
    def __init__(self):
        super().__init__()
        self.pos = p.vec(0, 0)
        self.vel = p.vec(0, 0)
        self.wait = 500
        self.wait_status = False
        self.turning = 0
        self.boltCD = 150
        self.fired = False
        # health
        self.health = 5
        self.dmgCD = 25 #################################################################################################################################################################################
        self.cooldown = False
        self.bossHealth = hb.HealthBar(200,70)
        self.bossHealth.render(self.pos.x, self.pos.y, self.health)

        # movement
        self.direction = random.randint(0, 1)  # 0 for Right, 1 for Left
        self.vel.x = 15 / 3  # Randomized velocity of the generated enemy
        self.mana = random.randint(2, 3)  # Randomized mana amount obtained upon


        if self.direction == 0:
            self.image = pygame.image.load("images/bosses/boss1_R.png")
        elif self.direction == 1:
            self.image = pygame.image.load("images/bosses/boss1.png")

        self.image = pygame.transform.scale(self.image, (int(p.WIDTH*0.08), int(p.HEIGHT*0.20)))
        self.rect = self.image.get_rect()

        # Sets the initial position of the enemy  #to-do: maybe allow enemy 2 to generate at different heights
        if self.direction == 0:
            self.pos.x = self.pos.x = int(p.WIDTH*0.05)
            self.pos.y = int(p.HEIGHT*0.64)
        if self.direction == 1:
            self.pos.x = self.pos.x = int(p.WIDTH*0.95)
            self.pos.y = int(p.HEIGHT*0.64)

    def move(self): # boss 1
        if r.cursor.wait == 1: return
        # Causes the enemy to change directions upon reaching the end of screen
        if self.pos.x >= (p.WIDTH - 50):
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
                bolt = bl.Bolt(self.pos.x, self.pos.y, self.direction)
                r.Bolts.add(bolt)
            self.wait -= 1

        if (self.direction_check()):
            self.turn()
            self.wait = 90
            self.turning = 1

        if self.wait_status == True: # determines how long the entity waits
            self.wait -= 5

        elif self.direction == 0:
            self.pos.x += self.vel.x
            self.wait += self.vel.x
        elif self.direction == 1:
            self.pos.x -= self.vel.x
            self.wait += self.vel.x

        self.rect.topleft = self.pos  # Updates rect


    def update(self): # boss 1

        self.bossHealth.render(self.pos.x, self.pos.y -80, self.health)
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
            # TODO: no contact damage

            # TODO: reset enemy projectile attack
            self.boltCD = 150

        if f_hits or s_hits and self.dmgCD == 25:
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
        # Displays the enemy on screen
        p.displaysurface.blit(self.image, self.rect)

    def direction_check(self):
        if (pl.player.pos.x - self.pos.x < 0 and self.direction == 0):
            return 1
        elif (pl.player.pos.x - self.pos.x > 0 and self.direction == 1):
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
            self.image = pygame.image.load("images/bosses/boss1_R.png")

            self.image = pygame.transform.scale(self.image, (int(p.WIDTH*0.08), int(p.HEIGHT*0.20)))
        else:
            self.direction = 1
            self.image = pygame.image.load("images/bosses/boss1.png")

            self.image = pygame.transform.scale(self.image, (int(p.WIDTH*0.08), int(p.HEIGHT*0.20)))