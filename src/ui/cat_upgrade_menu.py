import pygame
from src.extra_utils import Button


class UpgradeMenu:
    def __init__(self, x, y, cat_obj, cat_images):
        self.cat_images = cat_images
        self.x = x
        self.y = y
        self.cat_obj = cat_obj
        self.image = pygame.Surface((300, 300))
        self.image.fill((73, 71, 69))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.cat_image = self.CatImage(self)
        self.text = self.TextCharacteristics(self)

        self.buttons = {
            "upgrade": Button(x + 100, y + 25, 80, 40, "Upgrade", "white"),
            "destroy": Button(x + 200, y + 25, 80, 40, "Destroy", "red"),
        }

    class CatImage:
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            self.image = self.outer_instance.cat_images[self.outer_instance.cat_obj.cat_type]
            self.image = pygame.transform.scale(self.image, (80, 80))
            self.rect = self.image.get_rect(topleft=(self.outer_instance.x + 5, self.outer_instance.y + 5))

        def draw(self, screen):
            screen.blit(self.image, self.rect)

    class TextCharacteristics:
        def __init__(self, outer_instance):
            self.outer_instance = outer_instance
            self.font = pygame.font.Font(None, 28)
            self.money = 0

            self.text = self.get_characteristics(self.money)

        def get_characteristics(self, money):
            self.money = money
            name_obj = type(self.outer_instance.cat_obj).__name__
            cat = self.outer_instance.cat_obj
            text = [self.outer_instance.cat_obj.cat_type.replace("_", " ")]
            if name_obj in ["Wizard", "Electronic"]:
                text.append(f"Damage: {cat.damage}")
                text.append(f"Firing rate: {cat.cooldown}")
                text.append(f"Radius: {round(cat.base_radius / 32, 2)}")
            elif name_obj == "SunFlower":
                text.append(f"Income: {cat.coins_get}")
                text.append(f"Cooldown: {cat.time_sleep}")
            text.append(f"Upgrade cost: {cat.upgrade_cost}")
            return text

        def draw(self, screen):
            text_coord = self.outer_instance.y + 90
            for idx, line in enumerate(self.text):
                if idx != len(self.text) - 1:
                    string_rendered = self.font.render(line, True, "white")
                else:
                    string_rendered = self.font.render(line, True, "green" if self.money >=
                                                       self.outer_instance.cat_obj.upgrade_cost else "red")
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = self.outer_instance.x + 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.cat_image.draw(screen)
        self.text.draw(screen)
        for i in self.buttons.values():
            i.draw(screen)

    def update(self, money):
        upd = []
        self.text.text = self.text.get_characteristics(money)
        for i in self.buttons.values():
            upd.append(i.update())
        return upd
