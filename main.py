import pygame, random
from engine import *

pygame.init()

WINDOW_SIZE = (1280, 720)
window = pygame.display.set_mode(WINDOW_SIZE)

pixel = pygame.font.Font("joystix monospace.ttf", 30)
font = pygame.font.Font("Thunderman.ttf", 40)
small = pygame.font.Font("Thunderman.ttf", 20)
clock = pygame.time.Clock()

pygame.display.set_caption("Run my Dear (LD49)")

icon = pygame.transform.scale(pygame.image.load("sprites/deer.png").convert_alpha(),(64,64))
pygame.display.set_icon(icon)

# Variables ---------------------
speed_speed = 60
speed = 0
target_speed = 10
target_speed_speed = 0

difficulty = 1
score = 0
high_score = 0

instructions = True
mel = False

started = False
stage = 0

max_speed = 100

keys = []

clouds = []
cloud_timer = None

quotes = ["Keep Moving Forward","Move in silence|only speak when the time|comes to say checkmate","You can't get much done in life|if you only work on days|when you feel good","You should always waste time|when you don't have any.|Time is not the boss of you.|Rule 408.","If you walk the Footsteps|of a Stranger You will learn|things you neve knew.","Vision is the art|of seeing what is|invisible to others","Practice like you've never won|Perform like you've never lost","Once Upon|all of Space and Time|there was a|Blue Box"]
quote = ""

# Classes ----------------------
class deer(obj):
    def __init__(self, x, y, sprite):
        self.frames = get_frames(sprite, 512, 512)
        self.walking_frames = self.frames[1:4]
        self.walking_animation = Animation(self.walking_frames,10)
        
        self.small = pygame.transform.scale(self.frames[-1],(128,128))
        super().__init__("deer",x, y, 512, 512, self.frames[0])

        self.finished = False
        self.direction = -1
        self.s = False

    def update(self):
        global stage, started

        if stage == 0:
            self.x += (speed - target_speed) * Time.delta_time * difficulty

            if self.current_animation != None:
                self.current_animation.fps = (speed +25 )/5 if speed > 0 else 5
            
            if self.x > 850:
                self.direction = 1
            elif self.x < 550:
                self.direction = -1
            
            if self.x > 850 or self.x < 550:
                self.x += (Time.delta_time * 1500) * self.direction
                self.current_animation = None
                self.sprite = self.frames[4]
                if not self.s:
                    jump_snd.play()
                    self.s = True

            started = (self.x < 1280 + self.width /2) and (self.x > -self.width /2)
            
            if self.x > 1280 + self.width /2:
                self.s = True
                change_stage(1)
            elif (self.x < -self.width /2):
                self.s = True
                change_stage(2)

        elif stage == 1 or stage == 2:
            if ((self.x < 100) or (self.x > 1100)) and not self.finished:
                self.x += Time.delta_time * 600 * (1 if stage == 1 else -1) 
            else:
                self.finished = True
                self.x -= Time.delta_time * 300 if keys[pygame.K_a] else 0
                self.x += Time.delta_time * 300 if keys[pygame.K_d] else 0
                
                self.x = clamp(self.x,-self.width/2,800) if stage == 1 else clamp(self.x,300,1280+self.width/2)

                self.y -= Time.delta_time * 300 if keys[pygame.K_w] else 0
                self.y += Time.delta_time * 300 if keys[pygame.K_s] else 0
                self.y = clamp(self.y,0,720)
            

# Load sound -------------------
hit_snd = pygame.mixer.Sound('sound/hit.wav')
ss_snd = pygame.mixer.Sound('sound/ss.wav')
walk_snd = pygame.mixer.Sound('sound/walk.wav')
jump_snd = pygame.mixer.Sound('sound/jump.wav')

