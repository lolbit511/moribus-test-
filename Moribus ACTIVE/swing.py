import pygame
import parameters as p
import runtime_parameters as r
import Player as pl

class swing(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = pl.player.direction
        self.swoop_ani_R = [pygame.transform.scale(pygame.transform.flip(pygame.image.load("images/swing1.png"), True, False), (int(p.WIDTH * 0.15), int(p.HEIGHT * 0.15))),
                            pygame.transform.scale(pygame.transform.flip(pygame.image.load("images/swing2.png"), True, False), (int(p.WIDTH * 0.15), int(p.HEIGHT * 0.15))),
                            pygame.transform.scale(pygame.transform.flip(pygame.image.load("images/swing3.png"), True, False), (int(p.WIDTH * 0.15), int(p.HEIGHT * 0.15)))]
        self.swoop_ani_L = [pygame.transform.scale(pygame.image.load("images/swing1.png"),(int(p.WIDTH * 0.15), int(p.HEIGHT * 0.15))),
                            pygame.transform.scale(pygame.image.load("images/swing2.png"),(int(p.WIDTH * 0.15), int(p.HEIGHT * 0.15))),
                            pygame.transform.scale(pygame.image.load("images/swing3.png"),(int(p.WIDTH * 0.15), int(p.HEIGHT * 0.15)))]

        if self.direction == "RIGHT": # resizing
            self.image = pygame.transform.flip(pygame.image.load("images/swing1.png"), True, False)
            self.image = pygame.transform.scale(self.image, (int(p.WIDTH * 0.15), int(p.HEIGHT * 0.15)))
        else:
            self.image = pygame.image.load("images/swing1.png")
            self.image = pygame.transform.scale(self.image, (int(p.WIDTH * 0.15), int(p.HEIGHT * 0.15)))
        self.rect = self.image.get_rect(center=pl.player.pos)      #TODO: get center of the player sprite instead of the corner

        if self.direction == "RIGHT": # spawning object left or right of the player
            self.rect.x = pl.player.pos.x - int(p.WIDTH*0.03)
        else:
            self.rect.x = pl.player.pos.x - int(p.WIDTH*0.08)
        self.rect.y = pl.player.pos.y - int(p.HEIGHT*0.08)

    def attack(self):
        #print(abs(player.rect.x - self.rect.x))

        self.rect.y = pl.player.pos.y - int(p.HEIGHT*0.12)

        if abs(pl.player.rect.x - self.rect.x) < 100:
            #print("passed")
            if self.direction == "RIGHT":
                #self.image = pygame.transform.flip(pygame.image.load("images/swing.png"), True, False)
                #self.image = pygame.transform.scale(self.image, (105, 105))

                self.image = self.swoop_ani_R[(abs(pl.player.rect.x - self.rect.x) // 30)-1]
                #print((abs(player.rect.x - self.rect.x) // 30)-1)
                p.displaysurface.blit(self.image, self.rect)
            else:
                #self.image = pygame.image.load("images/swing.png")
                #self.image = pygame.transform.scale(self.image, (105, 105))
                #self.image = self.swoop_ani_L[abs(player.rect.x - self.rect.x) // 30]

                self.image = self.swoop_ani_L[(abs(pl.player.rect.x - self.rect.x) // 30)-1]
                #print((abs(player.rect.x - self.rect.x) // 30) - 1)
                p.displaysurface.blit(self.image, self.rect)

            if self.direction == "RIGHT":
                self.rect.move_ip(int(p.WIDTH*0.003), 0)
            else:
                self.rect.move_ip(int(p.WIDTH*0.003)*-1, 0)
            if pl.player.direction != self.direction:
                self.kill()
        else:
            self.kill()
            pl.player.attacking = False