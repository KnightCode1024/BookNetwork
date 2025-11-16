# BookNetwork Frontend

Фронтенд приложение для BookNetwork, построенное на React + TypeScript с использованием Clean Architecture.

## Технологический стек

- **React 19** - UI библиотека
- **TypeScript 5** - типизация
- **Vite 6** - сборщик и dev-сервер
- **Mantine 7** - библиотека компонентов
- **React Router 7** - маршрутизация
- **Zustand** - управление состоянием
- **Axios** - HTTP клиент

## Архитектура

Проект следует принципам Clean Architecture с разделением на слои:

- **Domain** - бизнес-логика, entities, интерфейсы репозиториев
- **Application** - use cases, бизнес-правила
- **Infrastructure** - реализация репозиториев, HTTP клиент, хранилище токенов
- **Presentation** - React компоненты, страницы, провайдеры

## Безопасность токенов

JWT токены хранятся в памяти (MemoryTokenStorage) для защиты от XSS атак. При перезагрузке страницы пользователю необходимо войти заново.

## Установка и запуск

### Локальная разработка

```bash
# Установка зависимостей
npm install

# Запуск dev-сервера
npm run dev

# Сборка для production
npm run build

# Предпросмотр production сборки
npm run preview
```

### Docker

```bash
# Сборка образа
docker build -t booknetwork-frontend .

# Запуск через docker-compose
docker-compose -f docker-compose.dev.yml up frontend
```

## Переменные окружения

Создайте файл `.env` на основе `.env.example`:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=BookNetwork
```

## Структура проекта

```
frontend/
├── src/
│   ├── domain/           # Domain слой
│   │   ├── entities/     # Сущности
│   │   └── repositories/ # Интерфейсы репозиториев
│   ├── application/      # Application слой
│   │   ├── useCases/     # Use cases
│   │   └── store/        # Zustand stores
│   ├── infrastructure/   # Infrastructure слой
│   │   ├── http/         # HTTP клиент
│   │   ├── storage/      # Хранилище токенов
│   │   └── repositories/ # Реализация репозиториев
│   ├── presentation/     # Presentation слой
│   │   ├── components/   # React компоненты
│   │   ├── pages/        # Страницы
│   │   └── providers/    # Context провайдеры
│   └── shared/           # Общие утилиты
├── public/               # Статические файлы
└── dist/                 # Собранное приложение
```

## API Endpoints

Приложение использует следующие endpoints бэкенда:

- `POST /auth/login/` - вход
- `POST /auth/register/` - регистрация
- `POST /auth/refresh/` - обновление токенов
- `POST /auth/verify/` - проверка токена

## Особенности

- Автоматическое обновление токенов при истечении access token
- Защищенные маршруты с редиректами
- Обработка ошибок аутентификации
- Валидация форм с помощью Mantine Form

