import pygame

from enum import Enum, auto


class Mixer():
    """Klasse, die für Musik und Soundeffekte zuständig ist"""
    class Sound(Enum):
        SLINGSHOT = auto()
        BUMPER = auto()
        STATIONARY_TARGET = auto()
        COLLISION = auto()
        DROP_TARGET = auto()

    def __init__(self):
        self.soundDict = {
            Mixer.Sound.SLINGSHOT: pygame.mixer.Sound("Assets/Sounds/Slingshot.wav"),
            Mixer.Sound.BUMPER: pygame.mixer.Sound("Assets/Sounds/Bumper.wav"),
            Mixer.Sound.STATIONARY_TARGET: pygame.mixer.Sound("Assets/Sounds/StationaryTarget.wav"),
            Mixer.Sound.DROP_TARGET: pygame.mixer.Sound("Assets/Sounds/DropTarget.wav"),
            Mixer.Sound.COLLISION: pygame.mixer.Sound("Assets/Sounds/Collision.wav")
        }
        self.soundDict[Mixer.Sound.BUMPER].set_volume(0.5)

        pygame.mixer.music.load("Assets/Music/Song.mp3")
        pygame.mixer.music.set_volume(0)
        self.switchMusicVolume()
        pygame.mixer.music.play(-1)

    def switchMusicVolume(self):
        """Setzt Lautstärke der Musik entweder auf 0.7 oder 0"""
        if pygame.mixer.music.get_volume() == 0:
            pygame.mixer.music.set_volume(0.7)
        else:
            pygame.mixer.music.set_volume(0)

    def switchMusicVolume(self):
        if mixer.music.get_volume() == 0:
            mixer.music.set_volume(0.7)
        else:
            mixer.music.set_volume(0)

    def playSound(self, sound:Sound):
        """Spielt Sound bei Kollision ab"""
        if (sound == Mixer.Sound.COLLISION and 
            pygame.mixer.Sound.get_num_channels(self.soundDict[sound]) > 0):
            #nicht mehr als ein Kollisionssound auf einmal
            return
        pygame.mixer.Sound.play(self.soundDict[sound])