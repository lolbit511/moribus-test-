import parameters as p
import pygame
import EventHandler as e
import runtime_parameters as r

class Map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hide = False
        self.image = pygame.image.load("images/Map.png")
        self.image = pygame.transform.scale(self.image, (int(p.WIDTH * 0.2), int(p.HEIGHT * 0.3)))

    def update(self):
        if self.hide == False and r.handler.world == 0:
            self.image = pygame.image.load("images/Map.png")
            self.image = pygame.transform.scale(self.image, (int(p.WIDTH * 0.2), int(p.HEIGHT * 0.3)))
            p.displaysurface.blit(self.image, (int(p.WIDTH * 0.4), int(p.HEIGHT * 0.53))) #0.83