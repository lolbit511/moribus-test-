import parameters as p
import pygame

class MusicManager:
    def __init__(self):
        super().__init__()
        self.volume = 0.05  # Default Volume

    def playsoundtrack(self, music, num, vol):
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(num)

    def playsound(self, sound, vol):
        sound.set_volume(vol)
        sound.play()

    def stop(self):
        pygame.mixer.music.stop()

mmanager = MusicManager()
mmanager.playsoundtrack(p.soundtrack[0], -1, 0.02) # TODO: last value changes volume
