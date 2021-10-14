import parameters as p
import pygame
import MusicManager as mm
import runtime_parameters as r
import HealthBar as hb


class Player(p.pygame.sprite.Sprite):
    def __init__(self):

        super().__init__()
        self.start = False
        self.startdone = False

        # Scale
        self.xRatio = int(0.10 * p.WIDTH)
        self.yRatio = int(0.19 * p.HEIGHT)

        self.image = p.pygame.image.load("images/player.png").convert()
        #self.imageorg = self.image
        #cropped = pygame.Surface((80, 80))
        #cropped.blit(self.image, (-80, -80))
        #self.subsurface = pygame.Surface.subsurface(20, 2, 80, 98)
        self.image = p.pygame.transform.scale(self.image, (self.xRatio, self.yRatio))
        self.rect = self.image.get_rect()

        # Position and direction
        self.vx = 0
        self.pos = p.vec((340, 240))
        self.vel = p.vec(0, 0)
        self.acc = p.vec(0, 0)
        self.direction = "RIGHT"
        self.jumping = False
        # Movement
        self.jumping = False
        self.running = False
        self.move_frame = 0
        self.jumpheight = (p.HEIGHT*0.035) * -1
        self.jump_timer = 250
        # Combat
        self.attacking = False
        self.attack_frame = 0
        self.attCD = 100
        self.slash = 0

        self.experience = 0
        self.mana = 0
        self.coin = 0
        self.magic_cooldown = 1

        # Stage
        self.stage = 1
        # Health

        self.cooldown = False



        # ## Attacking Animations
        # self.att_ani_L = [pygame.image.load("player.png"), pygame.image.load("player.png"),
        #              pygame.transform.flip(pygame.image.load("sword_right.png"), True, False),
        #              pygame.transform.flip(pygame.image.load("sword_right.png"), True, False),
        #              pygame.transform.flip(pygame.image.load("sword_right.png"), True, False),
        #              pygame.transform.flip(pygame.image.load("sword_right.png"), True, False),
        #              pygame.image.load("player.png")]
        #
        # self.att_ani_R = [pygame.transform.flip(pygame.image.load("player.png"), True, False),
        #              pygame.transform.flip(pygame.image.load("player.png"), True, False),
        #              pygame.image.load("sword_right.png"), pygame.image.load("sword_right.png"),
        #              pygame.image.load("sword_right.png"), pygame.image.load("sword_right.png"),
        #              pygame.transform.flip(pygame.image.load("player.png"), True, False)]

        # Run animation for the RIGHT
        self.run_ani_R = [pygame.transform.flip(pygame.image.load("images/player.png").convert(), True, False),
                          pygame.transform.flip(pygame.image.load("images/player.png").convert(), True, False),
                          pygame.transform.flip(pygame.image.load("images/player.png").convert(), True, False),
                          pygame.transform.flip(pygame.image.load("images/player.png").convert(), True, False),
                          pygame.transform.flip(pygame.image.load("images/playerWalk1.png").convert(), True, False),
                          pygame.transform.flip(pygame.image.load("images/playerWalk1.png").convert(), True, False),
                          pygame.transform.flip(pygame.image.load("images/playerWalk1.png").convert(), True, False),
                          pygame.transform.flip(pygame.image.load("images/playerWalk1.png").convert(), True, False)]

        self.run_ani_L = [pygame.image.load("images/player.png").convert(), pygame.image.load("images/player.png").convert(),
                     pygame.image.load("images/player.png").convert(), pygame.image.load("images/player.png").convert(),
                     pygame.image.load("images/playerWalk1.png").convert(), pygame.image.load("images/playerWalk1.png").convert(),
                     pygame.image.load("images/playerWalk1.png").convert(), pygame.image.load("images/playerWalk1.png").convert()]

        self.att_ani_R = [pygame.transform.flip(pygame.image.load("images/player.png").convert(), True, False)]
        self.att_ani_R = self.att_ani_R + [pygame.transform.flip(pygame.image.load("images/sword.png").convert(), True, False)] * self.attCD

        self.att_ani_R.append(pygame.image.load("images/player.png").convert())


        #print(self.att_ani_R)
        self.att_ani_L = [pygame.image.load("images/player.png").convert()]
        self.att_ani_L = self.att_ani_L + [pygame.image.load("images/sword.png").convert()] * self.attCD
        self.att_ani_L.append(pygame.transform.flip(pygame.image.load("images/player.png").convert(), True, False))

        #print(self.att_ani_L)


    def player_hit(self, damage = 10): #player
        if r.GO.GameEnded == False:

            #print("entering player hit")
            if self.cooldown == False: #
                mm.mmanager.playsound(p.playerHitSound, 0.3)
                self.cooldown = True  # Enable the cooldown
                pygame.time.set_timer(p.hit_cooldown, 1000)  # Resets cooldown in 1 second

                hb.healthCount = hb.healthCount - damage
                hb.health.image = p.health_ani[int(hb.healthCount/20)]

                if hb.healthCount <= 0:
                    mm.mmanager.playsound(p.playerDeathSound, 0.3)
                    self.kill()
                    mm.mmanager.stop()
                    mm.mmanager.playsoundtrack(p.soundtrack[2], -1, 0.1)
                    pygame.display.update()

    def move(self): #player
        if r.cursor.wait == 1: return
        self.acc = p.vec(0, int(p.HEIGHT*0.003)) # player gravity
        # Will set running to False if the player has slowed down to a certain extent
        if abs(self.vel.x) > 0.3:
            self.running = True
        else:
            self.running = False

        # Returns the current key presses
        pressed_keys = pygame.key.get_pressed()

        # Accelerates the player in the direction of the key press
        if self.attacking == False:

            if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]: #TODO: check if these
                self.acc.x = -p.ACC


            if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
                self.acc.x = p.ACC



        # Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * p.FRIC
        self.vel += self.acc
        for SW in r.Swings:
            SW.rect.x += self.vel.x + 0.5 * self.acc.x
        self.pos += self.vel + 0.5 * self.acc  # Updates Position with new values

        # This causes character warping from one point of the screen to the other
        if self.pos.x > p.WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = p.WIDTH

        self.rect.midbottom = self.pos  # Update rect with new pos


    def attack(self): #player
        if r.cursor.wait == 1: return
        # If attack frame has reached end of sequence, return to base frame
        if self.attack_frame > self.attCD-1:
            self.attack_frame = 0
            self.attacking = False

        print(self.attack_frame)
        if (self.attack_frame+1)%9 == 0:
            mm.mmanager.playsound(p.swordtrack[self.slash], 0.05)
            self.slash += 1
            if self.slash >= 2:
                self.slash = 0

        # Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = self.att_ani_R[self.attack_frame]
        elif self.direction == "LEFT":
            self.image = self.att_ani_L[self.attack_frame]

        # Update the current attack frame
        self.attack_frame += 1
        # Updates position with new values
        if self.direction == 0:
            self.pos.x += self.vel.x
        if self.direction == 1:
            self.pos.x -= self.vel.x

        self.rect.center = self.pos  # Updates rect



    def update(self): #player
        if self.jumpheight == -18:
            self.jump_timer -= 1
        if self.jump_timer < 0:
            self.jumpheight = -13
            self.jump_timer = 250

        if r.cursor.wait == 1: return
        # Move the character to the next frame if conditions are met
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = self.run_ani_R[self.move_frame]
                self.direction = "RIGHT"

            elif self.vel.x < 0:
                self.image = self.run_ani_L[self.move_frame]
                self.direction = "LEFT"

            self.move_frame += 1
            if self.move_frame == 8:  # return to starting animation at loop 8
                self.move_frame = 0


            # Returns to base frame if standing still and incorrect frame is showing
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = self.run_ani_R[self.move_frame]
            elif self.direction == "LEFT":
                self.image = self.run_ani_L[self.move_frame]

                # Checks for collision with the Player
        if r.Enemies != None:
            hits = pygame.sprite.spritecollide(self, r.Enemies, False)

                    # Activates upon either of the two expressions being true
            #if hits and player.attacking == True:
             #   self.kill()
                # print("Enemy killed")

            # If collision has occured and player not attacking, call "hit" function
            if hits and self.attacking == False:
                self.player_hit()



    def jump(self):
        self.rect.x += 1


        # Check to see if payer is in contact with the ground
        hits = pygame.sprite.spritecollide(self, r.ground_group, False)

        self.rect.x -= 1

        # If touching the ground, and not currently jumping, cause the player to jump.
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = self.jumpheight

player = Player()
r.Playergroup.add(player)