---
name: docker-compose
description: Generates Docker Compose development environments for Laravel (PHP, MySQL, Redis, Nginx) and Node.js (Node, PostgreSQL, Redis) stacks with Dockerfiles and configs.
type: skill
category: skills
allowed-tools: [Read, Write, Grep, Glob]
---

# Docker Compose Generator

This skill generates a complete Docker Compose development environment tailored to your project stack.

## Usage

Run `/docker-compose <stack>` where stack is one of: `laravel`, `node`, `fullstack`

## Structure

### For Laravel stack

Generates:
- `docker-compose.yml`: Services (app, nginx, mysql, redis, mailhog)
- `docker/php/Dockerfile`: PHP 8.3-FPM with extensions
- `docker/nginx/default.conf`: Nginx virtual host
- `docker/php/php.ini`: PHP config overrides
- `.dockerignore`

### For Node stack

Generates:
- `docker-compose.yml`: Services (app, postgres, redis)
- `docker/node/Dockerfile`: Node 20 with multi-stage build
- `.dockerignore`

### For Fullstack (Laravel + Angular/React)

Generates both backend and frontend services in one compose file.

## Standards

- **Named volumes** for data persistence (db, redis)
- **Health checks** on all services
- **Environment variables** via .env file (never hardcoded)
- **Multi-stage Dockerfiles** for production builds
- **Non-root user** in containers
- **Proper .dockerignore** to keep images small

## Implementation Steps

1. Detect or confirm the target stack (`laravel`, `node`, or `fullstack`).
2. Check for an existing `docker-compose.yml` and warn before overwriting.
3. Generate all files into the project root and `docker/` subdirectory.
4. Print a summary of created files and a quick-start command.

## Examples

### 1. Laravel Stack

#### docker-compose.yml

```yaml
# Docker Compose for Laravel development environment
# Usage: docker compose up -d

services:
  # -------------------------------------------------------
  # PHP-FPM application container
  # Runs artisan, queue workers, and serves PHP via FPM
  # -------------------------------------------------------
  app:
    build:
      context: .
      dockerfile: docker/php/Dockerfile
    container_name: laravel-app
    restart: unless-stopped
    working_dir: /var/www/html
    volumes:
      - .:/var/www/html                       # Mount project source code
      - ./docker/php/php.ini:/usr/local/etc/php/conf.d/custom.ini  # PHP overrides
    environment:
      DB_HOST: ${DB_HOST:-mysql}
      DB_PORT: ${DB_PORT:-3306}
      DB_DATABASE: ${DB_DATABASE:-laravel}
      DB_USERNAME: ${DB_USERNAME:-laravel}
      DB_PASSWORD: ${DB_PASSWORD:-secret}
      REDIS_HOST: ${REDIS_HOST:-redis}
      REDIS_PORT: ${REDIS_PORT:-6379}
    depends_on:
      mysql:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD-SHELL", "php-fpm-healthcheck || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
    networks:
      - laravel

  # -------------------------------------------------------
  # Nginx web server
  # Proxies HTTP requests to the PHP-FPM container
  # -------------------------------------------------------
  nginx:
    image: nginx:1.25-alpine
    container_name: laravel-nginx
    restart: unless-stopped
    ports:
      - "${APP_PORT:-8080}:80"
    volumes:
      - .:/var/www/html                              # Serve static assets directly
      - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      app:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/"]
      interval: 10s
      timeout: 5s
      retries: 3
    networks:
      - laravel

  # -------------------------------------------------------
  # MySQL 8 database
  # Data is persisted in a named volume
  # -------------------------------------------------------
  mysql:
    image: mysql:8.0
    container_name: laravel-mysql
    restart: unless-stopped
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD:-rootsecret}
      MYSQL_DATABASE: ${DB_DATABASE:-laravel}
      MYSQL_USER: ${DB_USERNAME:-laravel}
      MYSQL_PASSWORD: ${DB_PASSWORD:-secret}
    ports:
      - "${DB_EXTERNAL_PORT:-3306}:3306"
    volumes:
      - mysql-data:/var/lib/mysql               # Persist database files
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p${DB_ROOT_PASSWORD:-rootsecret}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    networks:
      - laravel

  # -------------------------------------------------------
  # Redis for caching, sessions, and queues
  # -------------------------------------------------------
  redis:
    image: redis:7-alpine
    container_name: laravel-redis
    restart: unless-stopped
    ports:
      - "${REDIS_EXTERNAL_PORT:-6379}:6379"
    volumes:
      - redis-data:/data                        # Persist Redis data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    networks:
      - laravel

  # -------------------------------------------------------
  # Mailhog for local email testing
  # Web UI available at http://localhost:8025
  # -------------------------------------------------------
  mailhog:
    image: mailhog/mailhog:latest
    container_name: laravel-mailhog
    restart: unless-stopped
    ports:
      - "${MAILHOG_PORT:-8025}:8025"            # Web UI
      - "${MAILHOG_SMTP_PORT:-1025}:1025"       # SMTP
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:8025"]
      interval: 10s
      timeout: 5s
      retries: 3
    networks:
      - laravel

networks:
  laravel:
    driver: bridge

volumes:
  mysql-data:
    driver: local
  redis-data:
    driver: local
```

