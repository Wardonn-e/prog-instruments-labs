import sys

import pygame
import colour
import random

SIZE_OF_WINDOW = [2000, 1500]
COUNT_OF_ENEMY = 20
RANDOM_SPEED = True
RANDOM_COLOR = True
INFINITY = True
BACKGROUND_COLOR = (0, 0, 0)
DEFAULT_STEP_WAVE = 20
DEFAULT_LAST_WAVE_SCORE = 1

pygame.init()
win = pygame.display.set_mode(SIZE_OF_WINDOW)

enemies_list = []
running = True
score = 0
player = None
wave = 1
step_wave = DEFAULT_STEP_WAVE
last_wave_score = DEFAULT_LAST_WAVE_SCORE
game_over = False
generate_enemy = True
play_again_rect = None
quit_rect = None

i_for_wave = 0
starting_time = False
end_flag_starting_time = False


class ManagementGame:
    @staticmethod
    def init():
        global play_again_rect, quit_rect, player
        player = Rect(
            100, 100, 1000, 1300, "white", False, False, False,
            False, 8, 0, False, False
        )
        for num in range(COUNT_OF_ENEMY + 1):
            Rect()
        play_again_rect = Rect(
            300, 200, 1450, 1000, "white", False, False, False,
            False, 0, 5, False, False
        )
        quit_rect = Rect(
            300, 200, 250, 1000, "white", False, False, False,
            False, 0, 5, False, False
        )

    @staticmethod
    def game_over():
        global game_over, running, player
        game_over = True
        running = False
        pygame.display.update()
        ManagementGame.clear_enemy()
        print('hi')

    @staticmethod
    def show_title(score):
        global wave
        text_score = pygame.font.Font(None, 80)
        win.blit(
            text_score.render(f"Score: {score}", False, (255, 255, 255)),
            (0, 0)
        )
        text_score = pygame.font.Font(None, 60)
        win.blit(
            text_score.render(f"wave: {wave}", False, (255, 0, 255)),
            (0, 60)
        )
        if game_over:
            ManagementGame.game_over_title()

    @staticmethod
    def game_over_title():
        global play_again_rect, quit_rect, player, running, generate_enemy
        global game_over, wave, last_wave_score, score, step_wave

        text = pygame.font.Font(None, 250)
        text2 = pygame.font.Font(None, 100)
        win.blit(
            text.render("GAME OVER", False, (255, 0, 0)),
            (460, 650)
        )
        win.blit(
            text2.render(f"final score: {score}", False, (255, 255, 255)),
            (720, 850)
        )

        play_again_rect.show()
        quit_rect.show()

        if (
            (play_again_rect.x < player.x < play_again_rect.x + play_again_rect.w) or
            (player.x < play_again_rect.x < player.x + player.w) or
            (player.x == play_again_rect.x)
        ):
            if (
                (play_again_rect.y < player.y < play_again_rect.y + play_again_rect.h) or
                (player.y < play_again_rect.y < player.y + player.h)
            ):
                running = True
                generate_enemy = True
                game_over = False
                last_wave_score = DEFAULT_LAST_WAVE_SCORE
                step_wave = DEFAULT_STEP_WAVE
                score = 0
                wave = 1

        if (
            (quit_rect.x < player.x < quit_rect.x + quit_rect.w) or
            (player.x < quit_rect.x < player.x + player.w) or
            (player.x == quit_rect.x)
        ):
            if (
                (quit_rect.y < player.y < quit_rect.y + quit_rect.h) or
                (player.y < quit_rect.y < player.y + player.h)
            ):
                pygame.quit()
                sys.exit()

        play_again_text = pygame.font.Font(None, 100)
        quit_text = pygame.font.Font(None, 100)
        win.blit(
            play_again_text.render("again", False, (255, 255, 255)),
            (1510, 1060)
        )
        win.blit(
            quit_text.render("quit", False, (255, 255, 255)),
            (330, 1060)
        )

    @staticmethod
    def clear_enemy():
        enemies_list.clear()
        player.x = 940
        player.y = 1100

    @staticmethod
    def manage_wave():
        global last_wave_score, step_wave, generate_enemy, wave
        global starting_time, running, end_flag_starting_time, COUNT_OF_ENEMY

        if (score - last_wave_score - step_wave) > 0:
            last_wave_score = score
            wave += 1
            COUNT_OF_ENEMY += 2
            step_wave += COUNT_OF_ENEMY * 2
            starting_time = True
            running = False
            ManagementGame.clear_enemy()
        ManagementGame.check_time(1000)
        if end_flag_starting_time and not game_over:
            generate_enemy = True
            running = True
            end_flag_starting_time = False

        if starting_time:
            text_wave = pygame.font.Font(None, 80)
            win.blit(
                text_wave.render(f"Wave: {wave}", False, (255, 255, 255)),
                (450, 650)
            )

    @staticmethod
    def check_time(count):
        global i_for_wave, starting_time, end_flag_starting_time
        i_for_wave += 1
        if i_for_wave - count == 0:
            i_for_wave = 0
            starting_time = False
            end_flag_starting_time = True
            return True
        return False

    @staticmethod
    def into_while():
        ManagementGame.show_title(score)
        ManagementGame.manage_wave()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move_y(False)
        if keys[pygame.K_DOWN]:
            player.move_y()
        if keys[pygame.K_LEFT]:
            player.move_x(False)
        if keys[pygame.K_RIGHT]:
            player.move_x()

        ManagementGame.check_player()
        player.show()
        if running:
            if generate_enemy:
                if len(enemies_list) < COUNT_OF_ENEMY:
                    Rect()

            for item in enemies_list:
                item.move_y()
                item.check()
        pygame.display.update()
        win.fill(BACKGROUND_COLOR)

    @staticmethod
    def check_player():
        global player
        if player.x + player.w > SIZE_OF_WINDOW[0]:
            player.x = SIZE_OF_WINDOW[0] - player.w
        if player.x < 0:
            player.x = 0
        if player.y < 0:
            player.y = 0
        if player.y + player.h > SIZE_OF_WINDOW[1]:
            player.y = SIZE_OF_WINDOW[1] - player.h


