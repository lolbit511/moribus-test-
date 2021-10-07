import parameters as p
import pygame
import EventHandler as e
import HealthBar as hb
import runtime_parameters as r

class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.headingFont = pygame.font.SysFont('Verdana', int(p.HEIGHT*0.1))
        self.text = self.headingFont.render(("Game Over"), True, (157, 3, 252))
        self.rect = self.text.get_rect(center=(p.WIDTH*0.5, p.HEIGHT*0.5))
        self.posx = 175
        self.posy = 100
        self.display = False
        self.GameEnded = False
        self.clear = False

    def GO_display(self):
        if hb.healthCount < 1:
            p.displaysurface.blit(self.text, self.rect)
            hb.healthCount = 0
            self.GameEnded = True