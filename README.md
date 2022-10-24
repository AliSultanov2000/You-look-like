Целью этого проекта является создание Telegram - бота, который по фотографии пользователя будет определять, на кого он похож из знаменитостей.
Этапы проекта:
1) Поиск данных (парсинг изображений)  
2) Написание программы обработки изображения  
3) Выбор оптимальной модели ML  
4) Обучение модели ML (происходит в среде Google Colab, используется GPU)  
5) Заключение модели ML в Docker - контейнер  
6) Создание Telegram - бота  
7) Внедрение модели ML в Telegram - бота  

Стек используемых технологий: Python, Keras, NumPy, face_recognition, Telegram API.


В качестве модели машиного обучения была выбрана многослойная нейронная сеть.
Для уменьшения переобучения используются слои Dropout. Для ускорения обучения - BatchNormalization.
Функция активации во всех слоях сети, (кроме последнего слоя) - ReLu

Обучение модели многослойной нейронной сети проводилось в среде Google Colab, с использованием GPU. Далее вся модель (веса, состояние оптимизатора а также другие параметры) была сохранена на локальном компьютере, с целью создания пайплайна, развёртывания модели в Docker-контейнер.

Пайплайн:
 - Анализ изображнения библиотекой face_recognition на предмет распознавания лица 
 - Если лицо на изображении распознано, вырезаем из изображения всё лишнее, оставляем только лицо
 - Изменяем изображение лица до 170х170 пикселей
 - Передаём ресайз-изображение в функцию face_encodings библиотеки face_recognitions, в итоге всё изображения кодируется в виде вектора размера 128х1
 - Передаём закодированное в виде вектора изображение на вход нейросети
 - На выходном слое нейросети 233 нейрона, выходные значения которых представляют вероятность принадлежности к конкретному классу (классом является определённая знаменитость), функцией активации выходного слоя является Softmax
 - Из выходных значений последнего слоя нейросети берём максимальное, индекс максимального значения является номером класса - это и является предсказанием нейросети по объекту. Для того чтобы выдать предсказание в виде строки, берём строку из словаря по текущему(максимальному) индексу. В конёчном счёте по строке (предсказанной метке) функция находит фотографию знаменитости из спарсенных данных и возвращает её.
