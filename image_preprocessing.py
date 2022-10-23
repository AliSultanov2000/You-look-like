import os
import shutil
import pickle
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


def image_resize(img: np.ndarray, width: int | float, height: int | float) -> np.ndarray:
    """Функция, которая изменяет размер изображений лица до стандартного размера"""
    return cv2.resize(img, (width, height))


def image_save(img: np.ndarray, save_img_path: str) -> None:
    """Функция, которая сохраняет изображение"""
    cv2.imwrite(save_img_path, img)


def face_detect(directory_path: str, new_directory_path: str) -> None:
    """Функция, которая отвечает за распознавание лиц на изображениях,
    вызывает ф-ии изменения размера изображения и сохранения в новой директории"""
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
                print(f'Ошибка обработки изображения: {img_path}')
        if len(face_location) > 1:
            print(f'Обнаружено несколько лиц на изображении: {img_path}')


def image_replace(directory_path: str) -> None:
    """Функция по переносу изображения из директории img_path в final_img_path"""
    img_path_list = get_path(directory_path)
    for img_path in img_path_list:
        try:
            new_img_path = img_path.replace('Celebrities(2)', 'Обработанные фотки')
            shutil.move(img_path, new_img_path)
        except FileNotFoundError:
            print(f'Не существует директории для этого изображения: {img_path}')


def get_id(directory_path: str) -> dict:
    """Функция, которая по каждому человеку получает id значение и сохраняет в словарь"""
    counter = 0
    id_dict = {}
    persons = os.listdir(directory_path)
    for person in persons:
        if person == '.DS_Store':
            continue
        if person not in id_dict:
            id_dict[person] = counter
            counter += 1
        else:
            continue
    return id_dict


id_person = get_id('/Users/alisultanov/Desktop/Обработанные фотки')


def get_embeddings_and_labels(directory_path: str) -> (np.array, np.array):
    """Функция получения эмбеддингов и меток классов для всех изображений из директории"""
    X_data = np.empty(128)
    y_data = []
    img_path_list = get_path(directory_path)
    for img_path in img_path_list:  # находимся на конкретном изображении из директории
        img = cv2.imread(img_path)
        img = face_recognition.face_encodings(img)
        if not img:
            continue
        X_data = np.vstack((X_data, img))  # добавили цифровое представление изображения
        name = img_path[46: img_path.rfind('/')]
        y_data.append(id_person[name])  # добавили метку класса
    X_data = X_data[1:]
    return np.array(X_data), np.array(y_data)


def pickle_save(file_name: str, data: np.array) -> None:
    """Функция сохранения эмбеддингов в формате .pkl
    (используется как для X, так и для y)"""
    with open(file_name, 'wb') as f:
        pickle.dump(data, f, protocol=5)


if __name__ == '__main__':
    X, y = get_embeddings_and_labels('/Users/alisultanov/Desktop/Обработанные фотки')
    pickle_save('embeddings.pkl', X)
    pickle_save('labels.pkl', y)