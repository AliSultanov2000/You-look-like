import os
import cv2
import json
import numpy as np

def get_data_information(directory_path: str) -> None:
    """Функция, которая выводит количество классов,
     а также количество изображений (объектов)"""
    directories = os.listdir(directory_path)
    if '.DS_Store' in directories:
        directories.remove('.DS_Store')
    print(f'Количество классов: {len(directories)}')
    image_count = 0
    for directory in directories:
        path = directory_path + '/' + directory
        for im in os.listdir(path):  # пробегаемся по названию изображени
            if im == '.DS_Store':  # удаляем из подсчёта скрытый файл .DS_Store
                continue
            if os.path.isfile(path + '/' + im):
                image_count += 1
    print(f'Количество изображений (объектов): {image_count}')



if __name__ == '__main__':
    get_data_information('/Users/alisultanov/Desktop/Обработанные фотки')

    
