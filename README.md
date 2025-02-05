# SELEBOT

## Описание
Небольшой телеграм бот кторый генерирует поздравления по трем параметрам: Имя, повод(мероприятие) и описание того поздравляют. 
Объем на генерацию ограничен 300 символами. 

Генерация происходит через API Gigachat от сбербанка. Бесплатная версия границена 1000000токенов. Узнать количество оставшихся на балансе токенов можно зайдя во вкладку "О боте"

Бот будет временно доступен для тестирования по адресу в телеграм: @Valik_assist_bot

## Запуск
Для запуска бота необходимо установить зависимости:
pip install -r requirements.txt

Для работы бота необходимо задать переменные окружения:
TELEGRAM_TOKEN = Телеграм токен бота
SCOPE = Имя генеративной модели гигачата ('GIGACHAT_API_PERS' для физ лиц)
AUTHORIZATION_KEY = Токен авторизации гигачата
CREATOR = ID автора бота (Опционально, если не нужны уведомления о генерациях, удалить строки 59-64)

Также для работы бота необходим корневой сертификат минцифр. Скачать бесплатно с госуслуг по ссылке: https://www.gosuslugi.ru/crt.
Для системы на ОС Windows - russian_trusted_root_ca.cer
Для системы на ОС Linux - russian_trusted_root_ca.crt
Имя сертификату дать: russian_trusted_root_ca.cer или поменять название в файле generate_seleg.py на нужный.

Для запуска бота необходимо запустить файл main.py:
selebot.py

## Автор
Бот создан Рубановым Валентином Сергеевичем
telegram: @ValikSht
почта: rubanov.valentin@ya.ru