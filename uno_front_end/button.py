class Button:
    def __init__(self, pygame_object, screen_object, path, x, y):
        self.pygame = pygame_object
        self.screen = screen_object

        self.image = pygame_object.image.load(path)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def scale(self, width, height):
        self.image = self.pygame.transform.scale(self.image, (width, height))
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_clicked(self):
        if self.rect.collidepoint(self.pygame.mouse.get_pos()):
            return True
        return False