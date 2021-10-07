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
        self.image = pygame.image.load("images/Enemy.png")

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

    def player_hit(self): #enemy

        if r.GO.GameEnded != True:
        # print("entering player hit")
            if self.cooldown == False:
                ####################################print("entered hit condition")
                self.cooldown = True  # Enable the cooldown
                pygame.time.set_timer(p.hit_cooldown, 1000)  # Resets cooldown in 1 second

                ####################################print("hit")
                pygame.display.update()

    def update(self): #enemy
        if r.cursor.wait == 1: return
        rand_num = numpy.random.uniform(0, 50)
        # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, r.Playergroup, False)

        s_hits = pygame.sprite.spritecollide(self, r.Swings, False)

        # Checks for collision with Fireballs
        f_hits = pygame.sprite.spritecollide(self, r.Fireballs, False)


        # Activates upon either of the two expressions being true
        if f_hits or s_hits:
            mm.mmanager.playsound(p.e1DeathSound, 0.3)

            #player.health = player.health + 3   ############################################################################################################
            # if pl.player.health > 100:
                # pl.player.health = 100
            if pl.player.mana < 100: pl.player.mana += self.mana  # Release mana
            pl.player.experience += 1  # Release expeiriance
            self.kill()
            r.handler.dead_enemy_count += 1
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
                item = it.Item(item_no)
                r.Items.add(item)
                # Sets the item location to the location of the killed enemy
                item.posx = self.pos.x
                item.posy = self.pos.y

        #If collision has occured and player not attacking, call "hit" function
        elif hits and pl.player.attacking == False:
            self.player_hit()
            #print("player died")
            #print(self.rect)

    def render(self):
        # Displayed the enemy on screen
        p.displaysurface.blit(self.image, (self.pos.x, self.pos.y))



