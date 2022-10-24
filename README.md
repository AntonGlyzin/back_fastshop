# Интернет-магазин на fastapi с админ панелью django

## Общий функционал.

![fastshop.gif](https://firebasestorage.googleapis.com/v0/b/antonio-glyzin.appspot.com/o/fastshop%2Fgit%2FScreenshot-2.png?alt=media&token=e93bc0ec-34c2-4237-adfe-c76460fdd2c2)
- Вывод списка товаров.
- Получение товара по ИД.
- Вывод списка товаров в корзине.
- Добавления, уменьшения и удаления товаров из корзины.
- Регистрация покупателя в системе.
- Авторизация покупателя.
- Сброс пароля через email.
- Смена пароля через email.
- Получения информации о своем профиле.
- Установка фото на свой профиль.
- Изменение профиля покупателя.
- Добавления и изменения пунктов доставки.
- Получения своих заказов по статусу.
- Оформление заказа при полной корзине.
- Уведомление на email при разных действиях с заказом.

## Админка 

|Функционал|Демонстрация|
|-|-|
|Просмотр общей информации о покупателе, его заказов, пунктов доставки и корзины покупателя.|![fastshop.gif](https://firebasestorage.googleapis.com/v0/b/antonio-glyzin.appspot.com/o/fastshop%2Fgit%2FPeek%202022-10-24%2011-25.gif?alt=media&token=f0e9167c-c117-4035-9cd1-852aefaedba4)|
|Добавление товара, редактирование, поиск и удаления.|![fastshop.gif](https://firebasestorage.googleapis.com/v0/b/antonio-glyzin.appspot.com/o/fastshop%2Fgit%2FPeek%202022-10-24%2013-24.gif?alt=media&token=4355f048-5592-4168-be53-37269dcfbeb7)|
|Просмотр всех заказов, поиск заказа, фильтрация, подтверждения о плате заказа.|![fastshop.gif](https://firebasestorage.googleapis.com/v0/b/antonio-glyzin.appspot.com/o/fastshop%2Fgit%2FPeek%202022-10-24%2013-20.gif?alt=media&token=bd53106a-ffe5-4101-a012-af9c91087a47)|

## Настройка БД
Для миграции БД нужно проделать следующее:
```bash
# сформировать схему базы
alembic revision --autogenerate
# миграция схемы
alembic upgrade <Номер>
# миграция от django
python manage.py migrate
```

## Пример .env файла
```.env
SECRET_KEY = 'секретный ключ'
BUCKET_STORAGE_NAME = 'букет firebase'
MAIL_PASSWORD = "пароль от почты"
MAIL_FROM = "email для уведомлений от лица магазина"
MAIL_ADMIN = "email для уведомлений админу"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
PGADMIN_DEFAULT_EMAIL = 'admin@admin.ru'
PGADMIN_DEFAULT_PASSWORD = 'admin'
DATABASE_URL = 'postgresql://postgres:postgres@db:5432/fastshop'
```
