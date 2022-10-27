import os
import pickle

PROCESSED_IMAGES_PATH = '/Users/alisultanov/Desktop/Обработанные фотки'

def get_information(directory_path: str) -> None:
    """A function that prints the number of classes,
     as well as the number of images (objects)"""
    directories = os.listdir(directory_path)
    if '.DS_Store' in directories:
        directories.remove('.DS_Store')
    print(f'Number of classes: {len(directories)}')
    image_count = 0
    for directory in directories:
        path = directory_path + '/' + directory
        for img_path in os.listdir(path):  # scrolling through the title of the image
            if img_path == '.DS_Store':  # remove the hidden .DS_Store file from the count
                continue
            if os.path.isfile(path + '/' + img_path):
                image_count += 1
    print(f'Number of images (objects): {image_count}')



def get_dataset_information(dataset_path: str) -> None:
    """A function that displays information about the size of the dataset
    dataset_path: embeddings.pkl or labels.pkl"""
    with open(dataset_path, 'rb') as file:
        dataset = pickle.load(file)
        print(f'Dataset size: {len(dataset)} objects')



if __name__ == '__main__':
    get_information(PROCESSED_IMAGES_PATH)
    get_dataset_information('embeddings.pkl')