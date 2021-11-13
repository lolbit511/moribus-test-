import pygame
import parameters as p
import runtime_parameters as r
import Player as pl

class Bolt(pygame.sprite.Sprite):
    def __init__(self, x, y, d):
        super().__init__()
        self.image = pygame.image.load("images/sabreclaw.png")
        self.image = pygame.transform.scale(self.image, (int(p.WIDTH*0.03),int(p.HEIGHT*0.03)))
        self.rect = self.image.get_rect()
        self.rect.x = x + 15
        self.rect.y = y + 20
        self.direction = d

    def fire(self):
        # Runs while the fireball is still within the screen w/ extra margind
        if -50 < self.rect.x < p.WIDTH+50:
            if self.direction == 0:
                self.image = pygame.image.load("images/sabreclaw.png")
                self.image = pygame.transform.scale(self.image, (int(p.WIDTH * 0.03), int(p.HEIGHT * 0.06)))
                p.displaysurface.blit(self.image, self.rect)
            else:
                self.image = pygame.transform.flip(pygame.image.load("images/sabreclaw.png"), True, False)
                self.image = pygame.transform.scale(self.image, (int(p.WIDTH * 0.03), int(p.HEIGHT * 0.06)))
                p.displaysurface.blit(self.image, self.rect)

            if self.direction == 0:
                self.rect.move_ip(int(p.WIDTH*0.01), 0)
            else:
                self.rect.move_ip(int(p.WIDTH*0.01)*-1, 0)
        else:
            self.kill()

        # Checks for collision with the Player
        hits = pygame.sprite.spritecollide(self, r.Playergroup, False)
        if hits and pl.player.sheildUp == False:
            pl.player.player_hit(15)
            self.kill()
        elif hits and pl.player.sheildUp == True:
            pl.player.player_hit(0)
            pl.player.mana = pl.player.mana - 5

            self.kill()