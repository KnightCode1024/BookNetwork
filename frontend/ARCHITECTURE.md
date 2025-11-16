# Архитектура Frontend приложения BookNetwork

## Обзор

Фронтенд приложение построено на принципах Clean Architecture, что обеспечивает:
- Разделение ответственности между слоями
- Независимость бизнес-логики от фреймворков
- Легкость тестирования
- Поддерживаемость кода

## Структура слоев

### 1. Domain Layer (Доменный слой)

**Назначение**: Содержит бизнес-логику и правила предметной области.

**Структура**:
- `entities/` - доменные сущности (User, Auth)
- `repositories/` - интерфейсы репозиториев (контракты)

**Принципы**:
- Не зависит от других слоев
- Содержит только TypeScript интерфейсы и типы
- Не содержит импортов из React или других библиотек

### 2. Application Layer (Слой приложения)

**Назначение**: Содержит use cases и бизнес-правила приложения.

**Структура**:
- `useCases/` - сценарии использования (LoginUseCase, RegisterUseCase, LogoutUseCase)
- `store/` - управление состоянием (Zustand stores)

**Принципы**:
- Зависит только от Domain слоя
- Содержит бизнес-логику приложения
- Использует интерфейсы из Domain, а не конкретные реализации

### 3. Infrastructure Layer (Инфраструктурный слой)

**Назначение**: Реализация технических деталей (HTTP, хранилище, внешние сервисы).

**Структура**:
- `http/` - HTTP клиент с interceptors
- `storage/` - хранилище токенов (MemoryTokenStorage)
- `repositories/` - реализация репозиториев (AuthRepositoryImpl)

**Принципы**:
- Реализует интерфейсы из Domain слоя
- Может зависеть от Application слоя для использования use cases
- Содержит технические детали (Axios, localStorage и т.д.)

### 4. Presentation Layer (Слой представления)

**Назначение**: UI компоненты, страницы, провайдеры.

**Структура**:
- `components/` - переиспользуемые компоненты (ProtectedRoute, PublicRoute)
- `pages/` - страницы приложения (LoginPage, RegisterPage, HomePage)
- `providers/` - React Context провайдеры (AuthProvider)

**Принципы**:
- Зависит от всех остальных слоев
- Использует use cases из Application слоя
- Содержит только UI логику

## Поток данных

```
User Action (Presentation)
    ↓
Use Case (Application)
    ↓
Repository Interface (Domain)
    ↓
Repository Implementation (Infrastructure)
    ↓
HTTP Client / Storage (Infrastructure)
    ↓
Backend API
```

## Безопасность токенов

### MemoryTokenStorage

Токены хранятся в памяти JavaScript для защиты от XSS атак:
- ✅ Не сохраняются в localStorage/sessionStorage
- ✅ Не сохраняются в cookies (которые могут быть доступны через JavaScript)
- ⚠️ Токены теряются при перезагрузке страницы (пользователю нужно войти заново)

### Автоматическое обновление токенов

HTTP клиент автоматически:
1. Добавляет access token к каждому запросу
2. Перехватывает 401 ошибки
3. Обновляет токены через refresh token
4. Повторяет оригинальный запрос с новым токеном
5. Обрабатывает очередь запросов во время обновления

## Маршрутизация

- `/login` - страница входа (PublicRoute)
- `/register` - страница регистрации (PublicRoute)
- `/` - главная страница (ProtectedRoute)

**ProtectedRoute**: Проверяет аутентификацию, редиректит на `/login` если не авторизован
**PublicRoute**: Редиректит на `/` если уже авторизован

## Управление состоянием

Используется Zustand для глобального состояния:
- `useAuthStore` - состояние аутентификации (user, isAuthenticated, isLoading)

## Расширение функциональности

### Добавление нового use case:

1. Создать интерфейс в `domain/repositories/`
2. Реализовать в `infrastructure/repositories/`
3. Создать use case в `application/useCases/`
4. Использовать в компонентах через `useAuth()` hook

### Добавление новой страницы:

1. Создать компонент в `presentation/pages/`
2. Добавить маршрут в `App.tsx`
3. Обернуть в `ProtectedRoute` или `PublicRoute` при необходимости

## Тестирование

Каждый слой можно тестировать независимо:
- Domain: Unit тесты для entities и интерфейсов
- Application: Unit тесты для use cases
- Infrastructure: Integration тесты для HTTP клиента и хранилища
- Presentation: Component тесты для React компонентов

