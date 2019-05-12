class Button:
    def __init__(self, pygame_object, screen_object, path, x, y):
        self.pygame = pygame_object
        self.screen = screen_object

        self.width = 30
        self.height = 30
        self.image = pygame_object.image.load(path)
        self.image = pygame_object.transform.scale(self.image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def check_clicked(self):
        if self.rect.collidepoint(self.pygame.mouse.get_pos()):
            return True
        return False