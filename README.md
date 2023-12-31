## cars_manufacture

Мини-проект для самостоятельного изучения и закрепления материала.  
Что реализовано:
- Celery worker для отправки эл.почты + Redis
- Написание кастомной регистрации, авторизации по JWT-токенам
- Отправка сообщений на указанную эл.почту при регистрации пользователя со ссылкой для её подтверждения
- Написание кастомной фильтрации
- Для документации используется Swagger
- В качестве базы данных используется PostgreSQL
- Используется Docker, backend добавлен в volume для того, чтобы не пересобирать образ после каждого изменения


## Как разернуть проект:
* Установите Docker desktop.
* Клонируйте репозиторий командой:  
`git clone git@github.com:sntchweb/car_manufacture.git`
* Создайте `.env` файл в директории /manufacture. Пример `.env` файла:
```bash
# SETTINGS
SECRET_KEY='django-insecure-q&o#d&f$!j4@ngynaj@-esb18!ejdejve1uf7fg302crjgyok)'
DEBUG='True'
ALLOWED_HOSTS='backend 127.0.0.1 localhost'

# E-MAIL CONST
EMAIL_HOST_USER='your_email'
EMAIL_HOST_PASSWORD='app_password'

# DATABASE
POSTGRES_DB=django
POSTGRES_USER=django
POSTGRES_PASSWORD=django
DB_NAME=django
DB_HOST=database
DB_PORT=5432

#CELERY
CELERY_BROKER_URL='redis://redis:6379/1'
```
* Откройте терминал и запустите сборку и запуск docker-контейнеров командой из корневой директории:  
`docker-compose up --build`

`API` будет доступно по адресу:
```bash
http://127.0.0.1:8000/api/v1/
```
Документация будет доступна по адресу:
```bash
http://127.0.0.1:8000/api/v1/docs/swagger/
```

## Примеры запросов и ответов:

```bash
Запрос: http://127.0.0.1:8000/api/v1/cars/4

Ответ: 
{
	"car_body": {
		"color": "белый",
		"body_type": "универсал"
	},
	"vin_code": "CBD110C5BC5F4CE2913AFD947E54B3AE",
	"creation_date": "2023-10-26",
	"components": [
		{
			"name": "задняя дверь",
			"amount": 2,
			"manufacturer_country": "Италия"
		},
		{
			"name": "руль",
			"amount": 1,
			"manufacturer_country": "Россия"
		}
	],
	"employee": {
		"id": 3,
		"username": "spetrov",
		"email": "spetrov@mail.ru",
		"first_name": "Сергей",
		"last_name": "Петров"
	}
}
```

```bash
Запрос: http://127.0.0.1:8000/api/v1/users/

Ответ:  
{
	"count": 3,
	"next": null,
	"previous": null,
	"results": [
		{
			"id": 1,
			"username": "qwerty",
			"email": "qwerty123@mail.ru",
			"first_name": "qwertyqq",
			"last_name": "qwertyww"
		},
		{
			"id": 5,
			"username": "artl",
			"email": "artemartem@mail.ru",
			"first_name": "art",
			"last_name": "las"
		},
		{
			"id": 3,
			"username": "spetrov",
			"email": "spetrov@mail.ru",
			"first_name": "Сергей",
			"last_name": "Петров"
		}
	]
}
```

```bash
Запрос: http://127.0.0.1:8000/api/v1/components/

Ответ:  
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "name": "лобовое стекло",
            "manufacturer_country": "Япония"
        },
        {
            "name": "задняя дверь",
            "manufacturer_country": "Италия"
        },
        {
            "name": "колесо",
            "manufacturer_country": "Япония"
        },
        {
            "name": "ремень ГРМ",
            "manufacturer_country": "Чехия"
        },
        {
            "name": "руль",
            "manufacturer_country": "Россия"
        }
    ]
}
```
