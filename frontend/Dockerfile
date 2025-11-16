# Простой Dockerfile для dev режима
FROM node:20-alpine

WORKDIR /app

# Копируем файлы зависимостей
COPY package.json ./

# Устанавливаем зависимости (используем npm install вместо npm ci для гибкости)
RUN npm install

# Копируем исходный код
COPY . .

# Открываем порт для dev сервера
EXPOSE 3000

# Команда запуска указывается в docker-compose.yml
