import time

import pygame


# static function to get if left mouse button is pressed
def get_mouse_clicked():
    return pygame.mouse.get_pressed()[0]


class Window:
    SIM_FPS = 60  # simulator runs at 60 fps
    FPSTicker = pygame.time.Clock()  # create pygame fps clock

    def __init__(self, window_title):

        # set up pygame window rendering
        pygame.init()
        self.draw_surface = pygame.display.set_mode((1920, 900))
        self.draw_surface.fill((255, 255, 255))

        self.title = window_title
        self.draw_callback = None
        self.click_callback = None
        self.event_handling_callback = None
        self.button_click_callback = None
        self.quit_callback = None
        self.update_callback = None
        self.prev_time = time.time()
        self.background_color = (255, 255, 255)

        pygame.display.set_caption(window_title)

        # buttons
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def set_rendering_callback(self, function):
        self.draw_callback = function

    def set_mouse_button_click_callback(self, function):
        self.click_callback = function

    def set_event_handling_callback(self, function):
        self.event_handling_callback = function

    def set_button_click_callback(self, function):
        self.button_click_callback = function

    def set_quit_callback(self, function):
        self.quit_callback = function

    def set_update_callback(self, function):
        self.update_callback = function

    def draw_buttons(self):

        # draw buttons if they are visible. appropriate co-ordinates set by states
        for button in self.buttons:
            if button.is_visible:
                button.draw(self.draw_surface)

    def draw_title(self):
        txt_surface = pygame.font.Font(None, 25).render(self.title, True, (0, 0, 0))
        self.draw_surface.blit(txt_surface, (640, 10))

    def set_background_color(self, color):
        self.background_color = color

    def quit(self):
        if self.quit_callback:
            self.quit_callback()
        pygame.quit()
        exit(0)

    def draw(self):
        self.draw_surface.fill(self.background_color)
        self.draw_title()
        self.draw_buttons()

        self.draw_callback(self.draw_surface)

    def run(self):

        while True:
            curr_time = time.time()
            if self.update_callback:
                self.update_callback(curr_time - self.prev_time)
                self.prev_time = curr_time

            for event in pygame.event.get():  # pass on events to the active state
                if self.event_handling_callback:
                    self.event_handling_callback(event)

                for button in self.buttons:  # pass on clicked buttons to the active state
                    if button.clicked(event) and event.type == pygame.MOUSEBUTTONUP:
                        if self.button_click_callback:
                            self.button_click_callback(button.ident)

                if event.type == pygame.QUIT:
                    self.quit()

            if get_mouse_clicked() and self.click_callback:
                self.click_callback()

            self.draw()

            pygame.display.update()  # update the display and delay if necessary for locked FPS
            self.FPSTicker.tick(self.SIM_FPS)
