import pygame
import parameters as p
import runtime_parameters as r
import Player as pl

class FireBall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = pl.player.direction



        if self.direction == "RIGHT":
            self.image = pygame.image.load("images/Shadow_Orb.png")
            self.image = pygame.transform.scale(self.image, (int(p.WIDTH*0.03),int(p.HEIGHT*0.03)))
        else:
            self.image = pygame.image.load("images/Shadow_Orb.png")
            self.image = pygame.transform.scale(self.image, (int(p.WIDTH*0.03),int(p.HEIGHT*0.03)))
        self.rect = self.image.get_rect(center=pl.player.pos)
        self.rect.x = pl.player.pos.x
        self.rect.y = pl.player.pos.y - int(p.HEIGHT*0.15)

    def fire(self): #movement of the fireball
        pl.player.magic_cooldown = 0
        # Runs while the fireball is still within the screen w/ extra margin
        if -20 < self.rect.x < p.WIDTH:
            if self.direction == "RIGHT":
                self.image = pygame.image.load("images/Shadow_Orb.png")
                self.image = pygame.transform.scale(self.image, (int(p.WIDTH * 0.03), int(p.HEIGHT * 0.03)))
                p.displaysurface.blit(self.image, self.rect)
            else:
                self.image = pygame.image.load("images/Shadow_Orb.png")
                self.image = pygame.transform.scale(self.image, (int(p.WIDTH*0.03),int(p.HEIGHT*0.03)))
                p.displaysurface.blit(self.image, self.rect)

            if self.direction == "RIGHT":
                self.rect.move_ip(int(p.WIDTH*0.025), 0)
            else:
                self.rect.move_ip(int(p.WIDTH*0.025)*-1, 0)
        else:
            self.kill()
            pl.player.magic_cooldown = 1
            pl.player.attacking = False