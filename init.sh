#!/bin/bash

set -e

echo "Запуск тестовых Docker контейнеров..."
sudo docker-compose -f test-docker-compose.yml up --remove-orphans --force-recreate -d

echo Проверяем, существует ли директория alembic
if [ ! -d "app/alembic" ]; then
    echo "Инициализация Alembic..."
    sudo docker exec -it todolistmonolith-test_backend-1 alembic init alembic
fi

# Обновляем файл env.py для использования тестового подключения
echo "Обновление файла env.py для тестовых миграций..."
sudo sudo docker exec -it todolistmonolith-test_backend-1 bash -c "cat > alembic/env.py << 'EOF'
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src.core.config import settings
from src.users.infrastructure.db.orm import DBUser
from src.tasks.infrastructure.db.orm import DBTask
from src.db.base import Base


config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)



config.set_main_option(\"sqlalchemy.url\", settings.test_database_url + \"?async_fallback=True\")
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option(\"sqlalchemy.url\")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={\"paramstyle\": \"named\"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix=\"sqlalchemy.\",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

EOF"

echo "Создание тестовой миграции..."
sudo sudo docker exec -it todolistmonolith-test_backend-1 alembic revision --autogenerate -m "Test migration"

echo "Применение тестовой миграции..."
sudo sudo docker exec -it todolistmonolith-test_backend-1 alembic upgrade head

echo "Прогоняем тесты..."
sudo sudo docker exec -it todolistmonolith-test_backend-1 pytest -v

echo "Откатываем миграцию..."
sudo sudo docker exec -it todolistmonolith-test_backend-1 alembic downgrade -1
sudo sudo docker exec -it todolistmonolith-test_backend-1 rm -rf alembic
sudo docker exec -it todolistmonolith-test_backend-1 alembic init alembic

echo "Выключаем тестовые контейнеры..."
sudo docker stop $(docker ps -q)

echo "Включаем итоговые контейнеры..."
sudo docker-compose up --remove-orphans -d

echo "Обновление файла env.py для миграций..."
sudo docker-compose run backend bash -c "cat > alembic/env.py << 'EOF'
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src.core.config import settings
from src.users.infrastructure.db.orm import DBUser
from src.tasks.infrastructure.db.orm import DBTask
from src.db.base import Base


config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)



config.set_main_option(\"sqlalchemy.url\", settings.database_url + \"?async_fallback=True\")
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option(\"sqlalchemy.url\")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={\"paramstyle\": \"named\"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix=\"sqlalchemy.\",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

EOF"

# Создаем миграцию
echo "Создание миграции..."
sudo docker-compose run backend alembic revision --autogenerate -m "Initial migration"

# Применяем миграцию
echo "Применение миграции..."
sudo docker-compose run backend alembic upgrade head

echo "Проект успешно инициализирован и запущен! Доступ по адресу http://localhost:8000"
