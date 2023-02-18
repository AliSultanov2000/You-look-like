import os
import shutil
import time
import requests
from bs4 import BeautifulSoup
from model_pipeline import json_load

DIRECTORY_PATH = json_load("directories_path.json")['DIRECTORY_PATH']  # here we store the raw images
DESKTOP_PATH = json_load("directories_path.json")['DESKTOP_PATH']

WEBSITE_LINK = 'https://www.theplace.ru'

def get_links() -> set:
    """A function that gets celebrity links from a website"""
    url = 'https://www.theplace.ru/photos/'
    links = []
    r = requests.get(url)
    soap = BeautifulSoup(r.text, 'html.parser')
    celebrities = soap.findAll('div', class_='col-md-4 col-sm-6 col-6')
    for celebrity in celebrities:
        try:
            link = celebrity.find('div', class_='model-item').find('a', class_='model-link').get('href')
            links.append(WEBSITE_LINK + link)

        except AttributeError:
            continue
    celeb_list = ['https://www.theplace.ru/photos/' + i + '/' for i in other_celebrities]
    links.extend(celeb_list)
    return set(links)


def save_image(urls: set) -> None:
    """Function that links to all celebrities saves images"""
    def save_func(im_link: str) -> None:
        """The function that is responsible for saving the image to the specified folder"""
        html_data = requests.get(im_link)
        html_data_cleaning = BeautifulSoup(html_data.text, 'html.parser')
        get_photo = requests.get(WEBSITE_LINK + html_data_cleaning.find('div', class_='content-wrapper').find('img', class_='pic big_pic').get('src'))
        photo_path = DESKTOP_PATH + f'/img{counter}.jpg'
        with open(photo_path, "wb") as out:
            out.write(get_photo.content)
        shutil.move(photo_path, path)

    counter = 0
    for url in urls:
        try:
            r = requests.get(url)
            soap = BeautifulSoup(r.text, 'html.parser')
            name = soap.find('div', class_='col-xl-9 col-lg-8 col-md-7 col-sm-12 main-col-content').find('h1', class_='my-3').text
            path = DIRECTORY_PATH + f'/{name}'  # save all images in this path
            if not os.path.isdir(path):
                os.mkdir(path)
            else:
                continue

            images = soap.find('div', class_='gallery-pics-list photos-pics-list').find('div', class_='row').findAll('div', class_='col-6 col-sm-6 col-md-6 col-lg-4 col-xl-3 pb-3')

            for image in images:  # processing the first block of images
                counter += 1
                im1_link = WEBSITE_LINK + image.find('div', class_='photos-pic-card').find('a', class_='photos-pic-card__link').get('href')
                save_func(im1_link)

            # processing other tags with photos from the site of the current person
            other_images = soap.find('div', class_='container-xl container-main').find('div', class_='row').find('div', class_='col-xl-9 col-lg-8 col-md-7 col-sm-12 main-col-content').find('div', class_='d-flex flex-wrap justify-content-center').findAll('div', class_='p-1')
            inner_counter = 1
            for other_image in other_images:  # processing the second block of images
                counter += 1
                inner_counter += 1
                im2_link = WEBSITE_LINK + other_image.find('div', class_='gallery-photo-card').find('a').get('href')
                save_func(im2_link)
                if inner_counter == 21:  # take only the first 20 photos from this block
                    break

        except AttributeError:
            pass
        time.sleep(0.05)


other_celebrities = []


if __name__ == '__main__':
    LINKS = get_links()
    save_image(LINKS)
