import parameters as p
import pygame
import runtime_parameters as r
import Player as pl
import EventHandler as e

class StatusBar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.statusWidth = p.WIDTH * 0.09
        self.surf = pygame.Surface((self.statusWidth, p.HEIGHT*0.21))

        self.rect = self.surf.get_rect(center=(p.WIDTH*0.9, p.HEIGHT*0.9)) #########################################################################################################################################################################################

    def update_draw(self):
        # Create the text to be displayed
        text1 = p.smallerfont.render("STAGE: " + str(r.handler.stage), True, p.color_white)
        text2 = p.smallerfont.render("EXP: " + str(pl.player.experience), True, p.color_white)
        text3 = p.smallerfont.render("MANA: " + str(pl.player.mana), True, p.color_white)
        text4 = p.smallerfont.render("PURSE: " + str(pl.player.coin), True, p.color_white)
        text5 = p.smallerfont.render("FPS: " + str(int(p.FPS_CLOCK.get_fps())), True, p.color_white)

        # Draw the text to the status bar
        p.displaysurface.blit(text1, (p.WIDTH*0.93,p.HEIGHT*0.03))
        p.displaysurface.blit(text2, (p.WIDTH*0.93,p.HEIGHT*0.06))
        p.displaysurface.blit(text3, (p.WIDTH*0.93,p.HEIGHT*0.09))
        p.displaysurface.blit(text4, (p.WIDTH*0.93,p.HEIGHT*0.12))
        p.displaysurface.blit(text5, (p.WIDTH*0.93,p.HEIGHT*0.15))