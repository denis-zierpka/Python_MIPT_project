import time
from threading import Thread
from time import sleep

import pygame

from app.local_info import Info

start_time = 0


class Game:
    def __init__(self):
        self.count_clicks = 0
        self.count_auto_clicks = 0
        self.money = 0

    def button_was_clicked(self, times=1):
        self.count_clicks += times
        self.money += times

    def buy_auto_clicker(self):
        if self.money >= Info.money_for_auto_clicker:
            self.count_auto_clicks += 1
            self.money -= Info.money_for_auto_clicker

    def update_rate(self):
        self.button_was_clicked(self.count_auto_clicks)
        sleep(Info.sleep_before_updating)
        self.update_rate()

    def get_money_str(self):
        return str(self.money // 100) + '.' + str(self.money % 100)

    def play(self):
        global start_time
        start_time = time.time()
        pygame.init()
        win = pygame.display.set_mode((Info.display_width, Info.display_height))
        pygame.display.set_caption('Clicker')
        th = Thread(target=self.update_rate, daemon=True)
        th.start()

        button_color = (0, 0, 0)
        text_color = (0, 0, 0)
        background_color = (255, 255, 255)

        run = True
        while run:
            try:
                pygame.time.delay(100)

                font = pygame.font.SysFont(Info.font_style, Info.font_size)
                text_count_clicks = font.render(
                    Info.clicked_times_info_str.format(str(self.count_clicks)),
                    True,
                    text_color,
                )
                text_money = font.render(
                    Info.money_info_str.format(self.get_money_str()), True, text_color
                )
                text_auto_clickers = font.render(
                    Info.auto_clicker_info_str.format(self.count_auto_clicks),
                    True,
                    text_color,
                )
                win.fill(background_color)
                win.blit(text_count_clicks, (Info.padding_left, 0))
                win.blit(text_money, (Info.padding_left, Info.font_size + 10))

                if self.count_clicks < 100:
                    button = pygame.draw.rect(win, button_color, (20, 100, 150, 150))
                else:
                    button = pygame.draw.circle(win, button_color, (95, 175), 75)

                win.blit(text_auto_clickers, (260, 100))
                button_buy = pygame.draw.rect(win, button_color, (260, 130, 230, 30))

                # add text to button_buy
                text_new = font.render(
                    'buy auto clicker' + str(), True, (255, 255, 255)
                )
                textRect = text_new.get_rect()
                textRect.center = button_buy.center
                win.blit(text_new, textRect)

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        if button.collidepoint(pos):
                            self.button_was_clicked()

                        if button_buy.collidepoint(pos):
                            self.buy_auto_clicker()
            except Exception:
                pygame.quit()

        pygame.quit()