jump_snd.set_volume(0.2)
pygame.mixer.music.load('sound/music.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0)


# Load images ------------------
me = pygame.image.load("sprites/me.png").convert()
inst = pygame.transform.scale(pygame.image.load("sprites/instructions.png").convert(),(1280,720))
deer_spr = pygame.image.load("sprites/deer.png").convert_alpha()
deer_frames = pygame.image.load("sprites/deer_animation_outlined.png").convert_alpha()
clouds_spr = pygame.image.load("sprites/clouds.png").convert_alpha()
clouds_night_spr = pygame.image.load("sprites/clouds_night.png").convert_alpha()
treadmill_spr = pygame.image.load("sprites/treadmill_animated.png").convert_alpha()
room_spr = pygame.image.load("sprites/room.png").convert()

deer_obj = deer(640, 400,pygame.transform.scale(deer_frames,((512)*5,512)))

cloud_frames = get_frames(clouds_spr,128,96)
cloud_night_frames = get_frames(clouds_night_spr,128,96)

treadmill_frames = get_frames(pygame.transform.scale(treadmill_spr,(600*7,400)),600,400)
treadmill_obj = obj("treadmill",650,460,600,400,sprite=treadmill_frames[0],order=1)
treadmill_obj.current_animation = Animation(treadmill_frames,3)

# Functions --------------------
def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

def change_target_speed():
    global target_speed_speed
    if started:
        target_speed_speed = random.uniform(-30,50) if target_speed < 50 else random.uniform(-50,30)
    speed_timer.reset()

speed_timer = Timer(0.5,change_target_speed)

def make_cloud():
    clouds.append((obj("cloud",1500,random.randrange(0,720),100,90,random.choice(cloud_frames)),random.randrange(300,int(800 + difficulty * 100))))
    cloud_timer.reset(time=2/difficulty)

def make_cloud2():
    clouds.append((obj("cloud",-100,random.randrange(0,720),100,90,random.choice(cloud_night_frames)),random.randrange(300,int(800 + difficulty * 100))))
    cloud_timer.reset(time=2/difficulty)

def new_quote():
    global quote

    quote = random.choice(quotes)

def change_stage(index):
    global started, stage, score, speed, target_speed,difficulty, cloud_timer, quote

    if index == 0:
        treadmill_obj.show = True
        deer_obj.sprite = deer_obj.frames[0]
        deer_obj.x, deer_obj.y = 640, 400
        deer_obj.width = deer_obj.height = 512
        deer_obj.state =  deer_obj.finished  = speed = target_speed = 0

        for c in clouds:
            c[0].kill()

        clouds.clear()
        difficulty = 1

    if stage != index:
        if index == 1 or index == 2:
            treadmill_obj.show = False
            started = False
            deer_obj.sprite = deer_obj.small if index == 1 else pygame.transform.flip(deer_obj.small,True,False)
            deer_obj.width = deer_obj.height = 128
        
        if index == 1: 
            deer_obj.x = -300
            cloud_timer = Timer(0.2,make_cloud)
        
        if index == 2:
            deer_obj.x = 1280+300
            cloud_timer = Timer(0.2,make_cloud2)
            

        stage = index

def main():
    global difficulty, speed, started, target_speed, keys, score, high_score, instructions, mel

    # left_foot = False
    
    running = True
    while running:
        # Events -----------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                

        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        if keys[pygame.K_m]:
            pygame.mixer.music.stop()


        # Update -----------------------
        if not mel:
            Time.update()
            Timer.update()
        if stage == 0:
            if started:
                Game.update()

                difficulty += Time.delta_time /10
                score += Time.delta_time * difficulty

                speed -= Time.delta_time * (speed_speed / 4) if speed > 0 else 0

                target_speed += target_speed_speed * Time.delta_time
                target_speed = clamp(target_speed,0,max_speed)

                if keys[pygame.K_SPACE]:
                    walk_snd.play(loops=-1)
                    speed += Time.delta_time * speed_speed
                else:
                    walk_snd.stop()

                # if left_foot and keys[pygame.K_a]:
                #     speed += Time.delta_time * speed_speed
                #     left_foot = False
                # if not left_foot and keys[pygame.K_d]:
                #     speed += Time.delta_time * speed_speed
                #     left_foot = True

                speed = clamp(speed,0,max_speed)
                treadmill_obj.current_animation.fps = (target_speed)*2 if target_speed > 0 else 5
            else:
                if keys[pygame.K_SPACE]:
                    if mel:
                        if instructions:
                            instructions = False
                        else:
                            Game.start()
                            change_stage(0)
                            ss_snd.play()
                            score = 0
                            deer_obj.current_animation = deer_obj.walking_animation
                            started = True

        if stage == 1:
            Game.update()

            difficulty += Time.delta_time /10
            score += Time.delta_time * difficulty

            for c in clouds:
                c[0].x -= Time.delta_time * c[1]

                if random.random() < 0.001:
                    c[0].y = random.randrange(0,720)

                if deer_obj.check_collison(c[0]):
                    if deer_obj.distance_to(c[0]) < 50:
                        new_quote()
                        hit_snd.play()
                        change_stage(0)
                
                if c[0].x < -c[0].width /2 -20:
                    c[0].kill()
                    clouds.remove(c)
        
        if stage == 2:
            Game.update()

            difficulty += Time.delta_time /10
            score += Time.delta_time * difficulty

            for c in clouds:
                c[0].x += Time.delta_time * c[1]

                if random.random() < 0.001:
                    c[0].y = random.randrange(0,720)

                if deer_obj.check_collison(c[0]):
                    if deer_obj.distance_to(c[0]) < 50:
                        new_quote()
                        hit_snd.play()
                        change_stage(0)
                
                if c[0].x > 1280 + c[0].width /2 + 20:
                    c[0].kill()
                    clouds.remove(c)

        # Rendering --------------------
        if stage == 0:
            window.fill((0,0,0))
            window.blit(room_spr,(0,0))
        elif stage == 1:
            window.fill("#3DB2FF")
        elif stage == 2:
            window.fill("#001E6C")


        Game.render(window)

        if stage == 0:
            ui.draw_text(window, quote,"black",(236,154),small,shadow=False)
            if started:
                ui.draw_bar(window, (1100,300),(40,250),"black","#CC9B6D",speed/max_speed,vertical=True,padding=0,border_size=6)
                ui.draw_bar(window, (1150,300),(40,250),"black","#FFC169",target_speed/max_speed,vertical=True,padding=0,border_size=6)
            elif score > 0 :
                ui.draw_text(window,str("Your score is " + str(int(score))),"white", (640,100),font, shadow_color="#A08445")
                if score >= high_score:
                    ui.draw_text(window,"New high score","white", (640,50),font, shadow_color="black")
                    high_score = score
            
            if not started:
                ui.draw_text(window,"Press space to play","white", (640,400),font, shadow_color="#40351B")


        if not (stage == 0 and not started):
            ui.draw_text(window,str("Score : " + str(int(score))),"white", (1100,50),pixel, shadow=False)
        
        if instructions:
            window.blit(inst,(0,0))
        
        if not mel:
            window.blit(me,(0,0))

        clock.tick(60)
        pygame.display.update()

def intro():
    global mel
    mel = True

Game.start()
Timer(3,intro)
new_quote()
main()