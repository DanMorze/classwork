import os
import sys

import pygame
import requests

#'формат ввода в командной строке: долгота широта маштаб'
toponym_coords, delta = " ".join(sys.argv[1:3]), " ".join(sys.argv[3:4])
toponym_longitude, toponym_lattitude = toponym_coords.split(" ")

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
            print(toponym_lattitude, toponym_longitude)
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    map_params = {
        "ll": ",".join([toponym_lattitude, toponym_longitude]),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }
    response = requests.get(map_api_server, params=map_params)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
