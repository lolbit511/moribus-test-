import parameters as p

class Ground(p.pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = p.pygame.image.load("images/Ground.png")
        self.image = p.pygame.transform.scale(self.image, (p.WIDTH,int(p.HEIGHT*0.2)))
        self.rect = self.image.get_rect(center=(int(p.WIDTH/2), int(p.HEIGHT*0.9)))
    def render(self):
        p.displaysurface.blit(self.image, (self.rect.x, self.rect.y))

class Background(p.pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgimage = p.pygame.image.load("images/background.png").convert()
        self.bgimage = p.pygame.transform.scale(self.bgimage, (int(p.WIDTH), int(p.HEIGHT)))
        #self.bgimage = pygame.transform.smoothscale(self.bgimage, (WIDTH, HEIGHT))
        self.bgY = 0
        self.bgX = 0

    def render(self):
        p.displaysurface.blit(self.bgimage, (self.bgX, self.bgY))