#### docker/php/Dockerfile

```dockerfile
# -----------------------------------------------------------
# PHP 8.3-FPM image for Laravel
# Includes common extensions and Composer
# -----------------------------------------------------------
FROM php:8.3-fpm-alpine AS base

# Install system dependencies required by PHP extensions
RUN apk add --no-cache \
    curl \
    libpng-dev \
    libjpeg-turbo-dev \
    freetype-dev \
    libzip-dev \
    icu-dev \
    oniguruma-dev \
    linux-headers \
    fcgi          # Needed for php-fpm-healthcheck

# Configure and install PHP extensions
RUN docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
        pdo_mysql \
        mbstring \
        gd \
        zip \
        intl \
        opcache \
        pcntl \
        bcmath

# Install Redis extension via PECL
RUN apk add --no-cache --virtual .build-deps $PHPIZE_DEPS \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && apk del .build-deps

# Install Composer from the official image
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

# Add a php-fpm health check script
RUN echo '#!/bin/sh' > /usr/local/bin/php-fpm-healthcheck \
    && echo 'SCRIPT_NAME=/ping SCRIPT_FILENAME=/ping REQUEST_METHOD=GET cgi-fcgi -bind -connect 127.0.0.1:9000 || exit 1' >> /usr/local/bin/php-fpm-healthcheck \
    && chmod +x /usr/local/bin/php-fpm-healthcheck

# Create a non-root user to run the application
RUN addgroup -g 1000 appuser \
    && adduser -u 1000 -G appuser -s /bin/sh -D appuser

# Set working directory
WORKDIR /var/www/html

# Switch to non-root user
USER appuser

EXPOSE 9000

CMD ["php-fpm"]
```

#### docker/nginx/default.conf

```nginx
# Nginx virtual host for Laravel
# Proxies PHP requests to the app container on port 9000

server {
    listen 80;
    server_name localhost;

    root /var/www/html/public;
    index index.php index.html;

    # Max upload size — should match php.ini upload_max_filesize
    client_max_body_size 64M;

    # Serve static files directly, fall back to index.php
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    # Pass PHP scripts to the app container via FastCGI
    location ~ \.php$ {
        fastcgi_pass app:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;

        # Timeouts for long-running requests
        fastcgi_read_timeout 300;
    }

    # Deny access to hidden files (.env, .git, etc.)
    location ~ /\. {
        deny all;
        access_log off;
        log_not_found off;
    }
}
```

#### docker/php/php.ini

```ini
; Custom PHP overrides for development
upload_max_filesize = 64M
post_max_size = 64M
memory_limit = 256M
max_execution_time = 300

; OPcache settings (tuned for development — revalidate every request)
opcache.enable = 1
opcache.revalidate_freq = 0
opcache.validate_timestamps = 1
opcache.max_accelerated_files = 10000
opcache.memory_consumption = 128
```

#### .dockerignore

```
node_modules
vendor
.git
.github
.idea
.vscode
storage/logs/*
storage/framework/cache/*
storage/framework/sessions/*
storage/framework/views/*
bootstrap/cache/*
.env
.env.backup
docker-compose.override.yml
```

### 2. Node Stack

#### docker-compose.yml

