import parameters as p
import pygame
import EventHandler as e
import runtime_parameters as r
import PButton as pb

class StageDisplay(pygame.sprite.Sprite): #
    def __init__(self):
        super().__init__()
        self.headingFont = pygame.font.SysFont('Verdana', int(p.HEIGHT*0.1))
        self.text = self.headingFont.render("STAGE: " + str(r.handler.stage), True, (157, 3, 252))
        self.rect = self.text.get_rect(center=(p.WIDTH*0.5, p.HEIGHT*0.5))
        self.posx = -100
        self.posy = 100
        self.display = False
        self.clear = False

    def stage_clear(self):
        self.text = p.headingfont.render(" ", True, p.color_dark)
        pb.PButton.imgdisp = 0
        if self.posx < 720:
            self.posx += 10
            p.displaysurface.blit(self.text, self.rect)
        else:
            self.display = False
            self.posx = -100
            self.posy = 100

    def move_display(self):
        # Create the text to be displayed
        self.text = self.headingFont.render("STAGE: " + str(r.handler.stage), True, (157, 3, 252))
        if self.posx < 700:
            self.posx += 5
            p.displaysurface.blit(self.text, (self.posx, self.posy))
        else:
            self.display = False
            self.kill()