import face_recognition
import cv2
import numpy as np
import logging
import json
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
from keras import models


def json_load(file_name: str) -> dict:
    """json file upload function"""
    with open(file_name, 'r') as file:
        return json.load(file)


ID_DICT = json_load('celebrities.json')

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def ml_pipeline(img_path: str) -> str:
    """The function of predicting the model for this object"""
    logging.info('Search for a face in an image')
    try:
        img = cv2.imread(img_path)
        face_location = face_recognition.face_locations(img)
        if len(face_location) == 0:
            return f'No face detected in the image'

        elif len(face_location) > 1:
            return f'Several faces have been detected in the image'

        else:
            logging.info('A prediction is formed...')
            width = face_location[0][1] - face_location[0][3]
            height = face_location[0][2] - face_location[0][0]
            img = img[face_location[0][0] - height // 3: face_location[0][0] + height, face_location[0][3]: face_location[0][3] + width]
            img = cv2.resize(img, (170, 170))
            img_encoded = face_recognition.face_encodings(img)
            prediction = ID_DICT[str(model.predict(np.array(img_encoded), verbose=0).argmax())]
            return f'The person in the image looks like: {prediction}'
    except TypeError:
        return f'Error when getting a link to an image'
    except cv2.error:
        return f'Image processing error, send the photo again'


if __name__ == '__main__':
    model = models.load_model('dl_model')
    print(ml_pipeline(''))