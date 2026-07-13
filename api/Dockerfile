# Laravel API — multi-stage for dev and prod.
# Requires a standard Laravel app in api/ (composer.json, artisan, etc.).

FROM composer:2 AS vendor
WORKDIR /app
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-scripts --no-autoloader --prefer-dist
COPY . .
RUN composer dump-autoload --optimize --no-dev

FROM php:8.3-fpm-alpine AS base
RUN apk add --no-cache \
    postgresql-dev \
    libzip-dev \
    icu-dev \
    && docker-php-ext-install pdo_pgsql zip intl opcache \
    && apk del --purge postgresql-dev libzip-dev icu-dev
WORKDIR /var/www/html
COPY docker/php.ini /usr/local/etc/php/conf.d/99-app.ini

FROM base AS dev
RUN apk add --no-cache $PHPIZE_DEPS \
    && pecl install xdebug \
    && docker-php-ext-enable xdebug \
    && apk del $PHPIZE_DEPS
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer
CMD ["php-fpm"]

FROM base AS prod
COPY --from=vendor /app /var/www/html
RUN chown -R www-data:www-data storage bootstrap/cache
USER www-data
CMD ["php-fpm"]
