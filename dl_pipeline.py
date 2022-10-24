import face_recognition
import cv2
import numpy as np
import pickle
import logging
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow
from data_preprocessing import id_person, image_resize
from tensorflow import keras
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from data_preprocessing import id_person
from keras import models

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def model_predict(img_path: str) -> str:
    """Функция предсказания модели по данному объекту"""
    logging.info('Происходит поиск лица на изображении')
    img = cv2.imread(img_path)
    face_location = face_recognition.face_locations(img)
    if len(face_location) == 0:
        print(f'Не обнаружено лицо на изображении: {img_path}')

    elif len(face_location) > 1:
        print(f'Обнаружено несколько лиц на изображении: {img_path}')

    else:
        logging.info('Лицо распознано, формируется предсказание')
        width = face_location[0][1] - face_location[0][3]
        height = face_location[0][2] - face_location[0][0]
        img = img[face_location[0][0] - height // 3: face_location[0][0] + height, face_location[0][3]: face_location[0][3] + width]
        img = image_resize(img, 170, 170)
        img_encoded = face_recognition.face_encodings(img)
        return f'Человек на изображении выглядит как: {id_person[str(model.predict(np.array(img_encoded), verbose=0).argmax())]}'




if __name__ == '__main__':
    model = models.load_model('dl_model')
    print(model_predict('/Users/alisultanov/Desktop/beautiful-asian-woman-posing-with-perfect-skin_23-2149369946.jpg.webp'))