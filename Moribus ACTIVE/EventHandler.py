import parameters as p
import pygame
import runtime_parameters as r
import Player as pl
import MusicManager as mm

volume = 0.02

class EventHandler():
    def __init__(self):
        self.world = 0
        self.next_level_started = False
        self.stage = 1
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.battle = False
        self.enemy_generation = pygame.USEREVENT + 1
        self.enemy_generation2 = pygame.USEREVENT + 2
        self.enemy_generation3 = pygame.USEREVENT + 3
        self.stage_enemies = []
        #self.stage_enemies.append(0)

        self.phase = 21
        for x in range(1, self.phase):
            self.stage_enemies.append(x) #formula for enemy generation
        print(self.stage_enemies)

    def next_stage(self):  # Code for when the next stage is clicked

        self.stage += 1
        self.enemy_count = 0
        self.dead_enemy_count = 0
        #print("Stage: " + str(self.stage))
        if self.world == 1:
            pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage))
        elif self.world == 2:
            pygame.time.set_timer(self.enemy_generation2, 1500 - (50 * self.stage))
        elif self.world == 2:
            pygame.time.set_timer(self.enemy_generation3, 1500 - (50 * self.stage))

    def update(self): #Event Handler
        #print("a:" , self.dead_enemy_count)
        #print("b:" , self.stage_enemies[self.stage - 1])
        if self.dead_enemy_count == self.stage_enemies[self.stage]:
            self.dead_enemy_count = 0
            r.stage_display.clear = True  #TODO: unsure
            r.stage_display.stage_clear()
            print("stageClear ACTIVE")

    def home(self):
        # Reset Battle code
        pygame.time.set_timer(self.enemy_generation, 0)
        pygame.time.set_timer(self.enemy_generation2, 0)
        pygame.time.set_timer(self.enemy_generation3, 0)

        self.battle = False
        self.enemy_count = 0
        self.dead_enemy_count = 0
        self.stage = 1
        self.world = 0

        # Destroy any enemies or items lying around
        for group in r.Enemies, r.Items:
            for entity in group:
                entity.kill()

        # Bring back normal backgrounds
        r.Map.hide = False
        r.background.bgimage = pygame.image.load("images/Background.png").convert()
        r.background.bgimage = pygame.transform.scale(r.background.bgimage, (p.WIDTH, p.HEIGHT))
        r.ground.image = pygame.image.load("images/Ground.png")

        r.ground.image = pygame.transform.scale(r.ground.image, (p.WIDTH, int(p.HEIGHT * 0.2)))
        r.ground.rect = r.ground.image.get_rect(center=(int(p.WIDTH / 2), int(p.HEIGHT * 0.9)))

    def saveG(self):
        f = open("guru99.txt", "w")
        # f=open("guru99.txt","a+")
        #for i in range(10):

        # everything that needs to be saved
        f.write(str(r.handler.stage) + "\n")
        f.write(str(pl.player.experience) + "\n")
        f.write(str(pl.player.mana) + "\n")
        f.write(str(pl.player.coin) + "\n")
        f.write(str(pl.player.health) +"\n")

        f.close()


    def loadG(self):
        #Open the file back and read the contents
        f=open("guru99.txt", "r")
        if f.mode == 'r':
            r.handler.stage = int(f.readline())
            pl.player.experience = int(f.readline())
            pl.player.mana = int(f.readline())
            pl.player.coin = int(f.readline())
            pl.player.health = int(f.readline())

        #or, readlines reads the individual line into a list
        #fl = f.readlines()
        #for x in fl:

            #print(x)



    def stage_handler(self):
        # Code for the Tkinter stage selection window
        self.root = p.Tk()
        self.root.geometry('295x270')
        width = 30
        button1 = p.Button(self.root, text="[Dungeon] Twilight Plains", width=width, height=2,
                         command=self.world1)
        button2 = p.Button(self.root, text="[Dungeon] Sabreclaw Wastelands", width=width, height=2,
                         command=self.world2)
        button3 = p.Button(self.root, text="[Town] Tarnstead Outlook", width=width, height=2,
                         command=self.world3)
        button4 = p.Button(self.root, text="[Dungeon] Iceborne Crypts", width=width, height=2,
                         command=self.world4)
        button5 = p.Button(self.root, text="[Dungeon] Mount Moru", width=width, height=2,
                         command=self.world5)

        button1.place(x=40, y=15)
        button2.place(x=40, y=65)
        button3.place(x=40, y=115)
        button4.place(x=40, y=165)
        button5.place(x=40, y=215)

        self.root.mainloop()

    def world1(self):
        self.root.destroy()
        self.world = 1
        pygame.time.set_timer(self.enemy_generation, 2000)
        # ground.image = pygame.image.load("images/Ground.png")
        r.ground.image = pygame.transform.scale(r.ground.image, (p.WIDTH, int(p.HEIGHT * 0.2)))
        r.ground.rect = r.ground.image.get_rect(center=(int(p.WIDTH / 2), int(p.HEIGHT * 0.9)))
        mm.mmanager.playsoundtrack(p.soundtrack[1], -1, volume)

        r.Map.hide = True
        self.battle = True
        #mmanager.playsoundtrack(soundtrack[0], -1, 0.05)

    def world2(self):
        self.root.destroy()
        r.background.bgimage = pygame.image.load("images/wasteland.png").convert()
        #ground.image = pygame.image.load("images/Ground.png")
        r.ground.image = pygame.transform.scale(r.ground.image, (p.WIDTH, int(p.HEIGHT * 0.2)))
        r.ground.rect = r.ground.image.get_rect(center=(int(p.WIDTH / 2), int(p.HEIGHT * 0.9)))
        mm.mmanager.playsoundtrack(p.soundtrack[1], -1, volume)

        pygame.time.set_timer(self.enemy_generation2, 2500)

        self.world = 2

        r.Map.hide = True
        self.battle = True
        #mmanager.playsoundtrack(soundtrack[1], -1, volume)

    def world3(self):

        self.world = 3
        self.battle = True
        # Empty for now

    def world4(self):

        self.battle = True
        # Empty for now

    def world5(self):

        self.battle = True
        # Empty for now


def gravity_check(self):
    hits = pygame.sprite.spritecollide(pl.player, r.ground_group, False)
    if self.vel.y > 0:
        if hits:
            lowest = hits[0]
            if self.pos.y < lowest.rect.bottom:
                self.pos.y = lowest.rect.top + int(p.HEIGHT * 0.045)
                self.vel.y = 0
                self.jumping = False