import parameters as p
import pygame
import EventHandler as e

class MenuDisplay:
    def __init__(self):
        super().__init__()
        self.headingFont = pygame.font.SysFont('Verdana', int(p.HEIGHT*0.05))
        self.text = self.headingFont.render("PRESS SPACE TO START", True, (255, 255, 255))
        self.rect = self.text.get_rect(center=(p.WIDTH*0.5, p.HEIGHT*0.5))
        self.posx = 175
        self.posy = 100
        self.display = True
        self.clear = False
    def move_display(self):
        # Create the text to be displayed
        #self.text = self.headingFont.render(self.text, True, (157, 3, 252))
        if self.posx < 700:
            self.posx += 0
            p.displaysurface.blit(self.text, self.rect)
        else:
            self.display = False
            self.kill() # currently working, ignore errord