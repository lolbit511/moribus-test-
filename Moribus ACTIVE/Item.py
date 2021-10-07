import parameters as p
import pygame
import MusicManager as mm
import runtime_parameters as r
import Player as pl
import HealthBar as hl

class Item(pygame.sprite.Sprite):
    def __init__(self, itemtype):
        super().__init__()
        if itemtype == 1:
            self.image = pygame.image.load("images/heart.png")
            self.image = pygame.transform.scale(self.image, (int(p.WIDTH * 0.05), int(p.HEIGHT * 0.07)))
        elif itemtype == 2:
            self.image = pygame.image.load("images/coin.png")
            self.image = pygame.transform.scale(self.image, (int(p.WIDTH*0.05), int(p.HEIGHT*0.07)))
        elif itemtype == 3:
            self.image = pygame.image.load("images/jump_potion.gif")
            self.image = pygame.transform.scale(self.image, (int(p.WIDTH*0.05), int(p.HEIGHT*0.07)))
        self.rect = self.image.get_rect()
        self.type = itemtype
        self.posx = 0
        self.posy = 0

    def render(self):
        self.rect.x = self.posx
        self.rect.y = self.posy + int(p.HEIGHT*0.07)
        p.displaysurface.blit(self.image, self.rect)

    def update(self): #item
        hits = pygame.sprite.spritecollide(self, r.Playergroup, False)
        # Code to be activated if item comes in contact with player
        if hits:
            # TODO: insert sound effect
            if hl.healthCount < 100 and self.type == 1: #############################################################################################################################
                hl.healthCount += 30
                if hl.healthCount > 100:
                    hl.healthCount = 100
                mm.mmanager.playsound(p.healthSound, 0.3)
                #health_ani.image = health_ani[player.health] # old code do not uncomment
                hl.health.image = p.health_ani[int(hl.healthCount / 20)] # error
                self.kill() #############################################################################################################################
            if self.type == 2:
                # handler.money += 1
                pl.player.coin += 1
                mm.mmanager.playsound(p.coinSound, 0.3)
                self.kill()
            if self.type == 3:
                mm.mmanager.playsound(p.boostSound, 0.3)
                print("jump boosted")
                pl.player.jumpheight = int(p.HEIGHT*0.05) * -1
                self.kill()