import os
import re
import shutil
import pickle
import json
import numpy as np
import cv2
import face_recognition
from model_pipeline import json_load


PROCESSED_IMAGES_PATH = json_load("directories_path.json")["PROCESSED_IMAGES_PATH"]


def get_path(directory_path: str) -> list:
    """A function that gets links to all existing images"""
    img_path_list = []
    directories = os.listdir(directory_path)
    if '.DS_Store' in directories:
        directories.remove('.DS_Store')
    for directory in directories:
        path = directory_path + '/' + directory
        for im in os.listdir(path):  # we run through the names of the images,  im is a specific image
            if im == '.DS_Store':  # we remove the hidden file from the calculation .DS_Store
                continue
            image_path = path + '/' + im
            if os.path.isfile(image_path):
                img_path_list.append(image_path)

    return img_path_list


def get_name(img_path: str) -> str:
    """A function that pulls a person's name from the path to the image"""
    delimiters = list(re.finditer("/", img_path))  # finding everything / in the path to the img file (to find a person's name)
    first_delimiter = delimiters[-2].span()[0]
    second_delimiter = delimiters[-1].span()[0] + 1
    name = img_path[first_delimiter + 1: second_delimiter - 1]
    return name


def face_detect(directory_path: str, new_directory_path: str) -> None:
    """The function that is responsible for recognizing faces in images,
    causes the image to be resized and saved in a new directory"""
    img_path_list = get_path(directory_path)
    for img_path in img_path_list:
        img = cv2.imread(img_path)  # the np.ndarray type is stored here
        face_location = face_recognition.face_locations(img)
        if len(face_location) == 0:
            print(f'No face detected in the image: {img_path}')
        elif len(face_location) > 1:
            print(f'Several faces have been detected in the image: {img_path}')
        else:
            try:
                width = face_location[0][1] - face_location[0][3]
                height = face_location[0][2] - face_location[0][0]
                img = img[face_location[0][0] - height // 3: face_location[0][0] + height, face_location[0][3]: face_location[0][3] + width]
                img = cv2.resize(img, (170, 170))
                name = get_name(img_path)
                name_path = new_directory_path + '/' + name
                if not os.path.isdir(name_path):
                    os.mkdir(name_path)
                new_img_path = name_path + img_path[img_path.rfind('/'):]
                cv2.imwrite(new_img_path, img)
                os.remove(img_path)  # we delete the image from the old file

            except cv2.error:
                print(f'Image processing error: {img_path}')
        if len(face_location) > 1:
            print(f'Several faces have been detected in the image: {img_path}')


def image_replace(directory_path: str, new_directory_path: str) -> None:
    """Function of transferring images from directory_path to new_directory_path"""
    img_path_list = get_path(directory_path)
    for img_path in img_path_list:
        try:
            delimiters = list(re.finditer("/", img_path))
            delimiter = delimiters[-2].span()[0]
            short_img_path = img_path[delimiter:]
            new_img_path = new_directory_path + short_img_path
            shutil.move(img_path, new_img_path)
        except FileNotFoundError:
            print(f'There is no directory for this image: {img_path}') 


def get_id(directory_path: str) -> dict:
    """A function that for each person gets an id value and saves it to a dictionary"""
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


ID_PERSON = get_id(PROCESSED_IMAGES_PATH)
ID_DICT = ID_PERSON.copy()
ID_DICT = {str(value): key for key, value in ID_DICT.items()}


def get_embeddings_and_labels(directory_path: str) -> (np.array, np.array):
    """Function to get embeddings and class tags for all images from a directory"""
    X_data = np.empty(128)
    y_data = []
    img_path_list = get_path(directory_path)
    for img_path in img_path_list:  # we are on a specific image from the directory
        img = cv2.imread(img_path)
        img = face_recognition.face_encodings(img)
        if not img:
            continue
        X_data = np.vstack((X_data, img))  # added a digital representation of the image
        name = get_name(img_path)
        y_data.append(ID_PERSON[name])  # added a class label
    X_data = X_data[1:]
    return np.array(X_data), np.array(y_data)


def pickle_save(file_name: str, data: np.array) -> None:
    """The function of saving embeddings in .pcl format
       (used for both X and y)"""
    with open(file_name, 'wb') as f:
        pickle.dump(data, f, protocol=5)


def json_save(file_name: str, id_name: dict) -> None:
    """Function that saves celebrity names in Json file"""
    with open(file_name, 'w') as file:
        json.dump(id_name, file, indent=1, ensure_ascii=False)


if __name__ == '__main__':
    json_save('celebrities.json', ID_DICT)
    X, y = get_embeddings_and_labels(PROCESSED_IMAGES_PATH)
    pickle_save('embeddings.pkl', X)
    pickle_save('labels.pkl', y)
