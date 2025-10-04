# Как работает авторизация

## Идея

1) Отправляем данные по `POST api/v1/auth/users/` с `email`, `username`, `password`
2) На почту пользователю приходит ссылка
3) Пользователь переходи по ссылке типа:
<http://127.0.0.1:8000/api/v1/auth/users/activation/MTA/cwqrsf-755ee7a329a94daf71cfbcf9ff13f393>
4) Он попадает на Фронтенд страницу (Браузер)
5) Фронтенд отправляем запрос на `POST http://127.0.0.1:8000/api/v1/auth/users/activation/` с данными:

```
{
"uid": "MTA",
"token": "cwqrsf-755ee7a329a94daf71cfbcf9ff13f393"
}
```

6) Этот запрос активирует пользователя и создаёт его. Кода ответа нет. Прсто активирует пользователя не сообщая об этом клиенту.

7) Потом делаем POST запрос на (Форма логина):
<http://127.0.0.1:8000/api/v1/jwt/create/>
с данными:

```
{
"username": "MTA",
"password": "cwqrsf-755ee7a329a94daf71cfbcf9ff13f393"
}
```

8) Получаем 2 токена. Их надо где-то хранить.:

 ```
 {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1OTI0MDY1OCwiaWF0IjoxNzU5MTU0MjU4LCJqdGkiOiIxNTEwMzkwNjQxMDc0NDBhOWVjYWY0ZDUzMDg3NDQ1NCIsInVzZXJfaWQiOiIxIn0.kkA416MvF6Lz1ad0KPfaexXtClUMR1x9MMUlzHIY6Xg",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU5MTU0NTU4LCJpYXQiOjE3NTkxNTQyNTgsImp0aSI6ImFlNTRiZjA4MGQ2NTQwZTY4MDZhZmY3MzY3MjU2ZGQxIiwidXNlcl9pZCI6IjEifQ.U1UDUYrd3v6a6-RIwy-0YWDIjQz5SjHyw2oYl-nSY8M"

}
 ```

9) `access` токен нужно от правлять со всеми запросами. Рефреш живёт 7 дней (он обновляет ключи) по `POST api/v1//auth/jwt/refresh/` c  рефреш токеном в запрсе. Получаем новые 2 ключа, которые нужно хранить
