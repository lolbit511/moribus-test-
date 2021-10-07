import parameters as p
import pygame

healthCount = 100

class HealthBar(p.pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/heart5.png")
        self.image = pygame.transform.scale(self.image, (int(p.WIDTH*0.5), int(0.5*(p.WIDTH*0.5))))
        self.regularFont = pygame.font.SysFont('Verdana', int(p.HEIGHT * 0.05))
        self.text = self.regularFont.render(str(healthCount), True, (255, 255, 255)) #### ❤
        self.rect = self.text.get_rect(center=(p.WIDTH * 0.38, p.HEIGHT * 0.075))

    def render(self):
        self.text = self.regularFont.render(str(healthCount), True, (255, 255, 255))
        p.displaysurface.blit(self.image, (10, 10))
        p.displaysurface.blit(self.text, self.rect)

health = HealthBar()
