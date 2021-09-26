import parameters as p
import pygame

class PButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.vec = vec(620, 300)
        self.imgdisp = 0

    def render(self, num):
        if (num == 2):
            self.image = pygame.image.load("images/home.png").convert()
            self.image = pygame.transform.scale(self.image,(int(p.WIDTH*0.05),int(p.HEIGHT*0.1)))
            self.vec = p.vec(int(p.WIDTH*0.9), int(p.HEIGHT*0.9))
        elif (num == 1):
            if p.cursor.wait == 0:
                self.image = pygame.image.load("images/pause.png").convert()
            else:
                self.image = pygame.image.load("images/play.png").convert()
            self.image = pygame.transform.scale(self.image, (int(p.WIDTH * 0.05), int(p.HEIGHT * 0.1)))
            self.vec = p.vec(int(p.WIDTH * 0.95), int(p.HEIGHT * 0.9))
        elif (num == 3):
            self.image = pygame.image.load("images/save.png").convert()
            self.image = pygame.transform.scale(self.image, (int(p.WIDTH * 0.05), int(p.HEIGHT * 0.1)))
            self.vec = p.vec(int(p.WIDTH*0.85), int(p.HEIGHT*0.9))
        elif (num == 4):
            self.image = pygame.image.load("images/load.png").convert()
            self.image = pygame.transform.scale(self.image, (int(p.WIDTH * 0.05), int(p.HEIGHT * 0.1)))
            self.vec = p.vec(int(p.WIDTH*0.8), int(p.HEIGHT*0.9))

        p.displaysurface.blit(self.image, self.vec)