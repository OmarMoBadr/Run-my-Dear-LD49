import pygame, time, math
from collections import defaultdict

class Game():
    def start():
        Time.start()

    def update():
        Time.update()
        Timer.update()
        Animation.update()
        obj.update_all()
    
    def render(surface):
        obj.render_all(surface)

class Time():
    delta_time = float()
    last_time = float()
    dt = float()
    speed = 1

    def start():
        Time.last_time = time.time()

    def update():
        Time.dt = time.time() - Time.last_time
        Time.last_time = time.time()

        Time.delta_time = Time.dt * Time.speed


class obj():
    objects = []
    world_camera = (0, 0)
    tagged = defaultdict(list)
    named = defaultdict(list)
    orderd = defaultdict(lambda: defaultdict(list))

    def __init__(self, name, x, y, w, h, sprite=None, order=0, order_layer=None, tags=[], show=True, collider=False, color=None, camera=True):
        self.name = name
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.components = []
        self.order = order
        self.order_layer = order_layer
        self.tags = tags
        self.sprite = sprite
        self.current_animation = None
        self.show = show
        self.color = color
        self.camera = camera

        obj.objects.append(self)

        obj.orderd[order_layer][order].append(self)

        for tag in self.tags:
            obj.tagged[tag].append(self)

        obj.named[self.name].append(self)

    def check_collison(self,other):
        return self.x < other.x + other.width and self.x + self.width > other.x and self.y < other.y + other.height and self.y + self.height > other.y

    def distance_to(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def direction_to(self, other):
        rads = math.atan2(-(other.y - self.y), other.x - self.x)
        rads %= 2 * math.pi
        return rads

    def draw_self_rect(self, surface):
        if self.on_screen(surface):
            pygame.draw.rect(surface, self.color, pygame.Rect(
                self.x - obj.world_camera[0] - self.width/2, self.y - obj.world_camera[1] - self.height/2, self.width, self.height))

    def update_sprite(self):
        if self.current_animation != None:
            self.sprite = self.current_animation.sprite

    def draw_self(self, surface):
        if self.on_screen(surface):
            self.update_sprite()

            if self.sprite != None:
                surface.blit(
                    self.sprite, (self.x - obj.world_camera[0] - self.width/2, self.y - obj.world_camera[1] - self.height/2))
    
    def change_order(self, order):
        if self.order != order:
            obj.orderd[self.order_layer][self.order].remove(self)
            obj.orderd[self.order_layer][order].append(self)
            self.order = order

    def get_rect(self):
        return pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)

    def on_screen(self, surface):
        w, h = surface.get_size()
        vertically = 0 < self.y - \
            obj.world_camera[1] + self.height/2 and self.y - \
            obj.world_camera[1] - self.height/2 < h
        horizontally = 0 < self.x - \
            obj.world_camera[0] + self.width/2 and self.x - \
            obj.world_camera[0] - self.width/2 < w
        return horizontally and vertically
    
    def world_pos(self):
        return (self.x - obj.world_camera[0],self.y - obj.world_camera[1])

    def get_objects_by_tag(tag):
        return obj.tagged[tag]

    def get_objects_by_tags(tags):
        full_list = []
        for tag in tags:
            for i in obj.tagged[tag]:
                full_list.append(i)

        return full_list

    def get_objects_by_name(name):
        return obj.named[name]

    def kill(self):
        if self not in obj.objects:
            return

        for co in self.components:
            co.kill()

        obj.objects.remove(self)
        for tag in self.tags:
            obj.tagged[tag].remove(self)

        obj.named[self.name].remove(self)

        obj.orderd[self.order_layer][self.order].remove(self)

        del self

    def update(self):
        pass

    def on_drawing(self, surface):
        pass

    def render_all(surface):
        for layer in obj.orderd:
            for order in sorted(obj.orderd[layer]):
                for object in obj.orderd[layer][order]:
                    if object.show == True:
                        if object.color == None:
                            object.draw_self(surface)
                        else:
                            object.draw_self_rect(surface)

        for object in obj.objects:
            object.on_drawing(surface)

    def update_all():
        for object in obj.objects:
            object.update()

