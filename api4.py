import os
import sys

import pygame
import requests

#'формат ввода в командной строке: долгота широта маштаб'
toponym_coords, delta = " ".join(sys.argv[1:3]), " ".join(sys.argv[3:4])
toponym_longitude, toponym_lattitude = toponym_coords.split(" ")
l = "map"


def show_text(text, font, position):
    font_color = pygame.Color("orange")
    text = font.render(text, 1, font_color)
    screen.blit(text, position)


def select_map():
    text = ['схема', 'спутник', 'гибрид']
    x = [10, 90, 190]
    font = pygame.font.Font(None, 30)
    for elem in range(len(text)):
        show_text(text[elem], font, (x[elem], 10))


pygame.init()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                delta = str(round((float(delta) + 0.1), 2))
            elif event.key == pygame.K_PAGEDOWN and float(delta) > 0.1:
                delta = str(round((float(delta) - 0.1), 2))
            elif event.key == pygame.K_UP and float(toponym_longitude) + float(delta) < 84.01:
                toponym_longitude = str(float(toponym_longitude) + 1.5 * float(delta))
            elif event.key == pygame.K_DOWN and float(toponym_longitude) - float(delta) > -84.01:
                toponym_longitude = str(float(toponym_longitude) - 1.5 * float(delta))
            elif event.key == pygame.K_RIGHT and float(toponym_lattitude) + float(delta) < 179.0:
                toponym_lattitude = str(float(toponym_lattitude) + 1.5 * float(delta))
            elif event.key == pygame.K_LEFT and float(toponym_lattitude) - float(delta) > -179.0:
                toponym_lattitude = str(float(toponym_lattitude) - 1.5 * float(delta))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 6 <= event.pos[0] <= 71 and 8 <= event.pos[1] <= 33:
                l = "map"
            if 86 <= event.pos[0] <= 171 and 8 <= event.pos[1] <= 33:
                l = "sat"
            if 186 <= event.pos[0] <= 266 and 8 <= event.pos[1] <= 33:
                l = "sat,skl"
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {
        "ll": ",".join([toponym_lattitude, toponym_longitude]),
        "spn": ",".join([delta, delta]),
        "l": l
    }
    response = requests.get(map_api_server, params=map_params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    select_map()
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
