# ToDoListMonolith

## Описание

ToDoListMonolith — простое в использовании монолитное бэкенд-приложение с jwt-аутентификацией/авторизацией, предоставляющее RESTful API для управления задачами, построенное на стеке технологий FastAPI, PostgreSQL, async SQLAlchemy и других. Этот проект предоставляет возможность пользователям регистрироваться, входить в свой аккаунт и эффективно организовывать и отслеживать свои задачи.

## Технологии

- **FastAPI**: Современный веб-фреймворк для создания APIs с высокой производительностью.
- **PostgreSQL**: Надежная реляционная база данных для хранения данных.
- **async SQLAlchemy**: Асинхронный ORM для работы с базой данных.
- **Alembic**: Инструмент для управления миграциями базы данных.
- **Redis**: Быстрая in-memory база данных для кэширования refresh-токенов.
- **pytest**: Фреймворк для тестирования.
- **Docker**: Платформа для контейнеризации приложений.
- **docker-compose**: Инструмент для определения и запуска многоконтейнерных Docker-приложений.

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/George-lab-star/ToDoListMonolith.git
   cd ToDoListMonolith
   ```

2. Убедитесь, что у вас установлен Docker и docker-compose.

3. Удалите папку с миграциями:

   ```bash
   sudo rm -rf backend/alembic
   ```

4. Создайте .env файл в корне проекта и наполните его:

   ```
   DB_USER=postgres
   DB_PASS=postgres
   DB_HOST=postgres
   DB_PORT=5432
   DB_NAME=postgres

   REDIS_USER=redis
   REDIS_PASS=redis
   REDIS_HOST=redis
   REDIS_PORT=6379
   REDIS_NAME=redis

   JWT_ALGORITHM=HS256
   JWT_SECRET=0202279efcfdbe31ea42de6a1dec6243
   ACCESS_TOKEN_EXPIRE_SECONDS=1800
   REFRESH_TOKEN_EXPIRE_SECONDS=5184000

   TEST_DB_USER=test_postgres
   TEST_DB_PASS=postgres
   TEST_DB_HOST=test_postgres
   TEST_DB_PORT=5432
   TEST_DB_NAME=postgres

   REDIS_USER=redis
   REDIS_PASS=redis
   REDIS_HOST=redis
   REDIS_PORT=6379
   REDIS_NAME=redis

   TEST_REDIS_HOST=test_redis
   ```

5. Запустите приложение с помощью инициализирующего bash-скрипта, запускающего контейнеры, прогоняющего миграции базы данных и тесты. Он находится в корне репозитория:

   ```bash
   sudo ./init.sh
   ```

## Использование

После успешного запуска приложения, вы сможете получить доступ к API по адресу [http://localhost:8000/docs](http://localhost:8000/docs).

## Контакты

Если у вас есть вопросы или предложения, не стесняйтесь обращаться:

- Георгий Ломакин
- email: georgelomakin99@gmail.com
- Ваш GitHub: [George-lab-star (я)](https://github.com/George-lab-star)