```yaml
# Docker Compose for Node.js development environment
# Usage: docker compose up -d

services:
  # -------------------------------------------------------
  # Node.js application container
  # Uses the dev target for hot reload during development
  # -------------------------------------------------------
  app:
    build:
      context: .
      dockerfile: docker/node/Dockerfile
      target: dev                                # Use the development stage
    container_name: node-app
    restart: unless-stopped
    ports:
      - "${APP_PORT:-3000}:3000"
    volumes:
      - .:/home/appuser/app                      # Mount source for hot reload
      - node_modules:/home/appuser/app/node_modules  # Preserve node_modules in volume
    environment:
      NODE_ENV: ${NODE_ENV:-development}
      DATABASE_URL: postgresql://${DB_USERNAME:-appuser}:${DB_PASSWORD:-secret}@postgres:5432/${DB_DATABASE:-appdb}
      REDIS_URL: redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 15s
    networks:
      - nodeapp

  # -------------------------------------------------------
  # PostgreSQL 16 database
  # Data persisted in a named volume
  # -------------------------------------------------------
  postgres:
    image: postgres:16-alpine
    container_name: node-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${DB_DATABASE:-appdb}
      POSTGRES_USER: ${DB_USERNAME:-appuser}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-secret}
    ports:
      - "${DB_EXTERNAL_PORT:-5432}:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data   # Persist database files
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USERNAME:-appuser} -d ${DB_DATABASE:-appdb}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s
    networks:
      - nodeapp

  # -------------------------------------------------------
  # Redis for caching and session storage
  # -------------------------------------------------------
  redis:
    image: redis:7-alpine
    container_name: node-redis
    restart: unless-stopped
    ports:
      - "${REDIS_EXTERNAL_PORT:-6379}:6379"
    volumes:
      - redis-data:/data                         # Persist Redis data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    networks:
      - nodeapp

networks:
  nodeapp:
    driver: bridge

volumes:
  postgres-data:
    driver: local
  redis-data:
    driver: local
  node_modules:
    driver: local
```

#### docker/node/Dockerfile

```dockerfile
# -----------------------------------------------------------
# Multi-stage Dockerfile for Node.js 20
# Stages: deps -> dev (with hot reload) -> build -> production
# -----------------------------------------------------------

# -- Stage 1: Install dependencies -------------------------
FROM node:20-alpine AS deps

WORKDIR /home/appuser/app

# Copy only package manifests to leverage Docker layer caching
COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./

# Install dependencies based on the available lock file
RUN if [ -f pnpm-lock.yaml ]; then \
      corepack enable && pnpm install --frozen-lockfile; \
    elif [ -f yarn.lock ]; then \
      yarn install --frozen-lockfile; \
    else \
      npm ci; \
    fi

# -- Stage 2: Development with hot reload ------------------
FROM node:20-alpine AS dev

# Create non-root user
RUN addgroup -g 1001 appuser \
    && adduser -u 1001 -G appuser -s /bin/sh -D appuser

# Install wget for health checks
RUN apk add --no-cache wget

WORKDIR /home/appuser/app

# Copy installed node_modules from deps stage
COPY --from=deps /home/appuser/app/node_modules ./node_modules
COPY . .

RUN chown -R appuser:appuser /home/appuser/app

USER appuser

EXPOSE 3000

# Start with hot reload (override in compose if needed)
CMD ["npm", "run", "dev"]

# -- Stage 3: Build for production -------------------------
FROM node:20-alpine AS build

WORKDIR /home/appuser/app

COPY --from=deps /home/appuser/app/node_modules ./node_modules
COPY . .

RUN npm run build

# -- Stage 4: Production image (minimal) -------------------
FROM node:20-alpine AS production

# Create non-root user
RUN addgroup -g 1001 appuser \
    && adduser -u 1001 -G appuser -s /bin/sh -D appuser

# Install wget for health checks
RUN apk add --no-cache wget

WORKDIR /home/appuser/app

# Copy only production dependencies and build output
COPY --from=deps /home/appuser/app/node_modules ./node_modules
COPY --from=build /home/appuser/app/dist ./dist
COPY package.json ./

RUN chown -R appuser:appuser /home/appuser/app

USER appuser

EXPOSE 3000

CMD ["node", "dist/main.js"]
```

#### .dockerignore

```
node_modules
dist
.git
.github
.idea
.vscode
coverage
.nyc_output
*.log
.env
.env.*
docker-compose.override.yml
```

## Quick Start Commands

After generating files, print these instructions:

```bash
# Laravel stack
docker compose up -d
docker compose exec app composer install
docker compose exec app php artisan key:generate
docker compose exec app php artisan migrate

# Node stack
docker compose up -d
docker compose exec app npm run migrate   # If applicable
```
