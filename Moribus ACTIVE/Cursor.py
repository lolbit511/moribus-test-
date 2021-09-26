import parameters as p
import pygame
import runtime_parameters as rp

class Cursor(pygame.sprite.Sprite): ########################################################################################################################################################
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/cursor.png")
        self.image = pygame.transform.scale(self.image, (int(p.WIDTH*0.025),int(p.HEIGHT*0.05)))
        self.rect = self.image.get_rect()
        self.wait = 0

    def pause(self):
        if self.wait == 1:
            self.wait = 0
        else:
            self.wait = 1

    def hover(self):
        if int(p.WIDTH*0.8) <= rp.mouse[0] <= p.WIDTH and int(p.HEIGHT*0.9) <= rp.mouse[1] <= p.HEIGHT:
            pygame.mouse.set_visible(False)
            rp.cursor.rect.center = pygame.mouse.get_pos()  # update position
            p.displaysurface.blit(rp.cursor.image, rp.cursor.rect)
        else:
            pygame.mouse.set_visible(True)