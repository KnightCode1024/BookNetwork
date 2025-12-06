# Книжная соц. сеть "Переплёт"


## Запуск

### Генерация ключей

```bash
# Перейти в папку бекенда
cd backend

# Создание папки для ключей
mkdir certs

# Переходим в папку для ключей
cd certs

# Генерация RSA приватного ключа
openssl genrsa -out jwt-private.pem 2048

# Генерация публичного ключа
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

## Создание супер пользователя для доступа к админке (Опционально)

```bash
# Интерактивный режим
python cli.py createsuperuser
```

```bash
# Задание аргументов напрямую
python cli.py createsuperuser --username admin --email admin@example.com --password secret123
```

### Запуск приложения

```bash
# Запуск чрез Makefile
make dev-up
```

### Посмотрите результат

- http://127.0.0.1:3000 (Фронтенд)
- http://127.0.0.1:8000 (Корень бекенда)
- http://127.0.0.1:8000/docs (Swagger документация бекенда)
- http://127.0.0.1:8000 (Админка)

## Полезные ссылки

- [Список задач](docs/TASK.md) 
- [Бэклог](docs/BACKLOG.md)
