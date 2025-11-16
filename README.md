# Книжная соц. сеть "Переплёт"


## Запуск

### Генерация ключей

```
# Создание папки для ключей
mkdir certs

# Переходим в папку для ключей
cd certs
```

```
# Генерация RSA приватного ключа
openssl genrsa -out jwt-private.pem 2048
```

```
# Генерация публичного ключа
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

### Запуск приложения

```
# Запуск чрез Makefile
make dev-up
```

### Посмотрите результат

перейдите на http://127.0.0.1:3000