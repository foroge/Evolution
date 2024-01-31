import pygame


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w):
        super().__init__()
        self.rect = self.image = self.backcolor = None
        self.color = (128, 128, 128)
        self.pos = (x, y)
        self.width = w
        self.active = False
        self.font = pygame.font.SysFont(None, 50)
        self.text = ""

    def draw(self, screen):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        size = (max(self.width, t_surf.get_width() + 10), t_surf.get_height() + 10)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(center=self.pos)
        screen.blit(self.image, self.rect)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) <= 20:
                    if self.text == "Username":
                        self.text = ""
                    self.text += event.unicode
        if self.text == "" or self.text == "Username":
            self.text = "Username"
            self.color = (128, 128, 128)
        else:
            self.color = (255, 255, 255)

