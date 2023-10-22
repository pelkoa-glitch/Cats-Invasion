import pygame.font
from pygame.sprite import Group
from heart import Heart


class Scoreboard:
    """Класс для вывода игровой информации."""
    def __init__(self, ai_game):
        """Инициализирует атрибуты подсчета очков."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Настройка шрифта для вывода счета.
        self.text_color = (170, 170, 170)
        self.font = pygame.font.SysFont(None, 30)
        # Подготовка исходного изображения.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_hearts()

    def prep_score(self):
        """Преобразует текущий счет в графическое изображение."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        score_str = 'Score: ' + score_str
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, None)

        # Вывод счета в правой верхней части экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 5

    def show_score(self):
        """Выводит текущий счет, рекорд и число оставшихся жизней."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.hearts.draw(self.screen)

    def prep_high_score(self):
        """Преобразует рекордный счет в графическое изображение."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        high_score_str = 'Max score: ' + high_score_str
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, None)

        # Рекорд выравнивается по центру верхней стороны.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Проверяет, появился ли новый рекорд."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Преобразует уровень в графическое изображение."""
        level_str = str(self.stats.level)
        level_str = 'Level: ' + level_str
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, None)

        # Уровень выводится под текущим счетом.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.left - 130
        self.level_rect.top = self.score_rect.top

    def prep_hearts(self):
        """Сообщает количество оставшихся жизней."""
        self.hearts = Group()
        for heart_number in range(self.stats.hearts_left):
            heart = Heart(self.ai_game)

            heart.rect.x = 10 + heart_number * heart.rect.width
            heart.rect.y = 10
            self.hearts.add(heart)
