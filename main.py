import pygame, random
from engine import *
from game import *

pygame.init()

WINDOW_SIZE = (1280, 720)
window = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
pygame.display.set_caption("Run my Dear (LD49)")

# Variables ---------------------
speed_speed = 30
speed = 0
target_speed = 10
target_speed_speed = 0

difficulty = 1

max_speed = 100
left_foot = False

# Classes ----------------------
class deer(obj):
    def __init__(self, x, y, sprite):
        self.frames = get_frames(sprite, 512, 512)
        super().__init__("deer",x, y, 512, 512, self.frames[0])

        self.walking_frames = self.frames[1:4]
        self.walking_animation = Animation(self.walking_frames,10)
        self.current_animation = self.walking_animation

    def update(self):
        self.x += (speed - target_speed) * Time.delta_time * difficulty

        if self.current_animation != None:
            self.current_animation.fps = (speed +25 )/5 if speed > 0 else 5
        
        if self.x > 850:
            self.x += Time.delta_time * 1500
            self.current_animation = None
            self.sprite = self.frames[4]
        if self.x < 550:
            self.x -= Time.delta_time * 1500
            self.current_animation = None

# Load images ------------------
deer_spr = pygame.image.load("sprites/deer.png").convert_alpha()
deer_frames = pygame.image.load("sprites/deer_animation_outlined.png").convert_alpha()
treadmill_spr = pygame.image.load("sprites/treadmill_animated.png").convert_alpha()
room_spr = pygame.image.load("sprites/room.png").convert()

deer_obj = deer(640, 380,pygame.transform.scale(deer_frames,((512)*5,512)))

treadmill_frames = get_frames(pygame.transform.scale(treadmill_spr,(600*7,400)),600,400)
treadmill_obj = obj("treadmill",650,435,600,400,sprite=treadmill_frames[0],order=1)
treadmill_obj.current_animation = Animation(treadmill_frames,3)

# Functions --------------------
def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

def change_target_speed():
    global target_speed_speed
    target_speed_speed = random.uniform(-30,50) if target_speed < 100 else random.uniform(-50,30)
    speed_timer.reset()

speed_timer = Timer(0.5,change_target_speed)

Game.start()
running = True
while running:
    # Events -----------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            

    keys = pygame.key.get_pressed()
    mouse_buttons = pygame.mouse.get_pressed()

    # Update -----------------------
    Game.update()

    # Game -------------------------
    difficulty += Time.delta_time /10

    speed -= Time.delta_time * (speed_speed / 2) if speed > 0 else 0

    target_speed += target_speed_speed * Time.delta_time
    target_speed = clamp(target_speed,0,max_speed)

    if left_foot and keys[pygame.K_a]:
        speed += Time.delta_time * speed_speed
        left_foot = False
    if not left_foot and keys[pygame.K_d]:
        speed += Time.delta_time * speed_speed
        left_foot = True

    speed = clamp(speed,0,max_speed)
    treadmill_obj.current_animation.fps = (target_speed) if target_speed > 0 else 5

    # Rendering --------------------
    window.fill((0,0,0))
    # window.fill("#A2A2A2")
    window.blit(room_spr,(0,0))

    Game.render(window)

    ui.draw_bar(window, (50,200),(200,40),"black","green",speed/max_speed)
    ui.draw_bar(window, (50,250),(200,40),"black","yellow",target_speed/max_speed)

    clock.tick(60)
    pygame.display.update()