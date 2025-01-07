FROM php:8.2-fpm-alpine

WORKDIR /var/www

RUN apk add --no-cache \
    bash \
    zip \
    unzip \
    git \
    curl \
    libpng-dev \
    oniguruma-dev \
    postgresql-dev \
    && docker-php-ext-install pdo pdo_mysql pdo_pgsql mbstring exif pcntl bcmath gd

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

COPY . .

RUN chown -R www-data:www-data /var/www \
    && chmod -R 775 /var/www/storage /var/www/bootstrap/cache

EXPOSE 9000

CMD ["php-fpm"]
