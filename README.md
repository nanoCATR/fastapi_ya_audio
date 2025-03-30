# Документация по развертыванию сервиса
## Env file
- Создать приложение: https://oauth.yandex.ru/. В redirect url указать `http://localhost/yandex_auth/token?code=`;
- Добавить `client_id` и `client_secret` в .env файл;
- Настроить остальные настройки конфигурации.

## Build and run docker containers
Зайти в папку проекта, написать следующую команду:
```sh
docker-compose up -d
```

## Swagger docs url
`localhost/docs`


