import os
import shutil
import pickle
import numpy as np
import cv2
import face_recognition

PROCESSED_IMAGES_PATH = '/Users/alisultanov/Desktop/Обработанные фотки'


def get_path(directory_path) -> list:
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


def image_resize(img: np.ndarray, width: int | float, height: int | float) -> np.ndarray:
    """A function that resizes face images to a standard size"""
    return cv2.resize(img, (width, height))


def image_save(img: np.ndarray, save_img_path: str) -> None:
    """A function that saves an image"""
    cv2.imwrite(save_img_path, img)


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
                img = image_resize(img, 170, 170)

                name = img_path[42: img_path.rfind('/')]
                name_path = new_directory_path + '/' + name
                if not os.path.isdir(name_path):
                    os.mkdir(name_path)
                new_img_path = name_path + img_path[img_path.rfind('/'):]
                image_save(img, new_img_path)
                os.remove(img_path)  # we delete the image from the old file

            except cv2.error:
                print(f'Image processing error: {img_path}')
        if len(face_location) > 1:
            print(f'Several faces have been detected in the image: {img_path}')


def image_replace(directory_path: str) -> None:
    """Function for transferring an image from the img_path directory to final_img_path"""
    img_path_list = get_path(directory_path)
    for img_path in img_path_list:
        try:
            new_img_path = img_path.replace('Celebrities(2)', 'Обработанные фотки')
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
    id_dict = {str(value): key for key, value in id_dict.items()}
    return id_dict


id_person = get_id(PROCESSED_IMAGES_PATH)


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
        name = img_path[46: img_path.rfind('/')]
        y_data.append(id_person[name])  # added a class label
    X_data = X_data[1:]
    return np.array(X_data), np.array(y_data)


def pickle_save(file_name: str, data: np.array) -> None:
    """The function of saving embeddings in .pcl format
       (used for both X and y)"""
    with open(file_name, 'wb') as f:
        pickle.dump(data, f, protocol=5)


if __name__ == '__main__':
    X, y = get_embeddings_and_labels(PROCESSED_IMAGES_PATH)
    pickle_save('embeddings.pkl', X)
    pickle_save('labels.pkl', y)
