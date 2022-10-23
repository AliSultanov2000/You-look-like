import os
import shutil
import time
import requests
from bs4 import BeautifulSoup


def get_links() -> set:
    """Функция, которая получает cсылки на знаменитостей из сайта"""
    url = 'https://www.theplace.ru/photos/'
    links = []
    r = requests.get(url)
    soap = BeautifulSoup(r.text, 'html.parser')
    celebrities = soap.findAll('div', class_='col-md-4 col-sm-6 col-6')
    for celebrity in celebrities:
        try:
            link = celebrity.find('div', class_='model-item').find('a', class_='model-link').get('href')
            links.append('https://www.theplace.ru' + link)

        except AttributeError:
            continue
    celeb_list = ['https://www.theplace.ru/photos/' + i + '/' for i in other_celebrities]
    links.extend(celeb_list)
    return set(links)


def save_image(urls: set) -> None:
    """Функция, которая по ссылкам на всех знаменитостей сохраняет изображения"""
    def save_func(im_link: str) -> None:
        """Функция, которая отвечает за сохранение изображения в указанную папку"""
        html_data = requests.get(im_link)
        html_data_cleaning = BeautifulSoup(html_data.text, 'html.parser')
        get_photo = requests.get('https://www.theplace.ru' + html_data_cleaning.find('div', class_='content-wrapper').find('img', class_='pic big_pic').get('src'))
        with open(f"/Users/alisultanov/Desktop/img{counter}.jpg", "wb") as out:
            out.write(get_photo.content)
        shutil.move(f"/Users/alisultanov/Desktop/img{counter}.jpg", path)

    counter = 0
    for url in urls:
        try:
            r = requests.get(url)
            soap = BeautifulSoup(r.text, 'html.parser')
            name = soap.find('div', class_='col-xl-9 col-lg-8 col-md-7 col-sm-12 main-col-content').find('h1', class_='my-3').text
            path = '/Users/alisultanov/Desktop/Celebrities' + f'/{name}'
            if not os.path.isdir(path):
                os.mkdir(path)
            else:
                continue

            images = soap.find('div', class_='gallery-pics-list photos-pics-list').find('div', class_='row').findAll('div', class_='col-6 col-sm-6 col-md-6 col-lg-4 col-xl-3 pb-3')

            for image in images:  # обрабатываем первый блок фотографий
                counter += 1
                im1_link = 'https://www.theplace.ru' + image.find('div', class_='photos-pic-card').find('a', class_='photos-pic-card__link').get('href')
                save_func(im1_link)

            # обрабатываем другие теги с фотографиями из сайта текущего человека
            other_images = soap.find('div', class_='container-xl container-main').find('div', class_='row').find('div', class_='col-xl-9 col-lg-8 col-md-7 col-sm-12 main-col-content').find('div', class_='d-flex flex-wrap justify-content-center').findAll('div', class_='p-1')
            inner_counter = 1
            for other_image in other_images:  # обрабатываем второй блок фотографий
                counter += 1
                inner_counter += 1
                im2_link = 'https://www.theplace.ru' + other_image.find('div', class_='gallery-photo-card').find('a').get('href')
                save_func(im2_link)
                if inner_counter == 21:  # берём только первые 20 фотографий из этого блока
                    break

        except AttributeError:
            pass
        time.sleep(0.05)


other_celebrities = ['alla_pugacheva', 'charlie_hunnam', 'jo_In_seong', 'channing_tatum',  'constance_wu',
                   'cee_lo_green', 'christian_bale', 'chris_evans', 'cillian_murphy', 'colin_farrel', 'bella_hadid', 'barack_obama',
                   'bradley_cooper', 'bred_pitt', 'bruce_willis', 'dakota_johnson',  'pitbull', 'shia_labeouf', 'kit_harington',
                     'nargis_fakhri', 'kate_clapp',  'alison_sudol', 'james_franco', 'jake_gyllenhaal', 'jamie_dornan', 'renee_lacombe', 'robbie_willams',
                     'jensen_ackles', 'jesse_eisenberg', 'jim_parsons', 'justin_timberlake', 'justin_bieber', 'lindsay_ellingson',
                     'leonardo_dicaprio', 'luke_evans', 'luis_fonsi', 'orlando_bloom', 'venus_williams', 'robert_downey_jr', 'vin_diesel',
                     'taraji_p._henson', 'tom_cruz', 'tobias_sorensen', 'tom_holland', 'tom_hardy', 'tom_welling', 'tupac_shakur', 'tobey_maguire',
                     'til_schweiger', 'zayn_malik', 'zac_efron', 'heath_ledger', 'xabi_alonso', 'will_smith', 'wilmer_valderrama',
                     'alek_wek', 'anna_kendrick', 'anna_semenovich', 'aiana_grande', 'ashanti', 'arlenis_sosa_pena', 'aaron_paul', 'al_pacino', 'alain_delon',
                     'ansel_elgort', 'antonio_banderas', 'andrey_arshavin', 'aleksey_chadov', 'aaron_johnson', 'aoi_miyazaki', 'alexa_bliss', 'bae_suzy', 'brighton_sharbino',
                      'ben_affleck', 'camille_hurel', 'cassie', 'christina_chiabotto', 'chulpan_khamatova', 'chris_hemsworth', 'chase_tang', 'charlie_sheen', 'michael_jfox',
                      'chris_odonnell', 'colin_morgan', 'cam_gigandet', 'callan_mcAuliffe', 'dima_nosov', 'david_villa', 'jessica_perez', 'jade_weber',
                     'emile_hirsch', 'emilia_fox', 'emily_browning', 'edward_furlong', 'sofia_vergara', 'janina_schiedlofski', 'james_norton', 'james_purefoy', 'lisa_edelstein',
                     'paul_walker', 'paul_wesley',  'Priyanka Chopra', 'zachary_quinto', 'zara', 'zaira_nara', 'zara_larsson', 'zendaya', 'zinadin_zidan',
                     'zach_braff', 'hugh_jackman', 'taron_egerton', 'tessa_thompson', 'salma_hayek', 'sarah_gadon', 'owen_wilson', 'lionel_messi', 'harry_styles',
                     'valeriy_meladze', 'arnold_schwarzenegger', 'aleksandra_bortich', 'andres_segura', 'andy_garcia', 'aaron_eckhart', 'ben_barnes', 'bow_wow',
                     'benjamin_bratt', 'brendon_urie', 'brandon_routh', 'brenton_thwaites', 'robin_williams', 'robert_pattinson', 'robin_thicke', 'roma_zver',
                     'roman_pavlyuchenko', 'rowan_atkinson', 'ruben_cortada', 'ryan_gosling', 'steven_mcqueen', 'Suriya', 'shawn_mendes', 'shane_west',
                     'snoop_dogg', 'peter_gallagher', 'pedro_pascal', 'samuel_smith']


if __name__ == '__main__':
    ls = get_links()
    save_image(ls)