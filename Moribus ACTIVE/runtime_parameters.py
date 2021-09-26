import parameters as p
import pygame
import Player
import Stage
import PButton
import Cursor
import HealthBar

attackCD = 1

background = Stage.Background()
ground = Stage.Ground()
ground_group = p.pygame.sprite.Group()
ground_group.add(ground)

Items = p.pygame.sprite.Group()
Pause = PButton()
Home = PButton()
savebutton = PButton()
loadbutton = PButton()

cursor = Cursor()
Fireballs = p.pygame.sprite.Group()
Bolts = p.pygame.sprite.Group()
Swings = p.pygame.sprite.Group()

player = Player()
Playergroup = p.pygame.sprite.Group()
Playergroup.add(player)

health = HealthBar()

#enemy = Enemy()
Enemies = p.pygame.sprite.Group()

#Enemies = []
#Enemies.add(enemy)

Map = Map()
handler = EventHandler()
stage_display = StageDisplay()
menu_display = MenuDisplay()
GO = GameOver()

mouse = pygame.mouse.get_pos()