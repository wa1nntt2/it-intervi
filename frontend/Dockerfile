# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Копируем package файлы для кэширования слоев
COPY package*.json ./

# Устанавливаем все зависимости (включая dev для сборки)
RUN npm ci

# Копируем исходный код
COPY . .

# Собираем production билд
RUN npm run build

# Production stage - nginx
FROM nginx:alpine

# Копируем собранные файлы
COPY --from=builder /app/dist /usr/share/nginx/html

# Копируем nginx конфигурацию
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Health check - используем 127.0.0.1 вместо localhost чтобы избежать IPv6
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://127.0.0.1/health || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
