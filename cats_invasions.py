import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from cat import Cat


class CatsInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализрует игру и создат игровые ресурсы."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Cat's Invasion")
        self.clock = pygame.time.Clock()
        # Создание экземпляра для хранения игровой статистики.
        # И панели результатов.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.cat_image_number = 0
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.cats = pygame.sprite.Group()
        self._create_fleet()
        # Создание кнопки Play.
        self.play_button = Button(self)

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()
            # Выполняется только при активной игре.
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_cats()
            self._update_screen()

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

        self.clock.tick(self.settings.fps)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.button_clicked = True
            # Сброс игровых настроек.
            self.settings.initialize_dynamic_settings()
            # Сброс игровой статистики.
            self.stats.reset_stats()
            self.stats.game_active = True
            self._update_screen()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_hearts()
            # Очистка списков котов и снарядов.
            self.cats.empty()
            self.bullets.empty()
            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()


    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиции снарядов.
        self.bullets.update()
        # Удаление снарядов вышедших за экран.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_cat_collisions()

    def _check_bullet_cat_collisions(self):
        # Проверка попаданий в котов.
        # При обнаружении попадания удалить снаряд и кота.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.cats, True, True)

        if collisions:
            for cats in collisions.values():
                self.stats.score += self.settings.cat_points * len(cats)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.cats:
            # Уничтожение существующих снарядов и создание нового флота.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Увеличение уровня.
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с котом."""
        if self.stats.hearts_left > 0:
            # Уменьшение количества оставшихся жизней.
            self.stats.hearts_left -= 1
            self.sb.prep_hearts()
            # Очистка списка котов и снарядов.
            self.cats.empty()
            self.bullets.empty()
            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()
            # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False

    def _update_cats(self):
        """Обновление позиции всех котов во флоте."""
        self._check_fleet_edges()
        self.cats.update()
        # Проверка коллизий "кот - корабль".
        if pygame.sprite.spritecollideany(self.ship, self.cats):
            self._ship_hit()
        # Проверить, добрались ли коты до нижнего края экрана.
        self._check_cats_bottom()

    def _create_fleet(self):
        """Создание флота вторжения."""
        # Создание кота и вычисление количества котов в ряду
        # Интервал между соседними котами равен ширине кота.
        cat = Cat(self)
        cat_width, cat_height = cat.rect.size
        available_space_x = self.settings.screen_width - (2 * cat_width)
        number_cats_x = available_space_x // (2 * cat_width)
        # Определяет количество рядов, помещающихся на экране.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * cat_height) - ship_height)
        number_rows = available_space_y // (2 * cat_height)
        # Создание флота вторжения.
        for row_number in range(number_rows):
            for cat_number in range(number_cats_x):
                self._create_cat(cat_number, row_number, self.cat_image_number)

    def _change_cat_img(self):
        """Меняет изображение картинки после создания кота"""
        if self.cat_image_number == 3:
            self.cat_image_number = 0
        else:
            self.cat_image_number += 1

    def _create_cat(self, cat_number, row_number, cat_image_number):
        """Создание кота и размещение его в ряду."""
        cat = Cat(self)
        cat_width, cat_height = cat.rect.size
        cat.x = cat_width + 2 * cat_width * cat_number
        cat.rect.x = cat.x
        cat.rect.y = cat.rect.height + 2 * cat.rect.height * row_number
        cat.image = self.settings.cat_images[cat_image_number]
        self.cats.add(cat)
        self._change_cat_img()

    def _check_fleet_edges(self):
        """Реагирует на достижение котами края."""
        for cat in self.cats.sprites():
            if cat.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет его направление."""
        for cat in self.cats.sprites():
            cat.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_cats_bottom(self):
        """Проверяет, добрались ли коты до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for cat in self.cats.sprites():
            if cat.rect.bottom >= screen_rect.bottom:
                """Происходит то же, что и при столкновении с кораблем."""
                self._ship_hit()
                break

    def _update_screen(self):
        """Обновляет изображение на экране и отображает новый экран."""
        self.screen.blit(self.settings.background_image, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.cats.draw(self.screen)
        # Вывод информации о счете.
        self.sb.show_score()
        # Кнопка Play отображается в том случае, если игра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button_up()
        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = CatsInvasion()
    ai.run_game()
