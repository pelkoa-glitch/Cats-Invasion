from settings import Settings


class Button:

    def __init__(self, ai_game):
        """Инициализирует атрибуты кнопки."""
        self.settings = Settings()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.play_button_up = self.settings.play_button_up
        self.play_button_down = self.settings.play_button_down
        self.rect = self.play_button_up.get_rect()
        self.rect2 = self.play_button_down.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect2.center = self.screen_rect.center

    def draw_button_up(self):
        """Отображение не нажатой кнопки."""
        self.screen.blit(self.play_button_up, self.rect)

    def draw_button_down(self):
        """Отображение нажатой кнопки."""
        self.screen.blit(self.play_button_down, self.rect2)
