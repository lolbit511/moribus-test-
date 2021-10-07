import parameters as p
import pygame
import Stage
import PButton as PB
import Cursor as c
import HealthBar as HB
import Map as m
import EventHandler as e
import StageDisplay as sd
import MenuDisplay as md
import GameOver as go
import StatusBar as sb
import swing as s

attackCD = 1

background = Stage.Background()
ground = Stage.Ground()
ground_group = p.pygame.sprite.Group()
ground_group.add(ground)

Items = p.pygame.sprite.Group()

Pause = PB.PButton()
Home = PB.PButton()
savebutton = PB.PButton()
loadbutton = PB.PButton()

cursor = c.Cursor()
Fireballs = p.pygame.sprite.Group()
Bolts = p.pygame.sprite.Group()
Swings = p.pygame.sprite.Group()

Playergroup = p.pygame.sprite.Group()



#enemy = Enemy()
Enemies = p.pygame.sprite.Group()

#Enemies = []
#Enemies.add(enemy)

Map = m.Map()
handler = e.EventHandler()
stage_display = sd.StageDisplay()
menu_display = md.MenuDisplay()
GO = go.GameOver()

mouse = pygame.mouse.get_pos()

status_bar = sb.StatusBar()