class Color:
    color_rgb = None
    NAME_OF_SOME_COLOR = [
        'DarkGreen', 'Green', 'DarkCyan', 'DeepSkyBlue', 'DarkTurquoise',
        'MediumSpringGreen', 'Lime', 'SpringGreen', 'Cyan', 'Aqua',
        'MidnightBlue', 'DodgerBlue', 'LightSeaGreen', 'ForestGreen',
        'SeaGreen', 'DarkSlateGray', 'DarkSlateGrey', 'LimeGreen',
        'MediumSeaGreen', 'Turquoise', 'RoyalBlue', 'SteelBlue',
        'DarkSlateBlue', 'MediumTurquoise'
    ]

    def __init__(self, color="white"):
        self.get_rgb(color)

    def get_rgb(self, color):
        c = list(colour.Color(color).get_rgb())
        c[0] = int(c[0] * 255)
        c[1] = int(c[1] * 255)
        c[2] = int(c[2] * 255)
        self.color_rgb = tuple(c)

    def get_color(self):
        return self.color_rgb

    def get_random_color(self):
        self.get_rgb(random.choice(self.NAME_OF_SOME_COLOR))


class Rect:
    x = None
    y = None
    w = None
    h = None
    color = None
    spead = None
    border = None
    rand_color = None
    rand_size = None
    rand_position_x = None
    rand_spead = None
    rand_border = None

    def __init__(
            self, w=0, h=0, x=0, y=0, color="white",
            rand_color=True, rand_size=True, rand_position_x=True,
            rand_spead=True, spead=5, border=5, append=True, rand_border=True
    ):
        self.rand_color = rand_color
        self.x = x
        self.y = y
        self.spead = spead
        self.color = color
        self.border = border
        self.rand_size = rand_size
        self.w = w
        self.h = h
        self.rand_position_x = rand_position_x
        self.rand_spead = rand_spead
        self.rand_border = rand_border
        self.random()
        self.show()

        if append:
            enemies_list.append(self)

    def move_y(self, direction=True):
        self.y += self.spead if direction else -self.spead
        self.show()
        self.destroyer()

    def random(self):
        if self.rand_color:
            color = Color()
            color.get_random_color()
            self.color = color.color_rgb
        if self.rand_size:
            self.w = random.randint(30, 150)
            self.h = random.randint(30, 150)
        if self.rand_position_x:
            self.x = random.randint(0, SIZE_OF_WINDOW[0])
        if self.rand_spead:
            self.spead = random.randint(1, 10)
        if self.rand_border:
            self.border = random.randint(4, 15) if random.randint(0, 1) else 0

    def move_x(self, direction=True):
        self.x += self.spead if direction else -self.spead
        self.show()
        self.destroyer()

    def show(self):
        pygame.draw.rect(
            win, self.color, ((self.x, self.y), (self.w, self.h)), self.border
        )

    def destroyer(self):
        if self.y > (SIZE_OF_WINDOW[1] + 200):
            enemies_list.remove(self)
            global score
            score += 1

    def check(self):
        if (
            (self.x < player.x < self.x + self.w) or
            (player.x < self.x < player.x + player.w) or
            (player.x == self.x)
        ):
            if (
                (self.y < player.y < self.y + self.h) or
                (player.y < self.y < player.y + player.h)
            ):
                ManagementGame.game_over()


ManagementGame.init()

while True:
    ManagementGame.into_while()
    events = pygame.event.get()
    for item in events:
        if item.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
