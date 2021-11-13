import numpy
import pygame # THIS IS THE ACTUAL FILE ON GITHUB (18/9/2021)
from pygame.locals import *
import sys
import random
from tkinter import filedialog
from tkinter import *
import datetime
import time

# freq, size, channel, buffsize
pygame.mixer.pre_init(44100, 16, 1, 512)
pygame.init()

#main variables
vec = pygame.math.Vector2
HEIGHT = 1000
WIDTH = HEIGHT*2 # 2400
ACC = WIDTH*0.0008 #######################################################################################new#######################################################################################new
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0
hit_cooldown = pygame.USEREVENT + 1
# defining font styles
headingfont = pygame.font.SysFont("Verdana", int(HEIGHT*0.3))
regularfont = pygame.font.SysFont('Corbel', int(HEIGHT*0.2)) # Currently unused
smallerfont = pygame.font.SysFont('Corbel', int(HEIGHT*0.03))
# light shade of the button
color_light = (170,170,170)
color_dark = (100,100,100)
color_white = (255,255,255)

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moribus")


# Moved health bar animations out so all other classes have easy access
health_ani = [pygame.image.load("images/heart0.png"), pygame.image.load("images/heart1.png"),
                      pygame.image.load("images/heart2.png"), pygame.image.load("images/heart3.png"),
                      pygame.image.load("images/heart4.png"), pygame.image.load("images/heart5.png")]


# Music and Sound ################################################################################################################################################################################################################################################

# mmanager.playsound(fsound, 0.3) < copy paste
soundtrack = ["Sounds/background_village.wav", "Sounds/battle_music.wav", "Sounds/gameover.wav"]

# player ability
swordtrack = [pygame.mixer.Sound("Sounds/sword1.wav"), pygame.mixer.Sound("Sounds/sword2.wav")]
fsound = pygame.mixer.Sound("Sounds/fireball_sound.wav") # player fireball

# Items
coinSound = pygame.mixer.Sound("Sounds/enemy_hit.wav") # player item
healthSound = pygame.mixer.Sound("Sounds/enemy_hit.wav") # player item
boostSound = pygame.mixer.Sound("Sounds/enemy_hit.wav") # player item

#Menu
bsound = pygame.mixer.Sound("Sounds/enemy_hit.wav") # button

#Hit/Death
e1DeathSound = pygame.mixer.Sound("Sounds/enemy_hit.wav") # enemy 1 death sound
e2DeathSound = pygame.mixer.Sound("Sounds/enemy_hit.wav") # enemy 2 death sound
e3HitSound = pygame.mixer.Sound("Sounds/enemy_hit.wav") # enemy 3 hit sound (boss 1)
e3DeathSound = pygame.mixer.Sound("Sounds/enemy_hit.wav") # enemy 3 death sound (boss 1)
playerHitSound = pygame.mixer.Sound("Sounds/enemy_hit.wav") # player hit sound
playerDeathSound = pygame.mixer.Sound("Sounds/enemy_hit.wav") # player hit sound

