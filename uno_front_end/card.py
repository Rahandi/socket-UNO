import os
import time

class Cards:
    def __init__(self, pygame_object, screen_object):
        self.pygame = pygame_object
        self.screen = screen_object
        self.cards = {}

    def __getitem__(self, key):
        return self.cards[key]

    def load(self, path):
        for f in os.listdir(path):
            if f not in ['card_back.png', 'card_back_alt.png']:
                name = f.replace('.png', '')
                name = name.split('_')
                temp = name[0]
                name[0] = name[1]
                name[1] = temp
                name = '_'.join(name)
                self.cards[name] = Card(self.pygame, self.screen, os.path.join(path, f))
                self.cards[name].name = name

class Card:
    def __init__(self, pygame_object, screen_object, image_path):
        self.pygame = pygame_object
        self.screen = screen_object
        self.width = 60
        self.height = 90
        self.image = pygame_object.image.load(image_path)
        self.image = pygame_object.transform.scale(self.image, (self.width, self.height))
        self.position_x = 0
        self.position_y = 0
        self.front = False
        self.status = 0
        self.status_time = 0
        self.disable = False
        self.name = None

    def place(self, x, y):
        self.position_x = x
        self.position_y = y
        self.screen.blit(self.image, (self.position_x, self.position_y))

    def scale(self, times):
        self.image = self.pygame.transform.scale(self.image, (int(self.width*times), int(self.height*times)))

    def check_clicked(self):
        mouse_x = self.pygame.mouse.get_pos()[0]
        mouse_y = self.pygame.mouse.get_pos()[1]

        if self.front:
            if mouse_x >= self.position_x and mouse_x <= (self.position_x+self.width):
                if mouse_y >= self.position_y and mouse_y <= (self.position_y+self.height):
                    if self.status == 0:
                        self.status = 1
                        self.status_time = time.time()
                    elif self.status == 1:
                        self.status = 0
        else:
            if mouse_x >= self.position_x and mouse_x <= (self.position_x+24):
                if mouse_y >= self.position_y and mouse_y <= (self.position_y+self.height):
                    if self.status == 0:
                        self.status = 1
                        self.status_time = time.time()
                    elif self.status == 1:
                        self.status = 0