import pygame
from pygame.sprite import Sprite


class Heart(Sprite):
    """Класс, представляющий одно сердце."""
    def __init__(self, ai_game):
        """Инициализирует корабль и задает его начальную позицию."""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Загружает изображение корабля, и получает прямоугольник.
        self.image = pygame.image.load('images/heart.bmp')
        self.rect = self.image.get_rect()
