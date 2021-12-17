import parameters as p
import pygame

healthCount = 100

class HealthBar(p.pygame.sprite.Sprite):
    def __init__(self,xWidth = int(p.WIDTH*0.4), yWidth = int(0.5*(p.WIDTH*0.4))):
        super().__init__()
        self.imageNumber = 5
        self.image = pygame.image.load("images/heart5.png")
        self.image = pygame.transform.scale(self.image, (xWidth, yWidth))
        self.regularFont = pygame.font.SysFont('Verdana', int(p.HEIGHT * 0.05))
        self.text = self.regularFont.render(str(healthCount), True, (255, 255, 255)) #### ❤
        self.rect = self.text.get_rect(center=(p.WIDTH * 0.32, p.HEIGHT * 0.075))

    def render(self,healthNum = healthCount,x = 10 ,y = 10, boss = False):

        print(self.imageNumber)
        self.rect = self.text.get_rect(center=(p.WIDTH * 0.32, p.HEIGHT * 0.075))
        self.text = self.regularFont.render(str(healthNum), True, (255, 255, 255))

        if boss == False:
            self.image = p.health_ani[self.imageNumber]
            self.image = pygame.transform.scale(self.image, (int(p.WIDTH*0.3), int(0.5*(p.WIDTH*0.3))))
            p.displaysurface.blit(self.text, self.rect)
        else:
            self.image = pygame.transform.scale(self.image, (int(p.WIDTH * 0.1), int(0.5 * (p.WIDTH * 0.1))))
            #p.displaysurface.blit(self.text, self.rect)

        p.displaysurface.blit(self.image, (x, y))

health = HealthBar()
