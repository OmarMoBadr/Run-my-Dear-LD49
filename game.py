from engine import *

class deer(obj):
    def __init__(self, x, y, sprite):
        self.frames = get_frames(sprite, 128, 128)
        super().__init__("deer",x, y, 128, 128, self.frames[0])

        self.walking_frames = self.frames[1:4]
        self.walking_animation = Animation(self.walking_frames,10)
        self.current_animation = self.walking_animation