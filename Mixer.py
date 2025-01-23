import pygame
import pygame.mixer as mixer

from enum import Enum, auto


class Mixer():
    class Sound(Enum):
        SLINGSHOT = auto()
        BUMPER = auto()
        STATIONARY_TARGET = auto()
        COLLISION = auto()
        DROP_TARGET = auto()

    def __init__(self):
        self.soundDict = {
            Mixer.Sound.SLINGSHOT: mixer.Sound("Assets/Sounds/Slingshot.wav"),
            Mixer.Sound.BUMPER: mixer.Sound("Assets/Sounds/Bumper.wav"),
            Mixer.Sound.STATIONARY_TARGET: mixer.Sound("Assets/Sounds/StationaryTarget.wav"),
            Mixer.Sound.DROP_TARGET: mixer.Sound("Assets/Sounds/DropTarget.wav"),
            Mixer.Sound.COLLISION: mixer.Sound("Assets/Sounds/Collision.wav")
        }
        self.soundDict[Mixer.Sound.BUMPER].set_volume(0.5)

    def playSound(self, sound:Sound):
        if (sound == Mixer.Sound.COLLISION) and (mixer.Sound.get_num_channels(self.soundDict[sound]) > 0):
            return
        mixer.Sound.play(self.soundDict[sound])