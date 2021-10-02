import pygame, time

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

class ui():
    def draw_bar(surface, pos, size, border_color, bar_color, progress, padding=3, border_size=1):
        progress = progress if progress > 0 else 0

        inner_pos = (pos[0] + padding, pos[1] + padding)
        inner_size = ((size[0] - padding * 2) * progress, size[1] - padding * 2)
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


    def draw_text(surface, text, color, pos, font):
        text = font.render(text, False, color)
        size = text.get_size()
        surface.blit(text, (pos[0] - size[0]/2, pos[1] - size[1]/2))


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