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

class Enemy(pygame.sprite.Sprite): # Enemy1
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
        self.health = 2
        self.maxhealth = self.health

        self.iframes = 15  # default value
        self.dmgCD = self.iframes

        self.cooldown = False
        self.hbWidth = int(p.HEIGHT*0.166)
        self.hbHeight = int(p.HEIGHT*0.0666)
        self.bossHealth = hb.HealthBar(self.hbWidth,self.hbHeight)
        self.bossHealth.render(5, self.pos.x, self.pos.y, True)

        # movement
        self.direction = random.randint(0, 1)  # 0 for Right, 1 for Left
        self.vel.x = 15 / 3  # Randomized velocity of the generated enemy
        self.mana = random.randint(2, 3)  # Randomized mana amount obtained upon


        if self.direction == 0:
            self.image = pygame.image.load("images/Enemy.png")
        elif self.direction == 1:
            self.image = pygame.image.load("images/Enemy.png")

        self.image = pygame.transform.scale(self.image, (int(p.WIDTH*0.08), int(p.HEIGHT*0.20)))
        self.rect = self.image.get_rect()


        # Sets the initial position of the enemy  #to-do: maybe allow enemy 2 to generate at different heights
        if self.direction == 0:
            self.pos.x = self.pos.x = int(p.WIDTH*0.05)
            self.pos.y = int(p.HEIGHT*0.64)
        if self.direction == 1:
            self.pos.x = self.pos.x = int(p.WIDTH*0.95)
            self.pos.y = int(p.HEIGHT*0.64)

    def move(self):  # enemy
        if r.cursor.wait == 1: return

        # Causes the enemy to change directions upon reaching the end of screen
        if self.pos.x >= (p.WIDTH - int(p.WIDTH * 0.08)):
            self.direction = 1
        elif self.pos.x <= 0:
            self.direction = 0
        # Updates position with new values
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x

        self.rect.center = self.pos  # Updates rect


    def update(self): # Enemy1
        self.bossHealth.image = p.health_ani[int((self.health/self.maxhealth)*5)]
        self.bossHealth.image = pygame.transform.scale(self.bossHealth.image, (self.hbWidth,self.hbHeight))
        self.bossHealth.render(5,self.pos.x-int(p.HEIGHT*0.092), self.pos.y-int(p.HEIGHT*0.07), True)

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
            self.dmgCD = self.iframes

            self.boltCD = 150

        if f_hits or s_hits and self.dmgCD == self.iframes: # TODO: add iframes
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
        self.rect.y = self.pos.y + int(p.HEIGHT * 0.01)
        p.displaysurface.blit(self.image, self.rect)



    def direction_check(self):
        if (pl.player.pos.x - self.pos.x < 0 and self.direction == 0):
            return 1
        elif (pl.player.pos.x - self.pos.x > 0 and self.direction == 1):
            return 1
        else:
            return 0

