import os
import numpy as np
import cv2
import face_recognition

def get_path(directory_path) -> list:
    """Функция, которая получает ссылки на все существующие изображения"""
    img_path_list = []
    directories = os.listdir(directory_path)
    if '.DS_Store' in directories:
        directories.remove('.DS_Store')
    for directory in directories:
        path = directory_path + '/' + directory
        for im in os.listdir(path):  # пробегаемся по названию изображений. im - это конкретное изображение
            if im == '.DS_Store':  # удаляем из подсчёта скрытый файл .DS_Store
                continue
            image_path = path + '/' + im
            if os.path.isfile(image_path):
                img_path_list.append(image_path)

    return img_path_list


def image_resize(img, width: int | float, height: int | float) -> np.ndarray:
    """Функция, которая изменяет размер изображений лица до стандартного размера"""
    return cv2.resize(img, (width, height))  # изменение размера изображения



def image_save(img: np.ndarray, save_img_path: str) -> None:
    """Функция, которая сохраняет изображение и удаляет старое"""
    cv2.imwrite(save_img_path, img)


# Todo: проверка данных в Celebrities(2) завершено - сделать функцию по переносу изобр-й из Celebrities(2) в Обработанные изображения

def face_detect(directory_path: str, new_directory_path: str) -> None:
    """Функция, которая отвечает за распознавание лиц на изображениях"""
    img_path_list = get_path(directory_path)
    for img_path in img_path_list:
        img = cv2.imread(img_path)  # здесь хранится тип np.ndarray
        face_location = face_recognition.face_locations(img)
        if len(face_location) == 0:
            print(f'Не обнаружено лицо на изображении: {img_path}')
        if len(face_location) == 1:
            try:
                width = face_location[0][1] - face_location[0][3]
                height = face_location[0][2] - face_location[0][0]
                img = img[face_location[0][0] - height // 3: face_location[0][0] + height, face_location[0][3]: face_location[0][3] + width]
                img = image_resize(img, 170, 170)  # Размер изображения согласован с архитектурой CNN

                name = img_path[42: img_path.rfind('/')]
                name_path = new_directory_path + '/' + name
                if not os.path.isdir(name_path):
                    os.mkdir(name_path)
                new_img_path = name_path + img_path[img_path.rfind('/'):]
                image_save(img, new_img_path)
                os.remove(img_path)  # удаляем изображение из старого файла (для удобства обработки в дальнейшем)

            except cv2.error:  # проблема вылезает из-за того, что face_recog выдает [], т.е len == 1 - заходим в этот блок, а матрицы изобр - нету. Проблема свелась к ручной обработке изображения
                print(f'Ошибка вылезла здесь: {img_path}')
        if len(face_location) > 1:
            print(f'Обнаружено несколько лиц на изображении: {img_path}')



def image_replace(img_path, final_img_path):
    """Функция по переносу изображения из директории img_path в final_img_path"""



def get_id(persons: list | tuple) -> dict:
    """Функция, которая по каждому человеку получает id значение и сохраняет в словарь"""
    counter = 0
    id_dict = {}
    for person in persons:
        if person not in id_dict:
            id_dict[person] = counter
            counter += 1
        else:
            continue
    return id_dict




# if __name__ == '__main__':
#     face_detect('/Users/alisultanov/Desktop/Celebrities(2)', '/Users/alisultanov/Desktop/Обработанные фотки')