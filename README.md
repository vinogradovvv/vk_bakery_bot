# Bakery Bot

<img src="https://img.shields.io/badge/python3.12-blue">
<img src="https://img.shields.io/badge/SQLAlchemy-blue">
<img src="https://img.shields.io/badge/Redis-blue">
<img src="https://img.shields.io/badge/PostgreSQL-blue">
<img src="https://img.shields.io/badge/vk_api-blue">
<img src="https://img.shields.io/badge/Transitions-blue">
<img src="https://img.shields.io/badge/Docker-blue">

Bakery Bot - это бот для VK, предназначенный для управления продуктами и категориями пекарни через сообщество. Он позволяет пользователям добавлять, удалять и просматривать продукты и категории через сообщения сообщества VK.

## Возможности

- Добавление, удаление и просмотр категорий
- Добавление, удаление и просмотр продуктов
- Административные функции для управления продуктами и категориями

## Требования

- Python 3.12
- Docker
- Docker Compose

## Установка

1. Клонируйте репозиторий:

    ```sh
    git clone https://github.com/yourusername/bakery_bot.git
    cd bakery_bot
    ```

2. Скопируйте или переименуйте файл переменных окружения для нужного окружения в каталоге `envs/`:

    ```sh
    - `envs/dev.env`
    - `envs/prod.env`

3. Соберите и запустите контейнеры Docker:

    ```sh
    docker-compose up -d
    ```

## Разработка

1. Убедитесь, что переменные окружения правильно настроены в файле `envs/dev.env`.
2. Запустите бота:

    ```sh
    docker-compose -f docker-compose-dev.yaml up
   python -m main.py
    ```

3. Бот начнет слушать сообщения VK и отвечать на них в соответствии с реализованными обработчиками.

## Структура проекта

- `bakery_bot/`: Содержит основную логику бота и обработчики.
- `config/`: Файлы конфигурации для логирования и других настроек.
- `db/`: Скрипты инициализации и управления базой данных.
- `services/`: Сервисные классы для обработки бизнес-логики.
- `envs/`: Файлы переменных окружения для различных окружений.
- `docker-compose.yaml`: Файл конфигурации Docker Compose.

## Вклад

1. Сделайте форк репозитория.
2. Создайте новую ветку (`git checkout -b feature-branch`).
3. Зафиксируйте свои изменения (`git commit -am 'Add new feature'`).
4. Отправьте изменения в ветку (`git push origin feature-branch`).
5. Создайте новый Pull Request.

## Лицензия

Этот проект лицензирован по лицензии MIT. См. файл [LICENSE](LICENSE) для получения подробной информации.