class ui():
    def draw_bar(surface, pos, size, border_color, bar_color, progress, vertical = False ,padding=3, border_size=1):
        progress = progress if progress > 0 else 0
        progress = progress if progress < 1 else 1
        
        if vertical:
            inner_size = (size[0] - padding, (size[1] - padding * 2) * progress)
            inner_pos = (pos[0] + padding, pos[1] + size[1] - ((size[1] - padding * 2) * progress) + padding)
        else:
            inner_size = ((size[0] - padding * 2) * progress, size[1] - padding * 2)
            inner_pos = (pos[0] + padding, pos[1] + padding)
        
        pygame.draw.rect(surface, bar_color, (inner_pos, inner_size))
        pygame.draw.rect(surface, border_color, (pos, size), border_size)


    def draw_button(surface, pos, size, text, background_color="white", text_color="black", border_color="black", border_size=1, font=None):
        rect = pygame.Rect(pos, size)

        pygame.draw.rect(surface, background_color, rect)
        pygame.draw.rect(surface, border_color, (pos, size), border_size)

        if isinstance(text, str):
            blit = font.render(text, True, text_color)
            s = blit.get_size()
        elif isinstance(text, pygame.Surface):
            blit = text
            s = blit.get_rect()
            s = (s.w, s.h)

        surface.blit(blit, (pos[0] + rect.w/2 - s[0] /
                    2, pos[1] + rect.h/2 - s[0]/2))

        return rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]


    def draw_panel(surface, pos, size, color="white", border_color="black", border_size=1, padding=2):
        inner_pos = (pos[0] + padding, pos[1] + padding)
        inner_size = ((size[0] - padding * 2), size[1] - padding * 2)

        pygame.draw.rect(surface, color, (inner_pos, inner_size))
        pygame.draw.rect(surface, border_color, (pos, size), border_size)


    def draw_text(surface, text, color, pos, font, shadow=True, shadow_pos=(1,1), shadow_color = "black", anti_alias=True, line_spacing=20):
        lines = text.split("|")
        line_spacing = line_spacing if len(lines) > 1 else 0
        for i, line in enumerate(lines):
            text_surf = font.render(line, anti_alias, color)
            size = text_surf.get_size()
            
            if shadow:
                shadow_surf = font.render(line, anti_alias, shadow_color)
                surface.blit(shadow_surf, (pos[0] - size[0]/2 + shadow_pos[0], pos[1] - len(lines) * line_spacing/2 - size[1]/2 + shadow_pos[1] + i * line_spacing))
            surface.blit(text_surf, (pos[0] - size[0]/2, pos[1] - len(lines) * line_spacing/2 - size[1]/2 + i * line_spacing))


class Timer():
    timers = []

    def __init__(self, duration, func):
        self.duration = duration
        self.time = duration
        self.func = func
        self.reseted_time = 0
        Timer.timers.append(self)

    def update():
        for timer in Timer.timers:
            if timer.reseted_time == 0:
                if timer.time > 0:
                    timer.time -= Time.delta_time
                else:
                    if timer.time != -1:
                        timer.func()
                        timer.time = -1
            else:
                timer.time = timer.reseted_time
                timer.reseted_time = 0

    def reset(self, time=None, func=None):
        self.reseted_time = self.duration if time == None else time
        self.func = self.func if func == None else func

    def kill(self):
        if self not in Timer.timers:
            return
        Timer.timers.remove(self)
        del self


class Animation():
    animations = []

    def __init__(self, frames, fps):
        self.frames = frames
        self.sprite = self.frames[0]
        self.current_frame = 0
        self.fps = fps
        self.time = 0
        Animation.animations.append(self)

    def next_frame(self):
        self.current_frame += 1
        if self.current_frame == len(self.frames):
            self.current_frame = 0

        self.sprite = self.frames[self.current_frame]

    def update():
        for animation in Animation.animations:
            animation.time -= Time.delta_time

            if animation.time <= 0:
                animation.time = 1 / animation.fps
                animation.next_frame()

    def kill(self):
        if self not in Animation.animations:
            return
        Animation.animations.remove(self)
        del self

def get_frames(sprite,w,h):
    frames = []
    cells = int(sprite.get_width() / w)

    for i in range(0,cells):
        frame = sprite.subsurface(pygame.Rect(i * w,0,w,h))
        frames.append(frame)

    return frames