import pygame


class Settings:
    """Класс для хранения настроек игры."""

    def __init__(self):
        """Инициализирует статичесике настройки игры."""
        # Параметры эрана.
        self.screen_width = 1024
        self.screen_height = 768
        self.bg_color = (88, 23, 117)
        self.background_image = pygame.image.load('images/background.bmp')
        self.fps = 60

        # Параметры корабля.
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Параметры снаряда.
        self.bullet_speed = 0.1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 255)
        self.bullets_allowed = 3

        # Настройки пришельцев.
        self.fleet_drop_speed = 10

        # Темп ускорения игры.
        self.speedup_scale = 1.1
        # Темп роста стоимости пришельцев
        self.score_scale = 1.5

        # Изображения кнопки
        self.play_button_up = pygame.image.load('images/play_button_up.bmp')
        self.play_button_down = pygame.image.load('images/play_button_down.bmp')

        # Изображения пришельцев
        self.alien_images = [pygame.image.load('images/catalien1.bmp'),
                             pygame.image.load('images/catalien2.bmp'),
                             pygame.image.load('images/catalien4.bmp'),
                             pygame.image.load('images/catalien3.bmp'),
                             ]

        # Запуск инициализации динамических настроек
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.ship_speed_factor = 10
        self.bullet_speed_factor = 10
        self.alien_speed_factor = 1

        # fleet_direction = 1 обозначает движение вправо, а -1 - влево.
        self.fleet_direction = 1
        # Подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        """Увеличение настройки скорости и стоимости пришельцев."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)