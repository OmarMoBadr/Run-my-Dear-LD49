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

max_speed = 200
left_foot = False

# Load images ------------------
deer_spr = pygame.image.load("sprites/deer.png").convert_alpha()
deer_frames = pygame.image.load("sprites/deer_animation_outlined.png").convert_alpha()
treadmill_spr = pygame.image.load("sprites/treadmill.png").convert_alpha()

deer_obj = deer(500,200,deer_frames)
treadmill_obj = obj("treadmill",500,200,128,128,sprite=treadmill_spr,order=1)

# Functions --------------------
def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

def change_target_speed():
    global target_speed_speed
    target_speed_speed = random.uniform(-10,20) if target_speed < 50 else random.uniform(-20,10)
    speed_timer.reset()

def check_loosing():
    if (abs(target_speed - speed) < 10):
        print("passed")
        losing_timer.reset()
    else:
        print("forward" if speed > target_speed else "backward")
        Time.speed = 0

speed_timer = Timer(0.5,change_target_speed)
losing_timer = Timer(4, check_loosing)

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
    speed -= Time.delta_time * (speed_speed / 3) if speed > 0 else 0

    target_speed += target_speed_speed * Time.delta_time
    target_speed = clamp(target_speed,0,max_speed)

    if left_foot and keys[pygame.K_a]:
        speed += Time.delta_time * speed_speed
        left_foot = False
    if not left_foot and keys[pygame.K_d]:
        speed += Time.delta_time * speed_speed
        left_foot = True

    speed = clamp(speed,0,max_speed)

    # Rendering --------------------
    window.fill("#A2A2A2")

    Game.render(window)

    # ui.draw_bar(window, (50,200),(200,40),"black","green",speed/max_speed)
    # ui.draw_bar(window, (50,250),(200,40),"black","yellow",target_speed/max_speed)

    clock.tick(60)
    pygame.display.update()